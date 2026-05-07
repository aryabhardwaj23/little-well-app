<template>
  <div
    :class="[
      'min-h-screen home-root',
      { 'large-text-mode': largeTextMode, 'high-contrast-mode': highContrastMode }
    ]"
  >
    <!-- Navigation Bar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="mx-auto px-8 max-w-[1440px]">
        <div class="flex items-center justify-between h-20 gap-8">
          <!-- Logo -->
          <div class="flex items-center cursor-pointer shrink-0" @click="router.push('/')">
            <img
              :src="littleHelpLogo"
              alt="LittleHelp logo"
              class="h-12 w-auto object-contain"
            />
          </div>

          <!-- Desktop Navigation Links -->
          <div class="flex items-center justify-end gap-2 flex-1">
            <button @click="handleLunchboxPlan" class="nav-link" type="button">
              Lunchbox Plan
            </button>

            <button @click="goProtected('/weekly-plan')" class="nav-link" type="button">
              Weekly Plan
            </button>

            <button @click="goProtected('/my-plans')" class="nav-link" type="button">
              My Plans
            </button>

            <button @click="router.push('/knowledge-hub-prototype')" class="nav-link" type="button">
              Knowledge Hub
            </button>

            <button @click="router.push('/about')" class="nav-link" type="button">
              About Us
            </button>

            <div ref="accessibilityMenuRef" class="relative">
              <button
                @click="toggleAccessibilityMenu"
                class="nav-link inline-flex items-center gap-1"
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
                  @click="toggleInteractiveGuide"
                  class="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors text-[#2C5F2D] hover:bg-[#F8F5EC]"
                >
                  Interactive Guide
                </button>

                <button
                  type="button"
                  @click="toggleLargeTextMode"
                  :class="[
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors mt-2',
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
                  Need help understanding the system? Accessibility settings can be changed anytime.
                </p>
              </div>
            </div>

            <!-- Auth Buttons -->
            <template v-if="isLoggedIn">
              <span class="text-sm text-muted-foreground px-2 whitespace-nowrap">
                Hi, {{ username }}
              </span>

              <button @click="handleLogout" class="nav-outline-button" type="button">
                Logout
              </button>
            </template>

            <template v-else>
              <button @click="router.push('/login')" class="nav-link nav-signin-link" type="button">
                Sign in
              </button>

              <button @click="router.push('/register')" class="nav-primary-button" type="button">
                Create account
              </button>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- User Guide Overlay -->
    <div v-if="showGuide" class="fixed inset-0 z-[100] pointer-events-none">
      <div class="absolute inset-0 bg-black/20"></div>

      <!-- Highlight Box -->
      <div
        v-if="highlightStyle"
        class="guide-highlight"
        :style="highlightStyle"
      ></div>

      <!-- Tooltip Card -->
      <div
        v-if="tooltipStyle"
        class="guide-tooltip pointer-events-auto"
        :style="tooltipStyle"
      >
        <p class="text-sm text-[#2C5F2D] font-semibold mb-2">
          Step {{ guideStep + 1 }} of {{ guideSteps.length }}
        </p>

        <h2 class="text-2xl text-[#2C5F2D] mb-3">
          {{ guideSteps[guideStep].title }}
        </h2>

        <p class="text-muted-foreground leading-relaxed">
          {{ guideSteps[guideStep].text }}
        </p>

        <div class="flex items-center justify-between mt-8">
          <button
            @click="skipGuide"
            class="px-4 py-2 text-gray-500 hover:text-gray-700 transition-colors"
            type="button"
          >
            Skip
          </button>

          <div class="flex items-center gap-2">
            <span
              v-for="(_, index) in guideSteps"
              :key="index"
              :class="[
                'w-2 h-2 rounded-full transition-colors',
                index === guideStep ? 'bg-[#2C5F2D]' : 'bg-gray-300'
              ]"
            ></span>
          </div>

          <button
            @click="nextGuideStep"
            class="px-5 py-2 bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg font-semibold transition-colors"
            type="button"
          >
            {{ guideStep === guideSteps.length - 1 ? 'Finish' : 'Next' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Hero Section -->
    <div ref="heroSection" class="hero-section pt-32 pb-14 bg-[#FAF9F6]">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="grid lg:grid-cols-2 gap-8 items-stretch">
          <div class="flex flex-col justify-center">
            <h1 class="text-4xl md:text-5xl leading-tight text-[#2C5F2D] mb-5">
              Fresh lunchbox planning made simple
            </h1>

            <p class="text-lg text-muted-foreground leading-relaxed max-w-xl">
              Create balanced lunchbox ideas for children aged 5–12 based on age, allergies and food preferences.
            </p>

            <div class="mt-8 space-y-4">
              <div ref="quickStartTarget" class="relative group">
                <button
                  @click="router.push('/quick-start')"
                  class="w-full bg-[#F8F5EC] rounded-2xl border border-[#E8DDC8] p-5 shadow-sm hover:shadow-md hover:border-[#DDCFB2] hover:bg-[#F5F0E4] transition-all text-left flex flex-col gap-4"
                  type="button"
                >
                  <p class="text-xl text-[#315F3A]">Try Quick Start</p>
                  <p class="text-sm text-[#315F3A] font-semibold">
                    Try a lunchbox plan in 1 minute
                  </p>
                </button>

                <div
                  class="hidden md:block absolute left-0 right-0 bottom-full mb-3 bg-white border border-[#A8D5BA]/40 rounded-xl shadow-lg p-4 text-sm text-muted-foreground leading-relaxed opacity-0 translate-y-1 pointer-events-none transition-all duration-200 group-hover:opacity-100 group-hover:translate-y-0 group-focus-within:opacity-100 group-focus-within:translate-y-0"
                >
                  Quick Start gently helps you begin with confidence — no profile setup needed. Choose age and optional allergies to generate a balanced lunchbox plan you can use right away.
                </div>

                <p class="md:hidden mt-2 text-xs text-muted-foreground leading-relaxed">
                  Quick Start lets you try a ready-to-use lunchbox recommendation without creating a profile first.
                </p>
              </div>

              <div ref="personalisedTarget" class="relative group">
                <button
                  @click="handleAddChild"
                  class="w-full bg-[#E5F2E8] rounded-2xl border border-[#8FC2A4]/60 p-5 shadow-sm hover:shadow-md hover:border-[#7DB593]/70 hover:bg-[#D9ECDF] transition-all text-left flex flex-col gap-4"
                  type="button"
                >
                  <p class="text-xl text-[#2C5F2D]">Get Personalised Lunchbox</p>
                  <p class="text-sm text-[#2C5F2D] font-semibold">
                    Start by creating a child profile around your nutrition needs
                  </p>
                </button>

                <div
                  class="hidden md:block absolute left-0 right-0 bottom-full mb-3 bg-white border border-[#A8D5BA]/40 rounded-xl shadow-lg p-4 text-sm text-muted-foreground leading-relaxed opacity-0 translate-y-1 pointer-events-none transition-all duration-200 group-hover:opacity-100 group-hover:translate-y-0 group-focus-within:opacity-100 group-focus-within:translate-y-0"
                >
                  Child Profile enables deeper personalisation. Save age, allergies, and food preferences to generate smarter lunchboxes and weekly plans.
                </div>

                <p class="md:hidden mt-2 text-xs text-muted-foreground leading-relaxed">
                  Save profile details for a more personalised and long-term lunchbox planning experience.
                </p>
              </div>
            </div>
          </div>

          <div class="relative flex items-center">
            <img
              src="https://images.pexels.com/photos/4252139/pexels-photo-4252139.jpeg?auto=compress&cs=tinysrgb&w=1400"
              alt="Healthy lunchbox ingredients and family-style meal prep"
              class="w-full h-[620px] object-cover rounded-3xl shadow-md"
            />

            <div class="absolute bottom-5 left-5 right-5 rounded-2xl shadow-md p-4 overflow-hidden">
              <div class="absolute inset-0 rounded-2xl bg-gradient-to-b from-transparent via-white/45 to-transparent backdrop-blur-sm"></div>
              <div class="relative z-10 grid sm:grid-cols-3 gap-3">
                <div class="rounded-xl bg-[#CDE7F0]/45 p-3 flex flex-col">
                  <p class="text-sm font-semibold text-[#374151] leading-snug">
                    Simplify nutrition choices
                  </p>
                  <div class="w-full h-12 rounded-full overflow-hidden mt-2">
                    <img
                      src="https://images.pexels.com/photos/1132047/pexels-photo-1132047.jpeg?auto=compress&cs=tinysrgb&w=800"
                      alt="Fresh vegetables fruits and milk ingredients"
                      class="w-full h-full object-cover"
                    />
                  </div>
                </div>

                <div class="rounded-xl bg-[#CDE7F0]/45 p-3 flex flex-col">
                  <p class="text-sm font-semibold text-[#374151] leading-snug">
                    Personalise for each child
                  </p>
                  <div class="w-full h-12 rounded-full overflow-hidden mt-2">
                    <img
                      src="https://images.pexels.com/photos/3872370/pexels-photo-3872370.jpeg?auto=compress&cs=tinysrgb&w=800"
                      alt="Parent preparing vegetables"
                      class="w-full h-full object-cover"
                    />
                  </div>
                </div>

                <div class="rounded-xl bg-[#CDE7F0]/45 p-3 flex flex-col">
                  <p class="text-sm font-semibold text-[#374151] leading-snug">
                    Plan healthier lunchboxes
                  </p>
                  <div class="w-full h-12 rounded-full overflow-hidden mt-2">
                    <img
                      src="https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800"
                      alt="Weekly meal prep containers"
                      class="w-full h-full object-cover"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!isLoggedIn" class="mt-8 bg-white border rounded-2xl p-5 text-center shadow-sm">
          <p class="text-muted-foreground">
            Sign in to save child profiles, weekly plans, and personalised recommendations.
          </p>
          <div class="flex justify-center gap-3 mt-4">
            <button
              @click="router.push('/login')"
              class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg px-6 py-2 transition-colors"
              type="button"
            >
              Sign in
            </button>
            <button
              @click="router.push('/register')"
              class="bg-white border border-[#A8D5BA] text-[#2C5F2D] rounded-lg px-6 py-2 hover:bg-[#A8D5BA]/10 transition-colors"
              type="button"
            >
              Create account
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Child Profile Section -->
    <div ref="childProfileSection" class="child-profile-section pt-14 pb-8 bg-white">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="mb-8">
          <h2 class="text-3xl mb-2 text-[#2C5F2D]">Your child profiles</h2>
          <p class="text-muted-foreground max-w-3xl">
            Manage profiles for children aged 5–12 and generate personalised lunchbox ideas whenever you need.
          </p>
        </div>

        <div v-if="!isLoggedIn" class="p-8 rounded-2xl border bg-[#FAF9F6] text-center">
          <p class="text-muted-foreground mb-5">
            Please sign in to view and manage your child profiles.
          </p>
          <button
            @click="router.push({ path: '/login', query: { redirect: '/child-info' } })"
            class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg px-8 py-3 transition-colors"
            type="button"
          >
            Sign in to continue
          </button>
        </div>

        <div v-else>
          <div
            v-if="isLoadingProfiles"
            class="mb-6 p-4 bg-[#FAF9F6] border rounded-xl text-center text-muted-foreground"
          >
            Loading profiles...
          </div>

          <div class="flex gap-6 overflow-x-auto pb-4 -mx-6 px-6">
            <div
              @click="handleAddChild"
              class="flex-shrink-0 w-[340px] min-h-[260px] p-6 rounded-2xl border-2 border-dashed border-[#A8D5BA] bg-[#A8D5BA]/5 flex flex-col items-center justify-center hover:bg-[#A8D5BA]/10 transition-colors cursor-pointer"
            >
              <div class="w-16 h-16 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center mb-3">
                <Plus class="w-8 h-8 text-[#2C5F2D]" />
              </div>
              <p class="text-lg text-[#2C5F2D] font-semibold">Add another child</p>
              <p class="text-sm text-muted-foreground text-center mt-2">
                Create a profile for a child aged 5–12 to get personalised meal suggestions
              </p>
            </div>

            <div
              v-for="profile in profiles"
              :key="profile.id"
              class="flex-shrink-0 w-[340px] p-6 rounded-2xl shadow-md hover:shadow-lg transition-shadow bg-white border"
            >
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="text-xl mb-1">
                    {{ profile.name }}
                    <span class="text-muted-foreground text-base">({{ profile.ageGroup }})</span>
                  </h3>
                </div>

                <div class="flex items-center gap-2">
                  <button
                    @click.stop="handleEditProfile(profile.id)"
                    class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    title="Edit profile"
                    type="button"
                  >
                    <Edit class="w-4 h-4" />
                  </button>

                  <button
                    @click.stop="handleDeleteProfile(profile.id, profile.name)"
                    class="p-2 hover:bg-red-50 rounded-lg transition-colors text-red-600"
                    title="Delete profile"
                    type="button"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </div>

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

              <button
                @click="handleViewMeals(profile.id)"
                class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-3 flex items-center justify-center gap-2 transition-colors"
                type="button"
              >
                Get Personalised Lunchboxes
                <ChevronRight class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Family Meal Planning -->
    <div ref="familySection" class="family-section pt-6 pb-12 bg-white">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="mb-8">
          <h2 class="text-3xl mb-2 text-[#2C5F2D]">Planning for more than one child?</h2>
          <p class="text-muted-foreground max-w-4xl leading-relaxed">
            We know every child has different needs. Select multiple profiles to generate family lunchbox ideas that consider each child's age, allergies and preferences, making busy mornings a little easier.
          </p>
        </div>

        <div class="p-8 rounded-2xl shadow-sm bg-white border">
          <p v-if="!isLoggedIn" class="text-sm text-muted-foreground mb-6">
            Sign in first to create child profiles and generate a family lunchbox plan.
          </p>

          <p v-else-if="profiles.length < 2" class="text-sm text-muted-foreground mb-6">
            Add at least two supported child profiles to generate a family lunchbox plan.
          </p>

          <div
            class="grid md:grid-cols-3 gap-4 mb-8"
            :class="{ 'opacity-60': !isLoggedIn || profiles.length < 2 }"
          >
            <div
              v-for="profile in profiles"
              :key="profile.id"
              @click="toggleFamilySelection(profile.id)"
              :class="[
                'p-4 rounded-xl border-2 cursor-pointer transition-all',
                selectedForFamily.includes(profile.id)
                  ? 'border-[#A8D5BA] bg-[#A8D5BA]/10'
                  : 'border-gray-200 hover:border-[#A8D5BA]/50'
              ]"
            >
              <div class="flex items-start gap-3">
                <input
                  type="checkbox"
                  :checked="selectedForFamily.includes(profile.id)"
                  class="mt-1"
                  @click.stop
                />

                <div class="flex-1">
                  <h4 class="font-medium mb-1">{{ profile.name }}</h4>
                  <p class="text-sm text-muted-foreground mb-2">
                    {{ profile.ageGroup }}
                  </p>

                  <div v-if="profile.nutritionFocus.length > 0" class="flex flex-wrap gap-1">
                    <span
                      v-for="focus in profile.nutritionFocus.slice(0, 2)"
                      :key="focus"
                      class="bg-[#A8D5BA]/20 text-[#2C5F2D] text-xs rounded-full px-2 py-0.5"
                    >
                      {{ focus }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="selectedForFamily.length > 0" class="bg-[#CDE7F0]/20 rounded-xl p-4 mb-6">
            <p class="text-sm text-center">
              <strong>{{ selectedForFamily.length }} children selected</strong> – Meals will be tailored to combine their nutrition needs
            </p>
          </div>

          <button
            @click="handleGenerateFamilyPlan"
            :disabled="!isLoggedIn || selectedForFamily.length === 0 || profiles.length < 2"
            class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            type="button"
          >
            Generate Family Lunchboxes
          </button>
        </div>
      </div>
    </div>

    <!-- Weekly Plan Section -->
    <div ref="weeklySection" class="weekly-section py-12 bg-[#FAF9F6]">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex flex-col md:flex-row md:items-center gap-8">
          <div class="w-16 h-16 bg-[#A8D5BA] rounded-full flex items-center justify-center flex-shrink-0">
            <CalendarDays class="w-8 h-8 text-[#2C5F2D]" />
          </div>

          <div class="flex-1">
            <h2 class="text-3xl mb-2 text-[#2C5F2D]">Plan the whole school week</h2>
            <p class="text-muted-foreground leading-relaxed">
              Choose your children, set your cooking frequency, and generate a weekly lunchbox plan that is practical, reusable, and easier to follow on busy school days.
            </p>
          </div>

          <div class="flex flex-col sm:flex-row gap-3">
            <button
              @click="goProtected('/weekly-plan')"
              class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg px-8 py-3 font-semibold transition-colors"
              type="button"
            >
              Build Weekly Plan
            </button>

            <button
              @click="goProtected('/my-plans')"
              class="bg-white hover:bg-[#FAF9F6] text-[#2C5F2D] border border-[#A8D5BA] rounded-lg px-8 py-3 font-semibold transition-colors"
              type="button"
            >
              View My Plans
            </button>
          </div>
        </div>

        <img
          src="https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg?auto=compress&cs=tinysrgb&w=1200"
          alt="Weekly meal prep containers on a table"
          class="mt-7 w-full h-52 object-cover rounded-2xl"
        />
      </div>
    </div>

    <!-- Knowledge Hub Entry -->
    <section class="relative overflow-hidden py-16">
      <div class="absolute inset-0 bg-gradient-to-br from-[#F3E9D7]/80 to-[#FAF9F6]"></div>
      <div
        class="absolute inset-0 bg-center bg-cover opacity-55"
        style="background-image: url('https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1600');"
      ></div>
      <div class="absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-[#FAF9F6] via-[#FAF9F6]/65 to-transparent"></div>

      <div class="container mx-auto px-6 max-w-5xl relative z-10 mt-4">
        <div class="bg-white/85 backdrop-blur-[1px] border border-[#E6E2D8] rounded-3xl p-8 md:p-12 text-center shadow-sm">
          <h2 class="text-3xl text-[#2C5F2D]">Questions about your lunchbox plan?</h2>
          <p class="mt-2 text-muted-foreground leading-relaxed">Why Choose LittleHelp</p>

          <button
            @click="router.push('/knowledge-hub-prototype')"
            class="mt-7 bg-[#2C5F2D] hover:bg-[#254F25] text-white rounded-lg px-8 py-3 font-semibold transition-colors"
            type="button"
          >
            Click to enter Knowledge Hub
          </button>
        </div>
      </div>
    </section>

    <footer class="relative bg-[#FAF9F6] border-t border-gray-200 pt-16 pb-12 overflow-visible">
      <div class="absolute -top-24 left-0 right-0 h-24 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6]/75 to-transparent pointer-events-none z-30"></div>
      <div class="absolute top-0 left-0 right-0 h-16 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6]/70 to-transparent pointer-events-none"></div>

      <div class="container mx-auto px-6 max-w-5xl text-center relative z-10">
        <h2 class="text-2xl text-[#2C5F2D]">LittleHelp</h2>

        <p class="mt-4 text-muted-foreground max-w-3xl mx-auto leading-relaxed">
          Helping families create practical, balanced, and child-friendly lunchbox plans through science-backed nutrition guidance.
        </p>

        <div class="mt-6 flex flex-wrap items-center justify-center gap-x-4 gap-y-2 text-sm text-[#2C5F2D]">
          <button @click="handleLunchboxPlan" type="button" class="hover:underline">Lunchbox Plan</button>
          <button @click="goProtected('/weekly-plan')" type="button" class="hover:underline">Weekly Plan</button>
          <button @click="goProtected('/my-plans')" type="button" class="hover:underline">My Plans</button>
          <button @click="router.push('/knowledge-hub-prototype')" type="button" class="hover:underline">Knowledge Hub</button>
          <button @click="router.push('/about')" type="button" class="hover:underline">About Us</button>
          <button @click="openAccessibilityFromFooter" type="button" class="hover:underline">Accessibility</button>
        </div>

        <p class="mt-6 text-xs text-muted-foreground">
          © 2026 LittleHelp. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import {
  Plus,
  Edit,
  Trash2,
  ChevronRight,
  ChevronDown,
  CalendarDays,
} from 'lucide-vue-next';
import { getChildren, deleteChild } from '../services/api';
import { useAuthStore } from '../stores/auth';
import littleHelpLogo from '../assets/littlehelp-logo.jpg';

const router = useRouter();
const authStore = useAuthStore();

const profiles = ref([]);
const selectedForFamily = ref([]);
const isLoadingProfiles = ref(false);

const heroSection = ref(null);
const quickStartTarget = ref(null);
const personalisedTarget = ref(null);
const childProfileSection = ref(null);
const familySection = ref(null);
const weeklySection = ref(null);

const showGuide = ref(false);
const guideStep = ref(0);
const highlightBox = ref(null);
const tooltipBox = ref(null);
const showAccessibilityMenu = ref(false);
const accessibilityMenuRef = ref(null);
const largeTextMode = ref(false);
const highContrastMode = ref(false);

const guideSteps = [
  {
    title: 'Welcome to LittleHelp',
    text: 'LittleHelp helps families create balanced lunchbox ideas for children aged 5–12.',
    target: 'hero',
  },
  {
    title: 'Try Quick Start',
    text: 'Use Quick Start to generate a lunchbox idea without creating a child profile first.',
    target: 'quickStart',
  },
  {
    title: 'Create a Child Profile',
    text: 'Create a child profile to get personalised lunchbox recommendations based on age, allergies, and nutrition needs.',
    target: 'personalised',
  },
  {
    title: 'Manage Child Profiles',
    text: 'Here you can add, edit, delete, and manage child profiles for personalised recommendations.',
    target: 'child',
  },
  {
    title: 'Plan for Multiple Children',
    text: 'Select more than one child to generate family lunchbox ideas that consider different needs.',
    target: 'family',
  },
  {
    title: 'Weekly Planning',
    text: 'Use Weekly Plan to build a practical lunchbox plan for the whole school week.',
    target: 'weekly',
  },
];

const isLoggedIn = computed(() => authStore.isAuthenticated);
const username = computed(() => authStore.user?.username || 'User');

const allergenIdToName = {
  47: 'Peanuts',
  40: 'Tree nuts',
  16: 'Milk',
  18: 'Eggs',
  24: 'Wheat',
  50: 'Soy',
  22: 'Fish',
  15: 'Shellfish',
};

const nutritionFocusLabels = {
  iron: 'Iron Support',
  calcium: 'Calcium Support',
  brain: 'Brain Development',
  immunity: 'Immune Support',
  vitamin_d: 'Vitamin D Support',
  energy: 'Sustained Energy',
  variety: 'Diet Variety',
};

const allowedAgeGroups = ['5-6 years', '7-9 years', '10-12 years'];

const getGuideTargetElement = () => {
  const target = guideSteps[guideStep.value]?.target;

  const targetMap = {
    hero: heroSection,
    quickStart: quickStartTarget,
    personalised: personalisedTarget,
    child: childProfileSection,
    family: familySection,
    weekly: weeklySection,
  };

  return targetMap[target]?.value || null;
};

const updateGuidePosition = () => {
  if (!showGuide.value) return;

  const element = getGuideTargetElement();

  if (!element) {
    highlightBox.value = null;
    tooltipBox.value = null;
    return;
  }

  const rect = element.getBoundingClientRect();
  const padding = 10;
  const tooltipWidth = Math.min(360, window.innerWidth - 32);
  const gap = 18;

  const highlightTop = Math.max(rect.top - padding, 88);
  const highlightLeft = Math.max(rect.left - padding, 16);
  const highlightWidth = Math.min(rect.width + padding * 2, window.innerWidth - highlightLeft - 16);
  const highlightHeight = Math.min(rect.height + padding * 2, window.innerHeight - highlightTop - 16);

  highlightBox.value = {
    top: highlightTop,
    left: highlightLeft,
    width: highlightWidth,
    height: highlightHeight,
  };

  let tooltipLeft = highlightLeft + highlightWidth + gap;
  let tooltipTop = highlightTop;

  if (tooltipLeft + tooltipWidth > window.innerWidth - 24) {
    tooltipLeft = highlightLeft;
    tooltipTop = highlightTop + highlightHeight + gap;
  }

  if (tooltipTop + 280 > window.innerHeight - 24) {
    tooltipTop = Math.max(96, highlightTop - 280 - gap);
  }

  if (tooltipLeft < 16) {
    tooltipLeft = 16;
  }

  if (tooltipTop < 96) {
    tooltipTop = 96;
  }

  tooltipBox.value = {
    top: tooltipTop,
    left: tooltipLeft,
    width: tooltipWidth,
  };
};

const highlightStyle = computed(() => {
  if (!highlightBox.value) return null;

  return {
    top: `${highlightBox.value.top}px`,
    left: `${highlightBox.value.left}px`,
    width: `${highlightBox.value.width}px`,
    height: `${highlightBox.value.height}px`,
  };
});

const tooltipStyle = computed(() => {
  if (!tooltipBox.value) return null;

  return {
    top: `${tooltipBox.value.top}px`,
    left: `${tooltipBox.value.left}px`,
    width: `${tooltipBox.value.width}px`,
  };
});

const scrollToGuideTarget = () => {
  const element = getGuideTargetElement();

  if (!element) return;

  element.scrollIntoView({
    behavior: 'smooth',
    block: 'center',
  });

  setTimeout(() => {
    updateGuidePosition();
  }, 450);
};

const nextGuideStep = () => {
  if (guideStep.value < guideSteps.length - 1) {
    guideStep.value += 1;
    scrollToGuideTarget();
    return;
  }

  finishGuide();
};

const finishGuide = () => {
  showGuide.value = false;
  guideStep.value = 0;
  highlightBox.value = null;
  tooltipBox.value = null;
  localStorage.setItem('littlehelp_user_guide_seen', 'true');
};

const skipGuide = () => {
  finishGuide();
};

const restartGuide = () => {
  guideStep.value = 0;
  showGuide.value = true;

  setTimeout(() => {
    scrollToGuideTarget();
  }, 50);
};

const toggleAccessibilityMenu = () => {
  showAccessibilityMenu.value = !showAccessibilityMenu.value;
};

const openAccessibilityFromFooter = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  setTimeout(() => {
    showAccessibilityMenu.value = true;
  }, 350);
};

const persistAccessibilitySettings = () => {
  localStorage.setItem('littlehelp_accessibility_large_text', largeTextMode.value ? '1' : '0');
  localStorage.setItem('littlehelp_accessibility_high_contrast', highContrastMode.value ? '1' : '0');
};

const toggleInteractiveGuide = () => {
  restartGuide();
  showAccessibilityMenu.value = false;
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

const goProtected = (path) => {
  if (!isLoggedIn.value) {
    router.push({
      path: '/login',
      query: { redirect: path },
    });
    return;
  }

  router.push(path);
};

const handleLogout = () => {
  authStore.logout();
  profiles.value = [];
  selectedForFamily.value = [];
  router.push('/');
};

const normalizeAgeGroup = (ageGroup) => {
  const mapping = {
    '5-6 years': '5-6 years',
    '7-9 years': '7-9 years',
    '10-12 years': '10-12 years',

    '3-6 years': '5-6 years',
    '6-9 years': '7-9 years',
    '9-12 years': '10-12 years',
    '12+ years': '10-12 years',
    '4-8': '7-9 years',
    '9-13': '10-12 years',

    '0-3 years': '',
    '2-3': '',
    '14-18': '',
  };

  return mapping[ageGroup] || '';
};

const mapAllergiesToNames = (allergies) => {
  if (!Array.isArray(allergies)) return [];

  return allergies.map((allergy) => {
    if (typeof allergy === 'string' && isNaN(Number(allergy))) {
      return allergy;
    }

    const id = Number(allergy);
    return allergenIdToName[id] || String(allergy);
  });
};

const handleAddChild = () => {
  localStorage.removeItem('littlewell_edit_child_id');
  goProtected('/child-info');
};

const handleLunchboxPlan = () => {
  childProfileSection.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  });
};

const isActiveStatus = (value) => {
  return value === 1 || value === '1' || value === true;
};

const mapStatusToNutritionFocus = (child) => {
  return [
    isActiveStatus(child.iron_status) ? 'iron' : null,
    isActiveStatus(child.calcium_status) ? 'calcium' : null,
    isActiveStatus(child.vitamin_d_status) ? 'immunity' : null,
    isActiveStatus(child.variety_status) ? 'variety' : null,
  ].filter(Boolean);
};

const mapChildToProfileCard = (child) => {
  const focusIds = mapStatusToNutritionFocus(child);
  const normalizedAgeGroup = normalizeAgeGroup(child.age_band);

  return {
    id: child.child_id,
    name: child.child_name,
    ageGroup: normalizedAgeGroup,
    originalAgeGroup: child.age_band,
    isSupportedAge: allowedAgeGroups.includes(normalizedAgeGroup),
    allergies: mapAllergiesToNames(child.allergies),
    dietaryRestriction: child.restriction_name || '',
    restrictionId: child.restriction_id || null,
    restrictionCode: child.restriction_code || '',
    nutritionFocus: focusIds.map((id) => nutritionFocusLabels[id]).filter(Boolean),
  };
};

const loadProfiles = async () => {
  if (!isLoggedIn.value) {
    profiles.value = [];
    selectedForFamily.value = [];
    return;
  }

  try {
    isLoadingProfiles.value = true;
    const children = await getChildren();

    const mappedProfiles = Array.isArray(children)
      ? children.map(mapChildToProfileCard)
      : [];

    profiles.value = mappedProfiles.filter((profile) => profile.isSupportedAge);
  } catch (error) {
    console.error('Failed to load children:', error);
  } finally {
    isLoadingProfiles.value = false;
  }
};

onMounted(() => {
  loadProfiles();

  largeTextMode.value = localStorage.getItem('littlehelp_accessibility_large_text') === '1';
  highContrastMode.value = localStorage.getItem('littlehelp_accessibility_high_contrast') === '1';

  const hasSeenGuide = localStorage.getItem('littlehelp_user_guide_seen');

  if (!hasSeenGuide) {
    showGuide.value = true;

    setTimeout(() => {
      scrollToGuideTarget();
    }, 300);
  }

  window.addEventListener('resize', updateGuidePosition);
  window.addEventListener('scroll', updateGuidePosition, true);
  document.addEventListener('click', handleDocumentClick);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateGuidePosition);
  window.removeEventListener('scroll', updateGuidePosition, true);
  document.removeEventListener('click', handleDocumentClick);
});

watch(
  () => authStore.token,
  () => {
    loadProfiles();
  }
);

const toggleFamilySelection = (id) => {
  if (!isLoggedIn.value) return;

  if (selectedForFamily.value.includes(id)) {
    selectedForFamily.value = selectedForFamily.value.filter((p) => p !== id);
  } else {
    selectedForFamily.value = [...selectedForFamily.value, id];
  }
};

const handleGenerateFamilyPlan = () => {
  if (!isLoggedIn.value) {
    router.push({
      path: '/login',
      query: { redirect: '/' },
    });
    return;
  }

  if (selectedForFamily.value.length > 0 && profiles.value.length >= 2) {
    const childIds = selectedForFamily.value.join(',');
    router.push(`/results?family=1&childIds=${childIds}`);
  }
};

const handleViewMeals = (profileId) => {
  goProtected(`/results?childId=${profileId}`);
};

const handleDeleteProfile = async (profileId, profileName) => {
  const confirmed = window.confirm(
    `Are you sure you want to delete ${profileName}'s profile? This action cannot be undone.`
  );

  if (!confirmed) return;

  try {
    await deleteChild(profileId);

    selectedForFamily.value = selectedForFamily.value.filter(
      (id) => String(id) !== String(profileId)
    );

    const activeChildId = localStorage.getItem('littlewell_active_child_id');
    if (activeChildId && String(activeChildId) === String(profileId)) {
      localStorage.removeItem('littlewell_active_child_id');
    }

    const editingChildId = localStorage.getItem('littlewell_edit_child_id');
    if (editingChildId && String(editingChildId) === String(profileId)) {
      localStorage.removeItem('littlewell_edit_child_id');
    }

    await loadProfiles();
  } catch (error) {
    console.error('Failed to delete child profile:', error);
    alert(`Failed to delete profile: ${error.message}`);
  }
};

const handleEditProfile = (profileId) => {
  localStorage.setItem('littlewell_edit_child_id', String(profileId));
  goProtected('/child-info');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}

.hero-section,
.child-profile-section,
.family-section,
.weekly-section {
  scroll-margin-top: 96px;
}

.guide-highlight {
  position: fixed;
  border: 3px solid #A8D5BA;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.08);
  box-shadow:
    0 0 0 9999px rgba(0, 0, 0, 0.45),
    0 0 0 8px rgba(168, 213, 186, 0.18),
    0 20px 60px rgba(0, 0, 0, 0.25);
  z-index: 101;
  pointer-events: none;
  transition: all 0.25s ease;
}

.guide-tooltip {
  position: fixed;
  z-index: 102;
  background: white;
  border: 1px solid rgba(168, 213, 186, 0.45);
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.28);
  transition: all 0.25s ease;
}

.nav-link {
  color: #2C5F2D;
  padding: 0.55rem 0.85rem;
  border-radius: 0.65rem;
  font-size: 0.92rem;
  line-height: 1.2;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(168, 213, 186, 0.12);
}

.nav-signin-link {
  text-decoration: underline;
  text-decoration-color: #2C5F2D;
  text-underline-offset: 3px;
}

.nav-link-disabled {
  color: #6b7280;
  padding: 0.55rem 0.85rem;
  border-radius: 0.65rem;
  font-size: 0.92rem;
  line-height: 1.2;
  white-space: nowrap;
  cursor: not-allowed;
}

.nav-primary-button {
  background-color: #A8D5BA;
  color: #2C5F2D;
  padding: 0.65rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.92rem;
  font-weight: 600;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.nav-primary-button:hover {
  background-color: #8FC2A4;
}

.nav-outline-button {
  background-color: white;
  border: 1px solid #A8D5BA;
  color: #2C5F2D;
  padding: 0.6rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.92rem;
  font-weight: 600;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.nav-outline-button:hover {
  background-color: rgba(168, 213, 186, 0.12);
}

.home-root.large-text-mode {
  font-size: 1.06rem;
}

.home-root.large-text-mode .nav-link,
.home-root.large-text-mode .nav-primary-button,
.home-root.large-text-mode .nav-outline-button {
  font-size: 1rem;
}

.home-root.high-contrast-mode {
  color: #111827;
  filter: contrast(1.08);
}

.home-root.high-contrast-mode .text-muted-foreground {
  color: #374151;
}
</style>