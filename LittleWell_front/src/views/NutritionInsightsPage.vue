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

      <!-- Detailed Insights -->
      <div class="grid md:grid-cols-2 gap-6 mb-8">
        <div
          v-for="(status, area) in insights"
          :key="area"
          class="bg-white rounded-2xl shadow-md p-6"
        >
          <div class="flex items-start gap-4 mb-4">
            <div :class="['w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0', getAreaColor(status)]">
              <component :is="getAreaIcon(area)" class="w-6 h-6 text-white" />
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-medium mb-1">{{ getAreaTitle(area) }}</h3>
              <span :class="['text-sm px-3 py-1 rounded-full', getStatusBadge(status)]">
                {{ getStatusLabel(status) }}
              </span>
            </div>
          </div>
          <p class="text-sm text-muted-foreground">
            {{ getAreaAdvice(area, status) }}
          </p>
        </div>
      </div>

      <!-- Recommendations -->
      <div class="bg-gradient-to-br from-[#A8D5BA]/20 to-[#CDE7F0]/20 rounded-2xl p-8 mb-8">
        <h2 class="text-2xl mb-6 flex items-center gap-2">
          <Lightbulb class="w-6 h-6 text-[#F7B267]" />
          Personalized Recommendations
        </h2>
        <div class="space-y-4">
          <div
            v-for="(rec, idx) in recommendations"
            :key="idx"
            class="flex items-start gap-3 p-4 bg-white rounded-lg"
          >
            <div class="w-8 h-8 bg-[#A8D5BA] rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
              <Check class="w-4 h-4 text-white" />
            </div>
            <p class="flex-1">{{ rec }}</p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4">
        <button
          @click="handleViewResults"
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Sparkles, Check, ChevronRight, Lightbulb, Apple, Droplet, Cookie, Carrot } from 'lucide-vue-next';
import { useNutritionCheckStore } from '../stores/nutritionCheck';

const router = useRouter();
const nutritionCheckStore = useNutritionCheckStore();

const score = ref(0);
const insights = ref({});
const recommendations = ref([]);

onMounted(() => {
  const result = nutritionCheckStore.result;

  if (!result || !result.nutritionInsights) {
    router.push('/nutrition-check');
    return;
  }

  score.value = result.score || 0;
  insights.value = result.nutritionInsights || {};
  recommendations.value = generateRecommendations(insights.value);
});

const handleViewResults = () => {
  const childId = localStorage.getItem('littlewell_edit_child_id')
    || localStorage.getItem('littlewell_active_child_id');

  if (childId) {
    router.push(`/results?childId=${childId}`);
  } else {
    router.push('/');
  }
};

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
  if (score >= 75) return 'Great job! Your child\'s diet is well-balanced.';
  if (score >= 50) return 'Good start! A few improvements can make a big difference.';
  return 'Let\'s work together to improve your child\'s nutrition.';
};

const getAreaColor = (status) => {
  const colors = {
    excellent: 'bg-[#A8D5BA]',
    good: 'bg-[#8BC34A]',
    needs: 'bg-[#F7B267]',
    poor: 'bg-[#E57373]',
  };
  return colors[status] || 'bg-gray-400';
};

const getStatusBadge = (status) => {
  const badges = {
    excellent: 'bg-[#A8D5BA]/20 text-[#2C5F2D]',
    good: 'bg-green-100 text-green-700',
    needs: 'bg-[#F7B267]/20 text-[#8B4513]',
    poor: 'bg-red-100 text-red-700',
  };
  return badges[status] || '';
};

const getStatusLabel = (status) => {
  const labels = {
    excellent: 'Excellent',
    good: 'Good',
    needs: 'Needs Improvement',
    poor: 'Needs Attention',
  };
  return labels[status] || status;
};

const getAreaIcon = (area) => {
  const icons = {
    fruits: Apple,
    water: Droplet,
    sugar: Cookie,
    protein: Carrot,
  };
  return icons[area] || Apple;
};

const getAreaTitle = (area) => {
  const titles = {
    fruits: 'Fruits & Vegetables',
    water: 'Hydration',
    sugar: 'Sugar Intake',
    protein: 'Protein Variety',
  };
  return titles[area] || area;
};

const getAreaAdvice = (area, status) => {
  const advice = {
    fruits: {
      excellent: 'Wonderful! Your child is getting plenty of vitamins and fiber.',
      good: 'Good progress! Try to add one more serving of colorful vegetables daily.',
      needs: 'Aim for 5 servings daily. Try adding fruit to breakfast and veggies to lunch.',
      poor: 'Fruits and vegetables are crucial. Start with 1-2 favorite fruits as snacks.',
    },
    water: {
      excellent: 'Perfect! Your child is well-hydrated throughout the day.',
      good: 'Good hydration! Encourage drinking water between meals too.',
      needs: 'Offer water regularly, especially during play. Try a fun water bottle.',
      poor: 'Hydration is essential. Set reminders and make water easily accessible.',
    },
    sugar: {
      excellent: 'Excellent! Your child is avoiding excessive sugar intake.',
      good: 'Good job limiting sugar! Continue to choose natural alternatives.',
      needs: 'Try to reduce sugary snacks. Offer fruit as a sweet alternative.',
      poor: 'High sugar affects mood and energy. Gradually reduce sweetened foods.',
    },
    protein: {
      excellent: 'Great! Your child gets protein from diverse sources.',
      good: 'Good variety! Consider adding legumes or fish occasionally.',
      needs: 'Introduce more protein sources. Try eggs, beans, or yogurt.',
      poor: 'Protein is vital for growth. Start with child-friendly options like cheese.',
    },
  };
  return advice[area]?.[status] || '';
};

const generateRecommendations = (insights) => {
  const recs = [];
  
  if (insights.fruits === 'needs' || insights.fruits === 'poor') {
    recs.push('Add colorful vegetables to lunchboxes - children eat with their eyes first!');
  }
  
  if (insights.water === 'needs' || insights.water === 'poor') {
    recs.push('Send a fun, reusable water bottle to school every day.');
  }
  
  if (insights.sugar === 'needs' || insights.sugar === 'poor') {
    recs.push('Replace sugary snacks with naturally sweet fruits like berries and melon.');
  }
  
  if (insights.protein === 'needs' || insights.protein === 'poor') {
    recs.push('Include protein in every meal - try hard-boiled eggs, cheese, or nut butter.');
  }
  
  recs.push('Involve your child in meal planning - they\'re more likely to eat what they help choose!');
  recs.push('Make meals colorful and fun with different shapes and arrangements.');
  
  return recs;
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>
