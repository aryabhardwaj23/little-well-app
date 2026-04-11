const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = 'Request failed';
    try {
      const errorData = await response.json();
      message = errorData.detail || JSON.stringify(errorData);
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