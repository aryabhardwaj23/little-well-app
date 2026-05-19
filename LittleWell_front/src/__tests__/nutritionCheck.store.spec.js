import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useNutritionCheckStore } from '@/stores/nutritionCheck';

describe('nutritionCheck store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('has a defined result state on init', () => {
    const store = useNutritionCheckStore();
    // The store initialises with an object (not null) — just check it exists
    expect(store.result).toBeDefined();
  });

  it('score is falsy (null or 0) before setResult is called', () => {
    const store = useNutritionCheckStore();
    expect(store.result.score).toBeFalsy();
  });

  it('nutritionInsights is null before setResult is called', () => {
    const store = useNutritionCheckStore();
    expect(store.result.nutritionInsights).toBeNull();
  });

  it('setResult stores the result', () => {
    const store = useNutritionCheckStore();
    const mockResult = {
      answers: { fruits: 'good', water: 'excellent', sugar: 'needs', protein: 'good' },
      nutritionInsights: { fruits: 'good', water: 'excellent', sugar: 'needs', protein: 'good' },
      score: 75,
      completedAt: '2026-05-15T00:00:00.000Z',
    };
    store.setResult(mockResult);
    expect(store.result).toEqual(mockResult);
  });

  it('setResult overwrites a previous result', () => {
    const store = useNutritionCheckStore();
    store.setResult({ score: 50 });
    store.setResult({ score: 80 });
    expect(store.result.score).toBe(80);
  });

  it('stores nutritionInsights correctly', () => {
    const store = useNutritionCheckStore();
    store.setResult({
      nutritionInsights: { fruits: 'excellent', water: 'good' },
      score: 90,
    });
    expect(store.result.nutritionInsights.fruits).toBe('excellent');
  });
});