from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.why_this_meal_service import generate_why_this_meal, generate_weekly_nutrition_story
from ..services.nutrition_classifier_service import predict

router = APIRouter(prefix='/ai-insights', tags=['AI Insights'])

class WhyThisMealRequest(BaseModel):
    meal_name: str
    child_age: int
    allergens: list[str] = []
    dietary_restrictions: list[str] = []
    season: Optional[str] = 'autumn'
    meal_type: Optional[str] = 'lunchbox'

class WeeklyStoryRequest(BaseModel):
    meals: list[str]
    child_age: int
    child_name: Optional[str] = 'your child'

class ClassifyRequest(BaseModel):
    nutriments: dict
    child_age: Optional[int] = 7

@router.post('/why-this-meal')
async def why_this_meal(request: WhyThisMealRequest):
    try:
        explanation = generate_why_this_meal(
            meal_name=request.meal_name, child_age=request.child_age,
            allergens=request.allergens, dietary_restrictions=request.dietary_restrictions,
            season=request.season, meal_type=request.meal_type)
        return {'meal_name': request.meal_name, 'explanation': explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/weekly-story')
async def weekly_story(request: WeeklyStoryRequest):
    try:
        story = generate_weekly_nutrition_story(
            meals=request.meals, child_age=request.child_age, child_name=request.child_name)
        return {'story': story}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/classify-nutrition')
async def classify_nutrition(request: ClassifyRequest):
    try:
        return predict(request.nutriments, request.child_age)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/train-classifier')
async def train_classifier():
    try:
        import pandas as pd, pickle, os
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report

        ausnut_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ausnut.csv')
        model_path  = os.path.join(os.path.dirname(__file__), '..', 'data', 'nutrition_classifier.pkl')

        df = pd.read_csv(ausnut_path)
        features = ['energy_kj','protein_g','fat_g','carbs_g',
                    'sugars_g','fibre_g','calcium_mg','iron_mg','sodium_mg']
        df = df.dropna(subset=features)

        def label(row):
            if row.sugars_g > 15 or row.sodium_mg > 400 or row.fat_g > 20:
                return 'at-risk'
            elif row.fibre_g >= 2 and row.sugars_g < 8 and row.sodium_mg < 200 and row.protein_g > 1:
                return 'balanced'
            else:
                return 'moderate'

        df['label'] = df.apply(label, axis=1)
        X = df[features].values
        y = df['label'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        clf.fit(X_train, y_train)
        report_dict = classification_report(y_test, clf.predict(X_test), output_dict=True)
        report_str  = classification_report(y_test, clf.predict(X_test))

        with open(model_path, 'wb') as f:
            pickle.dump({'model': clf, 'features': features, 'report': report_str}, f)

        return {
            'status': 'trained',
            'dataset': 'AUSNUT 2011-13 (real Australian food data)',
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'accuracy': round(report_dict['accuracy'] * 100, 1),
            'label_distribution': df['label'].value_counts().to_dict(),
            'classification_report': report_dict,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
