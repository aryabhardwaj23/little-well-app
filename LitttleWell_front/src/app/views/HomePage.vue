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