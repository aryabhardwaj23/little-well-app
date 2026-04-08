<template>
  <div class="min-h-screen py-12">
    <div class="container mx-auto px-6 max-w-3xl">
      <!-- Back Button -->
      <button
        @click="router.push('/')"
        class="mb-6 px-4 py-2 hover:bg-gray-100 rounded-lg transition-colors inline-flex items-center gap-2"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Home
      </button>

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl mb-4">Quick Meal Suggestions</h1>
        <p class="text-lg text-muted-foreground">
          Just a couple of quick questions to get you started
        </p>
      </div>

      <!-- Age Group Selection -->
      <div class="p-8 rounded-2xl shadow-sm mb-8 bg-white border">
        <label class="text-lg mb-4 block font-medium">What's your child's age?</label>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <button
            v-for="age in ageGroups"
            :key="age"
            @click="ageGroup = age"
            :class="[
              'p-4 rounded-lg border-2 transition-all',
              ageGroup === age
                ? 'border-[#A8D5BA] bg-[#A8D5BA]/10 text-[#2C5F2D]'
                : 'border-gray-200 hover:border-[#A8D5BA]/50'
            ]"
          >
            {{ age }}
          </button>
        </div>
      </div>