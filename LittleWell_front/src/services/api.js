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
    let message = `Request failed: ${response.status}`;

    try {
      const errorData = await response.json();

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