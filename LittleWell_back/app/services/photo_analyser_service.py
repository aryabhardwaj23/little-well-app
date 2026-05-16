import os, base64, json, re
import pandas as pd
from groq import Groq
from .nutrition_classifier_service import predict

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
AUSNUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ausnut.csv")

ADG_BY_AGE = {
    2:  {"energy_kj":4800,"protein_g":16,"fat_g":35,"carbs_g":155,"fibre_g":18,"calcium_mg":500,"iron_mg":9,"sodium_mg":700},
    4:  {"energy_kj":6000,"protein_g":20,"fat_g":40,"carbs_g":200,"fibre_g":18,"calcium_mg":700,"iron_mg":10,"sodium_mg":900},
    7:  {"energy_kj":7200,"protein_g":24,"fat_g":50,"carbs_g":250,"fibre_g":20,"calcium_mg":1000,"iron_mg":10,"sodium_mg":1200},
    11: {"energy_kj":8600,"protein_g":40,"fat_g":60,"carbs_g":300,"fibre_g":24,"calcium_mg":1300,"iron_mg":13,"sodium_mg":1400},
    14: {"energy_kj":10000,"protein_g":57,"fat_g":70,"carbs_g":345,"fibre_g":28,"calcium_mg":1300,"iron_mg":15,"sodium_mg":1600},
}

def get_adg(child_age):
    for age in sorted(ADG_BY_AGE.keys()):
        if child_age <= age:
            return ADG_BY_AGE[age]
    return ADG_BY_AGE[14]

def detect_food_labels(image_bytes: bytes) -> list:
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    prompt = """Look at this image and list every food item you can see.
Return ONLY a JSON array of food name strings, nothing else.
Example: ["pasta", "tomato sauce", "cheese", "apple"]
If no food is visible, return: ["unknown food"]"""
    resp = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role":"user","content":[
            {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
            {"type":"text","text":prompt}
        ]}],
        max_tokens=120, temperature=0.1,
    )
    text = resp.choices[0].message.content.strip()
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    words = re.sub(r'[\[\]"]','',text).split(',')
    return [w.strip() for w in words if w.strip()][:8] or ["unknown food"]

def match_ausnut(food_labels: list) -> pd.DataFrame:
    try:
        df = pd.read_csv(AUSNUT_PATH, encoding="latin-1")
        col_lower = {c.lower(): c for c in df.columns}
        name_col = next((col_lower[k] for k in col_lower if "food_name" in k or k == "food_name"), df.columns[0])
        matched = [df[df[name_col].str.contains(label, case=False, na=False)] for label in food_labels]
        result = pd.concat(matched).drop_duplicates() if matched else pd.DataFrame()
        return result.head(5)
    except FileNotFoundError:
        return pd.DataFrame()

def score_nutrition(matched_df: pd.DataFrame, child_age: int) -> dict:
    if matched_df.empty:
        return {"overall_score":55,"grade":"Fair","color":"amber","nutrient_scores":{},
                "note":"Add AUSNUT dataset to app/data/ausnut.csv for precise scoring"}
    adg = get_adg(child_age)
    col_lower = {c.lower(): c for c in matched_df.columns}

    def get_val(keywords):
        for kw in keywords:
            for lk, oc in col_lower.items():
                if kw in lk:
                    try: return float(matched_df[oc].iloc[0])
                    except: pass
        return None

    nutrients = {
        "energy_kj":  get_val(["energy_kj","energy"]),
        "protein_g":  get_val(["protein_g","protein"]),
        "fat_g":      get_val(["fat_g","fat"]),
        "carbs_g":    get_val(["carbs_g","carb"]),
        "fibre_g":    get_val(["fibre_g","fibre","fiber"]),
        "calcium_mg": get_val(["calcium_mg","calcium"]),
        "iron_mg":    get_val(["iron_mg","iron"]),
        "sodium_mg":  get_val(["sodium_mg","sodium"]),
    }

    scores = {}
    for key, val in nutrients.items():
        if val is not None and key in adg and adg[key] > 0:
            ratio = val / (adg[key] * 0.33)
            scores[key] = round(max(0, min(100, 100 - abs(1-ratio)*100)))

    overall_score = round(sum(scores.values())/len(scores)) if scores else 55
    if overall_score >= 80:   grade, color = "Excellent", "green"
    elif overall_score >= 60: grade, color = "Good",      "blue"
    elif overall_score >= 40: grade, color = "Fair",      "amber"
    else:                     grade, color = "Needs improvement", "red"

    # Run ML classifier on detected nutrients
    ml_result = predict(nutrients, child_age)

    return {
        "overall_score":   overall_score,
        "grade":           grade,
        "color":           color,
        "nutrient_scores": scores,
        "ml_classification": ml_result,
    }

def generate_ai_feedback(food_labels, nutrition_score, child_age, child_name="your child"):
    foods = ", ".join(food_labels[:6]) if food_labels else "the food items"
    grade = nutrition_score.get("grade","Fair")
    score = nutrition_score.get("overall_score",50)
    ml    = nutrition_score.get("ml_classification",{})
    ml_label = ml.get("display_label","")

    prompt = f"""You are a friendly children's nutritionist for the LittleWell app in Australia.
A parent photographed their child's lunchbox. Detected foods: {foods}.
Nutrition score for {child_name} (age {child_age}): {score}/100 — rated {grade}. ML classification: {ml_label}.
Write a warm 3-sentence feedback paragraph:
1. Acknowledge what foods were detected
2. Explain the {grade} rating for a {child_age}-year-old using Australian Dietary Guidelines
3. Give one specific easy improvement tip
Be encouraging. No bullet points. Parent-friendly language."""
    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        max_tokens=180, temperature=0.7,
    )
    return resp.choices[0].message.content.strip()
