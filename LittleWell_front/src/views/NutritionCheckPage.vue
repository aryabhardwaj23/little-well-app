<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-4xl">
      <!-- Back Button -->
      <button
        @click="goBack"
        class="mb-6 px-4 py-2 hover:bg-white rounded-lg transition-colors inline-flex items-center gap-2"
      >
        <ArrowLeft class="w-4 h-4" />
        Back
      </button>

      <!-- Header -->
      <div class="text-center mb-12">
        <div class="w-16 h-16 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center mx-auto mb-4">
          <ClipboardCheck class="w-8 h-8 text-white" />
        </div>
        <h1 class="text-4xl mb-4">Quick Nutrition Check</h1>
        <p class="text-lg text-muted-foreground">
          Answer a few questions about your child's current diet
        </p>
        <p class="text-sm text-muted-foreground mt-2">
          This helps us provide more personalized meal suggestions
        </p>
      </div>

      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex justify-between text-sm text-muted-foreground mb-2">
          <span>Question {{ currentQuestion + 1 }} of {{ questions.length }}</span>
          <span>{{ Math.round(((currentQuestion + 1) / questions.length) * 100) }}% complete</span>
        </div>
        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-[#A8D5BA] to-[#8FC2A4] transition-all duration-300"
            :style="{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }"
          ></div>
        </div>
      </div>

      <!-- Question Card -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-6">
        <div class="mb-6">
          <div class="flex items-start gap-3 mb-4">
            <div :class="['w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0', questions[currentQuestion].colorClass]">
              <component :is="questions[currentQuestion].icon" class="w-5 h-5 text-white" />
            </div>

            <div class="flex-1">
              <p class="text-sm text-muted-foreground mb-2">
                {{ questions[currentQuestion].category }}
              </p>
              <h2 class="text-xl font-medium">
                {{ questions[currentQuestion].question }}
              </h2>
            </div>
          </div>
        </div>

        <!-- Options -->
        <div class="space-y-3">
          <button
            v-for="option in questions[currentQuestion].options"
            :key="option.value"
            @click="selectAnswer(option.value)"
            :class="[
              'w-full p-4 rounded-lg border-2 text-left transition-all',
              answers[questions[currentQuestion].id] === option.value
                ? 'border-[#A8D5BA] bg-[#A8D5BA]/10'
                : 'border-gray-200 hover:border-[#A8D5BA]/50',
            ]"
          >
            <div class="flex items-center justify-between">
              <span>{{ option.label }}</span>

              <div
                v-if="answers[questions[currentQuestion].id] === option.value"
                class="w-5 h-5 bg-[#A8D5BA] rounded-full flex items-center justify-center"
              >
                <Check class="w-3 h-3 text-white" />
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex gap-4">
        <button
          v-if="currentQuestion > 0"
          @click="previousQuestion"
          class="px-8 py-4 bg-white border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Previous
        </button>

        <button
          v-if="currentQuestion < questions.length - 1"
          @click="nextQuestion"
          :disabled="!answers[questions[currentQuestion].id]"
          class="flex-1 px-8 py-4 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Next Question
        </button>

        <button
          v-else
          @click="handleComplete"
          :disabled="!answers[questions[currentQuestion].id]"
          class="flex-1 px-8 py-4 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex items-center justify-center gap-2"
        >
          <Check class="w-4 h-4" />
          Complete Check
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  ArrowLeft,
  Check,
  ClipboardCheck,
  Apple,
  Droplet,
  Cookie,
  Carrot,
} from 'lucide-vue-next';
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

const getActiveChildId = () => {
  return (
    route.query.childId ||
    localStorage.getItem('littlewell_active_child_id') ||
    localStorage.getItem('littlewell_edit_child_id') ||
    ''
  );
};

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
  const childId = getActiveChildId();

  if (childId) {
    router.push(`/profile-summary?childId=${childId}`);
    return;
  }

  router.push('/child-info');
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
  const percentage = (totalScore / maxScore) * 100;

  nutritionCheckStore.setResult({
    answers: { ...answers.value },
    nutritionInsights: insights,
    score: percentage,
    completedAt: new Date().toISOString(),
  });

  const childId = getActiveChildId();

  if (childId) {
    router.push(`/nutrition-insights?childId=${childId}`);
  } else {
    router.push('/nutrition-insights');
  }
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>