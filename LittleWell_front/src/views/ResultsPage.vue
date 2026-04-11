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
        <div
          v-for="lunchbox in mockLunchboxes"
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { RefreshCw, Sparkles, Leaf } from 'lucide-vue-next';

const router = useRouter();

const seasonalMode = ref(true);

const mockLunchboxes = [
  {
    id: '1',
    childName: 'Tommy',
    items: [
      {
        name: 'Steamed Rice',
        amount: '150g (about 3/4 cup)',
        image: 'https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400',
        section: 'carbs',
      },
      {
        name: 'Honey Glazed Chicken Wing',
        amount: '1 piece (about 80g)',
        image: 'https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=400',
        section: 'protein',
      },
      {
        name: 'Stir-fried Carrot Sticks',
        amount: '1/2 carrot (about 50g)',
        image: 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400',
        section: 'veggies',
      },
      {
        name: 'Apple Slices',
        amount: '1/2 apple (about 75g)',
        image: 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400',
        section: 'fruit',
      },
    ],
    nutritionFocus: ['High in Iron', 'Balanced Protein'],
    whyThisMeal: 'Chicken provides quality protein and iron to support energy levels. Carrots are rich in beta-carotene for healthy vision.',
    colorInsight: '💛 Kids love bright colors! The golden chicken and orange carrots create an appetizing, vibrant meal.',
    recipe: '1. Steam rice for 15 mins. 2. Bake chicken wing with honey glaze at 180°C for 20 mins.',
    supportType: 'iron',
  },
  {
    id: '2',
    items: [
      {
        name: 'Whole Grain Pasta',
        amount: '100g (about 1 cup cooked)',
        image: 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400',
        section: 'carbs',
      },
      {
        name: 'Mini Turkey Meatballs',
        amount: '3 pieces (about 90g)',
        image: 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=400',
        section: 'protein',
      },
      {
        name: 'Cherry Tomatoes',
        amount: '5-6 pieces (about 60g)',
        image: 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=400',
        section: 'veggies',
      },
      {
        name: 'Strawberry Hearts',
        amount: '4-5 pieces (about 80g)',
        image: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400',
        section: 'fruit',
      },
    ],
    nutritionFocus: ['Supports Immunity', 'Rich in Vitamins'],
    whyThisMeal: 'Turkey is a lean protein source, while tomatoes and strawberries provide vitamin C to boost immune system.',
    colorInsight: '❤️ The cheerful reds from tomatoes and strawberries make this lunchbox visually exciting.',
    recipe: '1. Cook pasta according to package. 2. Mix ground turkey with breadcrumbs, form small balls, bake 15 mins.',
    supportType: 'vitamins',
  },
  {
    id: '3',
    childName: 'Sophie',
    items: [
      {
        name: 'Quinoa',
        amount: '120g (about 2/3 cup)',
        image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400',
        section: 'carbs',
      },
      {
        name: 'Baked Salmon Nuggets',
        amount: '2 pieces (about 70g)',
        image: 'https://images.unsplash.com/photo-1485921325833-c519f76c4927?w=400',
        section: 'protein',
      },
      {
        name: 'Steamed Broccoli Florets',
        amount: '5-6 florets (about 60g)',
        image: 'https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=400',
        section: 'veggies',
      },
      {
        name: 'Orange Segments',
        amount: '1/2 orange (about 70g)',
        image: 'https://images.unsplash.com/photo-1580052614034-c55d20bfee3b?w=400',
        section: 'fruit',
      },
    ],
    nutritionFocus: ['Rich in Calcium', 'Omega-3 Boost'],
    whyThisMeal: 'Salmon and broccoli work together to provide calcium, vitamin D, and omega-3s for strong bones and healthy brain development.',
    colorInsight: '🧡 The vibrant greens and oranges create a beautiful rainbow effect.',
    recipe: '1. Cook quinoa in water (1:2 ratio) for 15 mins. 2. Cut salmon into nuggets, coat lightly with breadcrumbs, bake 12 mins.',
    supportType: 'calcium',
  },
];

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

const checkData = localStorage.getItem('nutriguide_nutrition_check');
let nutritionInsights = null;
if (checkData) {
  nutritionInsights = JSON.parse(checkData).nutritionInsights;
}

const needsSupport = nutritionInsights
  ? Object.entries(nutritionInsights)
      .filter(([_, status]) => status === 'needs' || status === 'improve')
      .map(([area, _]) => area)
  : [];

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