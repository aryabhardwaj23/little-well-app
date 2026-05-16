import os, pickle
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'nutrition_classifier.pkl')

DISPLAY = {
    'balanced': {'label': 'Balanced',  'color': 'green', 'emoji': '✅',
                 'message': 'This is a nutritious choice for your child.'},
    'moderate': {'label': 'Moderate',  'color': 'amber', 'emoji': '⚠️',
                 'message': 'Okay occasionally, but vary with healthier options.'},
    'at-risk':  {'label': 'At Risk',   'color': 'red',   'emoji': '🚫',
                 'message': 'High in sugar, salt or fat — best limited for children.'},
}

def predict(nutriments: dict, child_age: int = 7) -> dict:
    if not os.path.exists(MODEL_PATH):
        return {'class': 'unknown', 'confidence': 0,
                'message': 'Model not trained. POST /ai-insights/train-classifier first.'}

    with open(MODEL_PATH, 'rb') as f:
        saved = pickle.load(f)

    clf      = saved['model']
    features = saved['features']

    row = [float(nutriments.get(feat, 0) or 0) for feat in features]
    X   = np.array(row).reshape(1, -1)

    pred       = clf.predict(X)[0]
    proba      = clf.predict_proba(X)[0]
    confidence = round(float(max(proba)) * 100)
    display    = DISPLAY.get(pred, {'label': pred, 'color': 'gray', 'emoji': '❓', 'message': ''})

    age_note = ''
    if child_age <= 4 and pred == 'at-risk':
        age_note = ' Extra caution recommended for children under 5.'
    elif child_age >= 10 and pred == 'balanced':
        age_note = ' Great choice for active older children.'

    return {
        'class':         pred,
        'display_label': display['label'],
        'color':         display['color'],
        'emoji':         display['emoji'],
        'message':       display['message'] + age_note,
        'confidence':    confidence,
        'probabilities': {c: round(float(p)*100) for c, p in zip(clf.classes_, proba)},
    }
