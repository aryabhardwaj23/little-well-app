<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-3xl px-4 sm:px-6">
      <!-- Back Button -->
      <button
        @click="router.push('/')"
        class="mb-5 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-white sm:mb-6 sm:px-4"
        type="button"
        aria-label="Back to Home"
      >
        <ArrowLeft class="h-4 w-4" aria-hidden="true" />
        Back to Home
      </button>

      <!-- Header -->
      <header class="mb-8 text-center sm:mb-12">
        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          Quick Meal Suggestions
        </h1>

        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          Get simple lunchbox ideas for children aged 5–12
        </p>
      </header>

      <!-- Age Group Selection -->
      <section class="mb-5 rounded-2xl border bg-white p-5 shadow-sm sm:mb-8 sm:p-8">
        <fieldset>
          <legend class="mb-3 block text-lg font-semibold text-[#111827] sm:mb-4">
            What's your child's age?
          </legend>

          <p id="age-group-hint" class="mb-4 text-sm leading-relaxed text-muted-foreground">
            LittleWell currently supports school-aged children from 5 to 12 years old.
          </p>

          <div
            class="grid grid-cols-1 gap-2 sm:grid-cols-3 sm:gap-3"
            role="group"
            aria-describedby="age-group-hint"
          >
            <button
              v-for="age in ageGroups"
              :key="age"
              @click="ageGroup = age"
              :aria-pressed="ageGroup === age"
              :class="[
                'min-h-[48px] rounded-lg border-2 p-3 text-sm font-medium transition-all sm:p-4 sm:text-base',
                ageGroup === age
                  ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                  : 'border-gray-200 hover:border-[#A8D5BA]/50'
              ]"
              type="button"
            >
              {{ age }}
            </button>
          </div>
        </fieldset>
      </section>

      <!-- Allergies -->
      <section class="mb-5 rounded-2xl border bg-white p-5 shadow-sm sm:mb-8 sm:p-8">
        <fieldset>
          <legend class="mb-3 block text-lg font-semibold text-[#111827] sm:mb-4">
            Any allergies or intolerances? (optional)
          </legend>

          <p id="allergy-hint" class="mb-4 text-sm text-muted-foreground">
            Select all that apply
          </p>

          <div
            class="grid grid-cols-2 gap-2 sm:grid-cols-4 sm:gap-3"
            role="group"
            aria-describedby="allergy-hint"
          >
            <button
              v-for="allergy in commonAllergies"
              :key="allergy"
              @click="toggleAllergy(allergy)"
              :aria-pressed="allergies.includes(allergy)"
              :class="[
                'min-h-[48px] rounded-lg border-2 px-2 py-3 text-sm font-medium transition-all sm:p-4 sm:text-base',
                allergies.includes(allergy)
                  ? 'border-[#F7B267] bg-[#F7B267]/10 text-[#8B4513]'
                  : 'border-gray-200 hover:border-[#F7B267]/50'
              ]"
              type="button"
            >
              {{ allergy }}
            </button>
          </div>
        </fieldset>
      </section>

      <!-- Continue Button -->
      <div class="sticky bottom-0 z-20 -mx-4 bg-[#FAF9F6]/95 px-4 py-4 backdrop-blur sm:static sm:mx-0 sm:bg-transparent sm:px-0 sm:py-0 sm:backdrop-blur-0">
        <button
          @click="handleContinue"
          :disabled="!ageGroup"
          class="w-full rounded-xl bg-[#A8D5BA] py-4 text-base font-semibold text-[#2C5F2D] shadow-sm transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50 sm:text-lg"
          type="button"
          :aria-disabled="!ageGroup"
        >
          Get Meal Suggestions
        </button>
      </div>
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

const ageGroups = ['5-6 years', '7-9 years', '10-12 years'];

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
    allergies.value = allergies.value.filter((a) => a !== allergy);
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