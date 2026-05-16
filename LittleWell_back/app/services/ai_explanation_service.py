"""
AI Explanation Service — LittleWell
Generates "Why This Meal?" explanations using Groq LLaMA3.
"""
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_why_this_meal(
    meal_name: str,
    child_age_band: str,
    needs_support: list = [],
    allergies: list = [],
    is_seasonal: bool = False,
    nutrition_highlights: dict = {},
) -> str:
    support_str = ", ".join(needs_support) if needs_support else "balanced nutrition"
    allergy_str = ", ".join(allergies) if allergies else "none"
    seasonal_str = "Yes" if is_seasonal else "No"
    nutrients = []
    for nutrient, pct in nutrition_highlights.items():
        if pct and float(pct) > 20:
            nutrients.append(f"{nutrient.replace('_g','').replace('_mg','')} ({int(pct)}% daily needs)")
    nutrient_str = ", ".join(nutrients[:3]) if nutrients else "balanced macronutrients"

    prompt = f"""You are a friendly children's nutritionist writing for Australian parents.

Write a short 2-3 sentence "Why This Meal?" explanation for recommending "{meal_name}" in a child's lunchbox.

Child details:
- Age band: {child_age_band} years
- Nutritional needs: {support_str}
- Allergies: {allergy_str}
- Seasonal ingredients: {seasonal_str}
- Key nutrients provided: {nutrient_str}

Guidelines:
- Warm, simple language parents will understand
- Mention the child's specific age group
- Highlight 1-2 key nutritional benefits
- Mention seasonal freshness if applicable
- Keep it under 60 words
- Do not use bullet points
- Do not start with "This meal"
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
