<template>
  <div class="min-h-screen bg-[#FAF9F6]">
    <!-- Navigation -->
    <nav class="sticky top-0 z-10 border-b border-gray-200 bg-white/95 backdrop-blur">
      <div class="container mx-auto max-w-6xl px-4 sm:px-6">
        <div class="flex h-14 items-center justify-between sm:h-16">
          <button
            @click="goBack"
            class="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-gray-100 sm:px-4"
            type="button"
            aria-label="Back to Lunchboxes"
          >
            <ArrowLeft class="h-4 w-4" aria-hidden="true" />
            Back to Lunchboxes
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero Image Section -->
    <section class="relative h-[240px] overflow-hidden sm:h-[320px] md:h-[400px]" aria-label="Recipe image">
      <div v-if="recipe?.heroImage" class="absolute inset-0">
        <img
          :src="recipe.heroImage"
          :alt="recipe.name || 'Recipe image'"
          class="h-full w-full object-cover"
          @error="handleHeroImageError"
        />
        <div class="absolute inset-0 bg-black/20"></div>
      </div>

      <div
        v-else
        class="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4]"
      >
        <UtensilsCrossed class="h-20 w-20 text-white/30 sm:h-28 sm:w-28 md:h-32 md:w-32" aria-hidden="true" />
      </div>
    </section>

    <!-- Content -->
    <main class="py-6 sm:py-10 md:py-12">
      <div class="container mx-auto max-w-4xl px-4 sm:px-6">
        <div
          v-if="loading"
          class="py-16 text-center text-sm text-muted-foreground sm:py-20 sm:text-base"
          aria-live="polite"
          aria-busy="true"
        >
          Loading recipe...
        </div>

        <div v-else-if="error" class="py-16 text-center sm:py-20">
          <p class="mb-4 text-sm text-red-500 sm:text-base">{{ error }}</p>
          <button
            @click="retryLoad"
            class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm transition-colors hover:bg-gray-50"
            type="button"
          >
            Try Again
          </button>
        </div>

        <template v-else-if="recipe">
          <!-- Recipe Header -->
          <section class="relative z-10 mb-6 -mt-20 rounded-2xl bg-white p-5 shadow-sm sm:mb-8 sm:-mt-28 sm:p-8 md:-mt-32">
            <div class="mb-5 sm:mb-6">
              <div v-if="recipe.childName" class="mb-3">
                <span class="inline-flex items-center rounded-full bg-[#CDE7F0]/30 px-3 py-1 text-sm text-[#1B4965]">
                  For {{ recipe.childName }}
                </span>
              </div>

              <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
                {{ recipe.name }}
              </h1>
              <p class="text-sm leading-relaxed text-muted-foreground sm:text-lg">
                {{ recipe.description }}
              </p>
            </div>

            <!-- Tags -->
            <div v-if="recipe.tags.length > 0" class="mb-5 flex flex-wrap gap-2 sm:mb-6">
              <span
                v-for="tag in recipe.tags"
                :key="tag"
                class="rounded-full bg-[#A8D5BA]/20 px-3 py-1 text-sm text-[#2C5F2D]"
              >
                {{ tag }}
              </span>
            </div>

            <!-- Prep Info -->
            <div class="grid grid-cols-3 gap-2 border-y py-5 sm:gap-6 sm:py-6">
              <div class="text-center">
                <Clock class="mx-auto mb-2 h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" aria-hidden="true" />
                <p class="mb-1 text-xs text-muted-foreground sm:text-sm">Prep Time</p>
                <p class="text-sm font-semibold text-[#111827] sm:text-base">{{ recipe.prepTime }}</p>
              </div>

              <div class="text-center">
                <Users class="mx-auto mb-2 h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" aria-hidden="true" />
                <p class="mb-1 text-xs text-muted-foreground sm:text-sm">Servings</p>
                <p class="text-sm font-semibold text-[#111827] sm:text-base">{{ recipe.servings }}</p>
              </div>

              <div class="text-center">
                <Gauge class="mx-auto mb-2 h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" aria-hidden="true" />
                <p class="mb-1 text-xs text-muted-foreground sm:text-sm">
                  {{ recipe.difficultyLabel }}
                </p>
                <p class="text-sm font-semibold text-[#111827] sm:text-base">{{ recipe.difficulty }}</p>
              </div>
            </div>
          </section>

          <!-- Nutrition Benefits -->
          <section class="mb-6 rounded-2xl bg-gradient-to-br from-[#A8D5BA]/10 to-[#CDE7F0]/10 p-5 sm:mb-8 sm:p-8">
            <h2 class="mb-4 flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:text-2xl">
              <Sparkles class="h-5 w-5 text-[#F7B267] sm:h-6 sm:w-6" aria-hidden="true" />
              Why This Meal?
            </h2>
            <p class="mb-4 text-sm leading-relaxed text-muted-foreground sm:text-base">
              {{ recipe.whyThisMeal }}
            </p>
            <div v-if="recipe.colorInsight" class="rounded-xl bg-white p-4">
              <p class="text-sm leading-relaxed text-[#111827]">
                {{ recipe.colorInsight }}
              </p>
            </div>
          </section>

          <!-- Ingredients -->
          <section class="mb-6 rounded-2xl bg-white p-5 shadow-sm sm:mb-8 sm:p-8">
            <h2 class="mb-5 flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:mb-6 sm:text-2xl">
              <ShoppingCart class="h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" aria-hidden="true" />
              Ingredients
            </h2>

            <div v-if="normalizedIngredients.length > 0" class="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div
                v-for="section in normalizedIngredients"
                :key="section.section"
                class="space-y-3"
              >
                <h3 :class="['border-b-2 pb-2 text-base font-semibold text-[#111827] sm:text-lg', getSectionBorderColor(section.section)]">
                  {{ getSectionTitle(section.section) }}
                </h3>

                <ul class="space-y-3">
                  <li
                    v-for="(item, idx) in section.items"
                    :key="idx"
                    class="flex items-start gap-3"
                  >
                    <div
                      v-if="item.image"
                      class="h-12 w-12 shrink-0 overflow-hidden rounded-lg bg-gray-100 sm:h-14 sm:w-14"
                    >
                      <img
                        :src="item.image"
                        :alt="item.name"
                        class="h-full w-full object-cover"
                        @error="handleItemImageError"
                      />
                    </div>

                    <div
                      v-else
                      :class="[
                        'flex h-12 w-12 shrink-0 items-center justify-center rounded-lg border border-dashed p-1 text-center text-[10px] sm:h-14 sm:w-14',
                        getSectionPlaceholderStyle(section.section)
                      ]"
                    >
                      {{ formatSectionLabel(section.section) }}
                    </div>

                    <div class="flex flex-1 items-start gap-2">
                      <div :class="['mt-2 h-2 w-2 shrink-0 rounded-full', getSectionDotColor(section.section)]"></div>
                      <div class="min-w-0">
                        <p class="font-medium leading-snug text-muted-foreground">{{ item.name }}</p>
                        <p v-if="item.amount" class="mt-0.5 text-sm text-muted-foreground/80">
                          {{ item.amount }}
                        </p>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>

            <div v-else class="text-sm text-muted-foreground sm:text-base">
              No ingredient details available for this recipe.
            </div>
          </section>

          <!-- Instructions -->
          <section class="mb-6 rounded-2xl bg-white p-5 shadow-sm sm:mb-8 sm:p-8">
            <h2 class="mb-5 flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:mb-6 sm:text-2xl">
              <ChefHat class="h-5 w-5 text-[#F7B267] sm:h-6 sm:w-6" aria-hidden="true" />
              Instructions
            </h2>

            <div v-if="recipe.instructions.length > 0" class="space-y-4">
              <div
                v-for="(step, idx) in recipe.instructions"
                :key="idx"
                class="flex gap-3 sm:gap-4"
              >
                <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#A8D5BA] text-sm font-semibold text-white sm:h-10 sm:w-10 sm:text-base">
                  {{ idx + 1 }}
                </div>
                <p class="flex-1 pt-1 text-sm leading-relaxed text-muted-foreground sm:pt-2 sm:text-base">
                  {{ step }}
                </p>
              </div>
            </div>

            <div v-else class="text-sm leading-relaxed text-muted-foreground sm:text-base">
              <p>
                This lunchbox is ready to use as a practical meal suggestion. You can mix and match the recommended items to suit your child’s preferences.
              </p>
            </div>
          </section>

          <!-- Tips -->
          <section class="mb-6 rounded-2xl bg-[#CDE7F0]/20 p-5 sm:mb-8 sm:p-8">
            <h2 class="mb-4 flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:text-2xl">
              <Lightbulb class="h-5 w-5 text-[#F7B267] sm:h-6 sm:w-6" aria-hidden="true" />
              Parent Tips
            </h2>
            <ul class="space-y-3">
              <li
                v-for="(tip, idx) in recipe.tips"
                :key="idx"
                class="flex items-start gap-3"
              >
                <Check class="mt-0.5 h-5 w-5 shrink-0 text-[#A8D5BA]" aria-hidden="true" />
                <span class="text-sm leading-relaxed text-muted-foreground sm:text-base">{{ tip }}</span>
              </li>
            </ul>
          </section>

          <!-- Nutrition Focus -->
          <section class="rounded-2xl bg-white p-5 shadow-sm sm:p-8">
            <h2 class="mb-4 text-xl font-semibold text-[#2C5F2D] sm:text-2xl">
              Nutrition Focus
            </h2>
            <div v-if="recipe.nutritionFocus.length > 0" class="flex flex-wrap gap-2 sm:gap-3">
              <span
                v-for="focus in recipe.nutritionFocus"
                :key="focus"
                class="rounded-full bg-[#A8D5BA]/20 px-3 py-1.5 text-sm text-[#2C5F2D] sm:px-4 sm:py-2"
              >
                {{ focus }}
              </span>
            </div>
            <div v-else class="text-sm text-muted-foreground sm:text-base">
              No nutrition tags available for this recipe.
            </div>
          </section>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  ArrowLeft,
  Clock,
  Users,
  Sparkles,
  ShoppingCart,
  Check,
  Lightbulb,
  UtensilsCrossed,
  ChefHat,
  Gauge,
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const recipe = ref(null);
const loading = ref(true);
const error = ref('');

const normalizeInstructions = (instructions) => {
  if (Array.isArray(instructions)) return instructions.filter(Boolean);

  if (typeof instructions === 'string' && instructions.trim()) {
    return instructions
      .split(/\r?\n+/)
      .map((line) => line.trim())
      .filter(Boolean);
  }

  return [];
};

const normalizeIngredients = (raw) => {
  if (!Array.isArray(raw)) return [];

  if (raw.length > 0 && raw[0]?.section && Array.isArray(raw[0]?.items)) {
    return raw.map((section) => ({
      section: section.section,
      items: section.items.map((item) => {
        if (typeof item === 'string') {
          return {
            name: item,
            amount: '',
            image: null,
          };
        }

        return {
          name: item.name || '',
          amount: item.amount || '',
          image: item.image || null,
        };
      }),
    }));
  }

  const grouped = {};

  raw.forEach((item) => {
    const section = item.section || 'other';

    if (!grouped[section]) {
      grouped[section] = [];
    }

    grouped[section].push({
      name: item.name || '',
      amount: item.amount || '',
      image: item.image || null,
    });
  });

  return Object.entries(grouped).map(([section, items]) => ({
    section,
    items,
  }));
};

const normalizedIngredients = computed(() => {
  return normalizeIngredients(recipe.value?.ingredients || []);
});

const mapRouteStateToRecipe = (raw) => {
  if (!raw) return null;

  const title =
    raw.title ||
    raw.mealName ||
    raw.name ||
    raw.strMeal ||
    'Lunchbox Recommendation';

  const heroImage =
    raw.heroImage ||
    raw.mealImage ||
    raw.image ||
    raw.strMealThumb ||
    null;

  return {
    name: title,

    description:
      raw.description ||
      (raw.source === 'mealdb'
        ? 'A recipe-inspired lunchbox idea with practical ingredients.'
        : 'A practical lunchbox recommendation based on your child’s needs.'),

    prepTime:
      raw.prepTime ||
      raw.prep_time ||
      (raw.source === 'mealdb' ? '25 mins' : '15 mins'),

    servings:
      raw.servings ||
      raw.serving ||
      '1 child',

    difficulty:
      raw.difficulty ||
      (raw.source === 'mealdb' ? 'Recipe' : 'Easy'),

    difficultyLabel:
      raw.difficultyLabel ||
      (raw.source === 'mealdb' ? 'Type' : 'Difficulty'),

    heroImage,

    childName:
      raw.childName ||
      route.query.childName ||
      null,

    tags: Array.isArray(raw.tags)
      ? raw.tags
      : raw.category
        ? [raw.category]
        : raw.strCategory
          ? [raw.strCategory]
          : [],

    whyThisMeal:
      raw.whyThisMeal ||
      raw.why_this_meal ||
      'This option was selected to provide a balanced and practical lunchbox suggestion.',

    colorInsight:
      raw.colorInsight ||
      raw.color_insight ||
      '',

    ingredients:
      raw.ingredients ||
      raw.items ||
      [],

    instructions:
      normalizeInstructions(raw.instructions || raw.strInstructions),

    tips:
      Array.isArray(raw.tips) && raw.tips.length > 0
        ? raw.tips
        : [
            'Pack items separately if your child prefers different textures.',
            'Combine familiar foods with one new item for better acceptance.',
            'Use colorful fruit and vegetables to make lunchboxes more appealing.',
          ],

    nutritionFocus:
      Array.isArray(raw.nutritionFocus)
        ? raw.nutritionFocus
        : Array.isArray(raw.nutrition_focus)
          ? raw.nutrition_focus
          : [],
  };
};

const getSectionTitle = (section) => {
  const titles = {
    carbs: 'Carbohydrates',
    protein: 'Protein',
    veggies: 'Vegetables',
    fruit: 'Fruit',
    ingredient: 'Ingredients',
    other: 'Other Items',
  };

  return titles[section] || section;
};

const getSectionBorderColor = (section) => {
  const colors = {
    carbs: 'border-[#F7B267]',
    protein: 'border-[#A8D5BA]',
    veggies: 'border-[#8BC34A]',
    fruit: 'border-[#FF6B9D]',
    ingredient: 'border-[#CDE7F0]',
    other: 'border-gray-300',
  };

  return colors[section] || 'border-gray-300';
};

const getSectionDotColor = (section) => {
  const colors = {
    carbs: 'bg-[#F7B267]',
    protein: 'bg-[#A8D5BA]',
    veggies: 'bg-[#8BC34A]',
    fruit: 'bg-[#FF6B9D]',
    ingredient: 'bg-[#CDE7F0]',
    other: 'bg-gray-300',
  };

  return colors[section] || 'bg-gray-300';
};

const getSectionPlaceholderStyle = (section) => {
  const styles = {
    carbs: 'border-[#F7B267]/40 text-[#8B4513] bg-[#F7B267]/10',
    protein: 'border-[#A8D5BA]/40 text-[#2C5F2D] bg-[#A8D5BA]/10',
    veggies: 'border-[#8BC34A]/40 text-green-700 bg-green-50',
    fruit: 'border-[#FF6B9D]/40 text-pink-700 bg-pink-50',
    ingredient: 'border-[#CDE7F0]/40 text-[#1B4965] bg-[#CDE7F0]/20',
    other: 'border-gray-200 text-gray-500 bg-gray-50',
  };

  return styles[section] || styles.other;
};

const formatSectionLabel = (section) => {
  const labels = {
    carbs: 'Carbs',
    protein: 'Protein',
    veggies: 'Veggies',
    fruit: 'Fruit',
    ingredient: 'Ingredient',
    other: 'Item',
  };

  return labels[section] || 'Item';
};

const handleHeroImageError = (event) => {
  event.target.style.display = 'none';
};

const handleItemImageError = (event) => {
  event.target.style.display = 'none';
};

const fetchRecipeFromApi = async () => {
  const recipeId = route.params.id;
  const childName = route.query.childName || '';

  if (!recipeId) {
    throw new Error('Missing recipe ID');
  }

  const response = await fetch(
    `${API_BASE}/products/recommended/mealdb/recipe/${encodeURIComponent(recipeId)}?child_name=${encodeURIComponent(childName)}`
  );

  if (!response.ok) {
    let message = 'Failed to fetch recipe data';

    try {
      const errorData = await response.json();
      message = errorData.detail || JSON.stringify(errorData);
    } catch {
      message = await response.text();
    }

    throw new Error(message);
  }

  const data = await response.json();
  return mapRouteStateToRecipe(data);
};

const loadRecipe = async () => {
  try {
    loading.value = true;
    error.value = '';

    recipe.value = await fetchRecipeFromApi();
  } catch (err) {
    console.error('Failed to load recipe:', err);
    error.value = err.message || 'Failed to load recipe';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadRecipe();
});

const retryLoad = () => {
  loadRecipe();
};

const goBack = () => {
  if (route.query.from === 'weekly-plan') {
    router.push('/weekly-plan');
    return;
  }

  if (route.query.from === 'my-plans') {
    router.push('/my-plans');
    return;
  }

  if (route.query.from === 'results') {
    router.push({
      path: '/results',
      query: {
        childId: route.query.childId || '',
      },
    });
    return;
  }

  if (window.history.length > 1) {
    router.back();
  } else {
    router.push('/');
  }
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>