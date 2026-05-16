import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_why_this_meal(meal_name, child_age, allergens=[], dietary_restrictions=[], season="autumn", meal_type="lunchbox"):
    allergen_text = ", ".join(allergens) if allergens else "none"
    dietary_text = ", ".join(dietary_restrictions) if dietary_restrictions else "none"
    prompt = f"""You are a friendly children's nutritionist for the LittleWell app in Australia.
Write a warm 3-4 sentence "Why This Meal?" explanation for: "{meal_name}"
Child: {child_age} years old, allergens: {allergen_text}, dietary: {dietary_text}, season: {season}, type: {meal_type}
Explain nutrition benefits, allergen safety, seasonal freshness, and lunchbox practicality.
No bullet points. Parent-friendly language. Under 60 words."""
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120, temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

def generate_weekly_nutrition_story(meals, child_age, child_name="your child"):
    meals_text = ", ".join(meals)
    prompt = f"""You are a warm children's nutritionist for the LittleWell app in Australia.
Write a 2-3 sentence weekly nutrition summary for {child_name} (age {child_age}) 
who has been planned these meals: {meals_text}.
Sound like a supportive nutritionist. Be encouraging and specific."""
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150, temperature=0.7,
    )
    return resp.choices[0].message.content.strip()
