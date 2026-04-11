<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-6xl">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl mb-4">Nutritious Lunchboxes for Your Family</h1>
        <p class="text-lg text-muted-foreground">
          Colorful, balanced meals designed to delight and nourish your little ones
        </p>
      </div>

      <!-- Seasonal Toggle -->
      <div class="p-6 rounded-2xl shadow-sm mb-8 bg-white border">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-[#A8D5BA] rounded-full flex items-center justify-center flex-shrink-0">
              <Leaf class="w-6 h-6 text-[#2C5F2D]" />
            </div>
            <div>
              <h3 class="text-lg font-medium">{{ seasonNames[season] }} Seasonal Mode</h3>
              <p class="text-sm text-muted-foreground">
                Prioritize fresh, in-season ingredients for maximum nutrition
              </p>
            </div>
          </div>
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              v-model="seasonalMode"
              class="w-11 h-6 bg-gray-200 rounded-full appearance-none cursor-pointer relative
                     checked:bg-[#A8D5BA] transition-colors
                     after:content-[''] after:absolute after:top-0.5 after:left-0.5
                     after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-transform
                     checked:after:translate-x-5"
            />
          </label>
        </div>
      </div>

      <!-- Nutrition Support Areas (if available) -->
      <div v-if="needsSupport.length > 0" class="mb-8 p-6 bg-white border rounded-2xl shadow-sm">
        <div class="flex items-start gap-3">
          <Sparkles class="w-5 h-5 text-[#F7B267] mt-1" />
          <div>
            <h4 class="font-medium mb-2">Personalised for Your Child's Needs</h4>
            <p class="text-sm text-muted-foreground mb-3">
              These meals are tailored to provide extra support for:
            </p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="area in needsSupport"
                :key="area"
                class="text-xs bg-[#F7B267]/20 text-[#8B4513] px-3 py-1 rounded-full"
              >
                {{ area.charAt(0).toUpperCase() + area.slice(1) }} Support
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Lunchbox Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-if="isLoading" class="text-center py-10 text-muted-foreground">
          Loading personalised lunchbox recommendations...
        </div>

        <div v-else-if="lunchboxes.length === 0" class="text-center py-10 text-muted-foreground">
          No recommendations available yet. Please create a child profile first.
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="lunchbox in lunchboxes"
            :key="lunchbox.id"
            class="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
            @click="handleLunchboxClick(lunchbox.id)"
          >
          <!-- Child Name Badge (if exists) -->
          <div v-if="lunchbox.childName" class="px-6 pt-4">
            <span class="inline-flex items-center px-3 py-1 bg-[#CDE7F0]/30 text-[#1B4965] text-sm rounded-full">
              For {{ lunchbox.childName }}
            </span>
          </div>
          
    <!-- Items Grid -->
          <div class="p-6">
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div
                v-for="(item, idx) in lunchbox.items"
                :key="idx"
                class="relative"
              >
                <div class="aspect-square rounded-lg overflow-hidden bg-gray-100">
                  <img
                    :src="item.image"
                    :alt="item.name"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div
                  :class="[
                    'absolute top-2 left-2 w-3 h-3 rounded-full',
                    getSectionColor(item.section)
                  ]"
                ></div>
              </div>
            </div>

            <!-- Food Items List -->
            <div class="space-y-2 mb-4">
              <div
                v-for="(item, idx) in lunchbox.items"
                :key="idx"
                class="flex items-start gap-2"
              >
                <div :class="['w-2 h-2 rounded-full mt-1.5', getSectionColor(item.section)]"></div>
                <div class="flex-1">
                  <p class="text-sm font-medium">{{ item.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ item.amount }}</p>
                </div>
              </div>
            </div>

            <!-- Nutrition Focus Tags -->
            <div class="flex flex-wrap gap-2 mb-3">
              <span
                v-for="focus in lunchbox.nutritionFocus"
                :key="focus"
                :class="[
                  'text-xs px-3 py-1 rounded-full',
                  supportColors[lunchbox.supportType],
                  supportTextColors[lunchbox.supportType]
                ]"
              >
                {{ focus }}
              </span>
            </div>

            <!-- Why This Meal -->
            <p class="text-sm text-muted-foreground leading-relaxed">
              {{ lunchbox.whyThisMeal }}
            </p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="mt-12 flex gap-4 justify-center">
        <button
          @click="router.push('/')"
          class="px-8 py-3 bg-white border-2 border-[#A8D5BA] text-[#2C5F2D] rounded-lg hover:bg-[#A8D5BA]/10 transition-colors"
        >
          Back to Home
        </button>
        <button
          @click="loadRecommendations"
          class="px-8 py-3 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg transition-colors inline-flex items-center gap-2"
        >
          <RefreshCw class="w-4 h-4" />
          Generate New Meals
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { RefreshCw, Sparkles, Leaf } from 'lucide-vue-next';
import { getRecommendedProducts, getFamilyRecommendedProducts } from '../services/api';

const router = useRouter();
const route = useRoute();

const seasonalMode = ref(true);
const lunchboxes = ref([]);
const isLoading = ref(false);
const selectedChildId = ref(null);
const isFamilyMode = ref(false);
const selectedChildIds = ref([]);
const needsSupport = ref([]);

const loadRecommendations = async () => {
  const childId = route.query.childId;
  const childIdsParam = route.query.childIds;
  const family = route.query.family;

  try {
    isLoading.value = true;
    lunchboxes.value = [];
    needsSupport.value = [];

    // Family mode
    if (family && childIdsParam) {
      isFamilyMode.value = true;
      selectedChildId.value = null;

      selectedChildIds.value = String(childIdsParam)
        .split(',')
        .map(id => id.trim())
        .filter(Boolean);

      const data = await getFamilyRecommendedProducts(selectedChildIds.value, seasonalMode.value);

      lunchboxes.value = Array.isArray(data) ? data : data.lunchboxes || [];
      needsSupport.value = Array.isArray(data?.needsSupport) ? data.needsSupport : [];
      return;
    }

    // Single child mode
    if (childId) {
      isFamilyMode.value = false;
      selectedChildIds.value = [];
      selectedChildId.value = childId;

      const data = await getRecommendedProducts(childId, seasonalMode.value);

      lunchboxes.value = Array.isArray(data) ? data : data.lunchboxes || [];
      needsSupport.value = Array.isArray(data?.needsSupport) ? data.needsSupport : [];
      return;
    }

    // No params
    isFamilyMode.value = false;
    selectedChildId.value = null;
    selectedChildIds.value = [];
    lunchboxes.value = [];
    needsSupport.value = [];
  } catch (error) {
    console.error('Failed to load recommendations:', error);
    lunchboxes.value = [];
    needsSupport.value = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadRecommendations();
});

watch(seasonalMode, () => {
  loadRecommendations();
});

watch(
  () => [route.query.childId, route.query.childIds, route.query.family],
  () => {
    loadRecommendations();
  }
);

const supportColors = {
  iron: 'bg-[#F7B267]',
  calcium: 'bg-[#CDE7F0]',
  vitamins: 'bg-[#A8D5BA]',
  general: 'bg-purple-400',
};

const supportTextColors = {
  iron: 'text-white',
  calcium: 'text-[#1B4965]',
  vitamins: 'text-[#2C5F2D]',
  general: 'text-white',
};

const getCurrentSeason = () => {
  const month = new Date().getMonth();
  if (month >= 2 && month <= 4) return 'spring';
  if (month >= 5 && month <= 7) return 'summer';
  if (month >= 8 && month <= 10) return 'autumn';
  return 'winter';
};

const season = ref(getCurrentSeason());
const seasonNames = {
  spring: 'Spring',
  summer: 'Summer',
  autumn: 'Autumn',
  winter: 'Winter',
};

const getSectionColor = (section) => {
  const colors = {
    carbs: 'bg-[#F7B267]',
    protein: 'bg-[#A8D5BA]',
    veggies: 'bg-[#8BC34A]',
    fruit: 'bg-[#FF6B9D]',
  };
  return colors[section] || 'bg-gray-300';
};

const handleLunchboxClick = (id) => {
  router.push(`/recipe/${id}`);
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>