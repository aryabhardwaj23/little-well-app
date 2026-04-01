<template>
  <div class="min-h-screen">
    <!-- Navigation Bar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex items-center gap-2">
            <div class="w-10 h-10 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center">
              <Heart class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-semibold text-[#2C5F2D]">LittleWell</span>
          </div>

          <!-- Navigation Links -->
          <div class="hidden md:flex items-center gap-6">
            <button
              @click="router.push('/results')"
              class="text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg px-4 py-2 transition-colors"
            >
              Lunchbox Plan
            </button>
            
            <button
              disabled
              class="text-muted-foreground cursor-not-allowed relative px-4 py-2"
            >
              <BookOpen class="w-4 h-4 inline mr-2" />
              Knowledge Hub
              <span class="absolute -top-1 -right-2 bg-[#CDE7F0] text-[#1B4965] text-xs rounded-full px-1.5 py-0.5">
                Soon
              </span>
            </button>
            
            <button
              disabled
              class="text-muted-foreground cursor-not-allowed relative px-4 py-2"
            >
              <ScanLine class="w-4 h-4 inline mr-2" />
              Label Reader
              <span class="absolute -top-1 -right-2 bg-[#CDE7F0] text-[#1B4965] text-xs rounded-full px-1.5 py-0.5">
                Soon
              </span>
            </button>

            <button
              @click="router.push('/about')"
              class="text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg px-4 py-2 transition-colors"
            >
              About Us
            </button>
          </div>

          <!-- Mobile Menu Button -->
          <button class="md:hidden p-2">
            <Menu class="w-5 h-5" />
          </button>
        </div>
      </div>
    </nav>

    <div class="relative h-[500px] overflow-hidden mt-16">
      <img
        src="https://images.unsplash.com/photo-1758874961000-d8b11690ce22?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXJlbnQlMjBjb29raW5nJTIwd2l0aCUyMGNoaWxkJTIwa2l0Y2hlbnxlbnwxfHx8fDE3NzQzNDI2MjF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
        alt="Parent cooking with child"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-r from-black/60 to-black/30" />
      
      <div class="absolute inset-0 flex items-center">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="max-w-2xl text-white">
            <h1 class="text-5xl md:text-6xl mb-6 leading-tight">
              Seasonal, fresh lunchboxes made simple for your family
            </h1>
            <p class="text-xl md:text-2xl text-white/90">
              Science-backed nutrition with fresh, seasonal ingredients.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 2: Your Family Profiles -->
    <div class="py-16 bg-white">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl mb-2">Your Family Profiles</h2>
            <p class="text-muted-foreground">
              Personalised nutrition support for each child
            </p>
          </div>
        </div>

        <!-- Horizontal Scroll Cards -->
        <div class="flex gap-6 overflow-x-auto pb-4 -mx-6 px-6">
          <div
            v-for="profile in profiles"
            :key="profile.id"
            class="flex-shrink-0 w-[340px] p-6 rounded-2xl shadow-md hover:shadow-lg transition-shadow bg-white border"
          >
            <!-- Profile Header -->
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="text-xl mb-1">
                  {{ profile.name }} <span class="text-muted-foreground text-base">({{ profile.ageGroup }})</span>
                </h3>
              </div>
              <button
                @click="handleEditProfile(profile.id)"
                class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Edit class="w-4 h-4" />
              </button>
            </div>

            <!-- Profile Info -->
            <div class="space-y-3 mb-4">
              <div v-if="profile.allergies.length > 0">
                <p class="text-xs text-muted-foreground mb-1">Allergies</p>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="allergy in profile.allergies"
                    :key="allergy"
                    class="bg-[#F7B267]/20 text-[#8B4513] text-xs rounded-full px-2 py-1"
                  >
                    {{ allergy }}
                  </span>
                </div>
              </div>

              <div v-if="profile.dietaryRestriction">
                <p class="text-xs text-muted-foreground mb-1">Dietary restriction</p>
                <span class="bg-[#CDE7F0]/30 text-[#1B4965] text-xs rounded-full px-2 py-1 inline-block">
                  {{ profile.dietaryRestriction }}
                </span>
              </div>

              <div v-if="profile.nutritionFocus.length > 0">
                <p class="text-xs text-muted-foreground mb-1">Nutrition focus</p>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="focus in profile.nutritionFocus"
                    :key="focus"
                    class="bg-[#A8D5BA]/20 text-[#2C5F2D] text-xs rounded-full px-2 py-1"
                  >
                    {{ focus }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Action Button -->
            <button
              @click="handleViewMeals(profile.id)"
              class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-3 flex items-center justify-center gap-2 transition-colors"
            >
              View Lunchboxes
              <ChevronRight class="w-4 h-4" />
            </button>
          </div>

          <!-- Add New Profile Card -->
          <div class="flex-shrink-0 w-[340px] p-6 rounded-2xl border-2 border-dashed border-gray-300 flex flex-col items-center justify-center hover:border-[#A8D5BA] transition-colors cursor-pointer">
            <button
              @click="router.push('/child-profile')"
              class="flex flex-col items-center gap-3"
            >
              <div class="w-16 h-16 bg-[#A8D5BA]/10 rounded-full flex items-center justify-center">
                <Plus class="w-8 h-8 text-[#A8D5BA]" />
              </div>
              <p class="text-lg text-[#2C5F2D]">Add a child</p>
              <p class="text-sm text-muted-foreground text-center">
                Create a profile to get personalised meal suggestions
              </p>
            </button>
          </div>
        </div>
      </div>
    </div>