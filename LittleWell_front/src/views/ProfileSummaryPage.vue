<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-4xl">
      <!-- Header -->
      <div class="text-center mb-12">
        <div class="w-16 h-16 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center mx-auto mb-4">
          <Check class="w-8 h-8 text-white" />
        </div>
        <h1 class="text-4xl mb-4">Profile Complete!</h1>
        <p class="text-lg text-muted-foreground">
          Here's a summary of {{ childName }}'s profile
        </p>
      </div>

      <!-- Profile Summary Card -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <!-- Basic Info -->
        <div class="mb-8">
          <h2 class="text-2xl mb-6 flex items-center gap-2">
            <User class="w-6 h-6 text-[#A8D5BA]" />
            Basic Information
          </h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div>
              <p class="text-sm text-muted-foreground mb-1">Name</p>
              <p class="text-lg font-medium">{{ profile.name }}</p>
            </div>
            <div>
              <p class="text-sm text-muted-foreground mb-1">Age Group</p>
              <p class="text-lg font-medium">{{ profile.ageGroup }}</p>
            </div>
            <div v-if="profile.gender">
              <p class="text-sm text-muted-foreground mb-1">Gender</p>
              <p class="text-lg font-medium">{{ profile.gender }}</p>
            </div>
            <div>
              <p class="text-sm text-muted-foreground mb-1">Activity Level</p>
              <p class="text-lg font-medium capitalize">
                {{ profile.activityLevel || 'Moderate' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Dietary Information -->
        <div class="mb-8 pt-8 border-t">
          <h2 class="text-2xl mb-6 flex items-center gap-2">
            <Apple class="w-6 h-6 text-[#F7B267]" />
            Dietary Information
          </h2>

          <div class="space-y-4">
            <div v-if="profile.allergies && profile.allergies.length > 0">
              <p class="text-sm text-muted-foreground mb-2">Food Allergies</p>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="allergy in profile.allergies"
                  :key="allergy"
                  class="bg-[#F7B267]/20 text-[#8B4513] px-3 py-1 rounded-full text-sm"
                >
                  {{ allergy }}
                </span>
              </div>
            </div>

            <div v-if="profile.dietaryRestriction">
              <p class="text-sm text-muted-foreground mb-2">Dietary Restriction</p>
              <span class="bg-[#CDE7F0]/30 text-[#1B4965] px-3 py-1 rounded-full text-sm">
                {{ profile.dietaryRestriction }}
              </span>
            </div>

            <div v-if="profile.eatingHabit">
              <p class="text-sm text-muted-foreground mb-2">Eating Habits</p>
              <p class="text-base">{{ profile.eatingHabit }}</p>
            </div>

            <div v-if="profile.dislikes">
              <p class="text-sm text-muted-foreground mb-2">Foods to Avoid</p>
              <p class="text-base">{{ profile.dislikes }}</p>
            </div>
          </div>
        </div>

        <!-- Nutrition Focus -->
        <div v-if="nutritionFocus && nutritionFocus.length > 0" class="pt-8 border-t">
          <h2 class="text-2xl mb-6 flex items-center gap-2">
            <Sparkles class="w-6 h-6 text-[#A8D5BA]" />
            Nutrition Focus Areas
          </h2>
          <div class="flex flex-wrap gap-3">
            <span
              v-for="focus in nutritionFocus"
              :key="focus"
              class="bg-[#A8D5BA]/20 text-[#2C5F2D] px-4 py-2 rounded-full"
            >
              {{ getNutritionAreaName(focus) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4">
        <button
          @click="handleEdit"
          :disabled="saving"
          class="flex-1 px-8 py-4 bg-white border-2 border-[#A8D5BA] text-[#2C5F2D] rounded-lg hover:bg-[#A8D5BA]/10 transition-colors inline-flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <Edit class="w-4 h-4" />
          Edit Profile
        </button>

        <button
          @click="handleSave"
          :disabled="saving"
          class="flex-1 px-8 py-4 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg transition-colors inline-flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <Check class="w-4 h-4" />
          {{ saving ? 'Saving...' : 'Save & View Lunchboxes' }}
        </button>
      </div>

      <!-- Optional: Nutrition Check Prompt -->
      <div class="mt-8 p-6 bg-gradient-to-r from-[#CDE7F0]/30 to-[#A8D5BA]/20 rounded-2xl border border-[#A8D5BA]/30">
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center flex-shrink-0">
            <ClipboardCheck class="w-6 h-6 text-[#2C5F2D]" />
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium mb-2">Want more personalized suggestions?</h3>
            <p class="text-sm text-muted-foreground mb-4">
              Take our quick nutrition check to get even more tailored meal recommendations based on your child's current diet.
            </p>
            <button
              @click="handleNutritionCheck"
              class="text-sm text-[#2C5F2D] font-medium hover:underline inline-flex items-center gap-1"
            >
              Take Nutrition Check
              <ChevronRight class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Check, User, Apple, Sparkles, Edit, ChevronRight, ClipboardCheck } from 'lucide-vue-next';
import { useChildProfileStore } from '../stores/childProfile';
import { createChild, updateChild } from '../services/api';

const router = useRouter();
const childProfileStore = useChildProfileStore();

const childName = ref('your child');
const profile = ref({});
const nutritionFocus = ref([]);
const saving = ref(false);

const nutritionAreaNames = {
  iron: 'Iron Support',
  calcium: 'Calcium & Bone Health',
  brain: 'Brain Development',
  immunity: 'Immune Support',
  energy: 'Sustained Energy',
  variety: 'Diet Variety',
};

// Map front-end allergy labels to DB allergen_id
const allergyMap = {
  'Peanuts': 47,
  'Tree nuts': 40,
  'Milk': 16,
  'Eggs': 18,
  'Wheat': 24,
  'Soy': 50,
  'Fish': 22,
  'Shellfish': 15,
};

onMounted(() => {
  const draft = childProfileStore.childProfileDraft;

  profile.value = draft;
  childName.value = draft.name || 'your child';
  nutritionFocus.value = draft.nutritionFocus || [];
});

const getNutritionAreaName = (id) => {
  return nutritionAreaNames[id] || id;
};

const handleEdit = () => {
  router.push('/child-info');
};

const handleNutritionCheck = () => {
  const editingChildId = localStorage.getItem('littlewell_edit_child_id');
  if (editingChildId) {
    router.push(`/nutrition-check?childId=${editingChildId}`);
  } else {
    router.push('/nutrition-check');
  }
};

const handleSave = async () => {
  try {
    saving.value = true;

    const editingChildId = localStorage.getItem('littlewell_edit_child_id');

    const payload = {
      child_name: profile.value.name,
      age_band: profile.value.ageGroup,
      band_id: null,

      iron_status: nutritionFocus.value.includes('iron') ? 1 : 0,
      calcium_status: nutritionFocus.value.includes('calcium') ? 1 : 0,
      vitamin_d_status: nutritionFocus.value.includes('immunity') ? 1 : 0,
      variety_status: nutritionFocus.value.includes('variety') ? 1 : 0,

      religious_needs: profile.value.dietaryRestriction || '',

      allergies: (profile.value.allergies || [])
        .map((allergy) => allergyMap[allergy])
        .filter(Boolean),
    };

    let savedChild;

    if (editingChildId) {
      await updateChild(editingChildId, payload);
      savedChild = { child_id: editingChildId };
    } else {
      savedChild = await createChild(payload);
    }

    localStorage.removeItem('littlewell_edit_child_id');
    childProfileStore.resetDraft();

    router.push(`/results?childId=${savedChild.child_id}`);
  } catch (error) {
    console.error('Failed to save child profile:', error);
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