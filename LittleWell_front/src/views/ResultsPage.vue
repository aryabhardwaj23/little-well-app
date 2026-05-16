<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-6xl px-4 sm:px-6">
      <!-- Header -->
      <header class="mb-6 text-center sm:mb-8">
        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          Nutritious Lunchboxes for Children Aged 5–12
        </h1>

        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          Colorful, balanced lunchbox ideas designed for school-aged children
        </p>

        <div v-if="isFamilyMode" class="mt-3">
          <span class="inline-block rounded-full bg-[#CDE7F0]/30 px-3 py-1 text-sm text-[#1B4965]">
            Family plan mode
          </span>
        </div>

        <div v-if="isQuickMode" class="mt-3 text-center">
          <span class="inline-block rounded-full bg-[#F7B267]/20 px-3 py-1 text-sm text-[#8B4513]">
            Quick start mode
          </span>
        </div>
      </header>

      <!-- Seasonal Recommendation Info -->
      <section class="mb-6 rounded-2xl border bg-white p-5 shadow-sm sm:mb-8 sm:p-6">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:gap-4">
          <div
            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#A8D5BA] sm:h-12 sm:w-12"
            aria-hidden="true"
          >
            <Leaf class="h-5 w-5 text-[#2C5F2D] sm:h-6 sm:w-6" />
          </div>

          <div class="min-w-0 flex-1">
            <h3 class="text-lg font-semibold leading-tight text-[#2C5F2D]">
              {{ seasonNames[season] }} seasonal ingredients included
            </h3>

            <p class="mt-2 text-sm leading-relaxed text-muted-foreground">
              These lunchbox suggestions prioritise fresh, in-season vegetables where possible.
              Seasonal vegetables are often fresher, more flavourful, and easier to include in everyday school meals.
            </p>

            <div class="mt-3 flex flex-wrap gap-2">
              <span class="rounded-full bg-[#A8D5BA]/20 px-3 py-1 text-xs text-[#2C5F2D]">
                Fresher choices
              </span>
              <span class="rounded-full bg-[#CDE7F0]/30 px-3 py-1 text-xs text-[#1B4965]">
                Better flavour
              </span>
              <span class="rounded-full bg-[#F7B267]/20 px-3 py-1 text-xs text-[#8B4513]">
                School-friendly nutrition
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Nutrition Support Areas -->
      <section
        v-if="needsSupport.length > 0"
        class="mb-6 rounded-2xl border bg-white p-5 shadow-sm sm:mb-8 sm:p-6"
      >
        <div class="flex items-start gap-3">
          <Sparkles class="mt-1 h-5 w-5 shrink-0 text-[#F7B267]" aria-hidden="true" />

          <div class="min-w-0 flex-1">
            <h4 class="mb-2 font-semibold text-[#2C5F2D]">
              Personalised for Your Child's Needs
            </h4>

            <p class="mb-3 text-sm leading-relaxed text-muted-foreground">
              These meals are tailored to provide extra support for:
            </p>

            <div class="flex flex-wrap gap-2">
              <span
                v-for="area in needsSupport"
                :key="area"
                class="rounded-full bg-[#F7B267]/20 px-3 py-1 text-xs text-[#8B4513]"
              >
                {{ formatNeedLabel(area) }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Loading -->
      <div
        v-if="isLoading"
        class="rounded-2xl bg-white p-6 text-center text-sm text-muted-foreground shadow-sm sm:py-10 sm:text-base"
        aria-live="polite"
        aria-busy="true"
      >
        Loading personalised lunchbox recommendations...
      </div>

      <!-- Empty -->
      <div
        v-else-if="lunchboxes.length === 0"
        class="rounded-2xl bg-white p-6 text-center text-sm text-muted-foreground shadow-sm sm:py-10 sm:text-base"
      >
        No recommendations available yet. Please create a child profile first.
      </div>

      <!-- Main Lunchbox Grid -->
      <section v-else>
        <div class="mb-4 flex items-end justify-between gap-3">
          <h2 class="text-xl font-semibold text-[#2C5F2D] sm:text-2xl">
            Recommended Lunchboxes
          </h2>
          <span class="shrink-0 text-sm text-muted-foreground">
            {{ lunchboxes.length }} options
          </span>
        </div>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
          <article
            v-for="lunchbox in lunchboxes"
            :key="lunchbox.id"
            class="overflow-hidden rounded-2xl bg-white shadow-sm transition-shadow hover:shadow-md"
          >
            <!-- Child Badge -->
            <div v-if="lunchbox.childName" class="px-5 pt-4 sm:px-6">
              <span class="inline-flex items-center rounded-full bg-[#CDE7F0]/30 px-3 py-1 text-sm text-[#1B4965]">
                For {{ lunchbox.childName }}
              </span>
            </div>

            <div class="p-5 sm:p-6">
              <h3 class="mb-2 text-lg font-semibold leading-tight text-[#111827]">
                {{ lunchbox.title || lunchbox.mealName || 'Recommended Lunchbox' }}
              </h3>

              <div v-if="lunchbox.source || lunchbox.category" class="mb-4 flex flex-wrap gap-2">
                <span
                  v-if="lunchbox.source === 'mealdb'"
                  class="rounded-full bg-[#CDE7F0]/30 px-2 py-1 text-xs text-[#1B4965]"
                >
                  Recipe-based
                </span>
                <span
                  v-if="lunchbox.category"
                  class="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600"
                >
                  {{ lunchbox.category }}
                </span>
              </div>

              <!-- Food Items List -->
              <div class="mb-4 space-y-2">
                <div
                  v-for="(item, idx) in lunchbox.items"
                  :key="`${lunchbox.id}-${idx}`"
                  class="flex items-start gap-2"
                >
                  <div
                    :class="[
                      'mt-1.5 h-2 w-2 shrink-0 rounded-full',
                      getSectionColor(item.section)
                    ]"
                  ></div>

                  <div class="min-w-0 flex-1">
                    <p class="text-sm font-medium leading-snug text-[#111827]">
                      {{ item.name }}
                    </p>
                    <p class="text-xs leading-relaxed text-muted-foreground">
                      {{ formatItemAmount(item.amount) }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Nutrition Focus Tags -->
              <div
                v-if="Array.isArray(lunchbox.nutritionFocus) && lunchbox.nutritionFocus.length > 0"
                class="mb-3 flex flex-wrap gap-2"
              >
                <span
                  v-for="focus in lunchbox.nutritionFocus"
                  :key="focus"
                  :class="[
                    'rounded-full px-3 py-1 text-xs',
                    supportColors[lunchbox.supportType] || supportColors.general,
                    supportTextColors[lunchbox.supportType] || supportTextColors.general
                  ]"
                >
                  {{ focus }}
                </span>
              </div>

              <!-- Why This Meal -->
              <p v-if="lunchbox.whyThisMeal" class="text-sm leading-relaxed text-muted-foreground">
                {{ lunchbox.whyThisMeal }}
              </p>
            </div>
          </article>
        </div>
      </section>

      <!-- Recipe Inspiration -->
      <section v-if="showRecipeInspiration" class="mt-10 sm:mt-16">
        <div class="mb-5 flex flex-col gap-3 sm:mb-6 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 class="text-xl font-semibold text-[#2C5F2D] sm:text-2xl">
              Recipe Inspiration
            </h2>
            <p class="mt-1 text-sm leading-relaxed text-muted-foreground">
              {{ isFamilyMode
                ? 'Recipe ideas combined from multiple children in your family plan'
                : 'Extra recipe ideas powered by MealDB and AUSNUT' }}
            </p>
          </div>

          <button
            @click="loadRecipeInspiration"
            class="inline-flex w-full items-center justify-center rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium transition-colors hover:bg-gray-50 sm:w-auto sm:py-2"
            type="button"
          >
            Refresh Recipes
          </button>
        </div>

        <div
          v-if="recipeLoading"
          class="rounded-2xl bg-white p-6 text-center text-sm text-muted-foreground shadow-sm sm:py-8 sm:text-base"
          aria-live="polite"
          aria-busy="true"
        >
          Loading recipe inspiration...
        </div>

        <div v-else-if="recipeMeals.length > 0" class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
          <article
            v-for="meal in recipeMeals"
            :key="meal.id || meal.idMeal || meal.title || meal.mealName"
            class="cursor-pointer overflow-hidden rounded-2xl bg-white shadow-sm transition-shadow hover:shadow-md"
            @click="handleRecipeClick(meal)"
          >
            <div
              v-if="meal.heroImage || meal.mealImage"
              class="aspect-[16/9] overflow-hidden bg-gray-100"
            >
              <img
                :src="meal.heroImage || meal.mealImage"
                :alt="meal.title || meal.mealName || 'Recipe image'"
                class="h-full w-full object-cover"
                @error="handleImageError"
              />
            </div>

            <div class="p-5 sm:p-6">
              <h3 class="mb-2 text-lg font-semibold leading-tight text-[#111827]">
                {{ meal.title || meal.mealName || 'Recipe Inspiration' }}
              </h3>

              <div v-if="meal.category || meal.area || meal.childName" class="mb-3 flex flex-wrap gap-2">
                <span
                  v-if="meal.category"
                  class="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600"
                >
                  {{ meal.category }}
                </span>
                <span
                  v-if="meal.area"
                  class="rounded-full bg-[#CDE7F0]/30 px-2 py-1 text-xs text-[#1B4965]"
                >
                  {{ meal.area }}
                </span>
                <span
                  v-if="meal.childName && !isFamilyMode"
                  class="rounded-full bg-[#A8D5BA]/20 px-2 py-1 text-xs text-[#2C5F2D]"
                >
                  For {{ meal.childName }}
                </span>
              </div>

              <div
                v-if="Array.isArray(meal.nutritionFocus) && meal.nutritionFocus.length > 0"
                class="mb-3 flex flex-wrap gap-2"
              >
                <span
                  v-for="focus in meal.nutritionFocus"
                  :key="focus"
                  class="rounded-full bg-[#A8D5BA]/20 px-3 py-1 text-xs text-[#2C5F2D]"
                >
                  {{ focus }}
                </span>
              </div>

              <p v-if="meal.whyThisMeal" class="text-sm leading-relaxed text-muted-foreground">
                {{ meal.whyThisMeal }}
              </p>
            </div>
          </article>
        </div>

        <div
          v-else
          class="rounded-2xl bg-white p-6 text-center text-sm text-muted-foreground shadow-sm sm:py-8 sm:text-base"
        >
          No recipe inspiration available right now.
        </div>
      </section>

      <!-- Action Buttons -->
      <div class="mt-10 flex flex-col gap-3 sm:mt-12 sm:flex-row sm:justify-center sm:gap-4">
        <button
          @click="router.push('/')"
          class="inline-flex w-full items-center justify-center rounded-lg border-2 border-[#A8D5BA] bg-white px-8 py-3 font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10 sm:w-auto"
          type="button"
        >
          Back to Home
        </button>

        <button
          @click="loadEverything"
          class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto"
          type="button"
        >
          <RefreshCw class="h-4 w-4" aria-hidden="true" />
          Generate New Meals
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { RefreshCw, Sparkles, Leaf } from 'lucide-vue-next';
import {
  getRecommendedProducts,
  getFamilyRecommendedProducts,
  getQuickRecommendedProducts,
  getChildMealRecommendations,
} from '../services/api';

const router = useRouter();
const route = useRoute();

const isQuickMode = ref(false);
const isFamilyMode = ref(false);

// Seasonal recommendations are always enabled.
// The UI no longer shows a toggle, but API requests still send seasonal: true.
const seasonalMode = ref(true);

const lunchboxes = ref([]);
const recipeMeals = ref([]);

const isLoading = ref(false);
const recipeLoading = ref(false);

const selectedChildId = ref(null);
const selectedChildIds = ref([]);
const needsSupport = ref([]);

const allowedAgeGroups = ['5-6 years', '7-9 years', '10-12 years'];

const normalizeAgeGroup = (ageGroup) => {
  const mapping = {
    '5-6 years': '5-6 years',
    '7-9 years': '7-9 years',
    '10-12 years': '10-12 years',

    // Old values compatibility
    '0-3 years': '',
    '3-6 years': '5-6 years',
    '6-9 years': '7-9 years',
    '9-12 years': '10-12 years',
    '12+ years': '10-12 years',
    '2-3': '',
    '4-8': '7-9 years',
    '9-13': '10-12 years',
    '14-18': '',
  };

  return mapping[ageGroup] || '';
};

const showRecipeInspiration = computed(() => {
  return !isQuickMode.value && (
    !!selectedChildId.value || selectedChildIds.value.length > 0
  );
});

const loadRecommendations = async () => {
  const childId =
    route.query.childId || localStorage.getItem('littlewell_active_child_id');
  const childIdsParam = route.query.childIds;
  const family = route.query.family;

  const quick = route.query.quick;
  const quickAgeGroup = normalizeAgeGroup(route.query.ageGroup);
  const allergiesParam = route.query.allergies;

  try {
    isLoading.value = true;
    lunchboxes.value = [];
    needsSupport.value = [];

    isQuickMode.value = false;
    isFamilyMode.value = false;
    selectedChildId.value = null;
    selectedChildIds.value = [];

    // Quick mode
    if (quick && quickAgeGroup) {
      isQuickMode.value = true;

      if (!allowedAgeGroups.includes(quickAgeGroup)) {
        lunchboxes.value = [];
        needsSupport.value = [];
        return;
      }

      const allergies = allergiesParam
        ? String(allergiesParam)
            .split(',')
            .map((a) => a.trim())
            .filter(Boolean)
        : [];

      const data = await getQuickRecommendedProducts({
        ageGroup: quickAgeGroup,
        allergies,
        seasonal: seasonalMode.value,
      });

      lunchboxes.value = Array.isArray(data) ? data : data.lunchboxes || [];
      needsSupport.value = Array.isArray(data?.needsSupport)
        ? data.needsSupport
        : [];
      return;
    }

    // Family mode
    if (family && childIdsParam) {
      isFamilyMode.value = true;

      selectedChildIds.value = String(childIdsParam)
        .split(',')
        .map((id) => id.trim())
        .filter(Boolean);

      const data = await getFamilyRecommendedProducts(
        selectedChildIds.value,
        seasonalMode.value
      );

      lunchboxes.value = Array.isArray(data) ? data : data.lunchboxes || [];
      needsSupport.value = Array.isArray(data?.needsSupport)
        ? data.needsSupport
        : [];
      return;
    }

    // Single child mode
    if (childId) {
      selectedChildId.value = String(childId);

      const data = await getRecommendedProducts(childId, seasonalMode.value);

      lunchboxes.value = Array.isArray(data) ? data : data.lunchboxes || [];
      needsSupport.value = Array.isArray(data?.needsSupport)
        ? data.needsSupport
        : [];
      return;
    }

    lunchboxes.value = [];
    needsSupport.value = [];
  } catch (error) {
    console.error('Failed to load recommendations:', error);
    lunchboxes.value = [];
    needsSupport.value = [];
  } finally {
    isLoading.value = false;
  }
};

const dedupeMeals = (meals) => {
  const uniqueMap = new Map();

  for (const meal of meals) {
    const key =
      meal?.id ||
      meal?.idMeal ||
      meal?.title ||
      meal?.mealName;

    if (!key) continue;

    if (!uniqueMap.has(key)) {
      uniqueMap.set(key, meal);
    }
  }

  return Array.from(uniqueMap.values());
};

const loadRecipeInspiration = async () => {
  if (isQuickMode.value) {
    recipeMeals.value = [];
    return;
  }

  try {
    recipeLoading.value = true;

    // Single child mode
    if (!isFamilyMode.value && selectedChildId.value) {
      const data = await getChildMealRecommendations(selectedChildId.value);
      recipeMeals.value = Array.isArray(data?.lunchboxes) ? data.lunchboxes : [];
      return;
    }

    // Family mode: fetch recipes for each child, then merge + dedupe
    if (isFamilyMode.value && selectedChildIds.value.length > 0) {
      const results = await Promise.all(
        selectedChildIds.value.map((id) => getChildMealRecommendations(id))
      );

      const mergedMeals = results.flatMap((res) =>
        Array.isArray(res?.lunchboxes) ? res.lunchboxes : []
      );

      recipeMeals.value = dedupeMeals(mergedMeals);
      return;
    }

    recipeMeals.value = [];
  } catch (error) {
    console.error('Failed to load recipe inspiration:', error);
    recipeMeals.value = [];
  } finally {
    recipeLoading.value = false;
  }
};

const loadEverything = async () => {
  await loadRecommendations();
  await loadRecipeInspiration();
};

onMounted(() => {
  loadEverything();
});

watch(seasonalMode, () => {
  loadEverything();
});

watch(
  () => [
    route.query.childId,
    route.query.childIds,
    route.query.family,
    route.query.quick,
    route.query.ageGroup,
    route.query.allergies,
  ],
  () => {
    loadEverything();
  }
);

const supportColors = {
  iron: 'bg-[#F7B267]',
  calcium: 'bg-[#CDE7F0]',
  vitamin_d: 'bg-[#A8D5BA]',
  variety: 'bg-green-200',
  general: 'bg-purple-400',
};

const supportTextColors = {
  iron: 'text-white',
  calcium: 'text-[#1B4965]',
  vitamin_d: 'text-[#2C5F2D]',
  variety: 'text-green-800',
  general: 'text-white',
};

const getCurrentSeason = () => {
  const month = new Date().getMonth(); // 0-11
  if (month >= 8 && month <= 10) return 'spring'; // Sep-Nov
  if (month === 11 || month === 0 || month === 1) return 'summer'; // Dec-Feb
  if (month >= 2 && month <= 4) return 'autumn'; // Mar-May
  return 'winter'; // Jun-Aug
};

const season = ref(getCurrentSeason());

const seasonNames = {
  spring: 'Spring',
  summer: 'Summer',
  autumn: 'Autumn',
  winter: 'Winter',
};

const getSectionColor = (section) => {
  const colors = {
    carbs: 'bg-[#F7B267]',
    protein: 'bg-[#A8D5BA]',
    veggies: 'bg-[#8BC34A]',
    fruit: 'bg-[#FF6B9D]',
    ingredient: 'bg-[#CDE7F0]',
  };
  return colors[section] || 'bg-gray-300';
};

const formatNeedLabel = (area) => {
  const labels = {
    iron: 'Iron Support',
    calcium: 'Calcium Support',
    vitamin_d: 'Vitamin D Support',
    variety: 'Variety Support',
  };
  return labels[area] || area;
};

const formatItemAmount = (amount) => {
  if (!amount) return '';

  if (isFamilyMode.value && selectedChildIds.value.length > 1) {
    const childCount = selectedChildIds.value.length;

    if (String(amount).toLowerCase().includes('child-friendly portion')) {
      return `Portions for ${childCount} children`;
    }
  }

  return amount;
};

const handleImageError = (event) => {
  event.target.style.display = 'none';
};

const handleRecipeClick = (meal) => {
  const recipeBaseChildId =
    selectedChildId.value ||
    (selectedChildIds.value.length > 0 ? selectedChildIds.value[0] : '');

  router.push({
    path: `/recipe/${encodeURIComponent(meal.id || meal.idMeal)}`,
    query: {
      childId: recipeBaseChildId,
      source: 'mealdb',
      childName: meal.childName || '',
      from: 'results',
      family: isFamilyMode.value ? '1' : '',
    },
  });
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>