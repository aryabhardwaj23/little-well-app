<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-6xl px-4 sm:px-6">
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
        <div
          class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] sm:h-16 sm:w-16"
          aria-hidden="true"
        >
          <BookmarkCheck class="h-7 w-7 text-white sm:h-8 sm:w-8" />
        </div>

        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          My Saved Plans
        </h1>

        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          View, reuse, duplicate, and delete saved weekly plans
        </p>
      </header>

      <!-- Loading / Error -->
      <div
        v-if="isLoading"
        class="mb-6 rounded-xl border bg-white p-4 text-center text-sm text-muted-foreground sm:mb-8"
        aria-live="polite"
        aria-busy="true"
      >
        Loading saved plans…
      </div>

      <div
        v-if="errorMessage"
        role="alert"
        aria-live="assertive"
        class="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 sm:mb-8"
      >
        {{ errorMessage }}
      </div>

      <!-- Reuse Prompt -->
      <div
        v-if="weeklyPlans.length > 0 && showReusePrompt"
        class="mb-6 rounded-2xl border border-[#A8D5BA]/30 bg-gradient-to-r from-[#A8D5BA]/20 to-[#CDE7F0]/20 p-5 sm:mb-8 sm:p-6"
        role="region"
        aria-label="Reuse previous plan prompt"
      >
        <div class="flex flex-col gap-4 sm:flex-row sm:items-start">
          <div
            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-white sm:h-12 sm:w-12"
            aria-hidden="true"
          >
            <Sparkles class="h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" />
          </div>

          <div class="flex-1">
            <h3 class="mb-2 text-lg font-semibold text-[#2C5F2D]">
              Use your previous weekly plan?
            </h3>

            <p class="mb-4 text-sm leading-relaxed text-muted-foreground">
              You can reuse "{{ weeklyPlans[0].name }}" or adjust it to fit this week's needs.
            </p>

            <div class="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:gap-3">
              <button
                @click="handleReusePlan(weeklyPlans[0])"
                class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-6 py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto sm:py-2"
                type="button"
              >
                <Copy class="h-4 w-4" aria-hidden="true" />
                Reuse Plan
              </button>

              <button
                @click="handleAdjustPlan(weeklyPlans[0])"
                class="inline-flex w-full items-center justify-center gap-2 rounded-lg border-2 border-[#A8D5BA] bg-white px-6 py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10 sm:w-auto sm:py-2"
                type="button"
              >
                <Settings class="h-4 w-4" aria-hidden="true" />
                Adjust Plan
              </button>

              <button
                @click="showReusePrompt = false"
                class="inline-flex w-full items-center justify-center rounded-lg px-6 py-3 text-sm text-muted-foreground transition-colors hover:bg-white/70 hover:text-gray-700 sm:w-auto sm:py-2"
                type="button"
                aria-label="Dismiss reuse prompt"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div
        role="tablist"
        aria-label="Plan tabs"
        class="-mx-4 mb-6 flex gap-4 overflow-x-auto border-b px-4 sm:mx-0 sm:mb-8 sm:overflow-visible sm:px-0"
      >
        <button
          id="tab-weekly"
          role="tab"
          :aria-selected="activeTab === 'weekly'"
          aria-controls="panel-weekly"
          @click="activeTab = 'weekly'"
          :class="[
            'shrink-0 px-1 pb-4 text-sm transition-all sm:px-2 sm:text-base',
            activeTab === 'weekly'
              ? 'border-b-2 border-[#A8D5BA] text-[#2C5F2D] font-medium'
              : 'text-muted-foreground hover:text-gray-700'
          ]"
          type="button"
        >
          <CalendarDays class="mr-2 inline h-4 w-4" aria-hidden="true" />
          Weekly Plans ({{ weeklyPlans.length }})
        </button>

        <button
          id="tab-lunchboxes"
          role="tab"
          :aria-selected="activeTab === 'lunchboxes'"
          aria-controls="panel-lunchboxes"
          @click="activeTab = 'lunchboxes'"
          :class="[
            'shrink-0 px-1 pb-4 text-sm transition-all sm:px-2 sm:text-base',
            activeTab === 'lunchboxes'
              ? 'border-b-2 border-[#A8D5BA] text-[#2C5F2D] font-medium'
              : 'text-muted-foreground hover:text-gray-700'
          ]"
          type="button"
        >
          <UtensilsCrossed class="mr-2 inline h-4 w-4" aria-hidden="true" />
          Saved Lunchboxes ({{ savedLunchboxes.length }})
        </button>
      </div>

      <!-- Weekly Plans Panel -->
      <div
        id="panel-weekly"
        role="tabpanel"
        aria-labelledby="tab-weekly"
        v-if="activeTab === 'weekly'"
      >
        <div v-if="weeklyPlans.length === 0 && !isLoading" class="py-12 text-center sm:py-16">
          <div
            class="mx-auto mb-4 flex h-18 w-18 items-center justify-center rounded-full bg-gray-100 sm:h-20 sm:w-20"
            aria-hidden="true"
          >
            <CalendarDays class="h-9 w-9 text-gray-400 sm:h-10 sm:w-10" />
          </div>

          <h2 class="mb-2 text-xl font-semibold text-[#2C5F2D]">
            No weekly plans saved yet
          </h2>

          <p class="mb-6 text-sm text-muted-foreground sm:text-base">
            Create your first weekly plan to get started.
          </p>

          <button
            @click="router.push('/weekly-plan')"
            class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3 text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto"
            type="button"
          >
            <Plus class="h-4 w-4" aria-hidden="true" />
            Create Weekly Plan
          </button>
        </div>

        <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
          <article
            v-for="plan in weeklyPlans"
            :key="plan.id"
            class="rounded-2xl border bg-white p-5 shadow-sm transition-shadow hover:shadow-md sm:p-6"
          >
            <div class="mb-4 flex items-start justify-between gap-3">
              <div class="min-w-0 flex-1">
                <h2 class="mb-2 truncate text-lg font-semibold text-[#111827] sm:text-xl">
                  {{ plan.name }}
                </h2>

                <div class="mb-2 flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock class="h-4 w-4 shrink-0" aria-hidden="true" />
                  <span>{{ formatDate(plan.createdAt) }}</span>
                </div>
              </div>

              <button
                @click="handleDeletePlan(plan.id)"
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg transition-colors hover:bg-red-50"
                :aria-label="`Delete plan ${plan.name}`"
                type="button"
              >
                <Trash2 class="h-4 w-4 text-red-500" aria-hidden="true" />
              </button>
            </div>

            <div class="mb-4 space-y-3">
              <div class="flex items-center gap-2">
                <ChefHat class="h-4 w-4 shrink-0 text-[#A8D5BA]" aria-hidden="true" />
                <span class="text-sm">{{ plan.cookingFrequency }} cooking days/week</span>
              </div>

              <div class="flex items-center gap-2">
                <Leaf class="h-4 w-4 shrink-0 text-[#A8D5BA]" aria-hidden="true" />
                <span class="text-sm">{{ plan.season || 'Seasonal' }} plan</span>
              </div>

              <div v-if="plan.children.length > 0">
                <p class="mb-1 text-xs text-muted-foreground">For:</p>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="child in plan.children"
                    :key="child"
                    class="rounded-full bg-[#CDE7F0]/30 px-2 py-1 text-xs text-[#1B4965]"
                  >
                    {{ child }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Meal Preview -->
            <div class="mb-4 rounded-lg bg-[#FAF9F6] p-3">
              <p class="mb-2 text-xs text-muted-foreground">
                {{ plan.batches.length }} cooking sessions
              </p>

              <div class="space-y-3">
                <div
                  v-for="(batch, index) in plan.batches.slice(0, 2)"
                  :key="`${plan.id}-${index}`"
                  class="rounded-lg border bg-white p-3"
                >
                  <div class="flex items-start gap-3">
                    <div
                      v-if="batch.recipe.image"
                      class="h-14 w-14 shrink-0 overflow-hidden rounded-lg bg-gray-100"
                    >
                      <img
                        :src="batch.recipe.image"
                        :alt="batch.recipe.title"
                        class="h-full w-full object-cover"
                        @error="handleImageError"
                      />
                    </div>

                    <div class="min-w-0 flex-1">
                      <p class="mb-1 text-xs text-muted-foreground">
                        {{ batch.cookDay }}
                      </p>

                      <p class="truncate text-sm font-medium">
                        {{ batch.lunchbox.title }}
                      </p>

                      <p class="truncate text-xs text-[#1B4965]">
                        API recipe: {{ batch.recipe.title }}
                      </p>

                      <!-- Why This Meal AI Explanation -->
                      <div class="mt-3 rounded-lg border border-[#A8D5BA]/30 bg-[#FAF9F6] p-3">
                        <div class="flex items-center justify-between gap-3">
                          <div>
                            <p class="text-xs font-semibold text-[#2C5F2D]">
                              Why this meal?
                            </p>
                            <p class="text-xs text-muted-foreground">
                              AI explanation for this lunchbox choice.
                            </p>
                          </div>

                          <button
                            @click="explainMeal(plan, batch)"
                            :disabled="aiExplanationLoading[getMealKey(plan, batch)]"
                            class="shrink-0 rounded-lg bg-[#A8D5BA] px-3 py-2 text-xs font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:opacity-50"
                            type="button"
                          >
                            <span v-if="!aiExplanationLoading[getMealKey(plan, batch)]">
                              Generate
                            </span>
                            <span v-else>
                              Thinking...
                            </span>
                          </button>
                        </div>

                        <p
                          v-if="aiExplanations[getMealKey(plan, batch)]"
                          class="mt-3 text-xs leading-relaxed text-gray-700"
                        >
                          ✨ {{ aiExplanations[getMealKey(plan, batch)] }}
                        </p>

                        <p
                          v-if="aiExplanationErrors[getMealKey(plan, batch)]"
                          class="mt-3 text-xs text-red-500"
                        >
                          {{ aiExplanationErrors[getMealKey(plan, batch)] }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <p v-if="plan.batches.length > 2" class="mt-2 text-xs text-muted-foreground">
                + {{ plan.batches.length - 2 }} more sessions
              </p>
            </div>

            <!-- Actions -->
            <div class="grid grid-cols-2 gap-2">
              <button
                @click="handleViewPlan(plan)"
                class="inline-flex items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] py-2.5 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4]"
                type="button"
                :aria-label="`View plan ${plan.name}`"
              >
                <Eye class="h-4 w-4" aria-hidden="true" />
                View
              </button>

              <button
                @click="handleEditPlan(plan)"
                class="inline-flex items-center justify-center gap-2 rounded-lg border-2 border-[#A8D5BA] bg-white py-2.5 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10"
                type="button"
                :aria-label="`Edit plan ${plan.name}`"
              >
                <Edit class="h-4 w-4" aria-hidden="true" />
                Edit
              </button>

              <button
                @click="handleDuplicatePlan(plan)"
                class="col-span-2 inline-flex items-center justify-center gap-2 rounded-lg border-2 border-[#CDE7F0] bg-white px-3 py-2.5 text-sm font-medium text-[#1B4965] transition-colors hover:bg-[#CDE7F0]/10"
                :aria-label="`Duplicate plan ${plan.name}`"
                type="button"
              >
                <Copy class="h-4 w-4" aria-hidden="true" />
                Duplicate
              </button>
            </div>
          </article>
        </div>
      </div>

      <!-- Saved Lunchboxes Panel -->
      <div
        id="panel-lunchboxes"
        role="tabpanel"
        aria-labelledby="tab-lunchboxes"
        v-if="activeTab === 'lunchboxes'"
      >
        <div v-if="savedLunchboxes.length === 0" class="py-12 text-center sm:py-16">
          <div
            class="mx-auto mb-4 flex h-18 w-18 items-center justify-center rounded-full bg-gray-100 sm:h-20 sm:w-20"
            aria-hidden="true"
          >
            <UtensilsCrossed class="h-9 w-9 text-gray-400 sm:h-10 sm:w-10" />
          </div>

          <h2 class="mb-2 text-xl font-semibold text-[#2C5F2D]">
            No saved lunchboxes yet
          </h2>

          <p class="mb-6 text-sm text-muted-foreground sm:text-base">
            This tab is kept for future single lunchbox saving.
          </p>

          <button
            @click="router.push('/results')"
            class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3 text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto"
            type="button"
          >
            <Plus class="h-4 w-4" aria-hidden="true" />
            Explore Lunchboxes
          </button>
        </div>

        <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
          <article
            v-for="lunchbox in savedLunchboxes"
            :key="lunchbox.id"
            class="rounded-2xl border bg-white p-5 shadow-sm transition-shadow hover:shadow-md sm:p-6"
          >
            <h2 class="mb-2 text-lg font-semibold text-[#111827]">
              {{ lunchbox.name }}
            </h2>

            <p class="mb-4 text-sm leading-relaxed text-muted-foreground">
              {{ lunchbox.description || 'Nutritious and balanced meal' }}
            </p>

            <div class="grid grid-cols-[1fr_auto] gap-2">
              <button
                @click="router.push(`/recipe/${lunchbox.id}`)"
                class="rounded-lg bg-[#A8D5BA] py-2.5 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4]"
                type="button"
                :aria-label="`View lunchbox ${lunchbox.name}`"
              >
                View
              </button>

              <button
                @click="handleDeleteLunchbox(lunchbox.id)"
                class="flex h-10 w-10 items-center justify-center rounded-lg transition-colors hover:bg-red-50"
                type="button"
                :aria-label="`Delete lunchbox ${lunchbox.name}`"
              >
                <Trash2 class="h-4 w-4 text-red-500" aria-hidden="true" />
              </button>
            </div>
          </article>
        </div>
      </div>

      <!-- Bottom CTA -->
      <div class="mt-10 flex justify-center sm:mt-12">
        <button
          @click="router.push('/weekly-plan')"
          class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3 text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto"
          type="button"
        >
          <Plus class="h-4 w-4" aria-hidden="true" />
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
  getWhyThisMeal,
} from '../services/api';

const router = useRouter();

const activeTab = ref('weekly');
const savedPlans = ref([]);
const savedLunchboxes = ref([]);
const showReusePrompt = ref(true);
const isLoading = ref(false);
const errorMessage = ref('');

// AI explanation state
const aiExplanationLoading = ref({});
const aiExplanations = ref({});
const aiExplanationErrors = ref({});

// ── Normalise helpers ───────────────────────────
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
    reference_food_id: lunchbox.reference_food_id || meal.reference_food_id || null,
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

const normalizeRecipe = (meal) => {
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

const normalizeMeal = (meal, index = 0) => ({
  id: meal.meal_id || meal.id || `meal-${index}`,
  cookDay: meal.cook_day || meal.cookDay || meal.title || `Cook Session ${index + 1}`,
  coverDays: meal.cover_days || meal.coverDays || meal.covers || 'Selected days',
  prepTime: meal.prep_time_minutes ? `${meal.prep_time_minutes} mins` : meal.prepTime || '30 mins',
  lunchbox: normalizeLunchbox(meal, index),
  recipe: normalizeRecipe(meal),
});

const getSeasonNameFromId = (seasonId) =>
  ({
    1: 'Spring',
    2: 'Summer',
    3: 'Autumn',
    4: 'Winter',
  })[Number(seasonId)] || '';

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
    createdAt: plan.created_at || plan.createdAt || new Date().toISOString(),
  };
};

const loadSavedPlans = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';

    const plans = await getWeeklyPlans();
    savedPlans.value = Array.isArray(plans) ? plans.map(normalizePlan) : [];

    const localPlans = localStorage.getItem('nutriguide_saved_plans');
    const parsed = localPlans ? JSON.parse(localPlans) : [];
    savedLunchboxes.value = parsed.filter((plan) => plan.type === 'lunchbox');
  } catch (error) {
    console.error('Failed to load saved plans:', error);
    errorMessage.value = error.message || 'Failed to load saved plans.';
    savedPlans.value = [];

    const localPlans = localStorage.getItem('nutriguide_saved_plans');
    const parsed = localPlans ? JSON.parse(localPlans) : [];
    savedLunchboxes.value = parsed.filter((plan) => plan.type === 'lunchbox');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => loadSavedPlans());

const weeklyPlans = computed(() => savedPlans.value.filter((plan) => plan.type === 'weekly'));

const formatDate = (dateString) => {
  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) return 'Recently';

  const diffDays = Math.floor(Math.abs(new Date() - date) / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;

  return date.toLocaleDateString('en-AU', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

// ── AI explanation ───────────────────────────
const getMealKey = (plan, batch) => {
  return `${plan.id}-${batch.id || batch.lunchbox?.id || batch.recipe?.id || batch.lunchbox?.title}`;
};

const explainMeal = async (plan, batch) => {
  const mealKey = getMealKey(plan, batch);

  try {
    aiExplanationLoading.value[mealKey] = true;
    aiExplanationErrors.value[mealKey] = '';

    const mealName = batch.lunchbox?.title || batch.recipe?.title || 'Lunchbox meal';

    const data = await getWhyThisMeal({
      meal_name: mealName,
      child_age: 7,
      allergens: [],
      dietary_restrictions: [],
      season: plan.season || 'autumn',
      meal_type: 'lunchbox',
    });

    aiExplanations.value[mealKey] = data.explanation;
  } catch (error) {
    aiExplanationErrors.value[mealKey] =
      error.message || 'Could not generate explanation.';
  } finally {
    aiExplanationLoading.value[mealKey] = false;
  }
};

// ── Actions ───────────────────────────
const handleViewPlan = (plan) => router.push(`/weekly-plan?mode=view&planId=${plan.id}`);
const handleEditPlan = (plan) => router.push(`/weekly-plan?mode=edit&planId=${plan.id}`);
const handleReusePlan = (plan) => router.push(`/weekly-plan?mode=reuse&planId=${plan.id}`);
const handleAdjustPlan = (plan) => router.push(`/weekly-plan?mode=adjust&planId=${plan.id}`);

const handleDuplicatePlan = async (plan) => {
  try {
    errorMessage.value = '';
    await duplicateWeeklyPlan(plan.id);
    await loadSavedPlans();
  } catch (error) {
    errorMessage.value = error.message || 'Duplicate failed.';
  }
};

const handleDeletePlan = async (planId) => {
  if (!confirm('Are you sure you want to delete this plan?')) return;

  try {
    errorMessage.value = '';
    await deleteWeeklyPlan(planId);
    savedPlans.value = savedPlans.value.filter((plan) => String(plan.id) !== String(planId));
  } catch (error) {
    errorMessage.value = error.message || 'Failed to delete plan.';
  }
};

const handleDeleteLunchbox = (lunchboxId) => {
  if (!confirm('Are you sure you want to delete this lunchbox?')) return;

  savedLunchboxes.value = savedLunchboxes.value.filter(
    (lunchbox) => String(lunchbox.id) !== String(lunchboxId),
  );

  const localPlans = localStorage.getItem('nutriguide_saved_plans');
  const parsed = localPlans ? JSON.parse(localPlans) : [];

  localStorage.setItem(
    'nutriguide_saved_plans',
    JSON.stringify(parsed.filter((plan) => String(plan.id) !== String(lunchboxId))),
  );
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