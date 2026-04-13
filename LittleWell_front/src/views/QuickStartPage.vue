<template>
  <div class="min-h-screen py-12">
    <div class="container mx-auto px-6 max-w-3xl">
      <!-- Back Button -->
      <button
        @click="router.push('/')"
        class="mb-6 px-4 py-2 hover:bg-gray-100 rounded-lg transition-colors inline-flex items-center gap-2"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Home
      </button>

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl mb-4">Quick Meal Suggestions</h1>
        <p class="text-lg text-muted-foreground">
          Just a couple of quick questions to get you started
        </p>
      </div>

      <!-- Age Group Selection -->
      <div class="p-8 rounded-2xl shadow-sm mb-8 bg-white border">
        <label class="text-lg mb-4 block font-medium">What's your child's age?</label>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <button
            v-for="age in ageGroups"
            :key="age"
            @click="ageGroup = age"
            :class="[
              'p-4 rounded-lg border-2 transition-all',
              ageGroup === age
                ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                : 'border-gray-200 hover:border-[#A8D5BA]/50'
            ]"
          >
            {{ age }}
          </button>
        </div>
      </div>

      <!-- Allergies -->
      <div class="p-8 rounded-2xl shadow-sm mb-8 bg-white border">
        <label class="text-lg mb-4 block font-medium">
          Any allergies or intolerances? (optional)
        </label>
        <p class="text-sm text-muted-foreground mb-4">
          Select all that apply
        </p>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <button
            v-for="allergy in commonAllergies"
            :key="allergy"
            @click="toggleAllergy(allergy)"
            :class="[
              'p-4 rounded-lg border-2 transition-all',
              allergies.includes(allergy)
                ? 'border-[#F7B267] bg-[#F7B267]/10 text-[#8B4513]'
                : 'border-gray-200 hover:border-[#F7B267]/50'
            ]"
          >
            {{ allergy }}
          </button>
        </div>
      </div>

      <!-- Continue Button -->
      <button
        @click="handleContinue"
        :disabled="!ageGroup"
        class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Get Meal Suggestions
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft } from 'lucide-vue-next';

const router = useRouter();

const ageGroup = ref('');
const allergies = ref([]);

const ageGroups = ['0-3 years', '3-6 years', '6-9 years', '9-12 years', '12+ years'];

const commonAllergies = [
  'Peanuts',
  'Tree nuts',
  'Milk',
  'Eggs',
  'Wheat',
  'Soy',
  'Fish',
  'Shellfish',
];

const toggleAllergy = (allergy) => {
  if (allergies.value.includes(allergy)) {
    allergies.value = allergies.value.filter(a => a !== allergy);
  } else {
    allergies.value = [...allergies.value, allergy];
  }
};

const handleContinue = () => {
  const query = new URLSearchParams({
    quick: '1',
    ageGroup: ageGroup.value,
    allergies: allergies.value.join(','),
  });

  router.push(`/results?${query.toString()}`);
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>
