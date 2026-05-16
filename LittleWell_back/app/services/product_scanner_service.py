import os
import base64
import json
import re
import httpx
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/api/v2/product"

def extract_barcode_from_image(image_bytes: bytes) -> str | None:
    """Use Groq vision to read barcode number from product image."""
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    prompt = """Look at this image of a food product or its barcode.
If you can see a barcode or EAN/UPC number, return ONLY the digits, nothing else.
Example: 9300617781452
If you cannot see a barcode number clearly, return: NOT_FOUND"""
    resp = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": prompt},
            ]
        }],
        max_tokens=30,
        temperature=0.1,
    )
    text = resp.choices[0].message.content.strip()
    digits = re.sub(r'\D', '', text)
    return digits if len(digits) >= 8 else None

def lookup_product(barcode: str) -> dict | None:
    """Fetch product data from Open Food Facts."""
    url = f"{OPEN_FOOD_FACTS_URL}/{barcode}.json"
    with httpx.Client(timeout=10) as client:
        resp = client.get(url, headers={"User-Agent": "LittleWell-App/1.0"})
    if resp.status_code != 200:
        return None
    data = resp.json()
    if data.get("status") != 1:
        return None
    p = data["product"]
    nutriments = p.get("nutriments", {})
    return {
        "name": p.get("product_name", "Unknown Product"),
        "brand": p.get("brands", "Unknown Brand"),
        "image_url": p.get("image_url", ""),
        "nutriscore": p.get("nutriscore_grade", "").upper(),
        "nova_group": p.get("nova_group", ""),
        "ingredients": p.get("ingredients_text", "Not available"),
        "allergens": p.get("allergens_tags", []),
        "nutriments": {
            "energy_kj":    nutriments.get("energy-kj_100g", 0),
            "protein_g":    nutriments.get("proteins_100g", 0),
            "fat_g":        nutriments.get("fat_100g", 0),
            "saturated_fat_g": nutriments.get("saturated-fat_100g", 0),
            "carbs_g":      nutriments.get("carbohydrates_100g", 0),
            "sugars_g":     nutriments.get("sugars_100g", 0),
            "fibre_g":      nutriments.get("fiber_100g", 0),
            "sodium_mg":    nutriments.get("sodium_100g", 0) * 1000,
        }
    }

def generate_product_verdict(product: dict, child_age: int, child_name: str = "your child") -> dict:
    """Generate child-specific pros and cons using Groq."""
    n = product["nutriments"]
    prompt = f"""You are a children's nutritionist for the LittleWell app in Australia.

Product: {product['name']} by {product['brand']}
Nutri-Score: {product['nutriscore'] or 'Not rated'}
NOVA Group (processing level): {product['nova_group'] or 'Unknown'} (1=unprocessed, 4=ultra-processed)
Per 100g: Energy {n['energy_kj']}kj, Protein {n['protein_g']}g, Fat {n['fat_g']}g, 
Saturated fat {n['saturated_fat_g']}g, Sugar {n['sugars_g']}g, Fibre {n['fibre_g']}g, Sodium {n['sodium_mg']}mg
Allergens: {', '.join(product['allergens']) or 'none listed'}
Child: {child_name}, age {child_age}

Return ONLY valid JSON in this exact format:
{{
  "verdict": "good" or "moderate" or "avoid",
  "summary": "one sentence parent-friendly summary",
  "pros": ["pro 1", "pro 2"],
  "cons": ["con 1", "con 2"],
  "tip": "one practical serving tip for parents"
}}"""

    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )
    text = resp.choices[0].message.content.strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return {
        "verdict": "moderate",
        "summary": "Could not generate detailed verdict.",
        "pros": [],
        "cons": [],
        "tip": "Check the nutrition label before serving."
    }
