 <template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-4xl">
      <!-- Back Button -->
      <button
        @click="router.push('/')"
        class="mb-6 px-4 py-2 hover:bg-gray-100 rounded-lg transition-colors inline-flex items-center gap-2 bg-white"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Home
      </button>

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl mb-4">{{ isEditing ? 'Edit Profile' : 'Create Child Profile' }}</h1>
        <p class="text-lg text-muted-foreground">
          Tell us about your child to get personalised meal suggestions
        </p>
      </div>

      <!-- Form -->
      <div class="space-y-8">
        <!-- Basic Info -->
        <div class="p-8 rounded-2xl shadow-sm bg-white">
          <h2 class="text-2xl mb-6">Basic Information</h2>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Child's Name</label>
              <input
                v-model="formData.name"
                type="text"
                placeholder="e.g. Emma"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A8D5BA]"
              />
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">Age Group</label>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <button
                  v-for="age in ageGroups"
                  :key="age"
                  @click="formData.ageGroup = age"
                  :class="[
                    'p-3 rounded-lg border-2 transition-all',
                    formData.ageGroup === age
                      ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                      : 'border-gray-200 hover:border-[#A8D5BA]/50'
                  ]"
                >
                  {{ age }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Allergies -->
        <div class="p-8 rounded-2xl shadow-sm bg-white">
          <h2 class="text-2xl mb-6">Allergies & Intolerances</h2>
          <p class="text-sm text-muted-foreground mb-4">Select all that apply</p>
          
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <button
              v-for="allergy in commonAllergies"
              :key="allergy"
              @click="toggleAllergy(allergy)"
              :class="[
                'p-3 rounded-lg border-2 transition-all',
                formData.allergies.includes(allergy)
                  ? 'border-[#F7B267] bg-[#F7B267]/10 text-[#8B4513]'
                  : 'border-gray-200 hover:border-[#F7B267]/50'
              ]"
            >
              {{ allergy }}
            </button>
          </div>
        </div>

        <!-- Nutrition Focus -->
        <div class="p-8 rounded-2xl shadow-sm bg-white">
          <h2 class="text-2xl mb-6">Nutrition Focus</h2>
          <p class="text-sm text-muted-foreground mb-4">What would you like to focus on?</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <button
              v-for="focus in nutritionOptions"
              :key="focus"
              @click="toggleNutritionFocus(focus)"
              :class="[
                'p-4 rounded-lg border-2 transition-all text-left',
                formData.nutritionFocus.includes(focus)
                  ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                  : 'border-gray-200 hover:border-[#A8D5BA]/50'
              ]"
            >
              {{ focus }}
            </button>
          </div>
        </div>

        <!-- Save Button -->
        <button
          @click="handleSave"
          :disabled="!formData.name || !formData.ageGroup"
          class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ isEditing ? 'Update Profile' : 'Create Profile' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft } from 'lucide-vue-next';

const router = useRouter();

const isEditing = ref(false);

const formData = ref({
  name: '',
  ageGroup: '',
  allergies: [],
  dietaryRestriction: '',
  nutritionFocus: [],
});

const ageGroups = ['0-3 years', '3-6 years', '6-9 years', '9-12 years', '12+ years'];

const commonAllergies = [
  'Peanuts', 'Tree nuts', 'Milk', 'Eggs',
  'Wheat', 'Soy', 'Fish', 'Shellfish',
];

const nutritionOptions = [
  'Balanced nutrition',
  'Iron support',
  'Calcium support',
  'Brain development',
  'Immune support',
  'Diet variety',
];

onMounted(() => {
  const editingId = localStorage.getItem('nutriguide_editing_profile');
  if (editingId) {
    isEditing.value = true;
    const savedProfiles = localStorage.getItem('nutriguide_family_profiles');
    if (savedProfiles) {
      const profiles = JSON.parse(savedProfiles);
      const profile = profiles.find(p => p.id === editingId);
      if (profile) {
        formData.value = { ...profile };
      }
    }
  }
});

const toggleAllergy = (allergy) => {
  if (formData.value.allergies.includes(allergy)) {
    formData.value.allergies = formData.value.allergies.filter(a => a !== allergy);
  } else {
    formData.value.allergies = [...formData.value.allergies, allergy];
  }
};

const toggleNutritionFocus = (focus) => {
  if (formData.value.nutritionFocus.includes(focus)) {
    formData.value.nutritionFocus = formData.value.nutritionFocus.filter(f => f !== focus);
  } else {
    formData.value.nutritionFocus = [...formData.value.nutritionFocus, focus];
  }
};

const handleSave = () => {
  const savedProfiles = localStorage.getItem('nutriguide_family_profiles');
  let profiles = savedProfiles ? JSON.parse(savedProfiles) : [];
  
  if (isEditing.value) {
    profiles = profiles.map(p => p.id === formData.value.id ? formData.value : p);
  } else {
    const newProfile = {
      ...formData.value,
      id: Date.now().toString(),
    };
    profiles.push(newProfile);
  }
  
  localStorage.setItem('nutriguide_family_profiles', JSON.stringify(profiles));
  localStorage.removeItem('nutriguide_editing_profile');
  router.push('/');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>