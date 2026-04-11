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
