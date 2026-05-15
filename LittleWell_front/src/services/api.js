const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

function getAuthToken() {
  return localStorage.getItem('littlewell_token');
}

function buildHeaders(customHeaders = {}) {
  const token = getAuthToken();

  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...customHeaders,
  };
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: buildHeaders(options.headers || {}),
  });

  if (!response.ok) {
    let message = `Request failed: ${response.status}`;

    try {
      const errorData = await response.json();

      if (response.status === 401) {
        localStorage.removeItem('littlewell_token');
        localStorage.removeItem('littlewell_user');
      }

      if (typeof errorData.detail === 'string') {
        message = errorData.detail;
      } else if (Array.isArray(errorData.detail)) {
        message = errorData.detail
          .map((item) => {
            const field = item.loc ? item.loc.join(' -> ') : 'field';
            return `${field}: ${item.msg}`;
          })
          .join('\n');
      } else if (errorData.detail) {
        message = JSON.stringify(errorData.detail);
      } else {
        message = JSON.stringify(errorData);
      }
    } catch {
      message = await response.text();
    }

    throw new Error(message);
  }

  if (response.status === 204) return null;
  return response.json();
}

// children
export function getChildren() {
  return request('/children');
}

export function getChildById(childId) {
  return request(`/children/${childId}`);
}

export function createChild(payload) {
  return request('/children', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateChild(childId, payload) {
  return request(`/children/${childId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function deleteChild(childId) {
  return request(`/children/${childId}`, {
    method: 'DELETE',
  });
}

// recommendations / products
export function getRecommendedProducts(childId, seasonal = true) {
  return request(`/products/recommended?child_id=${childId}&seasonal=${seasonal}`);
}

export function getFamilyRecommendedProducts(childIds, seasonal = true) {
  const query = new URLSearchParams({
    child_ids: childIds.join(','),
    seasonal: String(seasonal),
  });

  return request(`/products/recommended/family?${query.toString()}`);
}

export function getQuickRecommendedProducts({ ageGroup, allergies = [], seasonal = true }) {
  const query = new URLSearchParams({
    ageGroup,
    allergies: allergies.join(','),
    seasonal: String(seasonal),
  });

  return request(`/products/recommended/quick?${query.toString()}`);
}

export function getChildMealRecommendations(childId) {
  return request(`/products/recommended/mealdb/child?child_id=${childId}`);
}

// weekly plans
export function createWeeklyPlan(payload) {
  return request('/weekly-plans', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getWeeklyPlans() {
  return request('/weekly-plans');
}

export function getWeeklyPlanById(planId) {
  return request(`/weekly-plans/${planId}`);
}

export function updateWeeklyPlan(planId, payload) {
  return request(`/weekly-plans/${planId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function deleteWeeklyPlan(planId) {
  return request(`/weekly-plans/${planId}`, {
    method: 'DELETE',
  });
}

export function duplicateWeeklyPlan(planId) {
  return request(`/weekly-plans/${planId}/duplicate`, {
    method: 'POST',
  });
}

export function swapWeeklyPlanMeal(planId, mealId, payload) {
  return request(`/weekly-plans/${planId}/meals/${mealId}/swap`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export const getMealRecipeDetail = async (mealId, childName = '') => {
  const query = childName ? `?child_name=${encodeURIComponent(childName)}` : '';

  return request(`/products/recommended/mealdb/recipe/${mealId}${query}`);
};

export function generateWeeklyPlanFromBackend(payload) {
  return request('/weekly-plans/generate', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

// knowledge hub
export function getKnowledgeChildrenServes() {
  return request('/knowledge/serves/children');
}

export function getKnowledgeFoodGroups() {
  return request('/knowledge/food-groups');
}

export function getKnowledgeAdditiveAwareness() {
  return request('/knowledge/additive-awareness');
}

export function getKnowledgeAdditiveHeatmap() {
  return request('/knowledge/additive-heatmap');
}