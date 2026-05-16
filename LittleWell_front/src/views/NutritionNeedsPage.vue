<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-5xl px-4 sm:px-6">
      <!-- Back Button -->
      <button
        @click="router.push('/child-info')"
        class="mb-5 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-white sm:mb-6 sm:px-4"
        type="button"
        aria-label="Go back to child information"
      >
        <ArrowLeft class="h-4 w-4" aria-hidden="true" />
        Back
      </button>

      <!-- Header -->
      <header class="mb-8 text-center sm:mb-12">
        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          Nutrition Focus Areas
        </h1>

        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          What would you like to focus on for {{ childName }}'s nutrition?
        </p>

        <p class="mt-2 text-xs leading-relaxed text-muted-foreground sm:text-sm">
          Select up to 3 areas. This step is optional.
        </p>
      </header>

      <!-- Focus Areas Grid -->
      <section class="mb-6 grid grid-cols-1 gap-4 md:mb-8 md:grid-cols-2 md:gap-6">
        <button
          v-for="area in nutritionAreas"
          :key="area.id"
          @click="toggleArea(area.id)"
          :disabled="selectedAreas.length >= 3 && !selectedAreas.includes(area.id)"
          :aria-pressed="selectedAreas.includes(area.id)"
          :aria-label="`${area.title}. ${area.description}`"
          :class="[
            'w-full rounded-2xl border-2 p-5 text-left transition-all sm:p-6',
            selectedAreas.includes(area.id)
              ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 shadow-sm'
              : 'border-gray-200 bg-white hover:border-[#A8D5BA]/50',
            selectedAreas.length >= 3 && !selectedAreas.includes(area.id)
              ? 'cursor-not-allowed opacity-50'
              : 'cursor-pointer'
          ]"
          type="button"
        >
          <div class="flex items-start gap-3 sm:gap-4">
            <div
              :class="[
                'flex h-11 w-11 shrink-0 items-center justify-center rounded-full sm:h-12 sm:w-12',
                area.bgColor
              ]"
              aria-hidden="true"
            >
              <component :is="area.icon" :class="['h-5 w-5 sm:h-6 sm:w-6', area.iconColor]" />
            </div>

            <div class="min-w-0 flex-1">
              <h3 class="mb-2 text-base font-semibold leading-snug text-[#111827] sm:text-lg">
                {{ area.title }}
              </h3>

              <p class="mb-3 text-sm leading-relaxed text-muted-foreground">
                {{ area.description }}
              </p>

              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="tag in area.tags"
                  :key="tag"
                  class="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <div v-if="selectedAreas.includes(area.id)" class="shrink-0">
              <div
                class="flex h-6 w-6 items-center justify-center rounded-full bg-[#A8D5BA]"
                aria-hidden="true"
              >
                <Check class="h-4 w-4 text-white" />
              </div>
            </div>
          </div>
        </button>
      </section>

      <!-- Selected Counter -->
      <div
        v-if="selectedAreas.length > 0"
        class="mb-6 rounded-xl border bg-white p-4 text-center shadow-sm sm:mb-8"
        aria-live="polite"
      >
        <p class="text-sm text-muted-foreground">
          <strong class="text-[#2C5F2D]">{{ selectedAreas.length }}</strong>
          of 3 focus areas selected
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col-reverse gap-3 sm:flex-row sm:gap-4">
        <button
          @click="handleSkip"
          class="w-full flex-1 rounded-lg border-2 border-gray-300 bg-white px-8 py-3.5 font-medium text-gray-700 transition-colors hover:bg-gray-50 sm:py-4"
          type="button"
        >
          Skip This Step
        </button>

        <button
          @click="handleContinue"
          :disabled="selectedAreas.length === 0"
          class="w-full flex-1 rounded-lg bg-[#A8D5BA] px-8 py-3.5 font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-50 sm:py-4"
          type="button"
          :aria-disabled="selectedAreas.length === 0"
        >
          Continue
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import {
  ArrowLeft,
  Check,
  Heart,
  Brain,
  Zap,
  Shield,
  Sparkles,
  Leaf,
} from 'lucide-vue-next';
import { useChildProfileStore } from '../stores/childProfile';

const router = useRouter();
const childProfileStore = useChildProfileStore();

const childName = ref('your child');
const selectedAreas = ref([]);

const nutritionAreas = [
  {
    id: 'iron',
    title: 'Does your child feel tired easily?',
    description: 'Help boost energy and reduce tiredness during the day',
    tags: ['Energy', 'Less tired'],
    icon: Heart,
    bgColor: 'bg-[#F7B267]/20',
    iconColor: 'text-[#F7B267]',
  },
  {
    id: 'calcium',
    title: 'Do you want to support strong growth?',
    description: 'Help build strong bones and support healthy development',
    tags: ['Growth', 'Bones'],
    icon: Sparkles,
    bgColor: 'bg-[#CDE7F0]/30',
    iconColor: 'text-[#1B4965]',
  },
  {
    id: 'brain',
    title: 'Does your child need help focusing?',
    description: 'Support concentration, memory, and learning',
    tags: ['Focus', 'Learning'],
    icon: Brain,
    bgColor: 'bg-purple-100',
    iconColor: 'text-purple-600',
  },
  {
    id: 'immunity',
    title: 'Does your child get sick often?',
    description: 'Help strengthen the immune system',
    tags: ['Immunity', 'Health'],
    icon: Shield,
    bgColor: 'bg-[#A8D5BA]/20',
    iconColor: 'text-[#2C5F2D]',
  },
  {
    id: 'energy',
    title: 'Do you want steady energy all day?',
    description: 'Keep energy levels balanced throughout the day',
    tags: ['Energy', 'Active'],
    icon: Zap,
    bgColor: 'bg-yellow-100',
    iconColor: 'text-yellow-600',
  },
  {
    id: 'variety',
    title: 'Is your child a picky eater?',
    description: 'Encourage trying new foods and a more balanced diet',
    tags: ['Variety', 'Balance'],
    icon: Leaf,
    bgColor: 'bg-green-100',
    iconColor: 'text-green-600',
  },
];

onMounted(() => {
  childName.value = childProfileStore.childProfileDraft.name || 'your child';
  selectedAreas.value = childProfileStore.childProfileDraft.nutritionFocus || [];
});

const toggleArea = (id) => {
  if (selectedAreas.value.includes(id)) {
    selectedAreas.value = selectedAreas.value.filter((areaId) => areaId !== id);
  } else if (selectedAreas.value.length < 3) {
    selectedAreas.value = [...selectedAreas.value, id];
  }
};

const handleContinue = () => {
  childProfileStore.updateDraft({
    nutritionFocus: selectedAreas.value,
  });

  router.push('/profile-summary');
};

const handleSkip = () => {
  childProfileStore.updateDraft({
    nutritionFocus: [],
  });

  router.push('/profile-summary');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>