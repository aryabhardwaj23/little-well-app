const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    let message = 'Request failed';
    try { const e = await response.json(); message = e.detail || JSON.stringify(e); }
    catch { message = await response.text(); }
    throw new Error(message);
  }
  if (response.status === 204) return null;
  return response.json();
}

export function getMealById(mealId) {
  return request(`/api/meals/${mealId}`);
}

export function searchMeals(query, limit = 10) {
  return request(`/api/meals/search?q=${encodeURIComponent(query)}&limit=${limit}`);
}

export function getMealsByCategory(category, limit = 12) {
  return request(`/api/meals/filter/category?category=${encodeURIComponent(category)}&limit=${limit}`);
}

export function getMealCategories() {
  return request('/api/meals/categories');
}

export function getRandomMeal() {
  return request('/api/meals/random');
}

export function getRecommendations({ category=null, highIron=false, highCalcium=false, lowSugar=false, highProtein=false, highFibre=false, childAge=null, limit=6 } = {}) {
  const params = new URLSearchParams({ high_iron: String(highIron), high_calcium: String(highCalcium), low_sugar: String(lowSugar), high_protein: String(highProtein), high_fibre: String(highFibre), limit: String(limit) });
  if (category) params.append('category', category);
  if (childAge) params.append('child_age', String(childAge));
  return request(`/api/recommend?${params.toString()}`);
}

// Legacy functions — keep these so existing views don't break
export function getChildren() { return Promise.resolve([]); }
export function getChildById() { return Promise.resolve(null); }
export function createChild() { return Promise.resolve(null); }
export function updateChild() { return Promise.resolve(null); }

export async function getRecommendedProducts(childId, seasonal = true) {
  const data = await getRecommendations({ limit: 6 });
  return { lunchboxes: formatAsLunchboxes(data.recommendations), needsSupport: [] };
}

export async function getFamilyRecommendedProducts(childIds, seasonal = true) {
  const data = await getRecommendations({ limit: childIds.length * 2 });
  return { lunchboxes: formatAsLunchboxes(data.recommendations), needsSupport: [] };
}

export async function getQuickRecommendedProducts({ ageGroup, allergies = [], seasonal = true }) {
  const ageMap = { '5-7': 6, '8-10': 9, '11-12': 12 };
  const data = await getRecommendations({ childAge: ageMap[ageGroup] || 8, limit: 6 });
  return { lunchboxes: formatAsLunchboxes(data.recommendations), needsSupport: [] };
}

function formatAsLunchboxes(recommendations = []) {
  return recommendations.map((meal) => ({
    id: meal.id,
    childName: null,
    supportType: meal.nutrition_labels?.includes('High iron') ? 'iron' : meal.nutrition_labels?.includes('High calcium') ? 'calcium' : 'general',
    nutritionFocus: meal.nutrition_labels || ['Balanced nutrition'],
    whyThisMeal: meal.nutrition_labels?.length ? `This meal is ${meal.nutrition_labels.slice(0,2).join(' and ').toLowerCase()}, great for growing children.` : `A balanced ${meal.category || ''} meal for children.`,
    items: (meal.ingredients || []).slice(0, 4).map((ing, idx) => ({
      name: ing.ingredient,
      amount: ing.measure || '',
      image: meal.image || `https://www.themealdb.com/images/ingredients/${encodeURIComponent(ing.ingredient)}-Small.png`,
      section: ['carbs','protein','veggies','fruit'][idx] || 'carbs',
    })),
  }));
}
