<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-5xl px-4 sm:px-6">
      <!-- Header -->
      <header class="mb-8 text-center sm:mb-12">
        <div
          :class="[
            'mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full sm:h-20 sm:w-20',
            getScoreColor(score)
          ]"
          aria-hidden="true"
        >
          <Sparkles class="h-8 w-8 text-white sm:h-10 sm:w-10" />
        </div>

        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          Your Nutrition Insights
        </h1>

        <p class="text-sm leading-relaxed text-muted-foreground sm:text-lg">
          Based on your child's current diet
        </p>
      </header>

      <!-- Overall Score Card -->
      <section class="mb-6 rounded-2xl bg-white p-6 text-center shadow-sm sm:mb-8 sm:p-8">
        <p class="mb-2 text-sm text-muted-foreground sm:text-base">
          Overall Nutrition Score
        </p>

        <div
          class="mb-3 text-5xl font-bold leading-none sm:mb-4 sm:text-6xl"
          :class="getScoreTextColor(score)"
        >
          {{ Math.round(score) }}%
        </div>

        <p class="mx-auto max-w-xl text-base leading-relaxed text-[#111827] sm:text-lg">
          {{ getScoreMessage(score) }}
        </p>
      </section>

      <!-- Detailed Insights -->
      <section class="mb-6 grid grid-cols-1 gap-4 sm:mb-8 md:grid-cols-2 md:gap-6">
        <article
          v-for="(status, area) in insights"
          :key="area"
          class="rounded-2xl bg-white p-5 shadow-sm sm:p-6"
        >
          <div class="mb-4 flex items-start gap-3 sm:gap-4">
            <div
              :class="[
                'flex h-11 w-11 shrink-0 items-center justify-center rounded-full sm:h-12 sm:w-12',
                getAreaColor(status)
              ]"
              aria-hidden="true"
            >
              <component :is="getAreaIcon(area)" class="h-5 w-5 text-white sm:h-6 sm:w-6" />
            </div>

            <div class="min-w-0 flex-1">
              <h3 class="mb-2 text-base font-semibold leading-tight text-[#111827] sm:text-lg">
                {{ getAreaTitle(area) }}
              </h3>

              <span
                :class="[
                  'inline-flex rounded-full px-3 py-1 text-xs font-medium sm:text-sm',
                  getStatusBadge(status)
                ]"
              >
                {{ getStatusLabel(status) }}
              </span>
            </div>
          </div>

          <p class="text-sm leading-relaxed text-muted-foreground">
            {{ getAreaAdvice(area, status) }}
          </p>
        </article>
      </section>

      <!-- Recommendations -->
      <section class="mb-6 rounded-2xl bg-gradient-to-br from-[#A8D5BA]/20 to-[#CDE7F0]/20 p-5 sm:mb-8 sm:p-8">
        <h2 class="mb-5 flex items-center gap-2 text-xl font-semibold leading-tight text-[#2C5F2D] sm:mb-6 sm:text-2xl">
          <Lightbulb class="h-5 w-5 shrink-0 text-[#F7B267] sm:h-6 sm:w-6" aria-hidden="true" />
          Personalized Recommendations
        </h2>

        <div class="space-y-3 sm:space-y-4">
          <div
            v-for="(rec, idx) in recommendations"
            :key="idx"
            class="flex items-start gap-3 rounded-xl bg-white p-4 shadow-sm"
          >
            <div
              class="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#A8D5BA] sm:h-8 sm:w-8"
              aria-hidden="true"
            >
              <Check class="h-4 w-4 text-white" />
            </div>

            <p class="flex-1 text-sm leading-relaxed text-[#111827] sm:text-base">
              {{ rec }}
            </p>
          </div>
        </div>
      </section>

      <!-- Action Buttons -->
      <div class="flex flex-col gap-3 sm:flex-row sm:gap-4">
        <button
          @click="handleViewResults"
          class="inline-flex w-full flex-1 items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-6 py-3.5 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:px-8 sm:py-4"
          type="button"
        >
          <ChevronRight class="h-4 w-4" aria-hidden="true" />
          View Personalized Lunchboxes
        </button>

        <button
          @click="router.push('/')"
          class="w-full flex-1 rounded-lg border-2 border-gray-300 bg-white px-6 py-3.5 font-medium text-gray-700 transition-colors hover:bg-gray-50 sm:px-8 sm:py-4"
          type="button"
        >
          Back to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  Sparkles,
  Check,
  ChevronRight,
  Lightbulb,
  Apple,
  Droplet,
  Cookie,
  Carrot,
} from 'lucide-vue-next';
import { useNutritionCheckStore } from '../stores/nutritionCheck';

const router = useRouter();
const route = useRoute();
const nutritionCheckStore = useNutritionCheckStore();

const score = ref(0);
const insights = ref({});
const recommendations = ref([]);

onMounted(() => {
  const result = nutritionCheckStore.result;

  if (!result || !result.nutritionInsights) {
    const childId = route.query.childId || '';

    if (childId) {
      router.push(`/nutrition-check?childId=${childId}`);
    } else {
      router.push('/nutrition-check');
    }

    return;
  }

  score.value = result.score || 0;
  insights.value = result.nutritionInsights || {};
  recommendations.value = generateRecommendations(insights.value);
});

const handleViewResults = () => {
  const childId =
    route.query.childId ||
    localStorage.getItem('littlewell_edit_child_id') ||
    localStorage.getItem('littlewell_active_child_id');

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
  if (score >= 75) return "Great job! Your child's diet is well-balanced.";
  if (score >= 50) return 'Good start! A few improvements can make a big difference.';
  return "Let's work together to improve your child's nutrition.";
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

  recs.push("Involve your child in meal planning - they're more likely to eat what they help choose!");
  recs.push('Make meals colorful and fun with different shapes and arrangements.');

  return recs;
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>