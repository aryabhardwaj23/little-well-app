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

      <!-- Loading / Error -->
      <div
        v-if="isLoading"
        class="mb-6 rounded-xl border bg-white p-4 text-center text-sm text-muted-foreground sm:mb-8 sm:text-base"
        aria-live="polite"
        aria-busy="true"
      >
        Loading...
      </div>

      <div
        v-if="errorMessage"
        class="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 sm:mb-8"
        role="alert"
        aria-live="assertive"
      >
        {{ errorMessage }}
      </div>

      <!-- Header -->
      <header v-if="!planGenerated" class="mb-8 text-center sm:mb-12">
        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          Plan Your Week, Simply
        </h1>

        <p class="mx-auto mb-5 max-w-3xl text-sm leading-relaxed text-muted-foreground sm:mb-6 sm:text-lg">
          Build a weekly lunchbox plan for children aged 5–12 using child profiles,
          database food recommendations, and recipe inspiration.
        </p>

        <div class="inline-flex items-center gap-2 rounded-full border bg-white px-5 py-2.5 text-sm shadow-sm sm:px-6 sm:py-3 sm:text-base">
          <component :is="getSeasonIcon()" class="h-5 w-5 text-[#A8D5BA]" aria-hidden="true" />
          <span class="font-medium text-[#2C5F2D]">{{ getSeasonName() }} Plan</span>
        </div>
      </header>

      <!-- Select Children -->
      <section v-if="!planGenerated" class="mb-8 sm:mb-12">
        <div class="mb-5 flex flex-col gap-3 sm:mb-6 sm:flex-row sm:items-center sm:justify-between">
          <h2 class="text-2xl font-semibold text-[#2C5F2D]">Select Children</h2>

          <button
            v-if="profiles.length === 0"
            @click="router.push('/child-info')"
            class="inline-flex w-full items-center justify-center rounded-lg bg-[#A8D5BA] px-5 py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto sm:py-2"
            type="button"
          >
            Add a Child
          </button>
        </div>

        <div v-if="profiles.length === 0" class="rounded-2xl border bg-white p-6 text-center sm:p-8">
          <p class="mb-4 text-sm leading-relaxed text-muted-foreground sm:text-base">
            No supported child profiles found. Create a child profile for a child aged 5–12 first.
          </p>

          <button
            @click="router.push('/child-info')"
            class="inline-flex w-full items-center justify-center rounded-lg bg-[#A8D5BA] px-8 py-3 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto"
            type="button"
          >
            Create 5–12 Child Profile
          </button>
        </div>

        <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-3">
          <button
            v-for="profile in profiles"
            :key="profile.id"
            @click="toggleChildSelection(profile.id)"
            :aria-pressed="selectedChildren.includes(profile.id)"
            :class="[
              'w-full rounded-2xl border-2 p-5 text-left transition-all sm:p-6',
              selectedChildren.includes(profile.id)
                ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 shadow-sm'
                : 'border-gray-200 bg-white hover:border-[#A8D5BA]/50'
            ]"
            type="button"
          >
            <div class="flex items-start gap-3">
              <input
                type="checkbox"
                :checked="selectedChildren.includes(profile.id)"
                class="mt-1 accent-[#A8D5BA]"
                tabindex="-1"
                aria-hidden="true"
                @click.stop
              />

              <div class="min-w-0 flex-1">
                <h3 class="mb-1 text-lg font-semibold leading-tight text-[#111827]">
                  {{ profile.name }}
                </h3>

                <p class="mb-3 text-sm text-muted-foreground">
                  {{ profile.ageGroup }}
                </p>

                <div v-if="profile.allergies.length > 0" class="mb-2">
                  <p class="mb-1 text-xs text-muted-foreground">Allergies</p>

                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="allergy in profile.allergies"
                      :key="allergy"
                      class="rounded-full bg-[#F7B267]/20 px-2 py-0.5 text-xs text-[#8B4513]"
                    >
                      {{ allergy }}
                    </span>
                  </div>
                </div>

                <div v-if="profile.nutritionFocus.length > 0">
                  <p class="mb-1 text-xs text-muted-foreground">Focus</p>

                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="focus in profile.nutritionFocus.slice(0, 2)"
                      :key="focus"
                      class="rounded-full bg-[#A8D5BA]/20 px-2 py-0.5 text-xs text-[#2C5F2D]"
                    >
                      {{ focus }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </button>
        </div>

        <div
          v-if="selectedChildren.length > 0"
          class="mt-4 rounded-lg border bg-white p-4 text-center shadow-sm"
          aria-live="polite"
        >
          <p class="text-sm">
            <strong class="text-[#2C5F2D]">
              {{ selectedChildren.length }} child(ren) selected
            </strong>
          </p>
        </div>
      </section>

      <!-- Cooking Frequency -->
      <section v-if="!planGenerated" class="mb-8 sm:mb-12">
        <h2 class="mb-5 text-2xl font-semibold text-[#2C5F2D] sm:mb-6">
          How often do you want to cook this week?
        </h2>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-3 md:gap-6">
          <button
            v-for="option in frequencyOptions"
            :key="option.value"
            @click="cookingFrequency = option.value"
            :aria-pressed="cookingFrequency === option.value"
            :class="[
              'w-full rounded-2xl border-2 p-5 text-center transition-all sm:p-8',
              cookingFrequency === option.value
                ? option.activeClass
                : 'border-gray-200 bg-white hover:border-[#A8D5BA]/50'
            ]"
            type="button"
          >
            <div
              :class="[
                'mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full sm:h-16 sm:w-16',
                option.iconClass
              ]"
              aria-hidden="true"
            >
              <ChefHat class="h-7 w-7 sm:h-8 sm:w-8" :class="option.iconTextClass" />
            </div>

            <h3 class="mb-2 text-xl font-bold text-[#111827] sm:text-2xl">
              {{ option.label }}
            </h3>

            <p class="text-sm leading-relaxed text-muted-foreground">
              {{ option.description }}
            </p>
          </button>
        </div>
      </section>

      <!-- Generate Button -->
      <div v-if="!planGenerated" class="mb-10 flex justify-center sm:mb-12">
        <button
          @click="generateWeeklyPlan"
          :disabled="selectedChildren.length === 0 || !cookingFrequency || isGenerating"
          class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#A8D5BA] px-8 py-4 text-base font-semibold text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:px-12 sm:text-lg"
          type="button"
          :aria-busy="isGenerating"
        >
          <CalendarDays class="h-5 w-5" aria-hidden="true" />
          {{ isGenerating ? 'Generating...' : 'Generate Weekly Plan' }}
        </button>
      </div>

      <!-- Generated Output -->
      <section v-if="planGenerated">
        <header class="mb-6 text-center sm:mb-8">
          <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
            Your Weekly Lunch Plan
          </h1>
          <p class="mx-auto max-w-3xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
            Each cooking session combines database food items with one API recipe idea.
          </p>
        </header>

        <div class="mb-6 grid grid-cols-1 gap-3 sm:mb-8 sm:flex sm:flex-wrap sm:justify-center sm:gap-4">
          <button
            @click="showSaveDialog = true"
            class="inline-flex items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4]"
            type="button"
          >
            <BookmarkPlus class="h-4 w-4" aria-hidden="true" />
            Save Plan
          </button>

          <button
            @click="regeneratePlan"
            class="inline-flex items-center justify-center gap-2 rounded-lg border-2 border-[#A8D5BA] bg-white px-8 py-3 font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10"
            type="button"
          >
            <RefreshCw class="h-4 w-4" aria-hidden="true" />
            Regenerate Plan
          </button>

          <button
            @click="router.push('/my-plans')"
            class="rounded-lg border-2 border-gray-300 bg-white px-8 py-3 font-medium text-gray-700 transition-colors hover:bg-gray-50"
            type="button"
          >
            My Plans
          </button>
        </div>

        <div class="space-y-6 sm:space-y-8">
          <article
            v-for="(batch, index) in weeklyBatches"
            :key="batch.id || index"
            class="rounded-2xl border bg-white p-5 shadow-sm sm:p-8"
          >
            <div class="mb-5 flex flex-col gap-3 sm:mb-6 md:flex-row md:items-center md:justify-between">
              <h2 class="flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:text-2xl">
                <CalendarCheck class="h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" aria-hidden="true" />
                {{ batch.cookDay }}
              </h2>

              <span class="w-fit rounded-full bg-[#CDE7F0]/30 px-4 py-1 text-sm text-[#1B4965]">
                Covers {{ batch.coverDays }}
              </span>
            </div>

            <div class="grid grid-cols-1 gap-5 lg:grid-cols-2 lg:gap-6">
              <!-- Database Lunchbox -->
              <div class="rounded-2xl border bg-[#FAF9F6] p-5 sm:p-6">
                <div class="mb-4 flex items-start justify-between gap-3">
                  <h3 class="text-lg font-semibold leading-tight text-[#111827] sm:text-xl">
                    {{ batch.lunchbox.title }}
                  </h3>

                  <span class="shrink-0 rounded-full border bg-white px-3 py-1 text-xs text-muted-foreground">
                    Database
                  </span>
                </div>

                <div class="mb-4 space-y-3">
                  <div
                    v-for="(item, idx) in batch.lunchbox.items"
                    :key="`${batch.id}-db-${idx}`"
                    class="flex items-start gap-3 rounded-lg bg-white p-3"
                  >
                    <div
                      :class="[
                        'mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full',
                        getSectionColor(item.section)
                      ]"
                    ></div>

                    <div class="min-w-0">
                      <p class="text-sm font-medium leading-snug text-[#111827]">
                        {{ item.name }}
                      </p>
                      <p class="text-xs leading-relaxed text-muted-foreground">
                        {{ formatWeeklyItemAmount(item.amount, batch.coverDays) }}
                      </p>
                    </div>
                  </div>
                </div>

                <div
                  v-if="batch.lunchbox.nutritionFocus.length > 0"
                  class="mb-4 flex flex-wrap gap-2"
                >
                  <span
                    v-for="focus in batch.lunchbox.nutritionFocus"
                    :key="focus"
                    class="rounded-full bg-[#A8D5BA]/20 px-3 py-1 text-xs text-[#2C5F2D]"
                  >
                    {{ focus }}
                  </span>
                </div>

                <p
                  v-if="batch.lunchbox.whyThisMeal"
                  class="text-sm leading-relaxed text-muted-foreground"
                >
                  {{ batch.lunchbox.whyThisMeal }}
                </p>
              </div>

              <!-- API Recipe -->
              <div class="overflow-hidden rounded-2xl border bg-white">
                <div
                  v-if="batch.recipe.image"
                  class="aspect-[16/9] overflow-hidden bg-gray-100"
                >
                  <img
                    :src="batch.recipe.image"
                    :alt="batch.recipe.title"
                    class="h-full w-full object-cover"
                    @error="handleImageError"
                  />
                </div>

                <div class="p-5 sm:p-6">
                  <div class="mb-3 flex items-start justify-between gap-3">
                    <h3 class="text-lg font-semibold leading-tight text-[#111827] sm:text-xl">
                      {{ batch.recipe.title }}
                    </h3>

                    <span class="shrink-0 rounded-full bg-[#CDE7F0]/30 px-3 py-1 text-xs text-[#1B4965]">
                      API Recipe
                    </span>
                  </div>

                  <div class="mb-4 flex flex-wrap gap-2">
                    <span
                      v-if="batch.recipe.category"
                      class="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600"
                    >
                      {{ batch.recipe.category }}
                    </span>

                    <span
                      v-if="batch.recipe.area"
                      class="rounded-full bg-[#CDE7F0]/30 px-2 py-1 text-xs text-[#1B4965]"
                    >
                      {{ batch.recipe.area }}
                    </span>

                    <span
                      v-for="focus in batch.recipe.nutritionFocus"
                      :key="focus"
                      class="rounded-full bg-[#A8D5BA]/20 px-2 py-1 text-xs text-[#2C5F2D]"
                    >
                      {{ focus }}
                    </span>
                  </div>

                  <p
                    v-if="batch.recipe.whyThisMeal"
                    class="mb-4 text-sm leading-relaxed text-muted-foreground"
                  >
                    {{ batch.recipe.whyThisMeal }}
                  </p>

                  <div class="grid grid-cols-1 gap-2 sm:grid-cols-2 sm:gap-3">
                    <button
                      @click="openRecipe(batch.recipe)"
                      :disabled="!batch.recipe.id"
                      class="inline-flex items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50"
                      type="button"
                    >
                      <BookOpen class="h-4 w-4" aria-hidden="true" />
                      View Recipe
                    </button>

                    <button
                      @click="swapApiRecipe(index)"
                      class="inline-flex items-center justify-center gap-2 rounded-lg border-2 border-[#A8D5BA] bg-white py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10"
                      type="button"
                    >
                      <RefreshCw class="h-4 w-4" aria-hidden="true" />
                      Swap Recipe
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-5 grid grid-cols-1 gap-3 sm:mt-6 md:grid-cols-3 md:gap-4">
              <div class="rounded-lg bg-[#A8D5BA]/10 p-4">
                <div class="flex items-start gap-2">
                  <Leaf class="mt-0.5 h-4 w-4 shrink-0 text-[#A8D5BA]" aria-hidden="true" />
                  <p class="text-sm leading-relaxed text-[#2C5F2D]">{{ batch.seasonalNote }}</p>
                </div>
              </div>

              <div class="rounded-lg bg-[#F7B267]/10 p-4">
                <div class="flex items-start gap-2">
                  <AlertCircle class="mt-0.5 h-4 w-4 shrink-0 text-[#F7B267]" aria-hidden="true" />
                  <p class="text-sm leading-relaxed text-[#8B4513]">
                    <strong>Storage:</strong> {{ batch.storageTip }}
                  </p>
                </div>
              </div>

              <div class="rounded-lg bg-[#CDE7F0]/20 p-4">
                <div class="flex items-start gap-2">
                  <Clock class="mt-0.5 h-4 w-4 shrink-0 text-[#1B4965]" aria-hidden="true" />
                  <p class="text-sm leading-relaxed text-[#1B4965]">
                    <strong>Prep:</strong> {{ batch.prepTime }}
                  </p>
                </div>
              </div>
            </div>
          </article>
        </div>
      </section>

      <!-- Save Dialog -->
      <div
        v-if="showSaveDialog"
        class="fixed inset-0 z-50 flex items-end justify-center bg-black/50 px-4 py-4 sm:items-center"
        role="dialog"
        aria-modal="true"
        aria-labelledby="save-plan-title"
        @click.self="showSaveDialog = false"
      >
        <div class="w-full max-w-md rounded-2xl bg-white p-5 shadow-2xl sm:p-8">
          <h3 id="save-plan-title" class="mb-3 text-2xl font-semibold text-[#2C5F2D] sm:mb-4">
            Name your plan
          </h3>

          <p class="mb-5 text-sm leading-relaxed text-muted-foreground sm:mb-6">
            Give your weekly plan a memorable name.
          </p>

          <input
            v-model="planName"
            type="text"
            placeholder="e.g. Week 1 - Simple family plan"
            class="mb-5 w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:border-transparent focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] sm:mb-6"
            autocomplete="off"
          />

          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <button
              @click="showSaveDialog = false"
              class="rounded-lg border-2 border-gray-300 bg-white px-6 py-3 font-medium text-gray-700 transition-colors hover:bg-gray-50"
              type="button"
            >
              Cancel
            </button>

            <button
              @click="savePlan"
              :disabled="!planName.trim() || isSaving"
              class="rounded-lg bg-[#A8D5BA] px-6 py-3 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50"
              type="button"
            >
              {{ isSaving ? 'Saving...' : 'Save Plan' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  ArrowLeft,
  ChefHat,
  CalendarDays,
  Leaf,
  BookmarkPlus,
  RefreshCw,
  CalendarCheck,
  Clock,
  AlertCircle,
  BookOpen,
  Sparkles,
} from 'lucide-vue-next';
import {
  getChildren,
  getRecommendedProducts,
  getFamilyRecommendedProducts,
  getChildMealRecommendations,
  getMealRecipeDetail,
  createWeeklyPlan,
  getWeeklyPlanById,
  generateWeeklyPlanFromBackend,
} from '../services/api';

const router = useRouter();
const route = useRoute();

const profiles = ref([]);
const selectedChildren = ref([]);
const cookingFrequency = ref(null);
const varietyPreference = ref('Balanced');
const mealStyle = ref('Mix of simple and varied');

const planGenerated = ref(false);
const showSaveDialog = ref(false);
const planName = ref('');
const weeklyBatches = ref([]);

const databaseLunchboxes = ref([]);
const apiRecipes = ref([]);

const isLoading = ref(false);
const isGenerating = ref(false);
const isSaving = ref(false);
const errorMessage = ref('');

const frequencyOptions = [
  {
    value: 2,
    label: '2 times per week',
    description: 'Cook less, reuse more',
    activeClass: 'border-[#A8D5BA] bg-[#A8D5BA]/10',
    iconClass: 'bg-[#A8D5BA]',
    iconTextClass: 'text-white',
  },
  {
    value: 3,
    label: '3 times per week',
    description: 'Balanced between variety and effort',
    activeClass: 'border-[#F7B267] bg-[#F7B267]/10',
    iconClass: 'bg-[#F7B267]',
    iconTextClass: 'text-white',
  },
  {
    value: 5,
    label: '5 times per week',
    description: 'More variety, more fresh meals',
    activeClass: 'border-[#CDE7F0] bg-[#CDE7F0]/20',
    iconClass: 'bg-[#CDE7F0]',
    iconTextClass: 'text-[#1B4965]',
  },
];

const allergenIdToName = {
  47: 'Peanuts',
  40: 'Tree nuts',
  16: 'Milk',
  18: 'Eggs',
  24: 'Wheat',
  50: 'Soy',
  22: 'Fish',
  15: 'Shellfish',
};

const nutritionFocusLabels = {
  iron: 'Iron Support',
  calcium: 'Calcium Support',
  vitamin_d: 'Vitamin D Support',
  immunity: 'Immune Support',
  variety: 'Diet Variety',
};

const allowedAgeGroups = ['5-6 years', '7-9 years', '10-12 years'];

const normalizeAgeGroup = (ageGroup) => {
  const mapping = {
    '5-6 years': '5-6 years',
    '7-9 years': '7-9 years',
    '10-12 years': '10-12 years',

    '3-6 years': '5-6 years',
    '6-9 years': '7-9 years',
    '9-12 years': '10-12 years',
    '12+ years': '10-12 years',
    '4-8': '7-9 years',
    '9-13': '10-12 years',

    '0-3 years': '',
    '2-3': '',
    '14-18': '',
  };

  return mapping[ageGroup] || '';
};

const isActiveStatus = (value) => {
  return value === 1 || value === '1' || value === true;
};

const toNullableInteger = (value) => {
  if (value === null || value === undefined || value === '') {
    return null;
  }

  const number = Number(value);
  return Number.isInteger(number) ? number : null;
};

const parseTags = (tags) => {
  if (Array.isArray(tags)) return tags;
  if (!tags) return [];

  return String(tags)
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean);
};

const mapAllergiesToNames = (allergies) => {
  if (!Array.isArray(allergies)) return [];

  return allergies.map((allergy) => {
    if (typeof allergy === 'string' && Number.isNaN(Number(allergy))) return allergy;
    const id = Number(allergy);
    return allergenIdToName[id] || String(allergy);
  });
};

const mapStatusToNutritionFocus = (child) => {
  return [
    isActiveStatus(child.iron_status) ? 'iron' : null,
    isActiveStatus(child.calcium_status) ? 'calcium' : null,
    isActiveStatus(child.vitamin_d_status) ? 'vitamin_d' : null,
    isActiveStatus(child.variety_status) ? 'variety' : null,
  ].filter(Boolean);
};

const mapChildToProfileCard = (child) => {
  const focusIds = mapStatusToNutritionFocus(child);
  const normalizedAgeGroup = normalizeAgeGroup(child.age_band);

  return {
    id: child.child_id,
    name: child.child_name,
    ageGroup: normalizedAgeGroup,
    originalAgeGroup: child.age_band,
    isSupportedAge: allowedAgeGroups.includes(normalizedAgeGroup),
    allergies: mapAllergiesToNames(child.allergies),
    dietaryRestriction: child.restriction_name || '',
    restrictionId: child.restriction_id || null,
    restrictionCode: child.restriction_code || '',
    nutritionFocus: focusIds.map((id) => nutritionFocusLabels[id]).filter(Boolean),
  };
};

const getCurrentSeason = () => {
  const month = new Date().getMonth();

  if (month >= 8 && month <= 10) return 'spring';
  if (month === 11 || month === 0 || month === 1) return 'summer';
  if (month >= 2 && month <= 4) return 'autumn';

  return 'winter';
};

const getSeasonIcon = () => {
  return getCurrentSeason() === 'spring' ? Leaf : Sparkles;
};

const getSeasonName = () => {
  const names = {
    spring: 'Spring',
    summer: 'Summer',
    autumn: 'Autumn',
    winter: 'Winter',
  };

  return names[getCurrentSeason()];
};

const getSeasonId = () => {
  const seasonMap = {
    spring: 1,
    summer: 2,
    autumn: 3,
    winter: 4,
  };

  return seasonMap[getCurrentSeason()] || null;
};

const getSectionColor = (section) => {
  const colors = {
    carbs: 'bg-[#F7B267]',
    protein: 'bg-[#A8D5BA]',
    veggies: 'bg-[#8BC34A]',
    fruit: 'bg-[#FF6B9D]',
    snack: 'bg-[#CDE7F0]',
    ingredient: 'bg-[#CDE7F0]',
  };

  return colors[section] || 'bg-gray-300';
};

const normalizeDatabaseLunchbox = (lunchbox, index = 0) => {
  const items = Array.isArray(lunchbox.items) ? lunchbox.items : [];

  const rawReferenceFoodId =
    lunchbox.reference_food_id ||
    lunchbox.referenceFoodId ||
    lunchbox.product_id ||
    lunchbox.food_id ||
    lunchbox.reference_id ||
    null;

  const referenceFoodId = toNullableInteger(rawReferenceFoodId);

  return {
    id: referenceFoodId || lunchbox.lunchbox_id || `db-${index}`,
    reference_food_id: referenceFoodId,
    title: lunchbox.title || lunchbox.mealName || lunchbox.name || 'Database Lunchbox',
    source: lunchbox.source || 'database',
    category: lunchbox.category || '',
    childName: lunchbox.childName || '',
    supportType: lunchbox.supportType || 'general',
    nutritionFocus: parseTags(lunchbox.nutritionFocus),
    whyThisMeal: lunchbox.whyThisMeal || '',
    items:
      items.length > 0
        ? items.map((item) => ({
            reference_food_id: toNullableInteger(
              item.reference_food_id ||
                item.referenceFoodId ||
                item.product_id ||
                item.food_id ||
                item.reference_id ||
                item.id ||
                null
            ),
            name: item.name || item.product_name || item.title || item.food_name || 'Food item',
            amount: item.amount || item.serving || item.quantity || item.serving_size || 'Recommended item',
            section: item.section || item.type || 'ingredient',
          }))
        : [
            {
              reference_food_id: referenceFoodId,
              name: lunchbox.title || lunchbox.mealName || lunchbox.name || 'Recommended item',
              amount: lunchbox.amount || lunchbox.serving || 'Recommended item',
              section: lunchbox.section || lunchbox.type || 'ingredient',
            },
          ],
  };
};

const normalizeApiRecipe = (meal, index = 0) => {
  const id = meal.id || meal.idMeal || meal.recipe_id || meal.recipeId || `recipe-${index}`;

  return {
    id,
    source: 'mealdb',
    title: meal.title || meal.mealName || meal.strMeal || 'Recipe Inspiration',
    image: meal.heroImage || meal.mealImage || meal.strMealThumb || meal.image_url || '',
    category: meal.category || meal.strCategory || '',
    area: meal.area || meal.strArea || '',
    childName: meal.childName || '',
    nutritionFocus: parseTags(meal.nutritionFocus),
    whyThisMeal: meal.whyThisMeal || '',
  };
};

const normalizeSavedMeal = (meal, index = 0) => {
  const lunchbox = normalizeDatabaseLunchbox(
    meal.lunchbox || {
      reference_food_id: meal.reference_food_id,
      id: meal.reference_food_id,
      title: meal.meal_title || meal.mealName,
      items: meal.items || meal.lunchbox_items || [],
      nutritionFocus: meal.nutrition_tags || meal.tags,
      whyThisMeal: meal.why_this_meal || meal.whyThisMeal,
    },
    index
  );

  const recipe = normalizeApiRecipe(
    meal.recipe || {
      id: meal.recipe_id,
      title:
        meal.recipe_title ||
        meal.recipeName ||
        meal.recipe?.title ||
        (meal.recipe_id ? `Recipe #${meal.recipe_id}` : ''),
      image_url: meal.image_url,
      category: meal.category,
      area: meal.area,
      nutritionFocus: meal.recipe_tags || meal.nutrition_tags,
      whyThisMeal: meal.recipe_note || meal.whyThisMeal,
    },
    index
  );

  return {
    id: meal.meal_id || meal.id || `saved-${index}`,
    cookDay: meal.cook_day || meal.cookDay || meal.title || `Cook Session ${index + 1}`,
    coverDays: meal.cover_days || meal.coverDays || meal.covers || 'Selected days',
    prepTime: meal.prep_time_minutes ? `${meal.prep_time_minutes} mins` : meal.prepTime || '30 mins',
    seasonalNote: meal.seasonal_note || meal.seasonalNote || 'Selected with seasonal ingredients.',
    storageTip: meal.storage_tip || meal.storageTip || 'Store safely in the fridge and keep chilled.',
    lunchbox,
    recipe,
  };
};

const hydrateSavedRecipes = async () => {
  const updatedBatches = await Promise.all(
    weeklyBatches.value.map(async (batch) => {
      const recipeId = batch.recipe?.id;

      const titleLooksLikeCode =
        !batch.recipe?.title ||
        String(batch.recipe.title).startsWith('Recipe #') ||
        String(batch.recipe.title) === 'Recipe Inspiration';

      if (!recipeId || !titleLooksLikeCode) {
        return batch;
      }

      try {
        const detail = await getMealRecipeDetail(recipeId, batch.recipe?.childName || '');
        const normalizedRecipe = normalizeApiRecipe(detail);

        return {
          ...batch,
          recipe: {
            ...batch.recipe,
            ...normalizedRecipe,
          },
        };
      } catch (error) {
        console.error('Failed to hydrate saved recipe:', error);
        return batch;
      }
    })
  );

  weeklyBatches.value = updatedBatches;

  apiRecipes.value = dedupeByKey(
    weeklyBatches.value
      .map((batch) => batch.recipe)
      .filter((recipe) => recipe?.id)
  ).map(normalizeApiRecipe);
};

const dedupeByKey = (items) => {
  const map = new Map();

  for (const item of items) {
    const key = item?.id || item?.idMeal || item?.title || item?.mealName || item?.name;
    if (!key) continue;
    if (!map.has(String(key))) map.set(String(key), item);
  }

  return Array.from(map.values());
};

const getCoverText = (frequency, index) => {
  const covers = {
    2: ['Monday to Wednesday', 'Thursday to Friday'],
    3: ['Monday to Tuesday', 'Wednesday to Thursday', 'Friday'],
    5: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
  };

  return covers[frequency]?.[index] || 'Selected days';
};

const getCookTitle = (frequency, index) => {
  const titles = {
    2: ['Cook on Sunday', 'Cook on Wednesday'],
    3: ['Cook on Sunday', 'Cook on Tuesday', 'Cook on Thursday'],
    5: ['Cook on Monday', 'Cook on Tuesday', 'Cook on Wednesday', 'Cook on Thursday', 'Cook on Friday'],
  };

  return titles[frequency]?.[index] || `Cook Session ${index + 1}`;
};

const getCookDayForDatabase = (cookDayText, index) => {
  const text = String(cookDayText || '').toLowerCase();

  const validDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const matchedDay = validDays.find((day) => text.includes(day.toLowerCase()));

  if (matchedDay) return matchedDay;

  const fallbackDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  return fallbackDays[index % fallbackDays.length];
};

const getCoveredDayCount = (coverDays) => {
  const text = String(coverDays || '').toLowerCase().trim();

  if (text.includes('monday to wednesday')) return 3;
  if (text.includes('thursday to friday')) return 2;
  if (text.includes('monday to tuesday')) return 2;
  if (text.includes('wednesday to thursday')) return 2;

  const singleDays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'];
  if (singleDays.includes(text)) return 1;

  return 1;
};

const formatWeeklyItemAmount = (amount, coverDays) => {
  if (!amount) return 'Recommended item';

  const childCount = selectedChildren.value.length || 1;
  const coveredDayCount = getCoveredDayCount(coverDays);
  const totalPortions = childCount * coveredDayCount;

  if (String(amount).toLowerCase().includes('child-friendly portion')) {
    return `${totalPortions} child-friendly ${totalPortions === 1 ? 'portion' : 'portions'}`;
  }

  return amount;
};

const buildWeeklyBatches = (lunchboxes, recipes) => {
  const count = cookingFrequency.value || 2;

  const safeLunchboxes =
    lunchboxes.length > 0
      ? lunchboxes
      : [normalizeDatabaseLunchbox({ title: 'Balanced Lunchbox', items: [] })];

  const safeRecipes =
    recipes.length > 0
      ? recipes
      : [normalizeApiRecipe({ title: 'Recipe Inspiration' })];

  return Array.from({ length: count }, (_, index) => {
    const lunchbox = safeLunchboxes[index % safeLunchboxes.length];
    const recipe = safeRecipes[index % safeRecipes.length];

    return {
      id: `batch-${Date.now()}-${index}`,
      cookDay: getCookTitle(count, index),
      coverDays: getCoverText(count, index),
      prepTime: count === 5 ? '20 mins' : count === 3 ? '30 mins' : '40 mins',
      seasonalNote: `${getSeasonName()} ingredients are prioritised where available.`,
      storageTip:
        count === 5
          ? 'Prepare fresh and keep chilled until lunch.'
          : 'Cook in batch, portion safely, and store in the fridge.',
      lunchbox,
      recipe,
    };
  });
};

const getReferenceFoodId = (batch) => {
  const possibleId =
    batch.lunchbox.reference_food_id ||
    batch.lunchbox.referenceFoodId ||
    batch.lunchbox.items?.[0]?.reference_food_id ||
    batch.lunchbox.items?.[0]?.referenceFoodId ||
    batch.lunchbox.items?.[0]?.product_id ||
    batch.lunchbox.items?.[0]?.food_id ||
    batch.lunchbox.items?.[0]?.id ||
    batch.lunchbox.product_id ||
    batch.lunchbox.food_id ||
    batch.lunchbox.id ||
    null;

  return toNullableInteger(possibleId);
};

const normalizeLunchboxItemsForSave = (items) => {
  if (!Array.isArray(items)) return [];

  return items.map((item) => ({
    reference_food_id: toNullableInteger(
      item.reference_food_id ||
        item.referenceFoodId ||
        item.product_id ||
        item.food_id ||
        item.reference_id ||
        item.id ||
        null
    ),
    name: item.name || item.product_name || item.title || item.food_name || 'Food item',
    amount: item.amount || item.serving || item.quantity || item.serving_size || 'Recommended item',
    section: item.section || item.type || 'ingredient',
  }));
};

const loadChildren = async () => {
  const children = await getChildren();

  const mappedProfiles = Array.isArray(children)
    ? children.map(mapChildToProfileCard)
    : [];

  profiles.value = mappedProfiles.filter((profile) => profile.isSupportedAge);
};

const loadExistingPlan = async (planId) => {
  const plan = await getWeeklyPlanById(planId);

  planName.value = plan.plan_name || plan.name || '';
  cookingFrequency.value = plan.cook_frequency || plan.cookingFrequency || 2;
  varietyPreference.value = plan.variety_preference || plan.varietyPreference || 'Balanced';
  mealStyle.value = plan.meal_style || plan.mealStyle || 'Mix of simple and varied';

  if (Array.isArray(plan.children)) {
    selectedChildren.value = plan.children
      .map((child) => Number(child.child_id || child.id || child))
      .filter(Boolean);
  } else if (Array.isArray(plan.child_ids)) {
    selectedChildren.value = plan.child_ids.map(Number).filter(Boolean);
  } else if (plan.child_id) {
    selectedChildren.value = [Number(plan.child_id)].filter(Boolean);
  }

  const meals = plan.meals || plan.batches || [];
  weeklyBatches.value = Array.isArray(meals) ? meals.map(normalizeSavedMeal) : [];

  databaseLunchboxes.value = weeklyBatches.value
    .map((batch) => batch.lunchbox)
    .filter(Boolean);

  apiRecipes.value = dedupeByKey(
    weeklyBatches.value
      .map((batch) => batch.recipe)
      .filter((recipe) => recipe?.id)
  ).map(normalizeApiRecipe);

  planGenerated.value = weeklyBatches.value.length > 0;

  if (planGenerated.value) {
    await hydrateSavedRecipes();
  }
};

onMounted(async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';

    await loadChildren();

    const childIds = route.query.childIds;
    if (childIds) {
      const queryChildIds = String(childIds)
        .split(',')
        .map((id) => Number(id))
        .filter(Boolean);

      const supportedProfileIds = profiles.value.map((profile) => Number(profile.id));

      selectedChildren.value = queryChildIds.filter((id) =>
        supportedProfileIds.includes(Number(id))
      );
    }

    const planId = route.query.planId;
    if (planId) {
      await loadExistingPlan(planId);
    }
  } catch (error) {
    console.error('Failed to initialise weekly plan page:', error);
    errorMessage.value = error.message || 'Failed to load weekly plan data.';
  } finally {
    isLoading.value = false;
  }
});

const toggleChildSelection = (id) => {
  if (selectedChildren.value.includes(id)) {
    selectedChildren.value = selectedChildren.value.filter((childId) => childId !== id);
  } else {
    selectedChildren.value = [...selectedChildren.value, id];
  }
};

const fetchLunchboxesFromDatabase = async () => {
  if (selectedChildren.value.length === 1) {
    const data = await getRecommendedProducts(selectedChildren.value[0], true);
    return Array.isArray(data) ? data : data.lunchboxes || [];
  }

  const data = await getFamilyRecommendedProducts(selectedChildren.value, true);
  return Array.isArray(data) ? data : data.lunchboxes || [];
};

const fetchRecipesFromApi = async () => {
  const results = await Promise.all(
    selectedChildren.value.map((childId) => getChildMealRecommendations(childId))
  );

  const merged = results.flatMap((res) =>
    Array.isArray(res?.lunchboxes) ? res.lunchboxes : []
  );

  return dedupeByKey(merged);
};

const generateWeeklyPlan = async () => {
  try {
    isGenerating.value = true;
    errorMessage.value = '';

    const data = await generateWeeklyPlanFromBackend({
      child_ids: selectedChildren.value,
      cook_frequency: cookingFrequency.value,
      variety_preference: varietyPreference.value,
      meal_style: mealStyle.value,
      season_id: getSeasonId(),
      seasonal: true,
    });

    const batches = Array.isArray(data?.batches) ? data.batches : [];

    weeklyBatches.value = batches.map((batch, index) => ({
      id: batch.id || `batch-${Date.now()}-${index}`,
      cookDay: batch.cookDay || `Cook Session ${index + 1}`,
      coverDays: batch.coverDays || 'Selected days',
      prepTime: batch.prepTime || '30 mins',
      seasonalNote: batch.seasonalNote || `${getSeasonName()} ingredients are prioritised where available.`,
      storageTip: batch.storageTip || 'Store safely in the fridge and keep chilled.',
      lunchbox: normalizeDatabaseLunchbox(batch.lunchbox || {}, index),
      recipe: normalizeApiRecipe(batch.recipe || {}, index),
    }));

    databaseLunchboxes.value = weeklyBatches.value
      .map((batch) => batch.lunchbox)
      .filter(Boolean);

    apiRecipes.value = weeklyBatches.value
      .map((batch) => batch.recipe)
      .filter((recipe) => recipe?.id);

    planGenerated.value = weeklyBatches.value.length > 0;

    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (error) {
    console.error('Failed to generate weekly plan:', error);
    errorMessage.value = error.message || 'Failed to generate weekly plan.';
  } finally {
    isGenerating.value = false;
  }
};

const regeneratePlan = () => {
  planGenerated.value = false;
  weeklyBatches.value = [];
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const swapApiRecipe = async (index) => {
  try {
    errorMessage.value = '';

    if (selectedChildren.value.length === 0) {
      errorMessage.value = 'Cannot swap recipe because no child profile is linked to this plan.';
      return;
    }

    const currentId = weeklyBatches.value[index]?.recipe?.id;

    const currentWeekRecipeIds = weeklyBatches.value
      .map((batch) => batch.recipe?.id)
      .filter(Boolean)
      .map((id) => String(id));

    const freshApiData = await fetchRecipesFromApi();
    const freshRecipes = freshApiData.map(normalizeApiRecipe);

    const replacement =
      freshRecipes.find((recipe) => {
        const recipeId = String(recipe.id);
        return recipeId !== String(currentId) && !currentWeekRecipeIds.includes(recipeId);
      }) ||
      freshRecipes.find((recipe) => String(recipe.id) !== String(currentId));

    if (!replacement) {
      errorMessage.value = 'No new recipe available right now. Please try again.';
      return;
    }

    apiRecipes.value = dedupeByKey([
      ...apiRecipes.value,
      ...freshRecipes,
    ]).map(normalizeApiRecipe);

    weeklyBatches.value[index] = {
      ...weeklyBatches.value[index],
      recipe: replacement,
    };
  } catch (error) {
    console.error('Failed to swap recipe:', error);
    errorMessage.value = error.message || 'Failed to swap recipe. Please try again.';
  }
};

const handleImageError = (event) => {
  event.target.style.display = 'none';
};

const openRecipe = (recipe) => {
  if (!recipe?.id) return;

  const recipeBaseChildId = selectedChildren.value[0] || '';

  const selectedProfile = profiles.value.find(
    (profile) => String(profile.id) === String(recipeBaseChildId)
  );

  router.push({
    path: `/recipe/${encodeURIComponent(recipe.id)}`,
    query: {
      childId: recipeBaseChildId,
      childName: selectedProfile?.name || recipe.childName || '',
      source: 'mealdb',
      from: 'weekly-plan',
    },
  });
};

const toMinutes = (prepTime) => {
  const number = parseInt(String(prepTime || '').replace(/\D/g, ''), 10);
  return Number.isFinite(number) ? number : null;
};

const savePlan = async () => {
  if (!planName.value.trim()) return;

  const payload = {
    plan_name: planName.value.trim(),
    child_ids: selectedChildren.value,
    cook_frequency: cookingFrequency.value,
    variety_preference: varietyPreference.value,
    meal_style: mealStyle.value,
    season_id: getSeasonId(),
    status: 'active',

    meals: weeklyBatches.value.map((batch, index) => ({
      reference_food_id: getReferenceFoodId(batch),
      cook_day: getCookDayForDatabase(batch.cookDay, index),
      cover_days: batch.coverDays,
      meal_title: batch.lunchbox.title,

      lunchbox_items: normalizeLunchboxItemsForSave(batch.lunchbox.items),

      servings: selectedChildren.value.length || 1,
      prep_time_minutes: toMinutes(batch.prepTime),
      nutrition_tags: Array.isArray(batch.lunchbox.nutritionFocus)
        ? batch.lunchbox.nutritionFocus.join(',')
        : '',
      seasonal_note: batch.seasonalNote,
      storage_tip: batch.storageTip,
      recipe_id: toNullableInteger(batch.recipe.id),
      image_url: batch.recipe.image || null,
    })),
  };

  try {
    isSaving.value = true;
    errorMessage.value = '';

    await createWeeklyPlan(payload);

    showSaveDialog.value = false;
    planName.value = '';
    router.push('/my-plans');
  } catch (error) {
    console.error('Failed to save weekly plan:', error);
    errorMessage.value = error.message || 'Failed to save weekly plan. Please try again.';
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>