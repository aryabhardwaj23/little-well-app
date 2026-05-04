<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation Bar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div
            class="flex items-center cursor-pointer"
            @click="goToHome"
          >
            <img
              :src="logoUrl"
              alt="LittleHelp logo"
              class="h-10 w-auto object-contain"
            />
          </div>

          <!-- Back Button -->
          <button
            @click="goToHome"
            type="button"
            class="inline-flex items-center px-4 py-2 text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg transition-colors"
          >
            <ArrowLeftIcon class="w-4 h-4 mr-2" />
            Back to Home
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="pt-16">
      <!-- Hero Section -->
      <section class="py-20 bg-[#FAF9F6]">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="grid md:grid-cols-2 gap-12 items-center">
            <!-- Left Content -->
            <div>
              <div class="inline-flex items-center gap-2 bg-white border border-[#A8D5BA]/40 text-[#2C5F2D] rounded-full px-4 py-2 text-sm font-medium mb-6 shadow-sm">
                <LeafIcon class="w-4 h-4" />
                Family nutrition made simpler
              </div>

              <h1 class="text-4xl md:text-5xl leading-tight text-[#2C5F2D] mb-6">
                Helping families plan healthier lunchboxes with confidence
              </h1>

              <div class="space-y-4 text-lg text-muted-foreground leading-relaxed">
                <p>
                  LittleHelp is a family-focused nutrition planning platform designed to help parents and caregivers make easier, more confident food choices for children.
                </p>
                <p>
                  We turn nutrition considerations such as age, allergies, dietary needs, and seasonal ingredients into practical lunchbox ideas that fit everyday routines.
                </p>
              </div>

              <div class="mt-8 flex flex-col sm:flex-row gap-3">
                <button
                  @click="goToHome"
                  type="button"
                  class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-xl px-8 py-3 font-semibold transition-colors shadow-sm"
                >
                  Start Planning
                </button>

                <button
                  @click="router.push('/quick-start')"
                  type="button"
                  class="bg-white hover:bg-[#FAF9F6] text-[#2C5F2D] border border-[#A8D5BA] rounded-xl px-8 py-3 font-semibold transition-colors"
                >
                  Try Quick Start
                </button>
              </div>
            </div>

            <!-- Right Image -->
            <div class="relative">
              <div class="rounded-3xl overflow-hidden shadow-xl bg-white p-2">
                <img
                  src="https://images.unsplash.com/photo-1627896067004-38a36f39e506?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXJlbnQlMjBzaG9wcGluZyUyMGZyZXNoJTIwdmVnZXRhYmxlcyUyMGdyb2Nlcnl8ZW58MXx8fHwxNzc1MDE4Njk1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                  alt="Parent choosing fresh vegetables"
                  class="w-full h-[420px] object-cover rounded-2xl"
                />
              </div>

              <div class="absolute -bottom-6 -left-6 bg-white rounded-2xl shadow-lg border p-5 max-w-xs">
                <p class="text-sm text-muted-foreground mb-1">Designed for</p>
                <p class="text-lg font-semibold text-[#2C5F2D]">
                  Parents of children aged 5–12
                </p>
              </div>

              <div class="absolute -top-6 -right-6 w-28 h-28 bg-[#A8D5BA]/30 rounded-full -z-10"></div>
              <div class="absolute -bottom-8 right-12 w-20 h-20 bg-[#F7B267]/30 rounded-full -z-10"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- Trust / Value Strip -->
      <section class="py-10 bg-white border-b border-gray-100">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="grid md:grid-cols-4 gap-6">
            <div class="text-center">
              <p class="text-2xl font-semibold text-[#2C5F2D]">5–12</p>
              <p class="text-sm text-muted-foreground">Child age range</p>
            </div>

            <div class="text-center">
              <p class="text-2xl font-semibold text-[#2C5F2D]">Personalised</p>
              <p class="text-sm text-muted-foreground">Age and needs based</p>
            </div>

            <div class="text-center">
              <p class="text-2xl font-semibold text-[#2C5F2D]">Seasonal</p>
              <p class="text-sm text-muted-foreground">Fresh food guidance</p>
            </div>

            <div class="text-center">
              <p class="text-2xl font-semibold text-[#2C5F2D]">Practical</p>
              <p class="text-sm text-muted-foreground">Built for busy routines</p>
            </div>
          </div>
        </div>
      </section>

      <!-- What We Offer -->
      <section class="py-20 bg-white">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="max-w-3xl mb-12">
            <h2 class="text-3xl md:text-4xl mb-4 text-[#2C5F2D]">What LittleHelp offers</h2>
            <p class="text-lg text-muted-foreground leading-relaxed">
              LittleHelp brings together nutrition guidance, child preferences, allergy awareness, and meal planning tools in one simple experience.
            </p>
          </div>

          <div class="grid md:grid-cols-3 gap-6">
            <div class="p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6] border border-gray-100">
              <div class="w-12 h-12 bg-[#A8D5BA] rounded-full flex items-center justify-center mb-5">
                <UsersIcon class="w-6 h-6 text-[#2C5F2D]" />
              </div>
              <h3 class="text-xl mb-3 text-[#2C5F2D] font-semibold">Family-focused planning</h3>
              <p class="text-muted-foreground leading-relaxed">
                Create child profiles and receive lunchbox ideas that consider age, allergies, dietary restrictions, and nutrition focus areas.
              </p>
            </div>

            <div class="p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6] border border-gray-100">
              <div class="w-12 h-12 bg-[#F7B267] rounded-full flex items-center justify-center mb-5">
                <HeartIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl mb-3 text-[#8B4513] font-semibold">Balanced lunchbox ideas</h3>
              <p class="text-muted-foreground leading-relaxed">
                Build practical lunchboxes with a mix of protein, grains, fruit, vegetables, and child-friendly options.
              </p>
            </div>

            <div class="p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6] border border-gray-100">
              <div class="w-12 h-12 bg-[#CDE7F0] rounded-full flex items-center justify-center mb-5">
                <CalendarDaysIcon class="w-6 h-6 text-[#1B4965]" />
              </div>
              <h3 class="text-xl mb-3 text-[#1B4965] font-semibold">Weekly meal planning</h3>
              <p class="text-muted-foreground leading-relaxed">
                Plan multiple days at once, choose how often to cook, and save weekly lunchbox plans for easier school-week preparation.
              </p>
            </div>

            <div class="p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6] border border-gray-100">
              <div class="w-12 h-12 bg-[#A8D5BA] rounded-full flex items-center justify-center mb-5">
                <SparklesIcon class="w-6 h-6 text-[#2C5F2D]" />
              </div>
              <h3 class="text-xl mb-3 text-[#2C5F2D] font-semibold">Simple nutrition guidance</h3>
              <p class="text-muted-foreground leading-relaxed">
                Understand food choices through clear explanations, without overwhelming nutrition jargon or strict dieting rules.
              </p>
            </div>

            <div class="p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6] border border-gray-100">
              <div class="w-12 h-12 bg-[#F7B267] rounded-full flex items-center justify-center mb-5">
                <LeafIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl mb-3 text-[#8B4513] font-semibold">Seasonal suggestions</h3>
              <p class="text-muted-foreground leading-relaxed">
                Receive practical suggestions that highlight seasonal produce and everyday ingredients suitable for lunchboxes.
              </p>
            </div>

            <div class="p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow bg-[#FAF9F6] border border-gray-100">
              <div class="w-12 h-12 bg-[#CDE7F0] rounded-full flex items-center justify-center mb-5">
                <ShieldIcon class="w-6 h-6 text-[#1B4965]" />
              </div>
              <h3 class="text-xl mb-3 text-[#1B4965] font-semibold">Privacy-conscious design</h3>
              <p class="text-muted-foreground leading-relaxed">
                LittleHelp is designed to work with minimal personal details. Families can use nicknames and manage profiles with privacy in mind.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- How It Helps -->
      <section class="py-20 bg-[#FAF9F6]">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="grid lg:grid-cols-2 gap-12 items-start">
            <div>
              <h2 class="text-3xl md:text-4xl mb-5 text-[#2C5F2D]">Built for real family routines</h2>
              <p class="text-lg text-muted-foreground leading-relaxed mb-8">
                Healthy eating advice can be hard to apply when mornings are busy. LittleHelp focuses on practical, realistic lunchbox support that parents can use quickly.
              </p>

              <div class="bg-white rounded-2xl shadow-sm border p-6">
                <p class="text-lg text-muted-foreground leading-relaxed">
                  Our goal is not to overwhelm families with information, but to help them make
                  <strong class="text-[#2C5F2D]"> confident, realistic, and repeatable choices</strong>.
                </p>
              </div>
            </div>

            <div class="space-y-5">
              <div class="flex items-start gap-4 bg-white rounded-2xl border p-5 shadow-sm">
                <div class="w-10 h-10 bg-[#A8D5BA] rounded-full flex items-center justify-center flex-shrink-0">
                  <CheckCircleIcon class="w-5 h-5 text-[#2C5F2D]" />
                </div>
                <div>
                  <h4 class="text-lg mb-1 font-semibold text-gray-800">Start with each child’s needs</h4>
                  <p class="text-muted-foreground">
                    Add age band, allergies, dietary restrictions, and nutrition focus areas to guide personalised recommendations.
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-4 bg-white rounded-2xl border p-5 shadow-sm">
                <div class="w-10 h-10 bg-[#F7B267] rounded-full flex items-center justify-center flex-shrink-0">
                  <TargetIcon class="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 class="text-lg mb-1 font-semibold text-gray-800">Generate lunchbox options</h4>
                  <p class="text-muted-foreground">
                    Receive food combinations and recipe inspiration that are easier to understand and prepare.
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-4 bg-white rounded-2xl border p-5 shadow-sm">
                <div class="w-10 h-10 bg-[#CDE7F0] rounded-full flex items-center justify-center flex-shrink-0">
                  <BookOpenIcon class="w-5 h-5 text-[#1B4965]" />
                </div>
                <div>
                  <h4 class="text-lg mb-1 font-semibold text-gray-800">Understand the reason behind choices</h4>
                  <p class="text-muted-foreground">
                    See simple explanations that connect food suggestions to nutrition needs and family preferences.
                  </p>
                </div>
              </div>

              <div class="flex items-start gap-4 bg-white rounded-2xl border p-5 shadow-sm">
                <div class="w-10 h-10 bg-[#A8D5BA] rounded-full flex items-center justify-center flex-shrink-0">
                  <CalendarDaysIcon class="w-5 h-5 text-[#2C5F2D]" />
                </div>
                <div>
                  <h4 class="text-lg mb-1 font-semibold text-gray-800">Save and reuse weekly plans</h4>
                  <p class="text-muted-foreground">
                    Keep useful weekly lunchbox plans so future preparation becomes faster and more consistent.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Principles -->
      <section class="py-20 bg-white">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="max-w-3xl mb-12">
            <h2 class="text-3xl md:text-4xl mb-4 text-[#2C5F2D]">Our principles</h2>
            <p class="text-lg text-muted-foreground leading-relaxed">
              LittleHelp is designed around clarity, practicality, and trust.
            </p>
          </div>

          <div class="grid md:grid-cols-3 gap-6">
            <div class="border-l-4 border-[#A8D5BA] bg-[#FAF9F6] rounded-r-2xl p-6">
              <h3 class="text-xl font-semibold text-[#2C5F2D] mb-3">Simple</h3>
              <p class="text-muted-foreground leading-relaxed">
                Information should be easy to understand and simple enough to act on.
              </p>
            </div>

            <div class="border-l-4 border-[#F7B267] bg-[#FAF9F6] rounded-r-2xl p-6">
              <h3 class="text-xl font-semibold text-[#8B4513] mb-3">Practical</h3>
              <p class="text-muted-foreground leading-relaxed">
                Recommendations should fit into real shopping, cooking, and lunch-packing routines.
              </p>
            </div>

            <div class="border-l-4 border-[#CDE7F0] bg-[#FAF9F6] rounded-r-2xl p-6">
              <h3 class="text-xl font-semibold text-[#1B4965] mb-3">Supportive</h3>
              <p class="text-muted-foreground leading-relaxed">
                The experience should guide families gently, without guilt, pressure, or unrealistic expectations.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Privacy Section -->
      <section class="py-20 bg-[#FAF9F6]">
        <div class="container mx-auto px-6 max-w-6xl">
          <div class="bg-white rounded-3xl shadow-sm border p-8 md:p-10">
            <div class="grid md:grid-cols-[auto,1fr] gap-6 items-start">
              <div class="w-16 h-16 bg-[#CDE7F0] rounded-full flex items-center justify-center">
                <ShieldIcon class="w-8 h-8 text-[#1B4965]" />
              </div>

              <div>
                <h2 class="text-3xl mb-4 text-[#2C5F2D]">Privacy and trust</h2>
                <p class="text-muted-foreground text-lg leading-relaxed mb-5">
                  LittleHelp is built to minimise unnecessary personal information. Families can use nicknames for child profiles, and the platform focuses only on the details needed to provide better lunchbox guidance.
                </p>

                <div class="grid sm:grid-cols-3 gap-4">
                  <div class="rounded-xl bg-[#FAF9F6] p-4">
                    <p class="font-semibold text-gray-800 mb-1">Profile control</p>
                    <p class="text-sm text-muted-foreground">Create, edit, or delete child profiles.</p>
                  </div>

                  <div class="rounded-xl bg-[#FAF9F6] p-4">
                    <p class="font-semibold text-gray-800 mb-1">Minimal details</p>
                    <p class="text-sm text-muted-foreground">Only use information relevant to lunchbox planning.</p>
                  </div>

                  <div class="rounded-xl bg-[#FAF9F6] p-4">
                    <p class="font-semibold text-gray-800 mb-1">Clear purpose</p>
                    <p class="text-sm text-muted-foreground">Information is used to support personalised recommendations.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Mission / CTA -->
      <section class="py-20 bg-gradient-to-br from-[#A8D5BA]/15 to-white">
        <div class="container mx-auto px-6 max-w-4xl text-center">
          <img
            :src="logoUrl"
            alt="LittleHelp logo"
            class="h-20 w-auto object-contain mx-auto mb-6"
          />

          <h2 class="text-3xl md:text-4xl mb-6 text-[#2C5F2D]">Our mission</h2>

          <p class="text-xl text-muted-foreground leading-relaxed mb-10 max-w-2xl mx-auto">
            To help families turn nutrition knowledge into simple, practical lunchboxes that children can enjoy and parents can prepare with confidence.
          </p>

          <button
            @click="goToHome"
            type="button"
            class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-xl px-10 py-4 text-lg font-semibold transition-colors shadow-sm"
          >
            Start Planning Lunchboxes
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import logoUrl from '../assets/littlehelp-logo.jpg';
import {
  Heart as HeartIcon,
  Users as UsersIcon,
  Target as TargetIcon,
  CheckCircle as CheckCircleIcon,
  Shield as ShieldIcon,
  Sparkles as SparklesIcon,
  ArrowLeft as ArrowLeftIcon,
  Leaf as LeafIcon,
  BookOpen as BookOpenIcon,
  CalendarDays as CalendarDaysIcon,
} from 'lucide-vue-next';

const router = useRouter();

const goToHome = () => {
  router.push('/');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>