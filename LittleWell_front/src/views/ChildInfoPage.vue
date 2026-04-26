<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-4xl">
      <!-- Back Button -->
      <button
        @click="router.push('/child-profile')"
        class="mb-6 px-4 py-2 hover:bg-white rounded-lg transition-colors inline-flex items-center gap-2"
      >
        <ArrowLeft class="w-4 h-4" />
        Back
      </button>

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl mb-4">Tell Us About Your Child</h1>
        <p class="text-lg text-muted-foreground">
          We'll use this information to personalize meal suggestions
        </p>
      </div>

      <!-- Form -->
      <div class="space-y-8">
        <!-- Basic Info -->
        <div class="p-8 rounded-2xl shadow-sm bg-white">
          <h2 class="text-2xl mb-6">Basic Information</h2>
          
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium mb-2">Child's Name (or nickname)</label>
              <input
                v-model="formData.name"
                type="text"
                placeholder="e.g. Emma"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent"
              />
              <p class="text-xs text-muted-foreground mt-1">We use nicknames only—no last names needed</p>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">Age</label>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <button
                  v-for="age in ageGroups"
                  :key="age"
                  @click="formData.ageGroup = age"
                  :class="[
                    'p-4 rounded-lg border-2 transition-all text-center',
                    formData.ageGroup === age
                      ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                      : 'border-gray-200 hover:border-[#A8D5BA]/50'
                  ]"
                >
                  {{ age }}
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">Gender (optional)</label>
              <div class="grid grid-cols-3 gap-3">
                <button
                  v-for="gender in genderOptions"
                  :key="gender"
                  @click="formData.gender = gender"
                  :class="[
                    'p-3 rounded-lg border-2 transition-all',
                    formData.gender === gender
                      ? 'border-[#CDE7F0] bg-[#CDE7F0]/20 text-[#1B4965]'
                      : 'border-gray-200 hover:border-[#CDE7F0]/50'
                  ]"
                >
                  {{ gender }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Health Information -->
        <div class="p-8 rounded-2xl shadow-sm bg-white">
          <h2 class="text-2xl mb-6">Health & Dietary Information</h2>
          
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium mb-2">Any food allergies?</label>
              <p class="text-sm text-muted-foreground mb-3">Select all that apply</p>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                <button
                  v-for="allergy in commonAllergies"
                  :key="allergy"
                  @click="toggleAllergy(allergy)"
                  :class="[
                    'p-3 rounded-lg border-2 transition-all text-sm',
                    formData.allergies.includes(allergy)
                      ? 'border-[#F7B267] bg-[#F7B267]/10 text-[#8B4513]'
                      : 'border-gray-200 hover:border-[#F7B267]/50'
                  ]"
                >
                  {{ allergy }}
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">Any dietary restrictions? (optional)</label>
              <select
                v-model="formData.dietaryRestriction"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent"
              >
                <option value="">No restrictions</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Vegan">Vegan</option>
                <option value="Halal">Halal</option>
                <option value="No pork">No pork</option>
                <option value="No beef">No beef</option>
                <option value="Pescatarian">Pescatarian</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">Activity level</label>
              <div class="grid grid-cols-3 gap-3">
                <button
                  v-for="level in activityLevels"
                  :key="level.value"
                  @click="formData.activityLevel = level.value"
                  :class="[
                    'p-4 rounded-lg border-2 transition-all',
                    formData.activityLevel === level.value
                      ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                      : 'border-gray-200 hover:border-[#A8D5BA]/50'
                  ]"
                >
                  <div class="text-2xl mb-1">{{ level.icon }}</div>
                  <div class="text-sm font-medium">{{ level.label }}</div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Eating Habits -->
        <div class="p-8 rounded-2xl shadow-sm bg-white">
          <h2 class="text-2xl mb-6">Eating Habits</h2>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">How would you describe your child's eating habits?</label>
              <div class="space-y-2">
                <label
                  v-for="habit in eatingHabits"
                  :key="habit"
                  class="flex items-center p-3 border-2 rounded-lg cursor-pointer hover:border-[#A8D5BA]/50 transition-colors"
                  :class="formData.eatingHabit === habit ? 'border-[#A8D5BA] bg-[#A8D5BA]/5' : 'border-gray-200'"
                >
                  <input
                    type="radio"
                    :value="habit"
                    v-model="formData.eatingHabit"
                    class="mr-3"
                  />
                  <span>{{ habit }}</span>
                </label>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">Any foods your child particularly dislikes?</label>
              <textarea
                v-model="formData.dislikes"
                rows="3"
                placeholder="e.g. mushrooms, eggplant..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent resize-none"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Continue Button -->
        <button
          @click="handleContinue"
          :disabled="!formData.name || !formData.ageGroup"
          class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-4 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Continue to Nutrition Focus
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft } from 'lucide-vue-next';
import { useChildProfileStore } from '../stores/childProfile';
import { getChildById } from '../services/api';

const router = useRouter();
const childProfileStore = useChildProfileStore();

const formData = ref({
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

onMounted(async () => {
  const editingChildId = localStorage.getItem('littlewell_edit_child_id');

  if (editingChildId) {
    try {
      const child = await getChildById(editingChildId);

      const draftData = {
        name: child.child_name || '',
        ageGroup: child.age_band || '',
        gender: child.gender || '',
        allergies: child.allergies || [],
        dietaryRestriction: child.religious_needs || '',
        activityLevel: child.activity_level || 'moderate',
        eatingHabit: child.eating_habit || '',
        dislikes: child.dislikes || '',
        nutritionFocus: mapStatusToNutritionFocus(child),
      };

      childProfileStore.updateDraft(draftData);

      formData.value = {
        ...formData.value,
        ...draftData,
      };
    } catch (error) {
      console.error('Failed to load child info for editing:', error);
    }
  } else {
    formData.value = {
      ...formData.value,
      ...childProfileStore.childProfileDraft,
    };
  }
});

const ageGroups = ['0-3 years', '3-6 years', '6-9 years', '9-12 years', '12+ years'];
const genderOptions = ['Boy', 'Girl', 'Prefer not to say'];

const mapStatusToNutritionFocus = (child) => {
  return [
    Number(child.iron_status) === 1 ? 'iron' : null,
    Number(child.calcium_status) === 1 ? 'calcium' : null,
    Number(child.vitamin_d_status) === 1 ? 'immunity' : null,
    Number(child.variety_status) === 1 ? 'variety' : null,
  ].filter(Boolean);
};

const commonAllergies = [
  'Peanuts', 'Tree nuts', 'Milk', 'Eggs',
  'Wheat', 'Soy', 'Fish', 'Shellfish',
];

const activityLevels = [
  { value: 'low', label: 'Light', icon: '🚶' },
  { value: 'moderate', label: 'Moderate', icon: '🏃' },
  { value: 'high', label: 'Active', icon: '⚡' },
];

const eatingHabits = [
  'Eats almost everything',
  'Usually willing to try new foods',
  'Picky eater - prefers familiar foods',
  'Very selective - limited food preferences',
];

const toggleAllergy = (allergy) => {
  if (formData.value.allergies.includes(allergy)) {
    formData.value.allergies = formData.value.allergies.filter(a => a !== allergy);
  } else {
    formData.value.allergies = [...formData.value.allergies, allergy];
  }
};

const handleContinue = () => {
  childProfileStore.updateDraft(formData.value);
  router.push('/nutrition-needs');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>