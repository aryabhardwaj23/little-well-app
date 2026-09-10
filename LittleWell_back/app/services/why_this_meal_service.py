import os
from typing import Any

from groq import Groq


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


GENERIC_PHRASES_TO_AVOID = [
    "balanced mix",
    "delicious",
    "energized throughout the day",
    "perfect for",
    "suitable for Autumn",
    "good for growth",
    "healthy choice",
]


def _safe_join(values: list[str] | None, fallback: str = "none") -> str:
    if not values:
        return fallback

    cleaned = [str(item).strip() for item in values if str(item).strip()]

    if not cleaned:
        return fallback

    return ", ".join(cleaned)


def _normalise_meal_text(meal: Any) -> str:
    """
    weekly-story can receive either:
    1. a simple string from the old frontend
    2. a structured dict from the improved frontend
    """
    if isinstance(meal, str):
        return meal.strip()

    if isinstance(meal, dict):
        nutrition_focus = meal.get("nutrition_focus", [])

        if isinstance(nutrition_focus, list):
            nutrition_focus_text = ", ".join(
                [str(item).strip() for item in nutrition_focus if str(item).strip()]
            )
        else:
            nutrition_focus_text = str(nutrition_focus or "").strip()

        parts = [
            f"Meal title: {meal.get('title', '')}" if meal.get("title") else "",
            (
                f"Recipe inspiration: {meal.get('recipe_title', '')}"
                if meal.get("recipe_title")
                else ""
            ),
            f"Cook day: {meal.get('cook_day', '')}" if meal.get("cook_day") else "",
            (
                f"Nutrition focus: {nutrition_focus_text}"
                if nutrition_focus_text
                else ""
            ),
            (
                f"Meal context: {meal.get('meal_context', '')}"
                if meal.get("meal_context")
                else ""
            ),
            (
                f"Meal explanation: {meal.get('explanation', '')}"
                if meal.get("explanation")
                else ""
            ),
        ]

        return ". ".join([part for part in parts if part]).strip()

    return str(meal).strip()


def _call_groq(
    prompt: str,
    max_tokens: int = 220,
    temperature: float = 0.5,
) -> str:
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not configured.")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are LittleWell's friendly children's nutrition assistant. "
                    "You write practical, parent-friendly explanations for Australian school lunchboxes. "
                    "Be specific, realistic, and avoid vague marketing language. "
                    "Do not invent exact nutrient numbers or medical claims."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].message.content.strip()


def generate_why_this_meal(
    meal_name: str,
    child_age: int,
    allergens: list[str] | None = None,
    dietary_restrictions: list[str] | None = None,
    season: str = "autumn",
    meal_type: str = "lunchbox",
) -> str:
    allergen_text = _safe_join(allergens)
    dietary_text = _safe_join(dietary_restrictions)
    avoid_text = ", ".join([f'"{phrase}"' for phrase in GENERIC_PHRASES_TO_AVOID])

    prompt = f"""
Write a "Why This Meal?" explanation for a saved school lunchbox meal.

Meal information:
{meal_name}

Child age:
{child_age} years old

Context:
- Allergens to avoid: {allergen_text}
- Dietary restrictions: {dietary_text}
- Season: {season}
- Meal type: {meal_type}

Writing requirements:
- Write 3 to 5 short sentences.
- Use parent-friendly language.
- Be specific to the meal information provided.
- Mention at least one concrete food, recipe feature, ingredient, nutrition tag, or lunchbox item if available.
- Explain why it helps a school-aged child, for example steady energy, fullness, protein, fibre, calcium, iron, vegetables, variety, or concentration.
- Include one practical lunchbox reason, such as easy to pack, make-ahead preparation, storage, reheating, variety across the week, or school-day convenience.
- If seasonal context is mentioned, explain it in a practical way instead of only saying it is seasonal.
- Do not use bullet points.
- Do not mention that you are an AI.
- Avoid vague phrases like {avoid_text} unless you explain the exact food, lunchbox item, or nutrient behind the claim.
- Do not invent allergies, medical needs, exact nutrient numbers, or guaranteed health outcomes.
- Keep it under 95 words.
"""

    return _call_groq(
        prompt=prompt,
        max_tokens=180,
        temperature=0.5,
    )


def generate_weekly_nutrition_story(
    meals: list[Any],
    child_age: int,
    child_name: str = "your child",
) -> str:
    meal_texts = [_normalise_meal_text(meal) for meal in meals]
    meal_texts = [meal for meal in meal_texts if meal]

    if not meal_texts:
        return (
            "This weekly plan gives the child a more organised lunchbox routine, "
            "but there is not enough meal detail to generate a specific nutrition summary."
        )

    formatted_meals = "\n".join(
        [f"{index + 1}. {meal}" for index, meal in enumerate(meal_texts)]
    )

    prompt = f"""
Write a "Why This Plan" weekly nutrition summary for LittleWell.

Child:
- Name: {child_name}
- Age: {child_age} years old

Meals in the weekly plan:
{formatted_meals}

Writing requirements:
- Write 1 clear paragraph with 4 to 6 sentences.
- Explain why the whole weekly plan works, not just list the meals.
- Mention variety across the school week.
- Mention age suitability for a {child_age}-year-old child.
- Mention practical parent benefits, such as cooking frequency, make-ahead planning, lunchbox storage, or reduced repetition.
- Mention nutrition benefits using only the available meal information, such as grains for energy, protein for fullness, vegetables or fruit for variety, calcium, iron, fibre, or balanced lunchbox structure.
- Do not say "This weekly plan includes X explained meals".
- Do not use bullet points.
- Do not mention that you are an AI.
- Avoid vague phrases such as "balanced mix", "delicious", "perfect", "healthy choice", or "energized throughout the day" unless tied to a specific food, lunchbox item, or nutrient.
- Do not invent exact nutrient numbers, allergies, medical needs, or guaranteed health outcomes.
- Keep it under 130 words.
"""

    return _call_groq(
        prompt=prompt,
        max_tokens=230,
        temperature=0.5,
    )