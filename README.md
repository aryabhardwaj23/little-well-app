# ML Model Evaluation Report 
## LittleWell — Iteration 3 | FIT5120 Industry Experience Studio 2026 S1
**Team 14 | MAI Student Submission - Suryansh Sharma**

---

## 1. Problem Statement

Australian children's lunchbox nutrition is a critical public health concern. Parents lack accessible tools to evaluate whether the foods they pack meet the Australian Dietary Guidelines (ADG) for their child's age group. This feature applies machine learning to automatically classify food items from a lunchbox photo as **Balanced**, **Moderate**, or **At-Risk** — providing an instant, evidence-based verdict to parents.

---

## 2. Dataset — AUSNUT 2011-13

| Attribute | Detail |
|---|---|
| Source | Food Standards Australia New Zealand (FSANZ) |
| Dataset name | AUSNUT 2011-13 AT Food Nutrient Database |
| Total records | 3,741 food items |
| Total columns | 15 (Survey ID, Public food key, Food Name, 12 nutrient columns) |
| Coverage | All major Australian food categories — fresh produce, dairy, meat, packaged goods, beverages, snacks |

### 2.1 Features Used (9 of 15 columns)

| Feature | Unit | Why it matters |
|---|---|---|
| energy_kj | kJ per 100g | Total energy density — high energy density linked to obesity risk in children |
| protein_g | g per 100g | Essential for growth and muscle development in school-age children |
| fat_g | g per 100g | Total fat — excess fat linked to cardiovascular risk |
| carbs_g | g per 100g | Primary energy source — important for cognitive function |
| sugars_g | g per 100g | Free sugars are the primary dietary concern for Australian children |
| fibre_g | g per 100g | Supports digestive health; Australian children are significantly under-consuming fibre |
| calcium_mg | mg per 100g | Critical for bone development in children aged 4-14 |
| iron_mg | mg per 100g | Iron deficiency is the most common nutritional deficiency in Australian children |
| sodium_mg | mg per 100g | Excess sodium linked to hypertension; processed foods are the main source |

### 2.2 Preprocessing Steps

1. Loaded CSV with `latin-1` encoding to handle special characters in food names
2. Fixed BOM character (`ï»¿`) in first column name caused by Excel export
3. Renamed columns from verbose AUSNUT names to clean snake_case feature names
4. Dropped rows with null values in any of the 9 feature columns (0 rows dropped — dataset was complete)
5. Applied ADG-based rule labelling (see Section 3)

---

## 3. Label Engineering — Australian Dietary Guidelines

Labels were derived from the Australian Dietary Guidelines (ADG) published by the National Health and Medical Research Council (NHMRC). A lunchbox is estimated to contribute 33% of a child's daily nutritional needs.

### Labelling Rules (per 100g)

| Label | Conditions | ADG Basis |
|---|---|---|
| **at-risk** | sugars_g > 15 OR sodium_mg > 400 OR fat_g > 20 | ADG limits for discretionary foods; WHO free sugar recommendations |
| **balanced** | fibre_g ≥ 2 AND sugars_g < 8 AND sodium_mg < 200 AND protein_g > 1 | ADG core food group criteria |
| **moderate** | All other cases | Foods that are acceptable but lack the full nutritional profile of core foods |

### Label Distribution

| Label | Count | Percentage |
|---|---|---|
| moderate | 1,772 | 47.4% |
| at-risk | 1,530 | 40.9% |
| balanced | 439 | 11.7% |
| **Total** | **3,741** | **100%** |

Note: Class imbalance was addressed using `class_weight='balanced'` in the RandomForestClassifier, which penalises misclassification of minority classes proportionally.

---

## 4. Model Architecture — RandomForestClassifier

| Hyperparameter | Value | Rationale |
|---|---|---|
| Algorithm | RandomForestClassifier | Robust to class imbalance, handles mixed-scale features, provides feature importance |
| n_estimators | 100 | Balance between accuracy and computational cost |
| random_state | 42 | Reproducibility |
| class_weight | balanced | Compensates for minority class (balanced: 11.7%) |
| Test split | 20% (749 samples) | Standard split; sufficient for evaluation |
| Train split | 80% (2,992 samples) | |

### Why RandomForest?

- Handles non-linear relationships between nutrients (e.g. high fibre AND low sugar = balanced, but high fibre AND high sodium = not balanced)
- No feature scaling required (unlike SVM or logistic regression)
- Provides feature importance — directly interpretable and demonstrable to stakeholders
- Robust to outliers in nutritional data (e.g. unusually high sodium in preserved foods)

---

## 5. Model Performance

### 5.1 Overall Accuracy

**99.7%** on 749 unseen test samples.

### 5.2 Classification Report

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| at-risk | 0.993 | 1.000 | 0.997 | 303 |
| balanced | 1.000 | 1.000 | 1.000 | 73 |
| moderate | 1.000 | 0.995 | 0.997 | 373 |
| **accuracy** | | | **0.997** | **749** |
| macro avg | 0.998 | 0.998 | 0.998 | 749 |
| weighted avg | 0.997 | 0.997 | 0.997 | 749 |

### 5.3 Feature Importance

| Rank | Feature | Importance |
|---|---|---|
| 1 | fibre_g | 26.1% |
| 2 | sodium_mg | 25.9% |
| 3 | sugars_g | 15.5% |
| 4 | energy_kj | 11.3% |
| 5 | fat_g | 8.2% |
| 6 | protein_g | 4.9% |
| 7 | carbs_g | 3.7% |
| 8 | iron_mg | 2.7% |
| 9 | calcium_mg | 1.7% |

**Interpretation:** Fibre and sodium are the dominant predictors, consistent with Australian dietary research showing fibre under-consumption and sodium overconsumption as the two most prevalent issues in children's diets. Sugar is the third most important, reflecting WHO and ADG guidance on free sugar limits.

---

## 6. Robustness Analysis

### 6.1 Tested Scenarios

| Test Input | Expected | Actual | Confidence |
|---|---|---|---|
| Apple (energy 218kJ, sugar 10.4g, fibre 2.4g, sodium 1mg) | moderate | moderate | 100% |
| Lays chips (energy 2198kJ, fat 32g, sodium 620mg) | at-risk | at-risk | 99% |
| Broccoli (energy 136kJ, fibre 2.6g, sodium 33mg) | balanced | balanced | 100% |
| Tim Tam (energy 2120kJ, sugar 40g, fat 27g) | at-risk | at-risk | 99% |

### 6.2 Known Limitations and Bias

1. **Western food bias:** AUSNUT 2011-13 was collected from Australian dietary surveys. Foods common in South Asian, East Asian, or Middle Eastern cuisines may be underrepresented or matched to approximate equivalents, potentially reducing accuracy for multicultural lunchboxes.

2. **Label subjectivity:** The balanced/moderate/at-risk labels are rule-based, derived from ADG thresholds. These thresholds are evidence-based but not universally agreed upon (e.g. sugar guidelines vary between WHO, ADG, and NHS).

3. **Portion-size assumption:** Classification is per 100g. Real lunchbox portions vary, so a food classified as "at-risk" per 100g may be acceptable in a small serving size.

4. **High accuracy note:** The 99.7% accuracy is expected given the rule-based labelling — the model is essentially learning the same rules that generated the labels. In production, labels from a registered dietitian panel would increase real-world validity.

---

## 7. Integration into LittleWell

### 7.1 Training Pipeline
```
ausnut_2011_13.csv → preprocessing → ADG labelling → train_test_split(0.2) 
→ RandomForestClassifier.fit() → nutrition_classifier.pkl
```

### 7.2 Inference Pipeline (at runtime)
```
Lunchbox photo → Groq vision → detected food labels 
→ match to ausnut.csv rows → extract 9 nutrient features 
→ nutrition_classifier.pkl.predict() → Balanced/Moderate/At-Risk + confidence %
→ Display ML badge in FoodAnalyserPage.vue
```

### 7.3 API Endpoint
- **POST /ai-insights/classify-nutrition** — classify any nutriment dict
- **POST /ai-insights/train-classifier** — retrain model on demand, returns full classification report

---

## 8. MAI Outcomes Satisfied

| MAI Requirement | How This Feature Satisfies It |
|---|---|
| Predictive analytics (classifier) | RandomForestClassifier predicts 3 nutrition classes |
| Open source ML tools | scikit-learn, pandas, numpy — all open source |
| Train a model | Model trained on AUSNUT dataset, saved as .pkl |
| Evaluate trained model | Precision, recall, F1 per class; feature importance |
| Select and use metrics | Accuracy (99.7%), macro avg F1 (0.998), per-class support |
| Diagnose and resolve issues | Class imbalance addressed with class_weight=balanced |
| Research problem + dataset | AUSNUT 2011-13, Food Standards Australia, ADG basis |

---

## 9. Tools and Libraries

| Tool | Version | Purpose |
|---|---|---|
| scikit-learn | 1.4.2 | RandomForestClassifier, train_test_split, classification_report |
| pandas | 2.2.2 | Dataset loading, preprocessing, feature extraction |
| numpy | 1.26.4 | Feature vector construction for inference |
| Python | 3.12 | Runtime environment |
| FastAPI | latest | REST API serving the classifier |
| Groq API | 1.1.1 | Vision model for food detection, LLM for feedback |

---

