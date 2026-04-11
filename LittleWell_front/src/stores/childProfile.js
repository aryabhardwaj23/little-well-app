import { defineStore } from 'pinia';

const defaultDraft = () => ({
  name: '',
  ageGroup: '',
  gender: '',
  allergies: [],
  dietaryRestriction: '',
  activityLevel: 'moderate',
  eatingHabit: '',
  dislikes: '',
  nutritionFocus: [],
});

export const useChildProfileStore = defineStore('childProfile', {
  state: () => ({
    childProfileDraft: defaultDraft(),
  }),

  actions: {
    updateDraft(payload) {
      this.childProfileDraft = {
        ...this.childProfileDraft,
        ...payload,
      };
    },

    resetDraft() {
      this.childProfileDraft = defaultDraft();
    },
  },
});