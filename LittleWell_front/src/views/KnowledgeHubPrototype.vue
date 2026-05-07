<template>
  <div
    :class="[
      'min-h-screen bg-[#FAF9F6] knowledgehub-root',
      { 'large-text-mode': largeTextMode, 'high-contrast-mode': highContrastMode }
    ]"
  >
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between h-16">
          <button @click="router.push('/')" class="flex items-center cursor-pointer" type="button">
            <img
              :src="logoUrl"
              alt="LittleHelp logo"
              class="h-10 w-auto object-contain"
            />
          </button>

          <div class="flex items-center gap-2">
            <button
              @click="router.push('/')"
              type="button"
              class="inline-flex items-center px-4 py-2 text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg transition-colors"
            >
              <ArrowLeft class="w-4 h-4 mr-2" />
              Back to Home
            </button>

            <div ref="accessibilityMenuRef" class="relative">
              <button
                @click="toggleAccessibilityMenu"
                class="inline-flex items-center gap-1 px-4 py-2 text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg transition-colors"
                type="button"
              >
                Accessibility
                <ChevronDown
                  :class="[
                    'w-3.5 h-3.5 transition-transform duration-200 translate-y-[1px]',
                    showAccessibilityMenu ? 'rotate-180' : 'rotate-0'
                  ]"
                />
              </button>

              <div
                v-if="showAccessibilityMenu"
                class="absolute right-0 mt-2 w-72 rounded-2xl border border-[#D6E7DC] bg-white shadow-xl p-4 z-50"
              >
                <p class="text-sm font-semibold text-[#2C5F2D]">Accessibility</p>
                <div class="h-px bg-[#E5E7EB] my-3"></div>

                <button
                  type="button"
                  @click="toggleLargeTextMode"
                  :class="[
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors',
                    largeTextMode
                      ? 'bg-[#F8F5EC] text-[#2C5F2D]'
                      : 'bg-transparent text-[#2C5F2D] hover:bg-[#F8F5EC]'
                  ]"
                >
                  Large Text Mode
                </button>

                <button
                  type="button"
                  @click="toggleHighContrastMode"
                  :class="[
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors mt-2',
                    highContrastMode
                      ? 'bg-[#F8F5EC] text-[#2C5F2D]'
                      : 'bg-transparent text-[#2C5F2D] hover:bg-[#F8F5EC]'
                  ]"
                >
                  High Contrast Mode
                </button>

                <div class="h-px bg-[#E5E7EB] my-3"></div>
                <p class="text-xs text-muted-foreground leading-relaxed">
                  Accessibility settings can be changed anytime.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="pt-36 pb-12">
      <div class="container mx-auto px-6 max-w-4xl text-center">
        <h1 class="text-4xl md:text-5xl mb-4 text-[#2C5F2D]">
          Questions about your lunchbox plan?
        </h1>
        <p class="text-xl text-muted-foreground max-w-2xl mx-auto">
          We're here to help you understand the science and care behind every recommendation we make for your family.
        </p>
      </div>
    </div>

    <!-- Why This Plan Section -->
    <div class="py-12">
      <div class="container mx-auto px-6 max-w-4xl">
        <div class="bg-white rounded-3xl shadow-sm p-8 md:p-12">
          <div class="flex items-center gap-3 mb-6">
            <h2 class="text-3xl text-[#2C5F2D]">Why This Plan?</h2>
          </div>

          <p class="text-muted-foreground mb-8">
            Select a saved plan to understand the nutritional thinking behind our recommendations.
          </p>

          <!-- Saved Plans Selector -->
          <div v-if="savedPlans.length" class="space-y-4 mb-8">
            <div
              v-for="plan in savedPlans"
              :key="plan.id"
              @click="selectedPlan = plan.id"
              :class="[
                'p-6 rounded-2xl border-2 cursor-pointer transition-all',
                selectedPlan === plan.id
                  ? 'border-[#A8D5BA] bg-[#A8D5BA]/5'
                  : 'border-gray-200 hover:border-[#A8D5BA]/50'
              ]"
            >
              <div class="flex items-start justify-between">
                <div class="flex items-start gap-4 flex-1">
                  <input
                    type="radio"
                    :checked="selectedPlan === plan.id"
                    class="mt-1"
                    @click.stop
                  />
                  <div class="flex-1">
                    <h3 class="text-lg font-medium mb-1">{{ plan.name }}</h3>
                    <p class="text-sm text-muted-foreground mb-3">{{ plan.description }}</p>
                    <div class="flex flex-wrap gap-2">
                      <span
                        v-for="tag in plan.tags"
                        :key="tag"
                        class="bg-[#A8D5BA]/20 text-[#2C5F2D] text-xs rounded-full px-3 py-1"
                      >
                        {{ tag }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="hidden sm:block w-36 h-24 rounded-2xl overflow-hidden border border-[#E5E7EB] ml-4 flex-shrink-0">
                  <img
                    :src="plan.image"
                    :alt="`${plan.name} meal preview`"
                    class="w-full h-full object-cover"
                  />
                </div>
              </div>
            </div>
          </div>
          <div v-else class="mb-8 rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-6 text-center">
            <p class="text-[#4B5563] mb-4">
              You do not have any saved plans yet. Please save a plan first to view explanations here.
            </p>
            <button
              type="button"
              class="px-5 py-2.5 rounded-lg bg-[#2C5F2D] text-white hover:bg-[#244E24] transition-colors"
              @click="goToWeeklyPlan"
            >
              Create Personalised Lunchbox Plan
            </button>
          </div>

          <!-- Plan Explanation -->
          <div v-if="selectedPlan" class="bg-[#FAF9F6] rounded-2xl p-6">
            <h3 class="text-lg font-medium mb-4 text-[#2C5F2D]">Why We Recommend This</h3>
            <div class="space-y-4">
              <div
                v-for="reason in getSelectedPlanReasons()"
                :key="reason.title"
                class="flex gap-3"
              >
                <div>
                  <h4 class="font-medium mb-1">{{ reason.title }}</h4>
                  <p class="text-sm text-muted-foreground">{{ reason.description }}</p>
                </div>
              </div>
            </div>
            <div class="mt-6 flex flex-wrap gap-3">
              <button
                type="button"
                class="px-4 py-2 rounded-lg bg-[#2C5F2D] text-white hover:bg-[#244E24] transition-colors"
                @click="modifyPlan"
              >
                Modify plan
              </button>
              <button
                type="button"
                class="px-4 py-2 rounded-lg border border-[#D1D5DB] text-[#374151] hover:bg-white transition-colors"
                @click="closePlan"
              >
                Close explanation
              </button>
            </div>
          </div>

          <div v-else-if="savedPlans.length" class="text-center py-8 text-muted-foreground">
            <p>Select a plan above to see detailed nutritional insights</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Why Choose LittleHelp Section -->
    <div class="py-12 pb-20 relative overflow-hidden">
      <div class="absolute inset-0 bg-[#FAF9F6]"></div>
      <div
        class="absolute inset-0 bg-center bg-cover opacity-60"
        style="background-image: url('https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1600');"
      ></div>
      <div class="absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-[#FAF9F6] via-[#FAF9F6]/70 to-transparent z-10"></div>
      <div class="container mx-auto px-6 max-w-4xl relative z-20">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl mb-4 text-[#2C5F2D]">Why Choose LittleHelp?</h2>
          <p class="text-xl text-muted-foreground">
            Backed by science, built with care for your family's wellbeing
          </p>
        </div>

        <!-- Stats Grid -->
        <div class="grid md:grid-cols-3 gap-6 mb-12">
          <div class="bg-white rounded-2xl p-8 text-center shadow-sm">
            <div class="text-5xl font-bold text-[#A8D5BA] mb-2">98%</div>
            <p class="text-sm text-muted-foreground">
              of parents report improved mealtime confidence
            </p>
          </div>

          <div class="bg-white rounded-2xl p-8 text-center shadow-sm">
            <div class="text-5xl font-bold text-[#F7B267] mb-2">3.5x</div>
            <p class="text-sm text-muted-foreground">
              more variety in children's diets within 4 weeks
            </p>
          </div>

          <div class="bg-white rounded-2xl p-8 text-center shadow-sm">
            <div class="text-5xl font-bold text-[#CDE7F0] mb-2">15min</div>
            <p class="text-sm text-muted-foreground">
              average time saved per day on meal planning
            </p>
          </div>
        </div>

        <!-- Key Benefits -->
        <div class="bg-white rounded-3xl shadow-sm p-8 md:p-12">
          <h3 class="text-2xl mb-8 text-center text-[#2C5F2D]">What Makes Us Different</h3>

          <div class="space-y-6">
            <!-- Benefit 1 -->
            <div class="flex gap-4">
              <div class="flex-1">
                <h4 class="text-lg font-medium mb-2">Science-Backed Nutrition</h4>
                <p class="text-muted-foreground leading-relaxed">
                  Every recommendation is grounded in peer-reviewed research on child development, cognitive function, and nutritional science. We translate complex studies into practical, everyday meals.
                </p>
              </div>
            </div>

            <!-- Benefit 2 -->
            <div class="flex gap-4">
              <div class="flex-1">
                <h4 class="text-lg font-medium mb-2">Seasonal & Fresh First</h4>
                <p class="text-muted-foreground leading-relaxed">
                  Our algorithm prioritizes ingredients at their peak season, ensuring maximum nutrient density, better taste, and lower environmental impact. Fresh food matters for growing bodies.
                </p>
              </div>
            </div>

            <!-- Benefit 3 -->
            <div class="flex gap-4">
              <div class="flex-1">
                <h4 class="text-lg font-medium mb-2">Personalized for Every Child</h4>
                <p class="text-muted-foreground leading-relaxed">
                  No two children are the same. We account for age, developmental stage, allergies, dietary restrictions, and specific nutritional needs to create truly individualized plans.
                </p>
              </div>
            </div>

            <!-- Benefit 4 -->
            <div class="flex gap-4">
              <div class="flex-1">
                <h4 class="text-lg font-medium mb-2">Built for Busy Parents</h4>
                <p class="text-muted-foreground leading-relaxed">
                  We understand your mornings are hectic. Our plans emphasize practical, time-efficient meals that don't compromise on nutrition. Real food for real life.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Research Foundation -->
        <div class="mt-12 relative rounded-3xl overflow-hidden">
          <div class="absolute inset-0 bg-white/90"></div>
          <div class="absolute inset-0 bg-gradient-to-br from-[#A8D5BA]/10 to-[#CDE7F0]/10"></div>

          <div class="relative z-10 p-8 md:p-12">
            <div class="flex items-start gap-4 mb-6">
              <div>
                <h3 class="text-2xl mb-2 text-[#2C5F2D]">Our Research Foundation</h3>
                <p class="text-muted-foreground leading-relaxed">
                  LittleHelp's recommendations are built on a foundation of pediatric nutrition research, child development studies, and dietary guidelines from leading health organizations including:
                </p>
              </div>
            </div>

            <div class="grid md:grid-cols-2 gap-4 text-sm text-muted-foreground">
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 bg-[#A8D5BA] rounded-full"></div>
                <span>WHO Dietary Guidelines for Children</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 bg-[#A8D5BA] rounded-full"></div>
                <span>Academy of Nutrition and Dietetics</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 bg-[#A8D5BA] rounded-full"></div>
                <span>Child Development Research</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 bg-[#A8D5BA] rounded-full"></div>
                <span>Seasonal Food & Sustainability Studies</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft, ChevronDown } from 'lucide-vue-next';
import logoUrl from '../assets/littlehelp-logo.jpg';

const router = useRouter();
const selectedPlan = ref(null);
const showAccessibilityMenu = ref(false);
const accessibilityMenuRef = ref(null);
const largeTextMode = ref(false);
const highContrastMode = ref(false);

// Mock saved plans
const savedPlans = ref([
  {
    id: '1',
    name: 'Emma\'s Spring Week Plan',
    description: 'Week of May 12-16, 2026 • 5 days',
    tags: ['Iron support', 'Dairy-free', 'Batch cooking 3x'],
    image: 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800',
  },
  {
    id: '2',
    name: 'Oliver\'s Balanced Nutrition',
    description: 'Week of May 12-16, 2026 • 5 days',
    tags: ['Calcium support', 'Nut-free', 'Batch cooking 2x'],
    image: 'https://images.pexels.com/photos/1211887/pexels-photo-1211887.jpeg?auto=compress&cs=tinysrgb&w=800',
  },
  {
    id: '3',
    name: 'Family Plan (Emma & Oliver)',
    description: 'Week of May 5-9, 2026 • 5 days',
    tags: ['Multi-child', 'Allergen-safe', 'Batch cooking 3x'],
    image: 'https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=800',
  },
]);

const planReasons = {
  '1': [
    {
      title: 'Iron-Rich Ingredients',
      description: 'We prioritize leafy greens, lentils, and fortified grains to support Emma\'s iron needs. These are paired with vitamin C sources to enhance absorption.',
    },
    {
      title: 'Dairy Alternatives',
      description: 'All meals use calcium-fortified plant milks and dairy-free proteins to ensure adequate nutrition without triggering allergies.',
    },
    {
      title: 'Seasonal Spring Produce',
      description: 'May brings peak-season asparagus, peas, and strawberries, which we feature for optimal freshness and nutrient density.',
    },
    {
      title: 'Age-Appropriate Portions',
      description: 'Meal sizes are calibrated for 6-9 year olds, balancing energy needs with healthy eating patterns.',
    },
  ],
  '2': [
    {
      title: 'Calcium-Focused Meals',
      description: 'Dairy products, fortified foods, and calcium-rich vegetables support Oliver\'s bone development during this critical growth phase.',
    },
    {
      title: 'Complete Nut Elimination',
      description: 'All recipes are carefully selected to avoid peanuts and tree nuts, with safe protein alternatives like seeds, beans, and legumes.',
    },
    {
      title: 'Variety for Picky Eaters',
      description: 'We include familiar favorites alongside gentle introductions to new foods, supporting healthy eating exploration for 3-6 year olds.',
    },
    {
      title: 'Texture & Color Balance',
      description: 'Meals are designed with appealing colors and age-appropriate textures to encourage engagement and enjoyment.',
    },
  ],
  '3': [
    {
      title: 'Multi-Child Nutrition Balance',
      description: 'This plan combines Emma and Oliver\'s nutritional needs, ensuring both get adequate iron, calcium, and age-appropriate portions.',
    },
    {
      title: 'Allergen-Safe for All',
      description: 'Every meal is free from dairy, peanuts, and tree nuts, making it safe for both children while maintaining nutritional completeness.',
    },
    {
      title: 'Efficient Batch Cooking',
      description: 'We consolidate meal prep into 3 sessions per week, saving you time while ensuring fresh, varied lunches for both kids.',
    },
    {
      title: 'Shared & Individual Components',
      description: 'Some elements are portioned differently for each child\'s age, while others can be shared, balancing efficiency with personalization.',
    },
  ],
};

const getSelectedPlanReasons = () => {
  return planReasons[selectedPlan.value] || [];
};

const modifyPlan = () => {
  router.push('/weekly-plan');
};

const closePlan = () => {
  selectedPlan.value = null;
};

const goToWeeklyPlan = () => {
  router.push('/weekly-plan');
};

const toggleAccessibilityMenu = () => {
  showAccessibilityMenu.value = !showAccessibilityMenu.value;
};

const persistAccessibilitySettings = () => {
  localStorage.setItem('littlehelp_accessibility_large_text', largeTextMode.value ? '1' : '0');
  localStorage.setItem('littlehelp_accessibility_high_contrast', highContrastMode.value ? '1' : '0');
};

const toggleLargeTextMode = () => {
  largeTextMode.value = !largeTextMode.value;
  persistAccessibilitySettings();
};

const toggleHighContrastMode = () => {
  highContrastMode.value = !highContrastMode.value;
  persistAccessibilitySettings();
};

const handleDocumentClick = (event) => {
  if (!showAccessibilityMenu.value) return;
  if (!accessibilityMenuRef.value?.contains(event.target)) {
    showAccessibilityMenu.value = false;
  }
};

onMounted(() => {
  largeTextMode.value = localStorage.getItem('littlehelp_accessibility_large_text') === '1';
  highContrastMode.value = localStorage.getItem('littlehelp_accessibility_high_contrast') === '1';
  document.addEventListener('click', handleDocumentClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick);
});
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}

.knowledgehub-root.large-text-mode {
  font-size: 1.06rem;
}

.knowledgehub-root.large-text-mode button,
.knowledgehub-root.large-text-mode p,
.knowledgehub-root.large-text-mode span,
.knowledgehub-root.large-text-mode h3,
.knowledgehub-root.large-text-mode h4 {
  font-size: 1.02em;
}

.knowledgehub-root.high-contrast-mode {
  color: #111827;
  filter: contrast(1.08);
}

.knowledgehub-root.high-contrast-mode .text-muted-foreground {
  color: #374151;
}
</style>
