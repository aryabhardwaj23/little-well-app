<template>
  <div class="min-h-screen py-12 bg-[#FAF9F6]">
    <div class="container mx-auto px-6 max-w-6xl">
      <!-- Back Button -->
      <button
        @click="router.push('/')"
        class="mb-6 px-4 py-2 hover:bg-white rounded-lg transition-colors inline-flex items-center gap-2"
        type="button"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Home
      </button>

      <!-- Loading / Error -->
      <div
        v-if="isLoading"
        class="mb-8 p-4 bg-white rounded-xl border text-center text-muted-foreground"
      >
        Loading...
      </div>

      <div
        v-if="errorMessage"
        class="mb-8 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl"
      >
        {{ errorMessage }}
      </div>

      <!-- Header -->
      <div v-if="!planGenerated" class="text-center mb-12">
        <h1 class="text-4xl mb-4">Plan Your Week, Simply</h1>
        <p class="text-lg text-muted-foreground mb-6">
          Build a weekly lunchbox plan using saved child profiles, database lunchbox recommendations,
          and recipe inspiration.
        </p>

        <div class="inline-flex items-center gap-2 bg-white rounded-full px-6 py-3 shadow-sm border">
          <component :is="getSeasonIcon()" class="w-5 h-5 text-[#A8D5BA]" />
          <span class="font-medium">{{ getSeasonName() }} Plan</span>
        </div>
      </div>

      <!-- Select Children -->
      <div v-if="!planGenerated" class="mb-12">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl">Select Children</h2>

          <button
            v-if="profiles.length === 0"
            @click="router.push('/child-info')"
            class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] px-5 py-2 rounded-lg transition-colors"
            type="button"
          >
            Add a Child
          </button>
        </div>

        <div v-if="profiles.length === 0" class="p-8 bg-white border rounded-2xl text-center">
          <p class="text-muted-foreground mb-4">
            No child profiles found. Create a child profile first to generate a weekly plan.
          </p>

          <button
            @click="router.push('/child-info')"
            class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] px-8 py-3 rounded-lg transition-colors"
            type="button"
          >
            Create Child Profile
          </button>
        </div>

        <div v-else class="grid md:grid-cols-3 gap-4">
          <div
            v-for="profile in profiles"
            :key="profile.id"
            @click="toggleChildSelection(profile.id)"
            :class="[
              'p-6 rounded-2xl border-2 cursor-pointer transition-all',
              selectedChildren.includes(profile.id)
                ? 'border-[#A8D5BA] bg-[#A8D5BA]/10'
                : 'border-gray-200 hover:border-[#A8D5BA]/50 bg-white'
            ]"
          >
            <div class="flex items-start gap-3">
              <input
                type="checkbox"
                :checked="selectedChildren.includes(profile.id)"
                class="mt-1"
                @click.stop
              />

              <div class="flex-1">
                <h3 class="text-lg font-medium mb-1">{{ profile.name }}</h3>
                <p class="text-sm text-muted-foreground mb-3">{{ profile.ageGroup }}</p>

                <div v-if="profile.allergies.length > 0" class="mb-2">
                  <p class="text-xs text-muted-foreground mb-1">Allergies</p>

                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="allergy in profile.allergies"
                      :key="allergy"
                      class="text-xs bg-[#F7B267]/20 text-[#8B4513] px-2 py-0.5 rounded-full"
                    >
                      {{ allergy }}
                    </span>
                  </div>
                </div>

                <div v-if="profile.nutritionFocus.length > 0">
                  <p class="text-xs text-muted-foreground mb-1">Focus</p>

                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="focus in profile.nutritionFocus.slice(0, 2)"
                      :key="focus"
                      class="text-xs bg-[#A8D5BA]/20 text-[#2C5F2D] px-2 py-0.5 rounded-full"
                    >
                      {{ focus }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="selectedChildren.length > 0"
          class="mt-4 p-4 bg-white rounded-lg border text-center"
        >
          <p class="text-sm">
            <strong class="text-[#2C5F2D]">
              {{ selectedChildren.length }} child(ren) selected
            </strong>
          </p>
        </div>
      </div>

      <!-- Cooking Frequency -->
      <div v-if="!planGenerated" class="mb-12">
        <h2 class="text-2xl mb-6">How often do you want to cook this week?</h2>

        <div class="grid md:grid-cols-3 gap-6">
          <div
            v-for="option in frequencyOptions"
            :key="option.value"
            @click="cookingFrequency = option.value"
            :class="[
              'p-8 rounded-2xl border-2 cursor-pointer transition-all text-center',
              cookingFrequency === option.value
                ? option.activeClass
                : 'border-gray-200 hover:border-[#A8D5BA]/50 bg-white'
            ]"
          >
            <div
              :class="[
                'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4',
                option.iconClass
              ]"
            >
              <ChefHat class="w-8 h-8" :class="option.iconTextClass" />
            </div>

            <h3 class="text-2xl font-bold mb-2">{{ option.label }}</h3>
            <p class="text-sm text-muted-foreground">{{ option.description }}</p>
          </div>
        </div>
      </div>