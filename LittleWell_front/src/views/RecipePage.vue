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
      <div v-if="recipe.heroImage" class="absolute inset-0">
        <img
          :src="recipe.heroImage"
          :alt="recipe.name"
          class="w-full h-full object-cover"
          @error="handleHeroImageError"
        />
        <div class="absolute inset-0 bg-black/20"></div>
      </div>

      <div
        v-else
        class="absolute inset-0 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] flex items-center justify-center"
      >
        <UtensilsCrossed class="w-32 h-32 text-white/30" />
      </div>
    </div>

    <!-- Content -->
    <div class="py-12">
      <div class="container mx-auto px-6 max-w-4xl">
        <!-- Recipe Header -->
        <div class="bg-white rounded-2xl shadow-lg p-8 -mt-32 relative z-10 mb-8">
          <div class="mb-6">
            <div v-if="recipe.childName" class="mb-3">
              <span class="inline-flex items-center px-3 py-1 bg-[#CDE7F0]/30 text-[#1B4965] text-sm rounded-full">
                For {{ recipe.childName }}
              </span>
            </div>

            <h1 class="text-4xl mb-4">{{ recipe.name }}</h1>
            <p class="text-lg text-muted-foreground">{{ recipe.description }}</p>
          </div>

          <!-- Tags -->
          <div v-if="recipe.tags.length > 0" class="flex flex-wrap gap-2 mb-6">
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
              <p class="text-sm text-muted-foreground mb-1">
                {{ recipe.difficultyLabel }}
              </p>
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
              v-for="section in normalizedIngredients"
              :key="section.section"
              class="space-y-3"
            >
              <h3 :class="['text-lg font-medium pb-2 border-b-2', getSectionBorderColor(section.section)]">
                {{ getSectionTitle(section.section) }}
              </h3>

              <ul class="space-y-3">
                <li
                  v-for="(item, idx) in section.items"
                  :key="idx"
                  class="flex items-start gap-3"
                >
                  <div
                    v-if="item.image"
                    class="w-14 h-14 rounded-lg overflow-hidden bg-gray-100 flex-shrink-0"
                  >
                    <img
                      :src="item.image"
                      :alt="item.name"
                      class="w-full h-full object-cover"
                      @error="handleItemImageError"
                    />
                  </div>

                  <div
                    v-else
                    :class="[
                      'w-14 h-14 rounded-lg border border-dashed flex items-center justify-center text-[10px] text-center p-1 flex-shrink-0',
                      getSectionPlaceholderStyle(section.section)
                    ]"
                  >
                    {{ formatSectionLabel(section.section) }}
                  </div>

                  <div class="flex-1 flex items-start gap-2">
                    <div :class="['w-2 h-2 rounded-full mt-2 flex-shrink-0', getSectionDotColor(section.section)]"></div>
                    <div>
                      <p class="text-muted-foreground font-medium">{{ item.name }}</p>
                      <p v-if="item.amount" class="text-sm text-muted-foreground/80">{{ item.amount }}</p>
                    </div>
                  </div>
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

          <div v-if="recipe.instructions.length > 0" class="space-y-4">
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

          <div v-else class="text-muted-foreground">
            <p>
              This lunchbox is ready to use as a practical meal suggestion. You can mix and match the recommended items to suit your child’s preferences.
            </p>
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
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  ArrowLeft, Heart, Clock, Users, Sparkles, ShoppingCart,
  Check, Lightbulb, UtensilsCrossed, ChefHat, Gauge
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();

const defaultRecipe = {
  name: 'Honey Glazed Chicken with Rice',
  description: 'A colorful, balanced meal packed with protein and nutrients',
  prepTime: '30 mins',
  servings: '1 child',
  difficulty: 'Easy',
  difficultyLabel: 'Difficulty',
  heroImage: null,
  childName: null,
  tags: ['High in Iron', 'Balanced Protein', 'Kid-Friendly'],
  whyThisMeal:
    'Chicken provides quality protein and iron to support energy levels throughout the day. Carrots are rich in beta-carotene for healthy vision, while rice offers sustained energy.',
  colorInsight:
    "💛 Kids love bright colors! The golden chicken and orange carrots create an appetizing, vibrant meal that research shows can naturally boost a child's appetite.",
  ingredients: [
    {
      section: 'carbs',
      items: [
        { name: '150g white or brown rice', amount: '', image: null },
        { name: '2 cups water', amount: '', image: null },
        { name: 'Pinch of salt', amount: '', image: null },
      ],
    },
    {
      section: 'protein',
      items: [
        { name: '1 chicken wing (about 80g)', amount: '', image: null },
        { name: '1 tbsp honey', amount: '', image: null },
        { name: '1 tsp soy sauce', amount: '', image: null },
        { name: '½ tsp garlic powder', amount: '', image: null },
      ],
    },
    {
      section: 'veggies',
      items: [
        { name: '½ carrot, cut into sticks', amount: '', image: null },
        { name: '1 tsp cooking oil', amount: '', image: null },
        { name: 'Pinch of salt', amount: '', image: null },
      ],
    },
    {
      section: 'fruit',
      items: [
        { name: '½ apple', amount: '', image: null },
        { name: 'Lemon juice (optional, to prevent browning)', amount: '', image: null },
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
    "If your child doesn't like carrots, try cucumber sticks or cherry tomatoes instead.",
    'The honey glaze can be made in batches and stored in the fridge for up to a week.',
  ],
  nutritionFocus: ['High in Iron', 'Balanced Protein', 'Rich in Vitamin A'],
};

const recipe = ref({ ...defaultRecipe });

const normalizeInstructions = (instructions) => {
  if (Array.isArray(instructions)) return instructions.filter(Boolean);

  if (typeof instructions === 'string' && instructions.trim()) {
    return instructions
      .split(/\r?\n+/)
      .map((line) => line.trim())
      .filter(Boolean);
  }

  return [];
};

const normalizeIngredients = (raw) => {
  if (!Array.isArray(raw)) return [];

  if (raw.length > 0 && raw[0]?.section && Array.isArray(raw[0]?.items)) {
    return raw.map((section) => ({
      section: section.section,
      items: section.items.map((item) => {
        if (typeof item === 'string') {
          return { name: item, amount: '', image: null };
        }
        return {
          name: item.name || '',
          amount: item.amount || '',
          image: item.image || null,
        };
      }),
    }));
  }

  const grouped = {};

  raw.forEach((item) => {
    const section = item.section || 'other';
    if (!grouped[section]) grouped[section] = [];

    grouped[section].push({
      name: item.name || '',
      amount: item.amount || '',
      image: item.image || null,
    });
  });

  return Object.entries(grouped).map(([section, items]) => ({
    section,
    items,
  }));
};

const normalizedIngredients = computed(() => {
  return normalizeIngredients(recipe.value.ingredients);
});

const mapRouteStateToRecipe = (raw) => {
  if (!raw) return null;

  const title =
    raw.title ||
    raw.mealName ||
    raw.name ||
    'Lunchbox Recommendation';

  const heroImage = raw.heroImage || raw.mealImage || null;

  return {
    name: title,
    description:
      raw.description ||
      (raw.source === 'mealdb'
        ? 'A recipe-inspired lunchbox idea with practical ingredients.'
        : 'A practical lunchbox recommendation based on your child’s needs.'),
    prepTime: raw.prepTime || (raw.source === 'mealdb' ? '25 mins' : '15 mins'),
    servings: raw.servings || '1 child',
    difficulty: raw.source === 'mealdb' ? 'Recipe' : 'Easy',
    difficultyLabel: raw.source === 'mealdb' ? 'Type' : 'Difficulty',
    heroImage,
    childName: raw.childName || null,
    tags: Array.isArray(raw.tags)
      ? raw.tags
      : raw.category
        ? [raw.category]
        : [],
    whyThisMeal:
      raw.whyThisMeal ||
      'This option was selected to provide a balanced and practical lunchbox suggestion.',
    colorInsight: raw.colorInsight || '',
    ingredients: raw.ingredients || raw.items || [],
    instructions: normalizeInstructions(raw.instructions),
    tips:
      Array.isArray(raw.tips) && raw.tips.length > 0
        ? raw.tips
        : [
            'Pack items separately if your child prefers different textures.',
            'Combine familiar foods with one new item for better acceptance.',
            'Use colorful fruit and vegetables to make lunchboxes more appealing.',
          ],
    nutritionFocus: Array.isArray(raw.nutritionFocus) ? raw.nutritionFocus : [],
  };
};

const getSectionTitle = (section) => {
  const titles = {
    carbs: 'Carbohydrates',
    protein: 'Protein',
    veggies: 'Vegetables',
    fruit: 'Fruit',
    ingredient: 'Ingredients',
    other: 'Other Items',
  };
  return titles[section] || section;
};

const getSectionBorderColor = (section) => {
  const colors = {
    carbs: 'border-[#F7B267]',
    protein: 'border-[#A8D5BA]',
    veggies: 'border-[#8BC34A]',
    fruit: 'border-[#FF6B9D]',
    ingredient: 'border-[#CDE7F0]',
    other: 'border-gray-300',
  };
  return colors[section] || 'border-gray-300';
};

const getSectionDotColor = (section) => {
  const colors = {
    carbs: 'bg-[#F7B267]',
    protein: 'bg-[#A8D5BA]',
    veggies: 'bg-[#8BC34A]',
    fruit: 'bg-[#FF6B9D]',
    ingredient: 'bg-[#CDE7F0]',
    other: 'bg-gray-300',
  };
  return colors[section] || 'bg-gray-300';
};

const getSectionPlaceholderStyle = (section) => {
  const styles = {
    carbs: 'border-[#F7B267]/40 text-[#8B4513] bg-[#F7B267]/10',
    protein: 'border-[#A8D5BA]/40 text-[#2C5F2D] bg-[#A8D5BA]/10',
    veggies: 'border-[#8BC34A]/40 text-green-700 bg-green-50',
    fruit: 'border-[#FF6B9D]/40 text-pink-700 bg-pink-50',
    ingredient: 'border-[#CDE7F0]/40 text-[#1B4965] bg-[#CDE7F0]/20',
    other: 'border-gray-200 text-gray-500 bg-gray-50',
  };
  return styles[section] || styles.other;
};

const formatSectionLabel = (section) => {
  const labels = {
    carbs: 'Carbs',
    protein: 'Protein',
    veggies: 'Veggies',
    fruit: 'Fruit',
    ingredient: 'Ingredient',
    other: 'Item',
  };
  return labels[section] || 'Item';
};

const handleHeroImageError = (event) => {
  event.target.style.display = 'none';
};

const handleItemImageError = (event) => {
  event.target.style.display = 'none';
};

onMounted(() => {
  console.log('Recipe ID:', route.params.id);

  const stateRecipe = history.state?.lunchbox;

  if (stateRecipe) {
    recipe.value = mapRouteStateToRecipe(stateRecipe);
  }
});
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>