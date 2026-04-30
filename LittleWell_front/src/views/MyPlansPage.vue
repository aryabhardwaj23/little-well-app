<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-6xl">
      <!-- Back Button -->
      <button
        @click="router.push('/')"
        class="mb-6 px-4 py-2 hover:bg-white rounded-lg transition-colors inline-flex items-center gap-2"
        type="button"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Home
      </button>

      <!-- Header -->
      <div class="text-center mb-12">
        <div class="w-16 h-16 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center mx-auto mb-4">
          <BookmarkCheck class="w-8 h-8 text-white" />
        </div>

        <h1 class="text-4xl mb-4">My Saved Plans</h1>
        <p class="text-lg text-muted-foreground">
          View, reuse, duplicate, and delete saved weekly plans
        </p>
      </div>

      <!-- Loading / Error -->
      <div
        v-if="isLoading"
        class="mb-8 p-4 bg-white rounded-xl border text-center text-muted-foreground"
      >
        Loading saved plans...
      </div>

      <div
        v-if="errorMessage"
        class="mb-8 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl"
      >
        {{ errorMessage }}
      </div>

      <!-- Reuse Prompt -->
      <div
        v-if="weeklyPlans.length > 0 && showReusePrompt"
        class="mb-8 p-6 bg-gradient-to-r from-[#A8D5BA]/20 to-[#CDE7F0]/20 rounded-2xl border border-[#A8D5BA]/30"
      >
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center flex-shrink-0">
            <Sparkles class="w-6 h-6 text-[#A8D5BA]" />
          </div>

          <div class="flex-1">
            <h3 class="text-lg font-medium mb-2">Use your previous weekly plan?</h3>

            <p class="text-sm text-muted-foreground mb-4">
              You can reuse "{{ weeklyPlans[0].name }}" or adjust it to fit this week's needs.
            </p>

            <div class="flex flex-wrap gap-3">
              <button
                @click="handleReusePlan(weeklyPlans[0])"
                class="text-sm bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] px-6 py-2 rounded-lg inline-flex items-center gap-2 transition-colors"
                type="button"
              >
                <Copy class="w-4 h-4" />
                Reuse Plan
              </button>

              <button
                @click="handleAdjustPlan(weeklyPlans[0])"
                class="text-sm bg-white border-2 border-[#A8D5BA] text-[#2C5F2D] px-6 py-2 rounded-lg hover:bg-[#A8D5BA]/10 transition-colors inline-flex items-center gap-2"
                type="button"
              >
                <Settings class="w-4 h-4" />
                Adjust Plan
              </button>

              <button
                @click="showReusePrompt = false"
                class="text-sm text-muted-foreground hover:text-gray-700"
                type="button"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex gap-4 mb-8 border-b">
        <button
          @click="activeTab = 'weekly'"
          :class="[
            'pb-4 px-2 transition-all',
            activeTab === 'weekly'
              ? 'border-b-2 border-[#A8D5BA] text-[#2C5F2D] font-medium'
              : 'text-muted-foreground hover:text-gray-700'
          ]"
          type="button"
        >
          <CalendarDays class="w-4 h-4 inline mr-2" />
          Weekly Plans ({{ weeklyPlans.length }})
        </button>

        <button
          @click="activeTab = 'lunchboxes'"
          :class="[
            'pb-4 px-2 transition-all',
            activeTab === 'lunchboxes'
              ? 'border-b-2 border-[#A8D5BA] text-[#2C5F2D] font-medium'
              : 'text-muted-foreground hover:text-gray-700'
          ]"
          type="button"
        >
          <UtensilsCrossed class="w-4 h-4 inline mr-2" />
          Saved Lunchboxes ({{ savedLunchboxes.length }})
        </button>
      </div>

      <!-- Weekly Plans -->
      <div v-if="activeTab === 'weekly'">
        <div v-if="weeklyPlans.length === 0 && !isLoading" class="text-center py-16">
          <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CalendarDays class="w-10 h-10 text-gray-400" />
          </div>

          <h3 class="text-xl mb-2">No weekly plans saved yet</h3>

          <p class="text-muted-foreground mb-6">
            Create your first weekly plan to get started.
          </p>

          <button
            @click="router.push('/weekly-plan')"
            class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] px-8 py-3 rounded-lg inline-flex items-center gap-2 transition-colors"
            type="button"
          >
            <Plus class="w-4 h-4" />
            Create Weekly Plan
          </button>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="plan in weeklyPlans"
            :key="plan.id"
            class="p-6 rounded-2xl shadow-md hover:shadow-lg transition-shadow bg-white border"
          >
            <!-- Plan Header -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <h3 class="text-xl font-medium mb-2">{{ plan.name }}</h3>

                <div class="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                  <Clock class="w-4 h-4" />
                  <span>{{ formatDate(plan.createdAt) }}</span>
                </div>
              </div>

              <button
                @click="handleDeletePlan(plan.id)"
                class="p-2 hover:bg-red-50 rounded-lg transition-colors"
                title="Delete plan"
                type="button"
              >
                <Trash2 class="w-4 h-4 text-red-500" />
              </button>
            </div>

            <!-- Plan Info -->
            <div class="space-y-3 mb-4">
              <div class="flex items-center gap-2">
                <ChefHat class="w-4 h-4 text-[#A8D5BA]" />
                <span class="text-sm">{{ plan.cookingFrequency }} cooking days/week</span>
              </div>

              <div class="flex items-center gap-2">
                <Leaf class="w-4 h-4 text-[#A8D5BA]" />
                <span class="text-sm">{{ plan.season || 'Seasonal' }} plan</span>
              </div>

              <div v-if="plan.children.length > 0">
                <p class="text-xs text-muted-foreground mb-1">For:</p>

                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="child in plan.children"
                    :key="child"
                    class="bg-[#CDE7F0]/30 text-[#1B4965] text-xs rounded-full px-2 py-1"
                  >
                    {{ child }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Meal Preview -->
            <div class="mb-4 p-3 bg-[#FAF9F6] rounded-lg">
              <p class="text-xs text-muted-foreground mb-2">
                {{ plan.batches.length }} cooking sessions
              </p>

              <div class="space-y-3">
                <div
                  v-for="(batch, index) in plan.batches.slice(0, 2)"
                  :key="`${plan.id}-${index}`"
                  class="bg-white rounded-lg p-3 border"
                >
                  <div class="flex items-start gap-3">
                    <div
                      v-if="batch.recipe.image"
                      class="w-14 h-14 rounded-lg overflow-hidden bg-gray-100 flex-shrink-0"
                    >
                      <img
                        :src="batch.recipe.image"
                        :alt="batch.recipe.title"
                        class="w-full h-full object-cover"
                        @error="handleImageError"
                      />
                    </div>

                    <div class="min-w-0">
                      <p class="text-xs text-muted-foreground mb-1">
                        {{ batch.cookDay }}
                      </p>

                      <p class="text-sm font-medium truncate">
                        {{ batch.lunchbox.title }}
                      </p>

                      <p class="text-xs text-[#1B4965] truncate">
                        API recipe: {{ batch.recipe.title }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <p v-if="plan.batches.length > 2" class="text-xs text-muted-foreground mt-2">
                + {{ plan.batches.length - 2 }} more sessions
              </p>
            </div>

            <!-- Actions -->
            <div class="flex gap-2">
              <button
                @click="handleViewPlan(plan)"
                class="flex-1 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-2 text-sm inline-flex items-center justify-center gap-2 transition-colors"
                type="button"
              >
                <Eye class="w-4 h-4" />
                View
              </button>

              <button
                @click="handleEditPlan(plan)"
                class="flex-1 bg-white border-2 border-[#A8D5BA] text-[#2C5F2D] rounded-lg py-2 text-sm hover:bg-[#A8D5BA]/10 transition-colors inline-flex items-center justify-center gap-2"
                type="button"
              >
                <Edit class="w-4 h-4" />
                Edit
              </button>

              <button
                @click="handleDuplicatePlan(plan)"
                class="bg-white border-2 border-[#CDE7F0] text-[#1B4965] rounded-lg py-2 px-3 text-sm hover:bg-[#CDE7F0]/10 transition-colors"
                title="Duplicate"
                type="button"
              >
                <Copy class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Saved Lunchboxes -->
      <div v-if="activeTab === 'lunchboxes'">
        <div v-if="savedLunchboxes.length === 0" class="text-center py-16">
          <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UtensilsCrossed class="w-10 h-10 text-gray-400" />
          </div>

          <h3 class="text-xl mb-2">No saved lunchboxes yet</h3>

          <p class="text-muted-foreground mb-6">
            This tab is kept for future single lunchbox saving.
          </p>

          <button
            @click="router.push('/results')"
            class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] px-8 py-3 rounded-lg inline-flex items-center gap-2 transition-colors"
            type="button"
          >
            <Plus class="w-4 h-4" />
            Explore Lunchboxes
          </button>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="lunchbox in savedLunchboxes"
            :key="lunchbox.id"
            class="p-6 rounded-2xl shadow-md hover:shadow-lg transition-shadow bg-white border cursor-pointer"
            @click="router.push(`/recipe/${lunchbox.id}`)"
          >
            <h3 class="text-lg font-medium mb-2">{{ lunchbox.name }}</h3>

            <p class="text-sm text-muted-foreground mb-4">
              {{ lunchbox.description || 'Nutritious and balanced meal' }}
            </p>

            <button
              @click.stop="handleDeleteLunchbox(lunchbox.id)"
              class="p-2 hover:bg-red-50 rounded-lg transition-colors"
              type="button"
            >
              <Trash2 class="w-4 h-4 text-red-500" />
            </button>
          </div>
        </div>
      </div>

      <!-- Bottom CTA -->
      <div class="mt-12 flex justify-center">
        <button
          @click="router.push('/weekly-plan')"
          class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] px-8 py-3 rounded-lg inline-flex items-center gap-2 transition-colors"
          type="button"
        >
          <Plus class="w-4 h-4" />
          Create Another Weekly Plan
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import {
  ArrowLeft,
  BookmarkCheck,
  CalendarDays,
  UtensilsCrossed,
  Plus,
  Clock,
  ChefHat,
  Leaf,
  Eye,
  Edit,
  Copy,
  Trash2,
  Sparkles,
  Settings,
} from 'lucide-vue-next';
import {
  getWeeklyPlans,
  deleteWeeklyPlan,
  duplicateWeeklyPlan,
} from '../services/api';

const router = useRouter();

const activeTab = ref('weekly');
const savedPlans = ref([]);
const savedLunchboxes = ref([]);
const showReusePrompt = ref(true);

const isLoading = ref(false);
const errorMessage = ref('');

const parseTags = (tags) => {
  if (Array.isArray(tags)) return tags;
  if (!tags) return [];

  return String(tags)
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean);
};

const normalizeChildren = (children) => {
  if (!Array.isArray(children)) return [];

  return children
    .map((child) => {
      if (typeof child === 'string') return child;
      return child.child_name || child.name || child.childName || '';
    })
    .filter(Boolean);
};

const normalizeLunchbox = (meal, index = 0) => {
  const lunchbox = meal.lunchbox || {};
  const items = lunchbox.items || meal.items || meal.lunchbox_items || [];

  return {
    id:
      lunchbox.id ||
      meal.reference_food_id ||
      meal.lunchbox_id ||
      meal.source_id ||
      `db-${index}`,

    reference_food_id:
      lunchbox.reference_food_id ||
      meal.reference_food_id ||
      null,

    title:
      lunchbox.title ||
      meal.meal_title ||
      meal.mealName ||
      meal.lunchbox_title ||
      'Database Lunchbox',

    nutritionFocus: parseTags(lunchbox.nutritionFocus || meal.nutrition_tags || meal.tags),
    whyThisMeal: lunchbox.whyThisMeal || meal.whyThisMeal || '',
    items: Array.isArray(items) ? items : [],
  };
};

const normalizeRecipe = (meal, index = 0) => {
  const recipe = meal.recipe || {};

  return {
    id: recipe.id || meal.recipe_id || meal.recipeId || null,

    title:
      recipe.title ||
      meal.recipe_title ||
      meal.recipeName ||
      (meal.recipe_id ? `Recipe #${meal.recipe_id}` : 'Recipe Inspiration'),

    image:
      recipe.image ||
      recipe.heroImage ||
      recipe.mealImage ||
      meal.image_url ||
      meal.heroImage ||
      meal.mealImage ||
      '',

    category: recipe.category || meal.category || '',
    area: recipe.area || meal.area || '',
    nutritionFocus: parseTags(recipe.nutritionFocus || meal.recipe_tags),
    whyThisMeal: recipe.whyThisMeal || meal.recipe_note || '',
  };
};

const normalizeMeal = (meal, index = 0) => {
  return {
    id: meal.meal_id || meal.id || `meal-${index}`,
    cookDay: meal.cook_day || meal.cookDay || meal.title || `Cook Session ${index + 1}`,
    coverDays: meal.cover_days || meal.coverDays || meal.covers || 'Selected days',
    prepTime: meal.prep_time_minutes ? `${meal.prep_time_minutes} mins` : meal.prepTime || '30 mins',
    lunchbox: normalizeLunchbox(meal, index),
    recipe: normalizeRecipe(meal, index),
  };
};

const normalizePlan = (plan) => {
  const meals = plan.meals || plan.batches || [];

  return {
    id: plan.plan_id || plan.id,
    type: 'weekly',
    name: plan.plan_name || plan.name || 'Untitled Weekly Plan',
    cookingFrequency: plan.cook_frequency || plan.cookingFrequency || meals.length || 0,
    season: plan.season || plan.season_name || getSeasonNameFromId(plan.season_id) || 'Seasonal',
    children: normalizeChildren(plan.children),
    batches: Array.isArray(meals) ? meals.map(normalizeMeal) : [],
    varietyPreference: plan.variety_preference || plan.varietyPreference,
    mealStyle: plan.meal_style || plan.mealStyle,
    createdAt: plan.created_at || plan.createdAt || new Date().toISOString(),
  };
};

const getSeasonNameFromId = (seasonId) => {
  const seasonMap = {
    1: 'Spring',
    2: 'Summer',
    3: 'Autumn',
    4: 'Winter',
  };

  return seasonMap[Number(seasonId)] || '';
};

const loadSavedPlans = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';

    const plans = await getWeeklyPlans();
    savedPlans.value = Array.isArray(plans) ? plans.map(normalizePlan) : [];

    const localPlans = localStorage.getItem('nutriguide_saved_plans');
    const parsedLocalPlans = localPlans ? JSON.parse(localPlans) : [];
    savedLunchboxes.value = parsedLocalPlans.filter((plan) => plan.type === 'lunchbox');
  } catch (error) {
    console.error('Failed to load saved plans:', error);
    errorMessage.value = error.message || 'Failed to load saved plans.';
    savedPlans.value = [];

    const localPlans = localStorage.getItem('nutriguide_saved_plans');
    const parsedLocalPlans = localPlans ? JSON.parse(localPlans) : [];
    savedLunchboxes.value = parsedLocalPlans.filter((plan) => plan.type === 'lunchbox');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadSavedPlans();
});

const weeklyPlans = computed(() => {
  return savedPlans.value.filter((plan) => plan.type === 'weekly');
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  if (Number.isNaN(date.getTime())) return 'Recently';

  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

const handleViewPlan = (plan) => {
  router.push(`/weekly-plan?mode=view&planId=${plan.id}`);
};

const handleEditPlan = (plan) => {
  router.push(`/weekly-plan?mode=edit&planId=${plan.id}`);
};

const handleReusePlan = (plan) => {
  router.push(`/weekly-plan?mode=reuse&planId=${plan.id}`);
};

const handleAdjustPlan = (plan) => {
  router.push(`/weekly-plan?mode=adjust&planId=${plan.id}`);
};

const handleDuplicatePlan = async (plan) => {
  try {
    errorMessage.value = '';
    await duplicateWeeklyPlan(plan.id);
    await loadSavedPlans();
  } catch (error) {
    console.error('Failed to duplicate plan:', error);
    errorMessage.value =
      error.message ||
      'Duplicate failed. Check that POST /weekly-plans/{plan_id}/duplicate exists in the backend.';
  }
};

const handleDeletePlan = async (planId) => {
  if (!confirm('Are you sure you want to delete this plan?')) return;

  try {
    errorMessage.value = '';
    await deleteWeeklyPlan(planId);
    savedPlans.value = savedPlans.value.filter((plan) => String(plan.id) !== String(planId));
  } catch (error) {
    console.error('Failed to delete plan:', error);
    errorMessage.value = error.message || 'Failed to delete plan. Please try again.';
  }
};

const handleDeleteLunchbox = (lunchboxId) => {
  if (!confirm('Are you sure you want to delete this lunchbox?')) return;

  savedLunchboxes.value = savedLunchboxes.value.filter(
    (lunchbox) => String(lunchbox.id) !== String(lunchboxId)
  );

  const localPlans = localStorage.getItem('nutriguide_saved_plans');
  const parsedLocalPlans = localPlans ? JSON.parse(localPlans) : [];
  const updatedLocalPlans = parsedLocalPlans.filter(
    (plan) => String(plan.id) !== String(lunchboxId)
  );

  localStorage.setItem('nutriguide_saved_plans', JSON.stringify(updatedLocalPlans));
};

const handleImageError = (event) => {
  event.target.style.display = 'none';
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>