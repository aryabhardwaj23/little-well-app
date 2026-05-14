<template>
  <div class="min-h-screen home-root">
    <!-- User Guide Overlay -->
    <div
      v-if="showGuide"
      class="fixed inset-0 z-[100] pointer-events-none"
      role="dialog"
      aria-modal="true"
      aria-labelledby="guide-title"
    >
      <div class="absolute inset-0 bg-black/20" aria-hidden="true"></div>

      <!-- Highlight Box -->
      <div
        v-if="highlightStyle"
        class="guide-highlight"
        :style="highlightStyle"
        aria-hidden="true"
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

        <h2 id="guide-title" class="text-2xl text-[#2C5F2D] mb-3">
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

          <div class="flex items-center gap-2" role="tablist" aria-label="Guide progress">
            <span
              v-for="(_, index) in guideSteps"
              :key="index"
              role="tab"
              :aria-selected="index === guideStep"
              :aria-label="`Step ${index + 1}`"
              :class="[
                'w-2 h-2 rounded-full transition-colors',
                index === guideStep ? 'bg-[#2C5F2D]' : 'bg-gray-300',
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
    <main>
      <section ref="heroSection" class="hero-section pt-12 pb-14 bg-[#FAF9F6]" aria-label="Hero">
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
                    aria-describedby="quick-start-desc"
                  >
                    <p class="text-xl text-[#315F3A]">Try Quick Start</p>
                    <p class="text-sm text-[#315F3A] font-semibold">
                      Try a lunchbox plan in 1 minute
                    </p>
                  </button>

                  <p id="quick-start-desc" class="md:hidden mt-2 text-xs text-muted-foreground leading-relaxed">
                    Quick Start lets you try a ready-to-use lunchbox recommendation without creating a profile first.
                  </p>

                  <div
                    class="hidden md:block absolute left-0 right-0 bottom-full mb-3 bg-white border border-[#A8D5BA]/40 rounded-xl shadow-lg p-4 text-sm text-muted-foreground leading-relaxed opacity-0 translate-y-1 pointer-events-none transition-all duration-200 group-hover:opacity-100 group-hover:translate-y-0 group-focus-within:opacity-100 group-focus-within:translate-y-0"
                    aria-hidden="true"
                  >
                    Quick Start gently helps you begin with confidence — no profile setup needed.
                  </div>
                </div>

                <div ref="personalisedTarget" class="relative group">
                  <button
                    @click="handleAddChild"
                    class="w-full bg-[#E5F2E8] rounded-2xl border border-[#8FC2A4]/60 p-5 shadow-sm hover:shadow-md hover:border-[#7DB593]/70 hover:bg-[#D9ECDF] transition-all text-left flex flex-col gap-4"
                    type="button"
                    aria-describedby="personalised-desc"
                  >
                    <p class="text-xl text-[#2C5F2D]">Get Personalised Lunchbox</p>
                    <p class="text-sm text-[#2C5F2D] font-semibold">
                      Start by creating a child profile around your nutrition needs
                    </p>
                  </button>

                  <p id="personalised-desc" class="md:hidden mt-2 text-xs text-muted-foreground leading-relaxed">
                    Save profile details for a more personalised and long-term lunchbox planning experience.
                  </p>

                  <div
                    class="hidden md:block absolute left-0 right-0 bottom-full mb-3 bg-white border border-[#A8D5BA]/40 rounded-xl shadow-lg p-4 text-sm text-muted-foreground leading-relaxed opacity-0 translate-y-1 pointer-events-none transition-all duration-200 group-hover:opacity-100 group-hover:translate-y-0 group-focus-within:opacity-100 group-focus-within:translate-y-0"
                    aria-hidden="true"
                  >
                    Child Profile enables deeper personalisation.
                  </div>
                </div>
              </div>
            </div>

            <div class="relative flex items-center">
              <img
                src="https://images.pexels.com/photos/4252139/pexels-photo-4252139.jpeg?auto=compress&cs=tinysrgb&w=1400"
                alt="Healthy lunchbox ingredients and family-style meal prep"
                class="w-full h-[620px] object-cover rounded-3xl shadow-md"
              />

              <div class="absolute bottom-5 left-5 right-5 rounded-2xl shadow-md p-4 overflow-hidden" aria-hidden="true">
                <div class="absolute inset-0 rounded-2xl bg-gradient-to-b from-transparent via-white/45 to-transparent backdrop-blur-sm"></div>

                <div class="relative z-10 grid sm:grid-cols-3 gap-3">
                  <div class="rounded-xl bg-[#CDE7F0]/45 p-3 flex flex-col">
                    <p class="text-sm font-semibold text-[#374151] leading-snug">Simplify nutrition choices</p>
                    <div class="w-full h-12 rounded-full overflow-hidden mt-2">
                      <img
                        src="https://images.pexels.com/photos/1132047/pexels-photo-1132047.jpeg?auto=compress&cs=tinysrgb&w=800"
                        alt=""
                        class="w-full h-full object-cover"
                        aria-hidden="true"
                      />
                    </div>
                  </div>

                  <div class="rounded-xl bg-[#CDE7F0]/45 p-3 flex flex-col">
                    <p class="text-sm font-semibold text-[#374151] leading-snug">Personalise for each child</p>
                    <div class="w-full h-12 rounded-full overflow-hidden mt-2">
                      <img
                        src="https://images.pexels.com/photos/3872370/pexels-photo-3872370.jpeg?auto=compress&cs=tinysrgb&w=800"
                        alt=""
                        class="w-full h-full object-cover"
                        aria-hidden="true"
                      />
                    </div>
                  </div>

                  <div class="rounded-xl bg-[#CDE7F0]/45 p-3 flex flex-col">
                    <p class="text-sm font-semibold text-[#374151] leading-snug">Plan healthier lunchboxes</p>
                    <div class="w-full h-12 rounded-full overflow-hidden mt-2">
                      <img
                        src="https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800"
                        alt=""
                        class="w-full h-full object-cover"
                        aria-hidden="true"
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
      </section>

      <!-- Child Profile Section -->
      <section
        id="child-profiles"
        ref="childProfileSection"
        class="child-profile-section pt-14 pb-8 bg-white"
        aria-label="Child profiles"
      >
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
              aria-live="polite"
              aria-busy="true"
            >
              Loading profiles...
            </div>

            <ul class="flex gap-6 overflow-x-auto pb-4 -mx-6 px-6 list-none" aria-label="Child profile cards">
              <li class="flex-shrink-0 w-[340px]">
                <button
                  @click="handleAddChild"
                  class="w-full min-h-[260px] p-6 rounded-2xl border-2 border-dashed border-[#A8D5BA] bg-[#A8D5BA]/5 flex flex-col items-center justify-center hover:bg-[#A8D5BA]/10 transition-colors cursor-pointer"
                  type="button"
                  aria-label="Add another child profile"
                >
                  <div class="w-16 h-16 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center mb-3" aria-hidden="true">
                    <Plus class="w-8 h-8 text-[#2C5F2D]" />
                  </div>

                  <p class="text-lg text-[#2C5F2D] font-semibold">Add another child</p>

                  <p class="text-sm text-muted-foreground text-center mt-2">
                    Create a profile for a child aged 5–12 to get personalised meal suggestions
                  </p>
                </button>
              </li>

              <li
                v-for="profile in profiles"
                :key="profile.id"
                class="flex-shrink-0 w-[340px]"
              >
                <article class="p-6 rounded-2xl shadow-md hover:shadow-lg transition-shadow bg-white border h-full flex flex-col">
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
                        :aria-label="`Edit ${profile.name}'s profile`"
                        type="button"
                      >
                        <Edit class="w-4 h-4" aria-hidden="true" />
                      </button>

                      <button
                        @click.stop="handleDeleteProfile(profile.id, profile.name)"
                        class="p-2 hover:bg-red-50 rounded-lg transition-colors text-red-600"
                        :aria-label="`Delete ${profile.name}'s profile`"
                        type="button"
                      >
                        <Trash2 class="w-4 h-4" aria-hidden="true" />
                      </button>
                    </div>
                  </div>

                  <div class="space-y-3 mb-4 flex-1">
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
                    :aria-label="`Get personalised lunchboxes for ${profile.name}`"
                  >
                    Get Personalised Lunchboxes
                    <ChevronRight class="w-4 h-4" aria-hidden="true" />
                  </button>
                </article>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Family Meal Planning -->
      <section ref="familySection" class="family-section pt-6 pb-12 bg-white" aria-label="Family planning">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="mb-8">
            <h2 class="text-3xl mb-2 text-[#2C5F2D]">Planning for more than one child?</h2>
            <p class="text-muted-foreground max-w-4xl leading-relaxed">
              We know every child has different needs. Select multiple profiles to generate family lunchbox ideas.
            </p>
          </div>

          <div class="p-8 rounded-2xl shadow-sm bg-white border">
            <p v-if="!isLoggedIn" class="text-sm text-muted-foreground mb-6">
              Sign in first to create child profiles and generate a family lunchbox plan.
            </p>

            <p v-else-if="profiles.length < 2" class="text-sm text-muted-foreground mb-6">
              Add at least two supported child profiles to generate a family lunchbox plan.
            </p>

            <fieldset
              class="grid md:grid-cols-3 gap-4 mb-8"
              :class="{ 'opacity-60': !isLoggedIn || profiles.length < 2 }"
            >
              <legend class="sr-only">Select children for family plan</legend>

              <div
                v-for="profile in profiles"
                :key="profile.id"
                @click="toggleFamilySelection(profile.id)"
                @keydown.enter="toggleFamilySelection(profile.id)"
                @keydown.space.prevent="toggleFamilySelection(profile.id)"
                :class="[
                  'p-4 rounded-xl border-2 cursor-pointer transition-all',
                  selectedForFamily.includes(profile.id)
                    ? 'border-[#A8D5BA] bg-[#A8D5BA]/10'
                    : 'border-gray-200 hover:border-[#A8D5BA]/50',
                ]"
                tabindex="0"
                role="checkbox"
                :aria-checked="selectedForFamily.includes(profile.id)"
                :aria-label="profile.name"
              >
                <div class="flex items-start gap-3">
                  <input
                    type="checkbox"
                    :checked="selectedForFamily.includes(profile.id)"
                    class="mt-1"
                    tabindex="-1"
                    aria-hidden="true"
                    @click.stop
                  />

                  <div class="flex-1">
                    <h4 class="font-medium mb-1">{{ profile.name }}</h4>
                    <p class="text-sm text-muted-foreground mb-2">{{ profile.ageGroup }}</p>

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
            </fieldset>

            <div
              v-if="selectedForFamily.length > 0"
              class="bg-[#CDE7F0]/20 rounded-xl p-4 mb-6"
              aria-live="polite"
            >
              <p class="text-sm text-center">
                <strong>{{ selectedForFamily.length }} children selected</strong>
                – Meals will be tailored to combine their nutrition needs
              </p>
            </div>

            <button
              @click="handleGenerateFamilyPlan"
              :disabled="!isLoggedIn || selectedForFamily.length === 0 || profiles.length < 2"
              class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              type="button"
              :aria-disabled="!isLoggedIn || selectedForFamily.length === 0 || profiles.length < 2"
            >
              Generate Family Lunchboxes
            </button>
          </div>
        </div>
      </section>

      <!-- Weekly Plan Section -->
      <section ref="weeklySection" class="weekly-section py-12 bg-[#FAF9F6]" aria-label="Weekly planning">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="flex flex-col md:flex-row md:items-center gap-8">
            <div class="w-16 h-16 bg-[#A8D5BA] rounded-full flex items-center justify-center flex-shrink-0" aria-hidden="true">
              <CalendarDays class="w-8 h-8 text-[#2C5F2D]" />
            </div>

            <div class="flex-1">
              <h2 class="text-3xl mb-2 text-[#2C5F2D]">Plan the whole school week</h2>
              <p class="text-muted-foreground leading-relaxed">
                Choose your children, set your cooking frequency, and generate a weekly lunchbox plan.
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
      </section>

      <!-- Knowledge Hub Entry -->
      <section class="relative overflow-hidden py-16" aria-label="Knowledge Hub">
        <div class="absolute inset-0 bg-gradient-to-br from-[#F3E9D7]/80 to-[#FAF9F6]" aria-hidden="true"></div>

        <div
          class="absolute inset-0 bg-center bg-cover opacity-55"
          style="background-image: url('https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1600');"
          aria-hidden="true"
        ></div>

        <div class="absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-[#FAF9F6] via-[#FAF9F6]/65 to-transparent" aria-hidden="true"></div>

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
    </main>

    <!-- Footer -->
    <footer class="relative bg-[#FAF9F6] border-t border-gray-200 pt-16 pb-12 overflow-visible">
      <div
        class="absolute -top-24 left-0 right-0 h-24 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6]/75 to-transparent pointer-events-none z-30"
        aria-hidden="true"
      ></div>

      <div class="container mx-auto px-6 max-w-5xl text-center relative z-10">
        <p class="text-2xl text-[#2C5F2D]">LittleHelp</p>

        <p class="mt-4 text-muted-foreground max-w-3xl mx-auto leading-relaxed">
          Helping families create practical, balanced, and child-friendly lunchbox plans through science-backed nutrition guidance.
        </p>

        <nav class="mt-6 flex flex-wrap items-center justify-center gap-x-4 gap-y-2 text-sm text-[#2C5F2D]" aria-label="Footer navigation">
          <button @click="handleLunchboxPlan" type="button" class="hover:underline">Lunchbox Plan</button>
          <button @click="goProtected('/weekly-plan')" type="button" class="hover:underline">Weekly Plan</button>
          <button @click="goProtected('/my-plans')" type="button" class="hover:underline">My Plans</button>
          <button @click="router.push('/knowledge-hub-prototype')" type="button" class="hover:underline">Knowledge Hub</button>
          <button @click="router.push('/about')" type="button" class="hover:underline">About Us</button>
        </nav>

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
  CalendarDays,
} from 'lucide-vue-next';
import { getChildren, deleteChild } from '../services/api';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// ── Profiles ────────────────────────────────────────────────────────────────
const profiles = ref([]);
const selectedForFamily = ref([]);
const isLoadingProfiles = ref(false);

// ── Guide refs ───────────────────────────────────────────────────────────────
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

  if (tooltipLeft < 16) tooltipLeft = 16;
  if (tooltipTop < 96) tooltipTop = 96;

  tooltipBox.value = {
    top: tooltipTop,
    left: tooltipLeft,
    width: tooltipWidth,
  };
};

const highlightStyle = computed(() =>
  highlightBox.value
    ? {
        top: `${highlightBox.value.top}px`,
        left: `${highlightBox.value.left}px`,
        width: `${highlightBox.value.width}px`,
        height: `${highlightBox.value.height}px`,
      }
    : null,
);

const tooltipStyle = computed(() =>
  tooltipBox.value
    ? {
        top: `${tooltipBox.value.top}px`,
        left: `${tooltipBox.value.left}px`,
        width: `${tooltipBox.value.width}px`,
      }
    : null,
);

const scrollToGuideTarget = () => {
  const element = getGuideTargetElement();
  if (!element) return;

  element.scrollIntoView({ behavior: 'smooth', block: 'center' });
  setTimeout(() => updateGuidePosition(), 450);
};

const restartGuide = () => {
  guideStep.value = 0;
  showGuide.value = true;
  setTimeout(() => scrollToGuideTarget(), 50);
};

const handleOpenHomeGuide = () => {
  restartGuide();
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

const skipGuide = () => finishGuide();

const goProtected = (path) => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: path } });
    return;
  }

  router.push(path);
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
    if (typeof allergy === 'string' && Number.isNaN(Number(allergy))) {
      return allergy;
    }

    return allergenIdToName[Number(allergy)] || String(allergy);
  });
};

const isActiveStatus = (value) => value === 1 || value === '1' || value === true;

const mapStatusToNutritionFocus = (child) => [
  isActiveStatus(child.iron_status) ? 'iron' : null,
  isActiveStatus(child.calcium_status) ? 'calcium' : null,
  isActiveStatus(child.vitamin_d_status) ? 'immunity' : null,
  isActiveStatus(child.variety_status) ? 'variety' : null,
].filter(Boolean);

const mapChildToProfileCard = (child) => {
  const focusIds = mapStatusToNutritionFocus(child);
  const normalizedAgeGroup = normalizeAgeGroup(child.age_band);

  return {
    id: child.child_id,
    name: child.child_name,
    ageGroup: normalizedAgeGroup,
    isSupportedAge: allowedAgeGroups.includes(normalizedAgeGroup),
    allergies: mapAllergiesToNames(child.allergies),
    dietaryRestriction: child.restriction_name || '',
    restrictionId: child.restriction_id || null,
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
    const mapped = Array.isArray(children) ? children.map(mapChildToProfileCard) : [];
    profiles.value = mapped.filter((profile) => profile.isSupportedAge);
  } catch (error) {
    console.error('Failed to load children:', error);
  } finally {
    isLoadingProfiles.value = false;
  }
};

onMounted(() => {
  loadProfiles();

  const hasSeenGuide = localStorage.getItem('littlehelp_user_guide_seen');

  if (!hasSeenGuide) {
    showGuide.value = true;
    setTimeout(() => scrollToGuideTarget(), 300);
  }

  window.addEventListener('open-home-user-guide', handleOpenHomeGuide);
  window.addEventListener('resize', updateGuidePosition);
  window.addEventListener('scroll', updateGuidePosition, true);
});

onBeforeUnmount(() => {
  window.removeEventListener('open-home-user-guide', handleOpenHomeGuide);
  window.removeEventListener('resize', updateGuidePosition);
  window.removeEventListener('scroll', updateGuidePosition, true);
});

watch(
  () => authStore.token,
  () => loadProfiles(),
);

const handleAddChild = () => {
  localStorage.removeItem('littlewell_edit_child_id');
  goProtected('/child-info');
};

const handleLunchboxPlan = () => {
  childProfileSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

const toggleFamilySelection = (id) => {
  if (!isLoggedIn.value) return;

  if (selectedForFamily.value.includes(id)) {
    selectedForFamily.value = selectedForFamily.value.filter((profileId) => profileId !== id);
  } else {
    selectedForFamily.value = [...selectedForFamily.value, id];
  }
};

const handleGenerateFamilyPlan = () => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: '/' } });
    return;
  }

  if (selectedForFamily.value.length > 0 && profiles.value.length >= 2) {
    router.push(`/results?family=1&childIds=${selectedForFamily.value.join(',')}`);
  }
};

const handleViewMeals = (profileId) => {
  goProtected(`/results?childId=${profileId}`);
};

const handleDeleteProfile = async (profileId, profileName) => {
  const confirmed = window.confirm(
    `Are you sure you want to delete ${profileName}'s profile? This action cannot be undone.`,
  );

  if (!confirmed) return;

  try {
    await deleteChild(profileId);

    selectedForFamily.value = selectedForFamily.value.filter(
      (id) => String(id) !== String(profileId),
    );

    const activeChildId = localStorage.getItem('littlewell_active_child_id');

    if (activeChildId && String(activeChildId) === String(profileId)) {
      localStorage.removeItem('littlewell_active_child_id');
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
</style>