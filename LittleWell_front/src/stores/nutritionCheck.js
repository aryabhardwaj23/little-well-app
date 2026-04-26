import { defineStore } from 'pinia';

const defaultResult = () => ({
  answers: {},
  nutritionInsights: null,
  score: null,
  completedAt: null,
});

export const useNutritionCheckStore = defineStore('nutritionCheck', {
  state: () => ({
    result: defaultResult(),
  }),

  actions: {
    setResult(payload) {
      this.result = {
        ...defaultResult(),
        ...payload,
      };
    },

    resetResult() {
      this.result = defaultResult();
    },
  },
});