<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-5xl">
      <!-- Back Button -->
      <button
        @click="router.push('/child-info')"
        class="mb-6 px-4 py-2 hover:bg-white rounded-lg transition-colors inline-flex items-center gap-2"
      >
        <ArrowLeft class="w-4 h-4" />
        Back
      </button>

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl mb-4">Nutrition Focus Areas</h1>
        <p class="text-lg text-muted-foreground">
          What would you like to focus on for {{ childName }}'s nutrition?
        </p>
        <p class="text-sm text-muted-foreground mt-2">
          Select up to 3 areas (optional - you can skip this step)
        </p>
      </div>

      <!-- Focus Areas Grid -->
      <div class="grid md:grid-cols-2 gap-6 mb-8">
        <div
          v-for="area in nutritionAreas"
          :key="area.id"
          @click="toggleArea(area.id)"
          :class="[
            'p-6 rounded-2xl border-2 cursor-pointer transition-all',
            selectedAreas.includes(area.id)
              ? 'border-[#A8D5BA] bg-[#A8D5BA]/10'
              : 'border-gray-200 hover:border-[#A8D5BA]/50 bg-white',
            selectedAreas.length >= 3 && !selectedAreas.includes(area.id)
              ? 'opacity-50 cursor-not-allowed'
              : ''
          ]"
        >
          <div class="flex items-start gap-4">
            <div :class="['w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0', area.bgColor]">
              <component :is="area.icon" :class="['w-6 h-6', area.iconColor]" />
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-medium mb-2">{{ area.title }}</h3>
              <p class="text-sm text-muted-foreground mb-3">{{ area.description }}</p>
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="tag in area.tags"
                  :key="tag"
                  class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <div v-if="selectedAreas.includes(area.id)" class="flex-shrink-0">
              <div class="w-6 h-6 bg-[#A8D5BA] rounded-full flex items-center justify-center">
                <Check class="w-4 h-4 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Selected Counter -->
      <div v-if="selectedAreas.length > 0" class="bg-white border rounded-xl p-4 mb-8 text-center">
        <p class="text-sm text-muted-foreground">
          <strong class="text-[#2C5F2D]">{{ selectedAreas.length }}</strong> of 3 focus areas selected
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4">
        <button
          @click="handleSkip"
          class="flex-1 px-8 py-4 bg-white border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Skip This Step
        </button>
        <button
          @click="handleContinue"
          :disabled="selectedAreas.length === 0"
          class="flex-1 px-8 py-4 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
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
import { ArrowLeft, Check, Heart, Brain, Zap, Shield, Sparkles, Leaf } from 'lucide-vue-next';
import { useChildProfileStore } from '../stores/childProfile';

const router = useRouter();
const childProfileStore = useChildProfileStore();

const childName = ref('your child');
const selectedAreas = ref([]);

const nutritionAreas = [
  {
    id: 'iron',
    title: 'Iron Support',
    description: 'Boost energy levels and support healthy blood development',
    tags: ['Energy', 'Growth', 'Concentration'],
    icon: Heart,
    bgColor: 'bg-[#F7B267]/20',
    iconColor: 'text-[#F7B267]',
  },
  {
    id: 'calcium',
    title: 'Calcium & Bone Health',
    description: 'Build strong bones and teeth during crucial growth years',
    tags: ['Bones', 'Teeth', 'Growth'],
    icon: Sparkles,
    bgColor: 'bg-[#CDE7F0]/30',
    iconColor: 'text-[#1B4965]',
  },
  {
    id: 'brain',
    title: 'Brain Development',
    description: 'Support cognitive function, memory, and learning',
    tags: ['Omega-3', 'Focus', 'Memory'],
    icon: Brain,
    bgColor: 'bg-purple-100',
    iconColor: 'text-purple-600',
  },
  {
    id: 'immunity',
    title: 'Immune Support',
    description: 'Strengthen natural defenses with vitamins and antioxidants',
    tags: ['Vitamin C', 'Zinc', 'Defense'],
    icon: Shield,
    bgColor: 'bg-[#A8D5BA]/20',
    iconColor: 'text-[#2C5F2D]',
  },
  {
    id: 'energy',
    title: 'Sustained Energy',
    description: 'Maintain steady energy throughout the day',
    tags: ['Complex carbs', 'Protein', 'Fiber'],
    icon: Zap,
    bgColor: 'bg-yellow-100',
    iconColor: 'text-yellow-600',
  },
  {
    id: 'variety',
    title: 'Diet Variety',
    description: 'Introduce diverse foods for balanced nutrition',
    tags: ['Exploration', 'Balance', 'Nutrients'],
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
    selectedAreas.value = selectedAreas.value.filter(a => a !== id);
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