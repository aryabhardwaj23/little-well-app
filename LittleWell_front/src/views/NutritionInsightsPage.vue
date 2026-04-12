<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-5xl">
      <!-- Header -->
      <div class="text-center mb-12">
        <div :class="['w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4', getScoreColor(score)]">
          <Sparkles class="w-10 h-10 text-white" />
        </div>
        <h1 class="text-4xl mb-4">Your Nutrition Insights</h1>
        <p class="text-lg text-muted-foreground">
          Based on your child's current diet
        </p>
      </div>

      <!-- Overall Score Card -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <div class="text-center">
          <p class="text-muted-foreground mb-2">Overall Nutrition Score</p>
          <div class="text-5xl font-bold mb-4" :class="getScoreTextColor(score)">
            {{ Math.round(score) }}%
          </div>
          <p class="text-lg">{{ getScoreMessage(score) }}</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4">
        <button
          @click="router.push('/results')"
          class="flex-1 px-8 py-4 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg transition-colors inline-flex items-center justify-center gap-2"
        >
          <ChevronRight class="w-4 h-4" />
          View Personalized Lunchboxes
        </button>
        <button
          @click="router.push('/')"
          class="flex-1 px-8 py-4 bg-white border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Back to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Sparkles, ChevronRight } from 'lucide-vue-next';

const router = useRouter();

const score = ref(0);

onMounted(() => {
  const checkData = localStorage.getItem('nutriguide_nutrition_check');
  if (checkData) {
    const data = JSON.parse(checkData);
    score.value = data.score || 0;
  } else {
    router.push('/nutrition-check');
  }
});

const getScoreColor = (score) => {
  if (score >= 75) return 'bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4]';
  if (score >= 50) return 'bg-gradient-to-br from-[#F7B267] to-[#E5A156]';
  return 'bg-gradient-to-br from-[#CDE7F0] to-[#B5D3E0]';
};

const getScoreTextColor = (score) => {
  if (score >= 75) return 'text-[#2C5F2D]';
  if (score >= 50) return 'text-[#8B4513]';
  return 'text-[#1B4965]';
};

const getScoreMessage = (score) => {
  if (score >= 75) return "Great job! Your child's diet is well-balanced.";
  if (score >= 50) return 'Good start! A few improvements can make a big difference.';
  return "Let's work together to improve your child's nutrition.";
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>