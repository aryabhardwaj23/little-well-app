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
          <button class="px-4 py-2 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg transition-colors inline-flex items-center gap-2">
            <Heart class="w-4 h-4" />
            Save Recipe
          </button>
        </div>
      </div>
    </nav>

    <!-- Loading -->
    <div v-if="isLoading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center text-muted-foreground">
        <div class="animate-spin w-8 h-8 border-2 border-[#A8D5BA] border-t-transparent rounded-full mx-auto mb-4"></div>
        Loading recipe...
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="errorMsg" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <p class="text-red-500 mb-4">{{ errorMsg }}</p>
        <button @click="router.push('/results')" class="px-6 py-2 bg-[#A8D5BA] text-[#2C5F2D] rounded-lg">
          Back to Results
        </button>
      </div>
    </div>

    <!-- Recipe Content -->
    <template v-else-if="recipe">
      <!-- Hero Image -->
      <div class="relative h-[300px] overflow-hidden">
        <img
          v-if="recipe.image"
          :src="recipe.image"
          :alt="recipe.name"
          class="w-full h-full object-cover"
        />
        <div v-else class="absolute inset-0 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] flex items-center justify-center">
          <UtensilsCrossed class="w-32 h-32 text-white/30" />
        </div>
      </div>

      <div class="py-8">
        <div class="container mx-auto px-6 max-w-4xl">

          <!-- Recipe Header Card -->
          <div class="bg-white rounded-2xl shadow-lg p-8 -mt-24 relative z-10 mb-8">
            <div class="mb-6">
              <h1 class="text-4xl mb-2">{{ recipe.name }}</h1>
              <p class="text-lg text-muted-foreground">{{ recipe.category }} · {{ recipe.area }}</p>
            </div>

            <!-- Nutrition Labels -->
            <div class="flex flex-wrap gap-2 mb-6">
              <span
                v-for="label in recipe.nutritionLabels"
                :key="label"
                class="bg-[#A8D5BA]/20 text-[#2C5F2D] px-3 py-1 rounded-full text-sm"
              >
                {{ label }}
              </span>
            </div>

            <!-- Prep Info -->
            <div class="grid grid-cols-3 gap-6 py-6 border-y">
              <div class="text-center">
                <Clock class="w-6 h-6 text-[#A8D5BA] mx-auto mb-2" />
                <p class="text-sm text-muted-foreground mb-1">Prep Time</p>
                <p class="font-medium">~30 mins</p>
              </div>
              <div class="text-center">
                <Users class="w-6 h-6 text-[#A8D5BA] mx-auto mb-2" />
                <p class="text-sm text-muted-foreground mb-1">Servings</p>
                <p class="font-medium">1–2 children</p>
              </div>
              <div class="text-center">
                <Gauge class="w-6 h-6 text-[#A8D5BA] mx-auto mb-2" />
                <p class="text-sm text-muted-foreground mb-1">Difficulty</p>
                <p class="font-medium">Easy</p>
              </div>
            </div>
          </div>

          <!-- Why This Meal -->
          <div v-if="recipe.whyThisMeal" class="bg-gradient-to-br from-[#A8D5BA]/10 to-[#CDE7F0]/10 rounded-2xl p-8 mb-8">
            <h2 class="text-2xl mb-4 flex items-center gap-2">
              <Sparkles class="w-6 h-6 text-[#F7B267]" />
              Why This Meal?
            </h2>
            <p class="text-muted-foreground leading-relaxed">{{ recipe.whyThisMeal }}</p>
          </div>

          <!-- Ingredients -->
          <div class="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 class="text-2xl mb-6 flex items-center gap-2">
              <ShoppingCart class="w-6 h-6 text-[#A8D5BA]" />
              Ingredients
            </h2>
            <ul class="grid md:grid-cols-2 gap-3">
              <li
                v-for="(ing, idx) in recipe.ingredients"
                :key="idx"
                class="flex items-start gap-3"
              >
                <div class="w-8 h-8 rounded-lg overflow-hidden flex-shrink-0 bg-gray-100">
                  <img
                    :src="`https://www.themealdb.com/images/ingredients/${encodeURIComponent(ing.ingredient)}-Small.png`"
                    :alt="ing.ingredient"
                    class="w-full h-full object-cover"
                    @error="e => e.target.style.display='none'"
                  />
                </div>
                <div>
                  <p class="text-sm font-medium">{{ ing.ingredient }}</p>
                  <p class="text-xs text-muted-foreground">{{ ing.measure }}</p>
                </div>
              </li>
            </ul>
          </div>

          <!-- Instructions -->
          <div v-if="recipe.instructions.length" class="bg-white rounded-2xl shadow-md p-8 mb-8">
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

          <!-- Source Link -->
          <div v-if="recipe.source" class="text-center text-sm text-muted-foreground">
            <a :href="recipe.source" target="_blank" class="text-[#2C5F2D] underline">
              View original recipe source ↗
            </a>
          </div>

        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  ArrowLeft, Heart, Clock, Users, Sparkles, ShoppingCart,
  UtensilsCrossed, ChefHat, Gauge,
} from 'lucide-vue-next';
import { getMealById } from '../services/api';

const router = useRouter();
const route  = useRoute();

const recipe   = ref(null);
const isLoading = ref(true);
const errorMsg  = ref('');

const parseInstructions = (raw = '') =>
  raw.split(/\r\n|\n/).map(s => s.trim()).filter(s => s.length > 2);

const buildRecipe = (meal) => ({
  name:           meal.name || meal.strMeal || 'Unknown Meal',
  category:       meal.category || meal.strCategory || '',
  area:           meal.area || meal.strArea || '',
  image:          meal.image || meal.strMealThumb || '',
  source:         meal.source || meal.strSource || '',
  instructions:   parseInstructions(meal.instructions || meal.strInstructions || ''),
  ingredients:    meal.ingredients || [],
  nutritionLabels: meal.nutrition_labels || [],
  whyThisMeal:    meal.why_this_meal || '',
});

onMounted(async () => {
  const id = route.params.id;
  if (!id) {
    errorMsg.value = 'No recipe ID provided.';
    isLoading.value = false;
    return;
  }
  try {
    const data = await getMealById(id);
    recipe.value = buildRecipe(data);
  } catch (err) {
    console.error('Failed to load recipe:', err);
    errorMsg.value = 'Could not load this recipe. It may no longer be available.';
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.text-muted-foreground { color: #6b7280; }
</style>
