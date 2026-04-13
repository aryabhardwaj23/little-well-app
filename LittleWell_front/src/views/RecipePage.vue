<template>
  <div class="min-h-screen bg-[#FAF9F6]">
    <!-- Navigation -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between h-16">
          <button
            @click="router.push('/results')"
            class="px-4 py-2 hover:bg-gray-100 rounded-lg transition-colors inline-flex items-center gap-2"
          >
            <ArrowLeft class="w-4 h-4" />
            Back to Lunchboxes
          </button>
          <button
            class="px-4 py-2 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg transition-colors inline-flex items-center gap-2"
          >
            <Heart class="w-4 h-4" />
            Save Recipe
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero Image Section -->
    <div class="relative h-[400px] overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] flex items-center justify-center">
        <UtensilsCrossed class="w-32 h-32 text-white/30" />
      </div>
    </div>

    <!-- Content -->
    <div class="py-12">
      <div class="container mx-auto px-6 max-w-4xl">
        <!-- Recipe Header -->
        <div class="bg-white rounded-2xl shadow-lg p-8 -mt-32 relative z-10 mb-8">
          <div class="mb-6">
            <h1 class="text-4xl mb-4">{{ recipe.name }}</h1>
            <p class="text-lg text-muted-foreground">{{ recipe.description }}</p>
          </div>

          <!-- Tags -->
          <div class="flex flex-wrap gap-2 mb-6">
            <span
              v-for="tag in recipe.tags"
              :key="tag"
              class="bg-[#A8D5BA]/20 text-[#2C5F2D] px-3 py-1 rounded-full text-sm"
            >
              {{ tag }}
            </span>
          </div>

          <!-- Prep Info -->
          <div class="grid grid-cols-3 gap-6 py-6 border-y">
            <div class="text-center">
              <Clock class="w-6 h-6 text-[#A8D5BA] mx-auto mb-2" />
              <p class="text-sm text-muted-foreground mb-1">Prep Time</p>
              <p class="font-medium">{{ recipe.prepTime }}</p>
            </div>
            <div class="text-center">
              <Users class="w-6 h-6 text-[#A8D5BA] mx-auto mb-2" />
              <p class="text-sm text-muted-foreground mb-1">Servings</p>
              <p class="font-medium">{{ recipe.servings }}</p>
            </div>
            <div class="text-center">
              <Gauge class="w-6 h-6 text-[#A8D5BA] mx-auto mb-2" />
              <p class="text-sm text-muted-foreground mb-1">Difficulty</p>
              <p class="font-medium">{{ recipe.difficulty }}</p>
            </div>
          </div>
        </div>

        <!-- Nutrition Benefits -->
        <div class="bg-gradient-to-br from-[#A8D5BA]/10 to-[#CDE7F0]/10 rounded-2xl p-8 mb-8">
          <h2 class="text-2xl mb-4 flex items-center gap-2">
            <Sparkles class="w-6 h-6 text-[#F7B267]" />
            Why This Meal?
          </h2>
          <p class="text-muted-foreground leading-relaxed mb-4">
            {{ recipe.whyThisMeal }}
          </p>
          <div v-if="recipe.colorInsight" class="p-4 bg-white rounded-lg">
            <p class="text-sm leading-relaxed">{{ recipe.colorInsight }}</p>
          </div>
        </div>

        <!-- Ingredients -->
        <div class="bg-white rounded-2xl shadow-md p-8 mb-8">
          <h2 class="text-2xl mb-6 flex items-center gap-2">
            <ShoppingCart class="w-6 h-6 text-[#A8D5BA]" />
            Ingredients
          </h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div
              v-for="section in recipe.ingredients"
              :key="section.section"
              class="space-y-3"
            >
              <h3 :class="['text-lg font-medium pb-2 border-b-2', getSectionBorderColor(section.section)]">
                {{ getSectionTitle(section.section) }}
              </h3>
              <ul class="space-y-2">
                <li
                  v-for="(item, idx) in section.items"
                  :key="idx"
                  class="flex items-start gap-2"
                >
                  <div :class="['w-2 h-2 rounded-full mt-2 flex-shrink-0', getSectionDotColor(section.section)]"></div>
                  <span class="text-muted-foreground">{{ item }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Instructions -->
        <div class="bg-white rounded-2xl shadow-md p-8 mb-8">
          <h2 class="text-2xl mb-6 flex items-center gap-2">
            <ChefHat class="w-6 h-6 text-[#F7B267]" />
            Instructions
          </h2>
          <div class="space-y-4">
            <div
              v-for="(step, idx) in recipe.instructions"
              :key="idx"
              class="flex gap-4"
            >
              <div class="w-10 h-10 bg-[#A8D5BA] text-white rounded-full flex items-center justify-center flex-shrink-0 font-medium">
                {{ idx + 1 }}
              </div>
              <p class="flex-1 pt-2 text-muted-foreground">{{ step }}</p>
            </div>
          </div>
        </div>

        <!-- Tips -->
        <div class="bg-[#CDE7F0]/20 rounded-2xl p-8 mb-8">
          <h2 class="text-2xl mb-4 flex items-center gap-2">
            <Lightbulb class="w-6 h-6 text-[#F7B267]" />
            Parent Tips
          </h2>
          <ul class="space-y-3">
            <li
              v-for="(tip, idx) in recipe.tips"
              :key="idx"
              class="flex items-start gap-3"
            >
              <Check class="w-5 h-5 text-[#A8D5BA] mt-0.5 flex-shrink-0" />
              <span class="text-muted-foreground">{{ tip }}</span>
            </li>
          </ul>
        </div>

        <!-- Nutrition Focus -->
        <div class="bg-white rounded-2xl shadow-md p-8">
          <h2 class="text-2xl mb-4">Nutrition Focus</h2>
          <div class="flex flex-wrap gap-3">
            <span
              v-for="focus in recipe.nutritionFocus"
              :key="focus"
              class="bg-[#A8D5BA]/20 text-[#2C5F2D] px-4 py-2 rounded-full"
            >
              {{ focus }}
            </span>
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
  ArrowLeft, Heart, Clock, Users, Sparkles, ShoppingCart,
  Check, Lightbulb, UtensilsCrossed, ChefHat, Gauge
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();

const recipe = ref({
  name: 'Honey Glazed Chicken with Rice',
  description: 'A colorful, balanced meal packed with protein and nutrients',
  prepTime: '30 mins',
  servings: '1 child',
  difficulty: 'Easy',
  tags: ['High in Iron', 'Balanced Protein', 'Kid-Friendly'],
  whyThisMeal: 'Chicken provides quality protein and iron to support energy levels throughout the day. Carrots are rich in beta-carotene for healthy vision, while rice offers sustained energy.',
  colorInsight: '💛 Kids love bright colors! The golden chicken and orange carrots create an appetizing, vibrant meal that research shows can naturally boost a child\'s appetite.',
  ingredients: [
    {
      section: 'carbs',
      items: [
        '150g white or brown rice',
        '2 cups water',
        'Pinch of salt',
      ],
    },
    {
      section: 'protein',
      items: [
        '1 chicken wing (about 80g)',
        '1 tbsp honey',
        '1 tsp soy sauce',
        '½ tsp garlic powder',
      ],
    },
    {
      section: 'veggies',
      items: [
        '½ carrot, cut into sticks',
        '1 tsp cooking oil',
        'Pinch of salt',
      ],
    },
    {
      section: 'fruit',
      items: [
        '½ apple',
        'Lemon juice (optional, to prevent browning)',
      ],
    },
  ],
  instructions: [
    'Rinse rice thoroughly and cook in a rice cooker or pot with 2 cups of water for about 15-20 minutes until fluffy.',
    'Preheat oven to 180°C (350°F). Mix honey, soy sauce, and garlic powder in a small bowl.',
    'Coat the chicken wing with the honey glaze and place on a baking tray lined with parchment paper.',
    'Bake for 20-25 minutes, turning once halfway through, until golden and cooked through.',
    'While chicken bakes, heat oil in a pan and quickly stir-fry carrot sticks for 3-4 minutes until slightly tender but still crisp.',
    'Cut apple into fun shapes like stars or wedges. Brush lightly with lemon juice if packing for later.',
    'Arrange all components in a lunchbox, keeping items separate for best presentation.',
  ],
  tips: [
    'You can prepare the rice and chicken the night before and refrigerate.',
    'Let your child help cut the apple with a safe, child-friendly cutter.',
    'If your child doesn\'t like carrots, try cucumber sticks or cherry tomatoes instead.',
    'The honey glaze can be made in batches and stored in the fridge for up to a week.',
  ],
  nutritionFocus: ['High in Iron', 'Balanced Protein', 'Rich in Vitamin A'],
});

const getSectionTitle = (section) => {
  const titles = {
    carbs: 'Carbohydrates',
    protein: 'Protein',
    veggies: 'Vegetables',
    fruit: 'Fruit',
  };
  return titles[section] || section;
};

const getSectionBorderColor = (section) => {
  const colors = {
    carbs: 'border-[#F7B267]',
    protein: 'border-[#A8D5BA]',
    veggies: 'border-[#8BC34A]',
    fruit: 'border-[#FF6B9D]',
  };
  return colors[section] || 'border-gray-300';
};

const getSectionDotColor = (section) => {
  const colors = {
    carbs: 'bg-[#F7B267]',
    protein: 'bg-[#A8D5BA]',
    veggies: 'bg-[#8BC34A]',
    fruit: 'bg-[#FF6B9D]',
  };
  return colors[section] || 'bg-gray-300';
};

onMounted(() => {
  // In a real app, you would fetch recipe data based on route.params.id
  console.log('Recipe ID:', route.params.id);
});
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>