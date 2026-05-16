<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-4xl px-4 sm:px-6">
      <!-- Back Button -->
      <button
        @click="goBack"
        class="mb-5 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-white sm:mb-6 sm:px-4"
        type="button"
        aria-label="Go back"
      >
        <ArrowLeft class="h-4 w-4" aria-hidden="true" />
        Back
      </button>

      <!-- Header -->
      <header class="mb-8 text-center sm:mb-12">
        <div
          class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] sm:h-16 sm:w-16"
          aria-hidden="true"
        >
          <ClipboardCheck class="h-7 w-7 text-white sm:h-8 sm:w-8" />
        </div>

        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          Quick Nutrition Check
        </h1>

        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          Answer a few questions about your child's current diet
        </p>

        <p class="mt-2 text-xs leading-relaxed text-muted-foreground sm:text-sm">
          This helps us provide more personalized meal suggestions
        </p>
      </header>

      <!-- Progress Bar -->
      <section class="mb-6 sm:mb-8" aria-label="Nutrition check progress">
        <div class="mb-2 flex justify-between gap-4 text-xs text-muted-foreground sm:text-sm">
          <span aria-live="polite">
            Question {{ currentQuestion + 1 }} of {{ questions.length }}
          </span>
          <span class="shrink-0">
            {{ Math.round(((currentQuestion + 1) / questions.length) * 100) }}% complete
          </span>
        </div>

        <div
          class="h-2 w-full overflow-hidden rounded-full bg-gray-200"
          role="progressbar"
          :aria-valuenow="currentQuestion + 1"
          :aria-valuemin="1"
          :aria-valuemax="questions.length"
          :aria-label="`Question ${currentQuestion + 1} of ${questions.length}`"
        >
          <div
            class="h-full bg-gradient-to-r from-[#A8D5BA] to-[#8FC2A4] transition-all duration-300"
            :style="{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }"
          ></div>
        </div>
      </section>

      <!-- Question Card -->
      <section class="mb-5 rounded-2xl bg-white p-5 shadow-sm sm:mb-6 sm:p-8">
        <div class="mb-5 sm:mb-6">
          <div class="flex items-start gap-3 sm:gap-4">
            <div
              :class="[
                'flex h-10 w-10 shrink-0 items-center justify-center rounded-full sm:h-11 sm:w-11',
                questions[currentQuestion].colorClass
              ]"
              aria-hidden="true"
            >
              <component :is="questions[currentQuestion].icon" class="h-5 w-5 text-white" />
            </div>

            <div class="min-w-0 flex-1">
              <p class="mb-2 text-xs text-muted-foreground sm:text-sm">
                {{ questions[currentQuestion].category }}
              </p>

              <h2
                class="text-lg font-semibold leading-snug text-[#111827] sm:text-xl"
                :id="`question-${currentQuestion}`"
              >
                {{ questions[currentQuestion].question }}
              </h2>
            </div>
          </div>
        </div>

        <!-- Options -->
        <div
          role="group"
          :aria-labelledby="`question-${currentQuestion}`"
          class="space-y-3"
        >
          <button
            v-for="option in questions[currentQuestion].options"
            :key="option.value"
            type="button"
            @click="selectAnswer(option.value)"
            :aria-pressed="answers[questions[currentQuestion].id] === option.value"
            :class="[
              'w-full rounded-xl border-2 p-4 text-left transition-all sm:rounded-lg',
              answers[questions[currentQuestion].id] === option.value
                ? 'border-[#A8D5BA] bg-[#A8D5BA]/10'
                : 'border-gray-200 hover:border-[#A8D5BA]/50'
            ]"
          >
            <div class="flex items-center justify-between gap-3">
              <span class="text-sm leading-relaxed text-[#111827] sm:text-base">
                {{ option.label }}
              </span>

              <div
                v-if="answers[questions[currentQuestion].id] === option.value"
                class="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#A8D5BA]"
                aria-hidden="true"
              >
                <Check class="h-3 w-3 text-white" />
              </div>
            </div>
          </button>
        </div>
      </section>

      <!-- Navigation Buttons -->
      <div class="flex flex-col-reverse gap-3 sm:flex-row sm:gap-4">
        <button
          v-if="currentQuestion > 0"
          @click="previousQuestion"
          type="button"
          class="w-full rounded-lg border-2 border-gray-300 bg-white px-8 py-3.5 text-gray-700 transition-colors hover:bg-gray-50 sm:w-auto sm:py-4"
        >
          Previous
        </button>

        <button
          v-if="currentQuestion < questions.length - 1"
          @click="nextQuestion"
          type="button"
          :disabled="!answers[questions[currentQuestion].id]"
          class="w-full flex-1 rounded-lg bg-[#A8D5BA] px-8 py-3.5 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50 sm:py-4"
          :aria-disabled="!answers[questions[currentQuestion].id]"
        >
          Next Question
        </button>

        <button
          v-else
          @click="handleComplete"
          type="button"
          :disabled="!answers[questions[currentQuestion].id]"
          class="inline-flex w-full flex-1 items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3.5 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50 sm:py-4"
          :aria-disabled="!answers[questions[currentQuestion].id]"
        >
          <Check class="h-4 w-4" aria-hidden="true" />
          Complete Check
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ArrowLeft, Check, ClipboardCheck, Apple, Droplet, Cookie, Carrot } from 'lucide-vue-next';
import { useNutritionCheckStore } from '../stores/nutritionCheck';

const router = useRouter();
const route = useRoute();
const nutritionCheckStore = useNutritionCheckStore();

const currentQuestion = ref(0);
const answers = ref({});

const questions = [
  {
    id: 'fruits',
    category: 'Fruits & Vegetables',
    question: 'How many servings of fruits and vegetables does your child eat daily?',
    icon: Apple,
    colorClass: 'bg-[#F7B267]',
    options: [
      { value: 'excellent', label: '5 or more servings' },
      { value: 'good', label: '3-4 servings' },
      { value: 'needs', label: '1-2 servings' },
      { value: 'poor', label: 'Less than 1 serving' },
    ],
  },
  {
    id: 'water',
    category: 'Hydration',
    question: 'How much water does your child drink each day?',
    icon: Droplet,
    colorClass: 'bg-[#CDE7F0]',
    options: [
      { value: 'excellent', label: '6+ glasses (1.5L+)' },
      { value: 'good', label: '4-5 glasses (1-1.5L)' },
      { value: 'needs', label: '2-3 glasses (500ml-1L)' },
      { value: 'poor', label: 'Less than 2 glasses' },
    ],
  },
  {
    id: 'sugar',
    category: 'Sugar & Processed Foods',
    question: 'How often does your child consume sugary snacks or drinks?',
    icon: Cookie,
    colorClass: 'bg-[#F7B267]',
    options: [
      { value: 'excellent', label: 'Rarely (once a week or less)' },
      { value: 'good', label: 'Sometimes (2-3 times a week)' },
      { value: 'needs', label: 'Often (4-5 times a week)' },
      { value: 'poor', label: 'Daily or multiple times daily' },
    ],
  },
  {
    id: 'protein',
    category: 'Protein',
    question: 'Does your child get protein from varied sources?',
    icon: Carrot,
    colorClass: 'bg-[#A8D5BA]',
    options: [
      { value: 'excellent', label: 'Yes, from multiple sources (meat, fish, eggs, legumes)' },
      { value: 'good', label: 'Yes, from 2-3 sources' },
      { value: 'needs', label: 'Only from 1-2 sources' },
      { value: 'poor', label: 'Very limited protein intake' },
    ],
  },
];

const selectAnswer = (value) => {
  answers.value[questions[currentQuestion.value].id] = value;
};

const nextQuestion = () => {
  if (currentQuestion.value < questions.length - 1) {
    currentQuestion.value++;
  }
};

const previousQuestion = () => {
  if (currentQuestion.value > 0) {
    currentQuestion.value--;
  }
};

const goBack = () => {
  const childId = route.query.childId;
  router.push(childId ? `/profile-summary?childId=${childId}` : '/profile-summary');
};

const handleComplete = () => {
  const insights = {
    fruits: answers.value.fruits || 'needs',
    water: answers.value.water || 'needs',
    sugar: answers.value.sugar || 'needs',
    protein: answers.value.protein || 'needs',
  };

  const scoreMap = {
    excellent: 4,
    good: 3,
    needs: 2,
    poor: 1,
  };

  const totalScore = Object.values(insights).reduce((sum, val) => sum + scoreMap[val], 0);
  const maxScore = Object.keys(insights).length * 4;

  nutritionCheckStore.setResult({
    answers: { ...answers.value },
    nutritionInsights: insights,
    score: (totalScore / maxScore) * 100,
    completedAt: new Date().toISOString(),
  });

  const childId = route.query.childId || '';
  router.push(childId ? `/nutrition-insights?childId=${childId}` : '/nutrition-insights');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>