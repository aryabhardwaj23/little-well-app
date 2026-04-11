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