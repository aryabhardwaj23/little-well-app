<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-4xl px-4 sm:px-6">
      <!-- Header -->
      <header class="mb-8 text-center sm:mb-12">
        <div
          class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] sm:h-16 sm:w-16"
          aria-hidden="true"
        >
          <Check class="h-7 w-7 text-white sm:h-8 sm:w-8" />
        </div>

        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          Profile Complete!
        </h1>

        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          Here's a summary of {{ childName }}'s profile
        </p>
      </header>

      <!-- Loading -->
      <div
        v-if="loading"
        class="mb-6 rounded-2xl bg-white p-6 text-center text-sm text-muted-foreground shadow-sm sm:mb-8 sm:p-8 sm:text-base"
        aria-live="polite"
        aria-busy="true"
      >
        Loading profile...
      </div>

      <!-- Profile Summary Card -->
      <section v-else class="mb-6 rounded-2xl bg-white p-5 shadow-sm sm:mb-8 sm:p-8">
        <!-- Basic Info -->
        <div class="mb-7 sm:mb-8">
          <h2 class="mb-5 flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:mb-6 sm:text-2xl">
            <User class="h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" aria-hidden="true" />
            Basic Information
          </h2>

          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6">
            <div class="rounded-xl bg-[#FAF9F6] p-4">
              <p class="mb-1 text-xs text-muted-foreground sm:text-sm">Name</p>
              <p class="text-base font-semibold text-[#111827] sm:text-lg">
                {{ profile.name || '-' }}
              </p>
            </div>

            <div class="rounded-xl bg-[#FAF9F6] p-4">
              <p class="mb-1 text-xs text-muted-foreground sm:text-sm">Age Group</p>
              <p class="text-base font-semibold text-[#111827] sm:text-lg">
                {{ profile.ageGroup || '-' }}
              </p>
            </div>

            <div v-if="profile.gender" class="rounded-xl bg-[#FAF9F6] p-4">
              <p class="mb-1 text-xs text-muted-foreground sm:text-sm">Gender</p>
              <p class="text-base font-semibold text-[#111827] sm:text-lg">
                {{ profile.gender }}
              </p>
            </div>

            <div class="rounded-xl bg-[#FAF9F6] p-4">
              <p class="mb-1 text-xs text-muted-foreground sm:text-sm">Activity Level</p>
              <p class="text-base font-semibold capitalize text-[#111827] sm:text-lg">
                {{ profile.activityLevel || 'Moderate' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Dietary Information -->
        <div class="mb-7 border-t pt-7 sm:mb-8 sm:pt-8">
          <h2 class="mb-5 flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:mb-6 sm:text-2xl">
            <Apple class="h-5 w-5 text-[#F7B267] sm:h-6 sm:w-6" aria-hidden="true" />
            Dietary Information
          </h2>

          <div class="space-y-5">
            <div>
              <p class="mb-2 text-sm text-muted-foreground">Food Allergies</p>

              <div v-if="profile.allergies && profile.allergies.length > 0" class="flex flex-wrap gap-2">
                <span
                  v-for="allergy in profile.allergies"
                  :key="allergy"
                  class="rounded-full bg-[#F7B267]/20 px-3 py-1 text-sm text-[#8B4513]"
                >
                  {{ allergy }}
                </span>
              </div>

              <p v-else class="text-base text-[#111827]">
                No allergies selected
              </p>
            </div>

            <div>
              <p class="mb-2 text-sm text-muted-foreground">Dietary Restriction</p>

              <span
                v-if="profile.dietaryRestriction"
                class="inline-flex rounded-full bg-[#CDE7F0]/30 px-3 py-1 text-sm text-[#1B4965]"
              >
                {{ profile.dietaryRestriction }}
              </span>

              <p v-else class="text-base text-[#111827]">
                No restrictions
              </p>
            </div>

            <div v-if="profile.eatingHabit">
              <p class="mb-2 text-sm text-muted-foreground">Eating Habits</p>
              <p class="text-base leading-relaxed text-[#111827]">
                {{ profile.eatingHabit }}
              </p>
            </div>
          </div>
        </div>

        <!-- Nutrition Focus -->
        <div class="border-t pt-7 sm:pt-8">
          <h2 class="mb-5 flex items-center gap-2 text-xl font-semibold text-[#2C5F2D] sm:mb-6 sm:text-2xl">
            <Sparkles class="h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" aria-hidden="true" />
            Nutrition Focus Areas
          </h2>

          <div v-if="nutritionFocus && nutritionFocus.length > 0" class="flex flex-wrap gap-2 sm:gap-3">
            <span
              v-for="focus in nutritionFocus"
              :key="focus"
              class="rounded-full bg-[#A8D5BA]/20 px-3 py-1.5 text-sm text-[#2C5F2D] sm:px-4 sm:py-2"
            >
              {{ getNutritionAreaName(focus) }}
            </span>
          </div>

          <p v-else class="text-sm leading-relaxed text-muted-foreground sm:text-base">
            No focus areas selected.
          </p>
        </div>
      </section>

      <!-- Action Buttons -->
      <div class="flex flex-col-reverse gap-3 sm:flex-row sm:gap-4">
        <button
          @click="handleEdit"
          :disabled="saving || loading"
          class="inline-flex w-full flex-1 items-center justify-center gap-2 rounded-lg border-2 border-[#A8D5BA] bg-white px-8 py-3.5 font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10 disabled:cursor-not-allowed disabled:opacity-50 sm:py-4"
          type="button"
        >
          <Edit class="h-4 w-4" aria-hidden="true" />
          Edit Profile
        </button>

        <button
          @click="handleSave"
          :disabled="saving || loading"
          class="inline-flex w-full flex-1 items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3.5 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50 sm:py-4"
          type="button"
        >
          <Check class="h-4 w-4" aria-hidden="true" />
          {{ saving ? 'Saving...' : 'Save & View Lunchboxes' }}
        </button>
      </div>

      <!-- Nutrition Check Prompt -->
      <section class="mt-6 rounded-2xl border border-[#A8D5BA]/30 bg-gradient-to-r from-[#CDE7F0]/30 to-[#A8D5BA]/20 p-5 sm:mt-8 sm:p-6">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-start">
          <div
            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-white sm:h-12 sm:w-12"
            aria-hidden="true"
          >
            <ClipboardCheck class="h-5 w-5 text-[#2C5F2D] sm:h-6 sm:w-6" />
          </div>

          <div class="flex-1">
            <h3 class="mb-2 text-lg font-semibold text-[#2C5F2D]">
              Want more personalized suggestions?
            </h3>

            <p class="mb-4 text-sm leading-relaxed text-muted-foreground">
              Take our quick nutrition check to get even more tailored meal recommendations based on your child's current diet.
            </p>

            <button
              @click="handleNutritionCheck"
              :disabled="saving || loading"
              class="inline-flex w-full items-center justify-center gap-1 rounded-lg bg-white px-4 py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:bg-transparent sm:px-0 sm:py-0 sm:hover:underline"
              type="button"
            >
              Take Nutrition Check
              <ChevronRight class="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  Check,
  User,
  Apple,
  Sparkles,
  Edit,
  ChevronRight,
  ClipboardCheck,
} from 'lucide-vue-next';
import { useChildProfileStore } from '../stores/childProfile';
import { createChild, updateChild, getChildById } from '../services/api';

const router = useRouter();
const route = useRoute();
const childProfileStore = useChildProfileStore();

const childName = ref('your child');
const profile = ref({});
const nutritionFocus = ref([]);
const saving = ref(false);
const loading = ref(false);

const allowedAgeGroups = ['5-6 years', '7-9 years', '10-12 years'];

const nutritionAreaNames = {
  iron: 'Iron Support',
  calcium: 'Calcium & Bone Health',
  brain: 'Brain Development',
  immunity: 'Immune Support',
  vitamin_d: 'Vitamin D Support',
  energy: 'Sustained Energy',
  variety: 'Diet Variety',
};

const allergyMap = {
  Peanuts: 47,
  'Tree nuts': 40,
  Milk: 16,
  Eggs: 18,
  Wheat: 24,
  Soy: 50,
  Fish: 22,
  Shellfish: 15,
};

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

const dietaryRestrictionOptions = [
  { label: 'Vegan', value: 1 },
  { label: 'Vegetarian', value: 2 },
  { label: 'Pescatarian', value: 3 },
  { label: 'Halal', value: 4 },
  { label: 'Kosher', value: 5 },
  { label: 'Coeliac Disease', value: 6 },
  { label: 'Lactose Intolerance', value: 7 },
  { label: 'Gluten Free', value: 8 },
];

const normalizeAgeGroup = (ageGroup) => {
  const mapping = {
    '5-6 years': '5-6 years',
    '7-9 years': '7-9 years',
    '10-12 years': '10-12 years',

    // Old values compatibility
    '3-6 years': '5-6 years',
    '6-9 years': '7-9 years',
    '9-12 years': '10-12 years',
    '12+ years': '10-12 years',
    '4-8': '7-9 years',
    '9-13': '10-12 years',
  };

  return mapping[ageGroup] || '';
};

const isActiveStatus = (value) => {
  return value === 1 || value === '1' || value === true;
};

const mapAllergiesToNames = (allergies) => {
  if (!Array.isArray(allergies)) return [];

  return allergies
    .map((allergy) => {
      if (typeof allergy === 'string' && Number.isNaN(Number(allergy))) {
        return allergy;
      }

      return allergenIdToName[Number(allergy)] || null;
    })
    .filter(Boolean);
};

const getRestrictionLabelById = (restrictionId, fallback = '') => {
  const option = dietaryRestrictionOptions.find(
    (item) => String(item.value) === String(restrictionId),
  );

  return option?.label || fallback || '';
};

const mapStatusToNutritionFocus = (child) => {
  return [
    isActiveStatus(child.iron_status) ? 'iron' : null,
    isActiveStatus(child.calcium_status) ? 'calcium' : null,
    isActiveStatus(child.vitamin_d_status) ? 'immunity' : null,
    isActiveStatus(child.variety_status) ? 'variety' : null,
  ].filter(Boolean);
};

const getActiveChildId = () => {
  return (
    route.query.childId ||
    localStorage.getItem('littlewell_active_child_id') ||
    localStorage.getItem('littlewell_edit_child_id') ||
    ''
  );
};

const mapChildToProfile = (child) => {
  return {
    name: child.child_name || '',
    ageGroup: normalizeAgeGroup(child.age_band),
    gender: child.gender || '',
    allergies: mapAllergiesToNames(child.allergies),
    restrictionId: child.restriction_id || null,
    dietaryRestriction: getRestrictionLabelById(
      child.restriction_id,
      child.restriction_name || '',
    ),
    activityLevel: child.activity_level || 'moderate',
    eatingHabit: child.eating_habit || '',
    nutritionFocus: mapStatusToNutritionFocus(child),
  };
};

const loadProfileFromChildId = async (childId) => {
  loading.value = true;

  try {
    const child = await getChildById(childId);
    const loadedProfile = mapChildToProfile(child);

    profile.value = loadedProfile;
    childName.value = loadedProfile.name || 'your child';
    nutritionFocus.value = loadedProfile.nutritionFocus || [];

    childProfileStore.updateDraft(loadedProfile);
    localStorage.setItem('littlewell_active_child_id', String(childId));
  } catch (error) {
    console.error('Failed to load child profile summary:', error);
  } finally {
    loading.value = false;
  }
};

const loadProfileFromDraft = () => {
  const draft = childProfileStore.childProfileDraft || {};
  const normalizedAgeGroup = normalizeAgeGroup(draft.ageGroup);

  profile.value = {
    ...draft,
    ageGroup: normalizedAgeGroup,
  };

  childName.value = draft.name || 'your child';
  nutritionFocus.value = draft.nutritionFocus || [];

  childProfileStore.updateDraft({
    ageGroup: normalizedAgeGroup,
  });
};

onMounted(async () => {
  const childId = getActiveChildId();

  if (childId) {
    await loadProfileFromChildId(childId);
    return;
  }

  loadProfileFromDraft();
});

const getNutritionAreaName = (id) => {
  return nutritionAreaNames[id] || id;
};

const handleEdit = () => {
  const childId = getActiveChildId();

  if (childId) {
    localStorage.setItem('littlewell_edit_child_id', String(childId));
  }

  router.push('/child-info');
};

const buildPayload = () => {
  const normalizedAgeGroup = normalizeAgeGroup(profile.value.ageGroup);

  if (!allowedAgeGroups.includes(normalizedAgeGroup)) {
    throw new Error('Please select a valid age group between 5 and 12 years old.');
  }

  return {
    child_name: profile.value.name || '',
    age_band: normalizedAgeGroup,
    band_id: null,

    iron_status: nutritionFocus.value.includes('iron') ? 1 : 0,
    calcium_status: nutritionFocus.value.includes('calcium') ? 1 : 0,
    vitamin_d_status:
      nutritionFocus.value.includes('immunity') || nutritionFocus.value.includes('vitamin_d')
        ? 1
        : 0,
    variety_status: nutritionFocus.value.includes('variety') ? 1 : 0,

    restriction_id: profile.value.restrictionId || null,

    allergies: (profile.value.allergies || [])
      .map((allergy) => allergyMap[allergy])
      .filter(Boolean),
  };
};

const saveProfile = async () => {
  const editingChildId = localStorage.getItem('littlewell_edit_child_id');
  const activeChildId = localStorage.getItem('littlewell_active_child_id');
  const routeChildId = route.query.childId || '';
  const existingChildId = routeChildId || editingChildId || activeChildId || '';

  const payload = buildPayload();

  let savedChildId = null;

  if (existingChildId) {
    await updateChild(existingChildId, payload);
    savedChildId = existingChildId;
  } else {
    const savedChild = await createChild(payload);

    savedChildId =
      savedChild?.child_id ||
      savedChild?.id ||
      savedChild?.child?.child_id ||
      savedChild?.child?.id ||
      null;
  }

  if (!savedChildId) {
    throw new Error('Profile was saved, but no child ID was returned.');
  }

  localStorage.setItem('littlewell_active_child_id', String(savedChildId));
  localStorage.removeItem('littlewell_edit_child_id');

  return String(savedChildId);
};

const handleSave = async () => {
  try {
    saving.value = true;
    const childId = await saveProfile();

    childProfileStore.resetDraft();
    router.push(`/results?childId=${childId}`);
  } catch (error) {
    console.error('Failed to save child profile:', error);
    alert(`Failed to save profile: ${error.message}`);
  } finally {
    saving.value = false;
  }
};

const handleNutritionCheck = async () => {
  try {
    saving.value = true;
    const childId = await saveProfile();

    childProfileStore.resetDraft();
    router.push(`/nutrition-check?childId=${childId}`);
  } catch (error) {
    console.error('Failed to save before nutrition check:', error);
    alert(`Failed to save profile: ${error.message}`);
  } finally {
    saving.value = false;
  }
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>