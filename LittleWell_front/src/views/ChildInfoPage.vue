<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="mx-auto w-full max-w-4xl px-4 sm:px-6">
      <!-- Back Button -->
      <button
        @click="router.push('/child-profile')"
        class="mb-5 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-white sm:mb-6 sm:px-4"
        type="button"
        aria-label="Go back to child profile"
      >
        <ArrowLeft class="h-4 w-4" aria-hidden="true" />
        Back
      </button>

      <!-- Header -->
      <header class="mb-7 text-center sm:mb-10 md:mb-12">
        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:text-4xl">
          Tell Us About Your Child
        </h1>
        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          LittleWell supports school-aged children from 5 to 12 years old.
        </p>
      </header>

      <!-- Form -->
      <div class="space-y-5 sm:space-y-8">
        <!-- Basic Info -->
        <section
          class="rounded-2xl bg-white p-5 shadow-sm sm:p-8"
          aria-label="Basic information"
        >
          <h2 class="mb-5 text-xl font-semibold text-[#2C5F2D] sm:mb-6 sm:text-2xl">
            Basic Information
          </h2>

          <div class="space-y-5 sm:space-y-6">
            <!-- Name -->
            <div>
              <label for="child-name" class="mb-2 block text-sm font-medium">
                Child's Name (or nickname)
              </label>
              <input
                id="child-name"
                v-model="formData.name"
                type="text"
                maxlength="20"
                placeholder="e.g. Emma"
                autocomplete="off"
                class="w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:border-transparent focus:outline-none focus:ring-2 focus:ring-[#A8D5BA]"
                @input="cleanNameInput"
                aria-describedby="child-name-hint"
              />
              <p id="child-name-hint" class="mt-1 text-xs leading-relaxed text-muted-foreground">
                Letters only, maximum 20 characters. We use nicknames only—no last names needed.
              </p>
            </div>

            <!-- Age Group -->
            <fieldset>
              <legend class="mb-2 block text-sm font-medium">Age</legend>
              <div
                class="grid grid-cols-1 gap-2 sm:grid-cols-3 sm:gap-3"
                role="group"
                aria-label="Select age group"
              >
                <button
                  v-for="age in ageGroups"
                  :key="age"
                  type="button"
                  @click="formData.ageGroup = age"
                  :aria-pressed="formData.ageGroup === age"
                  :class="[
                    'min-h-[48px] rounded-lg border-2 p-3 text-center text-sm font-medium transition-all sm:p-4 sm:text-base',
                    formData.ageGroup === age
                      ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                      : 'border-gray-200 hover:border-[#A8D5BA]/50'
                  ]"
                >
                  {{ age }}
                </button>
              </div>
              <p class="mt-2 text-xs leading-relaxed text-muted-foreground">
                This system is designed for children aged 5–12.
              </p>
            </fieldset>

            <!-- Gender -->
            <fieldset>
              <legend class="mb-2 block text-sm font-medium">Gender (optional)</legend>
              <div
                class="grid grid-cols-1 gap-2 sm:grid-cols-3 sm:gap-3"
                role="group"
                aria-label="Select gender"
              >
                <button
                  v-for="gender in genderOptions"
                  :key="gender"
                  type="button"
                  @click="formData.gender = gender"
                  :aria-pressed="formData.gender === gender"
                  :class="[
                    'min-h-[48px] rounded-lg border-2 p-3 text-sm font-medium transition-all sm:text-base',
                    formData.gender === gender
                      ? 'border-[#CDE7F0] bg-[#CDE7F0]/20 text-[#1B4965]'
                      : 'border-gray-200 hover:border-[#CDE7F0]/50'
                  ]"
                >
                  {{ gender }}
                </button>
              </div>
            </fieldset>
          </div>
        </section>

        <!-- Health Information -->
        <section
          class="rounded-2xl bg-white p-5 shadow-sm sm:p-8"
          aria-label="Health and dietary information"
        >
          <h2 class="mb-5 text-xl font-semibold text-[#2C5F2D] sm:mb-6 sm:text-2xl">
            Health & Dietary Information
          </h2>

          <div class="space-y-5 sm:space-y-6">
            <!-- Allergies -->
            <fieldset>
              <legend class="mb-1 block text-sm font-medium">Any food allergies?</legend>
              <p id="allergies-hint" class="mb-3 text-sm text-muted-foreground">
                Select all that apply
              </p>

              <div
                class="grid grid-cols-2 gap-2 sm:grid-cols-4"
                role="group"
                aria-describedby="allergies-hint"
              >
                <button
                  v-for="allergy in commonAllergies"
                  :key="allergy"
                  type="button"
                  @click="toggleAllergy(allergy)"
                  :aria-pressed="formData.allergies.includes(allergy)"
                  :class="[
                    'min-h-[46px] rounded-lg border-2 px-2 py-3 text-sm font-medium transition-all',
                    formData.allergies.includes(allergy)
                      ? 'border-[#F7B267] bg-[#F7B267]/10 text-[#8B4513]'
                      : 'border-gray-200 hover:border-[#F7B267]/50'
                  ]"
                >
                  {{ allergy }}
                </button>
              </div>
            </fieldset>

            <!-- Dietary Restrictions -->
            <div>
              <label for="dietary-restriction" class="mb-2 block text-sm font-medium">
                Any dietary restrictions? (optional)
              </label>
              <select
                id="dietary-restriction"
                v-model="formData.restrictionId"
                class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-base focus:border-transparent focus:outline-none focus:ring-2 focus:ring-[#A8D5BA]"
                aria-describedby="dietary-restriction-hint"
              >
                <option :value="null">No restrictions</option>
                <option
                  v-for="option in dietaryRestrictionOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
              <p
                id="dietary-restriction-hint"
                class="mt-1 text-xs leading-relaxed text-muted-foreground"
              >
                This is saved as restriction_id and matched with the dietary restriction database.
              </p>
            </div>

            <!-- Activity Level -->
            <fieldset>
              <legend class="mb-2 block text-sm font-medium">Activity level</legend>
              <p id="activity-hint" class="mb-3 text-sm leading-relaxed text-muted-foreground">
                Choose the option that best matches your child's usual daily activity.
              </p>

              <div
                class="grid grid-cols-1 gap-2 sm:grid-cols-3 sm:gap-3"
                role="group"
                aria-describedby="activity-hint"
              >
                <button
                  v-for="level in activityLevels"
                  :key="level.value"
                  type="button"
                  @click="formData.activityLevel = level.value"
                  :aria-pressed="formData.activityLevel === level.value"
                  :class="[
                    'rounded-lg border-2 p-4 text-left transition-all',
                    formData.activityLevel === level.value
                      ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                      : 'border-gray-200 hover:border-[#A8D5BA]/50'
                  ]"
                >
                  <div class="mb-2 text-2xl" aria-hidden="true">
                    {{ level.icon }}
                  </div>
                  <div class="mb-1 text-sm font-semibold">
                    {{ level.label }}
                  </div>
                  <div class="text-xs leading-relaxed text-muted-foreground">
                    {{ level.description }}
                  </div>
                </button>
              </div>
            </fieldset>
          </div>
        </section>

        <!-- Continue Button -->
        <div class="sticky bottom-0 z-20 -mx-4 bg-[#FAF9F6]/95 px-4 py-4 backdrop-blur sm:static sm:mx-0 sm:bg-transparent sm:px-0 sm:py-0 sm:backdrop-blur-0">
          <button
            @click="handleContinue"
            :disabled="!formData.name || !formData.ageGroup"
            class="w-full rounded-xl bg-[#A8D5BA] py-4 text-base font-semibold text-[#2C5F2D] shadow-sm transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50 sm:text-lg"
            type="button"
            :aria-disabled="!formData.name || !formData.ageGroup"
          >
            Continue to Nutrition Focus
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft } from 'lucide-vue-next';
import { useChildProfileStore } from '../stores/childProfile';
import { getChildById } from '../services/api';

const router = useRouter();
const childProfileStore = useChildProfileStore();

const formData = ref({
  name: '',
  ageGroup: '',
  gender: '',
  allergies: [],
  restrictionId: null,
  dietaryRestriction: '',
  activityLevel: 'moderate',
  eatingHabit: '',
  nutritionFocus: [],
});

const ageGroups = ['5-6 years', '7-9 years', '10-12 years'];
const genderOptions = ['Boy', 'Girl', 'Prefer not to say'];
const commonAllergies = ['Peanuts', 'Tree nuts', 'Milk', 'Eggs', 'Wheat', 'Soy', 'Fish', 'Shellfish'];

const dietaryRestrictionOptions = [
  { label: 'Vegan', value: 1, code: 'VEGAN' },
  { label: 'Vegetarian', value: 2, code: 'VEGETARIAN' },
  { label: 'Pescatarian', value: 3, code: 'PESCATARIAN' },
  { label: 'Halal', value: 4, code: 'HALAL' },
  { label: 'Kosher', value: 5, code: 'KOSHER' },
  { label: 'Coeliac Disease', value: 6, code: 'COELIAC' },
  { label: 'Lactose Intolerance', value: 7, code: 'LACTOSE_INT' },
  { label: 'Gluten Free', value: 8, code: 'GLUTEN_FREE' },
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

const activityLevels = [
  {
    value: 'low',
    label: 'Light',
    icon: '🚶',
    description: 'Mostly seated activities, light walking, or limited active play.',
  },
  {
    value: 'moderate',
    label: 'Moderate',
    icon: '🏃',
    description: 'Regular play, walking, school activities, or some sports during the week.',
  },
  {
    value: 'high',
    label: 'Active',
    icon: '⚡',
    description: 'Very active most days, with frequent sports, running, or high-energy play.',
  },
];

// Keep this data field for compatibility with the store/backend flow.
// It is intentionally not shown in the UI.
const eatingHabits = [
  'Eats almost everything',
  'Usually willing to try new foods',
  'Picky eater - prefers familiar foods',
  'Very selective - limited food preferences',
];

const isActiveStatus = (value) => value === 1 || value === '1' || value === true;

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
  };

  return mapping[ageGroup] || '';
};

const mapStatusToNutritionFocus = (child) =>
  [
    isActiveStatus(child.iron_status) ? 'iron' : null,
    isActiveStatus(child.calcium_status) ? 'calcium' : null,
    isActiveStatus(child.vitamin_d_status) ? 'immunity' : null,
    isActiveStatus(child.variety_status) ? 'variety' : null,
  ].filter(Boolean);

const mapAllergiesToNames = (allergies) => {
  if (!Array.isArray(allergies)) return [];

  return allergies
    .map((allergy) => {
      if (typeof allergy === 'string' && commonAllergies.includes(allergy)) {
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

const cleanNameInput = () => {
  formData.value.name = formData.value.name.replace(/[^A-Za-z\s]/g, '').slice(0, 20);
};

onMounted(async () => {
  const editingChildId = localStorage.getItem('littlewell_edit_child_id');

  if (editingChildId) {
    try {
      const child = await getChildById(editingChildId);

      const draftData = {
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

      childProfileStore.updateDraft(draftData);
      formData.value = JSON.parse(JSON.stringify(draftData));
    } catch (error) {
      console.error('Failed to load child info for editing:', error);
    }
  } else {
    const draft = childProfileStore.childProfileDraft || {};

    formData.value = {
      ...formData.value,
      ...draft,
      ageGroup: normalizeAgeGroup(draft.ageGroup) || '',
      restrictionId: draft.restrictionId || null,
      dietaryRestriction: draft.dietaryRestriction || '',
    };
  }
});

const toggleAllergy = (allergy) => {
  if (formData.value.allergies.includes(allergy)) {
    formData.value.allergies = formData.value.allergies.filter((a) => a !== allergy);
  } else {
    formData.value.allergies = [...formData.value.allergies, allergy];
  }
};

const handleContinue = () => {
  formData.value.ageGroup = normalizeAgeGroup(formData.value.ageGroup);
  formData.value.dietaryRestriction = getRestrictionLabelById(formData.value.restrictionId);

  childProfileStore.updateDraft(formData.value);
  router.push('/nutrition-needs');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>