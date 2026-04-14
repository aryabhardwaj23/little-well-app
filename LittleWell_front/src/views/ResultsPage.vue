<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-6xl">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl mb-4">Nutritious Lunchboxes for Your Family</h1>
        <p class="text-lg text-muted-foreground">
          Colorful, balanced meals designed to delight and nourish your little ones
        </p>

        <div v-if="isFamilyMode" class="mt-3">
          <span class="inline-block px-3 py-1 rounded-full text-sm bg-[#CDE7F0]/30 text-[#1B4965]">
            Family plan mode
          </span>
        </div>

        <div v-if="isQuickMode" class="mt-3 text-center">
          <span class="inline-block px-3 py-1 rounded-full text-sm bg-[#F7B267]/20 text-[#8B4513]">
            Quick start mode
          </span>
        </div>
      </div>

      <!-- Seasonal Toggle -->
      <div class="p-6 rounded-2xl shadow-sm mb-8 bg-white border">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-[#A8D5BA] rounded-full flex items-center justify-center flex-shrink-0">
              <Leaf class="w-6 h-6 text-[#2C5F2D]" />
            </div>
            <div>
              <h3 class="text-lg font-medium">{{ seasonNames[season] }} Seasonal Mode</h3>
              <p class="text-sm text-muted-foreground">
                Prioritize fresh, in-season ingredients for maximum nutrition
              </p>
            </div>
          </div>

          <label class="flex items-center gap-2 cursor-pointer">
            <input
              v-model="seasonalMode"
              type="checkbox"
              class="w-11 h-6 bg-gray-200 rounded-full appearance-none cursor-pointer relative
                     checked:bg-[#A8D5BA] transition-colors
                     after:content-[''] after:absolute after:top-0.5 after:left-0.5
                     after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-transform
                     checked:after:translate-x-5"
            />
          </label>
        </div>
      </div>

      <!-- Nutrition Support Areas -->
      <div v-if="needsSupport.length > 0" class="mb-8 p-6 bg-white border rounded-2xl shadow-sm">
        <div class="flex items-start gap-3">
          <Sparkles class="w-5 h-5 text-[#F7B267] mt-1" />
          <div>
            <h4 class="font-medium mb-2">Personalised for Your Child's Needs</h4>
            <p class="text-sm text-muted-foreground mb-3">
              These meals are tailored to provide extra support for:
            </p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="area in needsSupport"
                :key="area"
                class="text-xs bg-[#F7B267]/20 text-[#8B4513] px-3 py-1 rounded-full"
              >
                {{ formatNeedLabel(area) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-10 text-muted-foreground">
        Loading personalised lunchbox recommendations...
      </div>

      <!-- Empty -->
      <div v-else-if="lunchboxes.length === 0" class="text-center py-10 text-muted-foreground">
        No recommendations available yet. Please create a child profile first.
      </div>

      <!-- Main Lunchbox Grid -->
      <div v-else>
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-medium">Recommended Lunchboxes</h2>
          <span class="text-sm text-muted-foreground">
            {{ lunchboxes.length }} options
          </span>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="lunchbox in lunchboxes"
            :key="lunchbox.id"
            class="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
            @click="handleLunchboxClick(lunchbox)"
          >
            <!-- Hero Image -->
            <div
              v-if="lunchbox.heroImage"
              class="aspect-[16/9] bg-gray-100 overflow-hidden"
            >
              <img
                :src="lunchbox.heroImage"
                :alt="lunchbox.title || lunchbox.mealName || 'Lunchbox image'"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
            </div>

            <!-- Child Badge -->
            <div v-if="lunchbox.childName" class="px-6 pt-4">
              <span class="inline-flex items-center px-3 py-1 bg-[#CDE7F0]/30 text-[#1B4965] text-sm rounded-full">
                For {{ lunchbox.childName }}
              </span>
            </div>

            <div class="p-6">
              <h3 class="text-lg font-medium mb-2">
                {{ lunchbox.title || lunchbox.mealName || 'Recommended Lunchbox' }}
              </h3>

              <div v-if="lunchbox.source || lunchbox.category" class="flex flex-wrap gap-2 mb-4">
                <span
                  v-if="lunchbox.source === 'mealdb'"
                  class="text-xs bg-[#CDE7F0]/30 text-[#1B4965] px-2 py-1 rounded-full"
                >
                  Recipe-based
                </span>
                <span
                  v-if="lunchbox.category"
                  class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full"
                >
                  {{ lunchbox.category }}
                </span>
              </div>

              <!-- Items Grid -->
              <div class="grid grid-cols-2 gap-3 mb-4">
                <div
                  v-for="(item, idx) in lunchbox.items"
                  :key="idx"
                  class="relative"
                >
                  <div
                    v-if="item.image"
                    class="aspect-square rounded-lg overflow-hidden bg-gray-100"
                  >
                    <img
                      :src="item.image"
                      :alt="item.name"
                      class="w-full h-full object-cover"
                      @error="handleImageError"
                    />
                  </div>

                  <div
                    v-else
                    class="aspect-square rounded-lg border border-dashed border-gray-200 bg-[#FAF9F6] flex items-center justify-center text-xs text-muted-foreground text-center p-2"
                  >
                    {{ formatSectionLabel(item.section) }}
                  </div>

                  <div
                    :class="[
                      'absolute top-2 left-2 w-3 h-3 rounded-full',
                      getSectionColor(item.section)
                    ]"
                  ></div>
                </div>
              </div>

              <!-- Food Items List -->
              <div class="space-y-2 mb-4">
                <div
                  v-for="(item, idx) in lunchbox.items"
                  :key="`${lunchbox.id}-${idx}`"
                  class="flex items-start gap-2"
                >
                  <div
                    :class="[
                      'w-2 h-2 rounded-full mt-1.5',
                      getSectionColor(item.section)
                    ]"
                  ></div>
                  <div class="flex-1">
                    <p class="text-sm font-medium">{{ item.name }}</p>
                    <p class="text-xs text-muted-foreground">{{ item.amount }}</p>
                  </div>
                </div>
              </div>

              <!-- Nutrition Focus Tags -->
              <div
                v-if="Array.isArray(lunchbox.nutritionFocus) && lunchbox.nutritionFocus.length > 0"
                class="flex flex-wrap gap-2 mb-3"
              >
                <span
                  v-for="focus in lunchbox.nutritionFocus"
                  :key="focus"
                  :class="[
                    'text-xs px-3 py-1 rounded-full',
                    supportColors[lunchbox.supportType] || supportColors.general,
                    supportTextColors[lunchbox.supportType] || supportTextColors.general
                  ]"
                >
                  {{ focus }}
                </span>
              </div>

              <!-- Why This Meal -->
              <p v-if="lunchbox.whyThisMeal" class="text-sm text-muted-foreground leading-relaxed">
                {{ lunchbox.whyThisMeal }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recipe Inspiration -->
      <div v-if="showRecipeInspiration" class="mt-16">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-2xl font-medium">Recipe Inspiration</h2>
            <p class="text-sm text-muted-foreground">
              Extra recipe ideas powered by MealDB and AUSNUT
            </p>
          </div>
          <button
            @click="loadRecipeInspiration"
            class="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm"
          >
            Refresh Recipes
          </button>
        </div>

        <div v-if="recipeLoading" class="text-center py-8 text-muted-foreground">
          Loading recipe inspiration...
        </div>

        <div v-else-if="recipeMeals.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="meal in recipeMeals"
            :key="meal.id"
            class="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
            @click="handleLunchboxClick(meal)"
          >
            <div
              v-if="meal.heroImage || meal.mealImage"
              class="aspect-[16/9] bg-gray-100 overflow-hidden"
            >
              <img
                :src="meal.heroImage || meal.mealImage"
                :alt="meal.title || meal.mealName || 'Recipe image'"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
            </div>

            <div class="p-6">
              <h3 class="text-lg font-medium mb-2">
                {{ meal.title || meal.mealName || 'Recipe Inspiration' }}
              </h3>

              <div v-if="meal.category || meal.area" class="flex flex-wrap gap-2 mb-3">
                <span
                  v-if="meal.category"
                  class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full"
                >
                  {{ meal.category }}
                </span>
                <span
                  v-if="meal.area"
                  class="text-xs bg-[#CDE7F0]/30 text-[#1B4965] px-2 py-1 rounded-full"
                >
                  {{ meal.area }}
                </span>
              </div>

              <div
                v-if="Array.isArray(meal.nutritionFocus) && meal.nutritionFocus.length > 0"
                class="flex flex-wrap gap-2 mb-3"
              >
                <span
                  v-for="focus in meal.nutritionFocus"
                  :key="focus"
                  class="text-xs px-3 py-1 rounded-full bg-[#A8D5BA]/20 text-[#2C5F2D]"
                >
                  {{ focus }}
                </span>
              </div>

              <p v-if="meal.whyThisMeal" class="text-sm text-muted-foreground leading-relaxed">
                {{ meal.whyThisMeal }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="mt-12 flex gap-4 justify-center">
        <button
          @click="router.push('/')"
          class="px-8 py-3 bg-white border-2 border-[#A8D5BA] text-[#2C5F2D] rounded-lg hover:bg-[#A8D5BA]/10 transition-colors"
        >
          Back to Home
        </button>

        <button
          @click="loadEverything"
          class="px-8 py-3 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg transition-colors inline-flex items-center gap-2"
        >
          <RefreshCw class="w-4 h-4" />
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
const seasonalMode = ref(true);

const lunchboxes = ref([]);
const recipeMeals = ref([]);

const isLoading = ref(false);
const recipeLoading = ref(false);

const selectedChildId = ref(null);
const selectedChildIds = ref([]);
const needsSupport = ref([]);

const showRecipeInspiration = computed(() => {
  return !isQuickMode.value && !isFamilyMode.value && !!selectedChildId.value;
});

const loadRecommendations = async () => {
  const childId =
    route.query.childId || localStorage.getItem('littlewell_active_child_id');
  const childIdsParam = route.query.childIds;
  const family = route.query.family;

  const quick = route.query.quick;
  const quickAgeGroup = route.query.ageGroup;
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
      selectedChildId.value = childId;

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

const loadRecipeInspiration = async () => {
  if (!selectedChildId.value || isQuickMode.value || isFamilyMode.value) {
    recipeMeals.value = [];
    return;
  }

  try {
    recipeLoading.value = true;
    const data = await getChildMealRecommendations(selectedChildId.value);
    recipeMeals.value = Array.isArray(data?.lunchboxes) ? data.lunchboxes : [];
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
  const month = new Date().getMonth();
  if (month >= 2 && month <= 4) return 'spring';
  if (month >= 5 && month <= 7) return 'summer';
  if (month >= 8 && month <= 10) return 'autumn';
  return 'winter';
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

const formatSectionLabel = (section) => {
  const labels = {
    carbs: 'Carbs',
    protein: 'Protein',
    veggies: 'Veggies',
    fruit: 'Fruit',
    ingredient: 'Ingredient',
  };
  return labels[section] || 'Item';
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

const handleImageError = (event) => {
  event.target.style.display = 'none';
};

const handleLunchboxClick = (lunchbox) => {
  router.push({
    path: `/recipe/${lunchbox.id}`,
    query: {
      childId: selectedChildId.value || '',
      source: lunchbox.source || '',
      childName: lunchbox.childName || '',
    },
    state: {
      lunchbox,
    },
  });
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>