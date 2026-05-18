<template>
  <div class="min-h-screen bg-[#FAF9F6] py-6 sm:py-10 md:py-12">
    <div class="container mx-auto max-w-6xl px-4 sm:px-6">
      <!-- Back Button -->
      <button
        @click="router.push('/')"
        class="mb-5 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-white sm:mb-6 sm:px-4"
        type="button"
        aria-label="Back to Home"
      >
        <ArrowLeft class="h-4 w-4" aria-hidden="true" />
        Back to Home
      </button>

      <!-- Header -->
      <header class="mb-8 text-center sm:mb-12">
        <div
          class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] sm:h-16 sm:w-16"
          aria-hidden="true"
        >
          <BookmarkCheck class="h-7 w-7 text-white sm:h-8 sm:w-8" />
        </div>

        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:mb-4 sm:text-4xl">
          My Saved Plans
        </h1>

        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg">
          View, reuse, edit, duplicate, and understand your saved weekly lunchbox plans.
        </p>
      </header>

      <!-- Loading / Error -->
      <div
        v-if="isLoading"
        class="mb-6 rounded-xl border bg-white p-4 text-center text-sm text-muted-foreground sm:mb-8"
        aria-live="polite"
        aria-busy="true"
      >
        Loading saved plans…
      </div>

      <div
        v-if="errorMessage"
        role="alert"
        aria-live="assertive"
        class="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 sm:mb-8"
      >
        {{ errorMessage }}
      </div>

      <!-- Reuse Prompt -->
      <section
        v-if="sortedWeeklyPlans.length > 0 && showReusePrompt"
        class="mb-6 rounded-2xl border border-[#A8D5BA]/30 bg-gradient-to-r from-[#A8D5BA]/20 to-[#CDE7F0]/20 p-5 sm:mb-8 sm:p-6"
        role="region"
        aria-label="Reuse previous plan prompt"
      >
        <div class="flex flex-col gap-4 lg:flex-row lg:items-start">
          <div
            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-white sm:h-12 sm:w-12"
            aria-hidden="true"
          >
            <Sparkles class="h-5 w-5 text-[#A8D5BA] sm:h-6 sm:w-6" />
          </div>

          <div class="flex-1">
            <div class="mb-4 flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h2 class="mb-2 text-lg font-semibold text-[#2C5F2D]">
                  Reuse a saved weekly plan?
                </h2>

                <p class="text-sm leading-relaxed text-muted-foreground">
                  Choose one of your saved plans and either reuse it directly or adjust it for this week.
                </p>
              </div>

              <button
                @click="showReusePrompt = false"
                class="self-start rounded-lg px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-white/70 hover:text-gray-700"
                type="button"
                aria-label="Dismiss reuse prompt"
              >
                Dismiss
              </button>
            </div>

            <!-- Desktop / Tablet Plan Selector -->
            <div class="hidden gap-3 md:grid md:grid-cols-2 lg:grid-cols-3">
              <button
                v-for="plan in sortedWeeklyPlans.slice(0, 6)"
                :key="`reuse-${plan.id}`"
                type="button"
                @click="selectedReusePlanId = String(plan.id)"
                :class="[
                  'rounded-2xl border-2 bg-white p-4 text-left transition-all',
                  selectedReusePlanId === String(plan.id)
                    ? 'border-[#A8D5BA] shadow-sm'
                    : 'border-white hover:border-[#A8D5BA]/60'
                ]"
              >
                <div class="mb-2 flex items-start justify-between gap-2">
                  <h3 class="line-clamp-1 text-sm font-semibold text-[#111827]">
                    {{ plan.name }}
                  </h3>

                  <span
                    v-if="selectedReusePlanId === String(plan.id)"
                    class="rounded-full bg-[#A8D5BA]/30 px-2 py-0.5 text-xs text-[#2C5F2D]"
                  >
                    Selected
                  </span>
                </div>

                <p class="mb-2 text-xs text-muted-foreground">
                  {{ formatDate(plan.createdAt) }} ·
                  {{ plan.batches.length }} session{{ plan.batches.length === 1 ? '' : 's' }}
                </p>

                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="tag in buildWhyTags(plan).slice(0, 3)"
                    :key="`${plan.id}-${tag}`"
                    class="rounded-full bg-[#CDE7F0]/35 px-2 py-1 text-[11px] text-[#1B4965]"
                  >
                    {{ tag }}
                  </span>
                </div>
              </button>
            </div>

            <!-- Mobile Plan Selector -->
            <div class="md:hidden">
              <label class="mb-2 block text-sm font-medium text-[#2C5F2D]">
                Select a plan
              </label>

              <select
                v-model="selectedReusePlanId"
                class="w-full rounded-xl border border-[#D1D5DB] bg-white px-4 py-3 text-sm outline-none focus:border-[#A8D5BA] focus:ring-2 focus:ring-[#A8D5BA]/30"
              >
                <option
                  v-for="plan in sortedWeeklyPlans"
                  :key="`reuse-mobile-${plan.id}`"
                  :value="String(plan.id)"
                >
                  {{ plan.name }} — {{ formatDate(plan.createdAt) }}
                </option>
              </select>
            </div>

            <div
              v-if="selectedReusePlan"
              class="mt-4 rounded-2xl border border-white/70 bg-white/70 p-4"
            >
              <p class="mb-3 text-sm text-[#374151]">
                Selected:
                <span class="font-semibold text-[#2C5F2D]">
                  {{ selectedReusePlan.name }}
                </span>
              </p>

              <div class="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:gap-3">
                <button
                  @click="handleReusePlan(selectedReusePlan)"
                  class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-6 py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto sm:py-2"
                  type="button"
                >
                  <Copy class="h-4 w-4" aria-hidden="true" />
                  Reuse Selected Plan
                </button>

                <button
                  @click="handleAdjustPlan(selectedReusePlan)"
                  class="inline-flex w-full items-center justify-center gap-2 rounded-lg border-2 border-[#A8D5BA] bg-white px-6 py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10 sm:w-auto sm:py-2"
                  type="button"
                >
                  <Settings class="h-4 w-4" aria-hidden="true" />
                  Adjust Selected Plan
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Weekly Plans -->
      <section aria-labelledby="weekly-plans-heading">
        <div class="mb-5 flex flex-col gap-2 sm:mb-6 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 id="weekly-plans-heading" class="text-2xl font-semibold text-[#2C5F2D]">
              Weekly Plans
            </h2>

            <p class="text-sm text-muted-foreground">
              {{ weeklyPlans.length }} saved plan{{ weeklyPlans.length === 1 ? '' : 's' }}
            </p>
          </div>

          <button
            @click="router.push('/weekly-plan')"
            class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-5 py-3 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto sm:py-2.5"
            type="button"
          >
            <Plus class="h-4 w-4" aria-hidden="true" />
            Create Weekly Plan
          </button>
        </div>

        <div
          v-if="weeklyPlans.length === 0 && !isLoading"
          class="rounded-3xl border bg-white py-12 text-center shadow-sm sm:py-16"
        >
          <div
            class="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-gray-100"
            aria-hidden="true"
          >
            <CalendarDays class="h-10 w-10 text-gray-400" />
          </div>

          <h2 class="mb-2 text-xl font-semibold text-[#2C5F2D]">
            No weekly plans saved yet
          </h2>

          <p class="mb-6 text-sm text-muted-foreground sm:text-base">
            Create your first weekly plan to get started.
          </p>

          <button
            @click="router.push('/weekly-plan')"
            class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3 text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto"
            type="button"
          >
            <Plus class="h-4 w-4" aria-hidden="true" />
            Create Weekly Plan
          </button>
        </div>

        <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
          <article
            v-for="plan in sortedWeeklyPlans"
            :key="plan.id"
            class="rounded-2xl border bg-white p-5 shadow-sm transition-shadow hover:shadow-md sm:p-6"
          >
            <div class="mb-4 flex items-start justify-between gap-3">
              <div class="min-w-0 flex-1">
                <h3 class="mb-2 truncate text-lg font-semibold text-[#111827] sm:text-xl">
                  {{ plan.name }}
                </h3>

                <div class="mb-2 flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock class="h-4 w-4 shrink-0" aria-hidden="true" />
                  <span>{{ formatDate(plan.createdAt) }}</span>
                </div>
              </div>

              <button
                @click="handleDeletePlan(plan.id)"
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg transition-colors hover:bg-red-50"
                :aria-label="`Delete plan ${plan.name}`"
                type="button"
              >
                <Trash2 class="h-4 w-4 text-red-500" aria-hidden="true" />
              </button>
            </div>

            <div class="mb-4 space-y-3">
              <div class="flex items-center gap-2">
                <ChefHat class="h-4 w-4 shrink-0 text-[#A8D5BA]" aria-hidden="true" />
                <span class="text-sm">{{ plan.cookingFrequency }} cooking days/week</span>
              </div>

              <div class="flex items-center gap-2">
                <Leaf class="h-4 w-4 shrink-0 text-[#A8D5BA]" aria-hidden="true" />
                <span class="text-sm">{{ plan.season || 'Seasonal' }} plan</span>
              </div>

              <div v-if="plan.children.length > 0">
                <p class="mb-1 text-xs text-muted-foreground">For:</p>

                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="child in plan.children"
                    :key="child.id || child.fallbackId || child.displayName"
                    class="rounded-full bg-[#CDE7F0]/30 px-2 py-1 text-xs text-[#1B4965]"
                  >
                    {{ child.displayName }}
                    <span v-if="child.age"> · {{ child.age }}</span>
                    <span v-else-if="child.ageBand"> · {{ child.ageBand }}</span>
                  </span>
                </div>
              </div>
            </div>

            <!-- Meal Preview -->
            <div class="mb-4 rounded-lg bg-[#FAF9F6] p-3">
              <p class="mb-2 text-xs text-muted-foreground">
                {{ plan.batches.length }} cooking session{{ plan.batches.length === 1 ? '' : 's' }}
              </p>

              <div v-if="plan.batches.length > 0" class="space-y-3">
                <div
                  v-for="(batch, index) in plan.batches.slice(0, 2)"
                  :key="`${plan.id}-${index}`"
                  class="rounded-lg border bg-white p-3"
                >
                  <div class="flex items-start gap-3">
                    <div class="h-14 w-14 shrink-0 overflow-hidden rounded-lg bg-gray-100">
                      <img
                        :src="batch.recipe.image || PLAN_IMAGE_FALLBACK"
                        :alt="batch.recipe.title"
                        class="h-full w-full object-cover"
                        @error="handleImageError"
                      />
                    </div>

                    <div class="min-w-0 flex-1">
                      <p class="mb-1 text-xs text-muted-foreground">
                        {{ batch.cookDay }}
                      </p>

                      <p class="truncate text-sm font-medium">
                        {{ batch.lunchbox.title }}
                      </p>

                      <p class="truncate text-xs text-[#1B4965]">
                        Recipe inspiration: {{ batch.recipe.title }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div
                v-else
                class="rounded-lg border border-dashed bg-white p-3 text-sm text-muted-foreground"
              >
                No meal preview available for this plan.
              </div>

              <p v-if="plan.batches.length > 2" class="mt-2 text-xs text-muted-foreground">
                + {{ plan.batches.length - 2 }} more session{{ plan.batches.length - 2 === 1 ? '' : 's' }}
              </p>
            </div>

            <!-- Actions -->
            <div class="grid grid-cols-2 gap-2">
              <button
                @click="handleViewPlan(plan)"
                class="inline-flex items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] py-2.5 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4]"
                type="button"
                :aria-label="`View plan ${plan.name}`"
              >
                <Eye class="h-4 w-4" aria-hidden="true" />
                View
              </button>

              <button
                @click="handleEditPlan(plan)"
                class="inline-flex items-center justify-center gap-2 rounded-lg border-2 border-[#A8D5BA] bg-white py-2.5 text-sm font-medium text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10"
                type="button"
                :aria-label="`Edit plan ${plan.name}`"
              >
                <Edit class="h-4 w-4" aria-hidden="true" />
                Edit
              </button>

              <button
                @click="handleDuplicatePlan(plan)"
                class="col-span-2 inline-flex items-center justify-center gap-2 rounded-lg border-2 border-[#CDE7F0] bg-white px-3 py-2.5 text-sm font-medium text-[#1B4965] transition-colors hover:bg-[#CDE7F0]/10"
                :aria-label="`Duplicate plan ${plan.name}`"
                type="button"
              >
                <Copy class="h-4 w-4" aria-hidden="true" />
                Duplicate
              </button>
            </div>
          </article>
        </div>
      </section>

      <!-- Why This Plan -->
      <section id="why-this-plan" class="scroll-mt-8 py-12">
        <div class="mb-6 text-center">
          <h2 class="mb-3 text-2xl font-semibold text-[#2C5F2D] md:text-3xl">
            Why This Plan?
          </h2>

          <p class="mx-auto max-w-3xl text-sm leading-relaxed text-muted-foreground md:text-base">
            Select a saved weekly plan and generate separate AI explanations for each lunchbox meal.
          </p>
        </div>

        <div class="rounded-3xl border border-[#E8E4DC] bg-white p-5 shadow-sm sm:p-8 md:p-10">
          <div v-if="whyPlanDisplayList.length" class="mb-8 grid grid-cols-1 gap-4 lg:grid-cols-2">
            <button
              v-for="row in whyPlanDisplayList"
              :key="row.id"
              @click="handleSelectWhyPlan(row.id)"
              type="button"
              :class="[
                'rounded-2xl border-2 p-4 text-left transition-all sm:p-5',
                selectedWhyPlanId === row.id
                  ? 'border-[#A8D5BA] bg-[#A8D5BA]/5'
                  : 'border-gray-200 hover:border-[#A8D5BA]/50'
              ]"
            >
              <div class="flex items-start gap-4">
                <div
                  class="hidden h-20 w-28 shrink-0 overflow-hidden rounded-2xl border border-[#E5E7EB] bg-gray-100 sm:block"
                >
                  <img
                    :src="row.image || PLAN_IMAGE_FALLBACK"
                    :alt="`${row.name} meal preview`"
                    class="h-full w-full object-cover"
                    @error="handleImageError"
                  />
                </div>

                <div class="min-w-0 flex-1">
                  <div class="mb-1 flex items-start justify-between gap-2">
                    <h3 class="line-clamp-1 text-base font-semibold text-[#111827]">
                      {{ row.name }}
                    </h3>

                    <span
                      v-if="selectedWhyPlanId === row.id"
                      class="shrink-0 rounded-full bg-[#A8D5BA]/30 px-2 py-0.5 text-xs text-[#2C5F2D]"
                    >
                      Selected
                    </span>
                  </div>

                  <p class="mb-3 text-sm text-muted-foreground">
                    {{ row.description }}
                  </p>

                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in row.tags"
                      :key="tag"
                      class="rounded-full bg-[#A8D5BA]/20 px-3 py-1 text-xs text-[#2C5F2D]"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </div>
            </button>
          </div>

          <div
            v-else-if="!isLoading"
            class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-6 text-center"
          >
            <p class="mb-4 text-[#4B5563]">
              You do not have any saved plans yet. Please save a plan first to view AI explanations here.
            </p>

            <button
              type="button"
              class="rounded-lg bg-[#2C5F2D] px-5 py-2.5 text-white transition-colors hover:bg-[#244E24]"
              @click="goToWeeklyPlanFromWhy"
            >
              Create Personalised Lunchbox Plan
            </button>
          </div>

          <div v-if="selectedWhyPlan" class="rounded-2xl bg-[#FAF9F6] p-5 sm:p-6">
            <div class="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h3 class="mb-2 text-lg font-semibold text-[#2C5F2D]">
                  AI Explanation for This Plan
                </h3>

                <p class="text-sm leading-relaxed text-muted-foreground">
                  Each meal is explained separately, then the results are summarised for the whole weekly plan.
                </p>
              </div>

              <button
                type="button"
                class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#2C5F2D] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-[#244E24] disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
                :disabled="whyPlanLoading"
                @click="generateWhyThisPlan"
              >
                <Sparkles class="h-4 w-4" aria-hidden="true" />

                <span v-if="!whyPlanLoading">
                  {{ currentWhyPlanExplanation ? 'Regenerate AI Explanation' : 'Generate AI Explanation' }}
                </span>

                <span v-else>
                  Thinking...
                </span>
              </button>
            </div>

            <div class="mb-5 rounded-2xl border bg-white p-4">
              <p class="mb-2 text-sm font-medium text-[#111827]">
                Selected plan:
                <span class="text-[#2C5F2D]">
                  {{ selectedWhyPlan.name }}
                </span>
              </p>

              <p class="mb-2 text-sm leading-relaxed text-muted-foreground">
                Meals used for AI explanation:
                <span class="text-[#374151]">
                  {{ getPlanAiPromptMealName(selectedWhyPlan) }}
                </span>
              </p>

              <p class="text-sm leading-relaxed text-muted-foreground">
                Child age used:
                <span class="text-[#374151]">
                  {{ getPlanAgeDisplay(selectedWhyPlan) }}
                </span>
              </p>

              <div
                v-if="!getResolvedPlanChildAge(selectedWhyPlan)"
                class="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4"
              >
                <label class="mb-2 block text-sm font-medium text-amber-800">
                  Age was not found by child name. Please select an age for this weekly plan.
                </label>

                <select
                  :value="fallbackChildAgesByPlan[String(selectedWhyPlan.id)] || ''"
                  @change="setManualAgeForPlan(selectedWhyPlan.id, $event.target.value)"
                  class="w-full rounded-lg border border-amber-300 bg-white px-3 py-2 text-sm outline-none focus:border-[#A8D5BA] focus:ring-2 focus:ring-[#A8D5BA]/30 sm:max-w-xs"
                >
                  <option value="">Select age</option>
                  <option
                    v-for="age in supportedChildAges"
                    :key="age"
                    :value="age"
                  >
                    {{ age }} years old
                  </option>
                </select>
              </div>
            </div>

            <div
              v-if="whyPlanError"
              class="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
            >
              {{ whyPlanError }}
            </div>

            <div v-if="currentWhyPlanExplanation" class="space-y-5">
              <!-- Plan Summary -->
              <div class="rounded-2xl border border-[#A8D5BA]/40 bg-white p-5">
                <div class="mb-3 flex items-center gap-2">
                  <Sparkles class="h-4 w-4 text-[#2C5F2D]" aria-hidden="true" />

                  <h4 class="font-semibold text-[#2C5F2D]">
                    AI Plan Summary
                  </h4>
                </div>

                <p class="whitespace-pre-line text-sm leading-relaxed text-[#374151]">
                  {{ currentWhyPlanExplanation }}
                </p>
              </div>

              <!-- Meal-by-meal AI Explanation -->
              <div class="space-y-3">
                <h4 class="font-semibold text-[#2C5F2D]">
                  Meal-by-meal explanation
                </h4>

                <div
                  v-for="meal in currentMealExplanations"
                  :key="meal.id"
                  :class="[
                    'rounded-2xl border bg-white p-5',
                    meal.hasError ? 'border-red-200' : 'border-[#E5E7EB]'
                  ]"
                >
                  <div class="mb-2 flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <p class="text-sm font-semibold text-[#111827]">
                        {{ meal.title }}
                      </p>

                      <p
                        v-if="meal.recipeTitle"
                        class="text-xs text-[#1B4965]"
                      >
                        Recipe inspiration: {{ meal.recipeTitle }}
                      </p>
                    </div>

                    <span class="text-xs text-muted-foreground">
                      {{ meal.cookDay }}
                    </span>
                  </div>

                  <p
                    :class="[
                      'whitespace-pre-line text-sm leading-relaxed',
                      meal.hasError ? 'text-red-600' : 'text-[#374151]'
                    ]"
                  >
                    {{ meal.explanation }}
                  </p>
                </div>
              </div>
            </div>

            <div
              v-else-if="!whyPlanLoading"
              class="rounded-2xl border border-dashed border-[#D1D5DB] bg-white p-5 text-center text-sm text-muted-foreground"
            >
              Click “Generate AI Explanation” to understand why this saved plan may be suitable.
            </div>

            <div
              v-if="whyPlanLoading"
              class="rounded-2xl border border-[#A8D5BA]/30 bg-white p-5 text-center text-sm text-muted-foreground"
            >
              Generating AI explanations meal by meal…
            </div>

            <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
              <button
                type="button"
                class="rounded-lg bg-[#2C5F2D] px-4 py-2 text-white transition-colors hover:bg-[#244E24]"
                @click="modifySelectedWhyPlan"
              >
                Modify plan
              </button>

              <button
                type="button"
                class="rounded-lg border border-[#D1D5DB] px-4 py-2 text-[#374151] transition-colors hover:bg-white"
                @click="closeWhyPlanExplanation"
              >
                Close explanation
              </button>
            </div>
          </div>

          <div v-else-if="whyPlanDisplayList.length" class="py-8 text-center text-muted-foreground">
            <p>Select a plan above to generate an AI explanation.</p>
          </div>
        </div>
      </section>

      <!-- Bottom CTA -->
      <div class="mt-2 flex justify-center sm:mt-4">
        <button
          @click="router.push('/weekly-plan')"
          class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#A8D5BA] px-8 py-3 text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto"
          type="button"
        >
          <Plus class="h-4 w-4" aria-hidden="true" />
          Create Another Weekly Plan
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  ArrowLeft,
  BookmarkCheck,
  CalendarDays,
  Plus,
  Clock,
  ChefHat,
  Leaf,
  Eye,
  Edit,
  Copy,
  Trash2,
  Sparkles,
  Settings,
} from 'lucide-vue-next';

import {
  getWeeklyPlans,
  getChildren,
  deleteWeeklyPlan,
  duplicateWeeklyPlan,
  getWhyThisMeal,
} from '../services/api';

const router = useRouter();
const route = useRoute();

const PLAN_IMAGE_FALLBACK =
  'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800';

const supportedChildAges = [5, 6, 7, 8, 9, 10, 11, 12];

const selectedWhyPlanId = ref(null);
const selectedReusePlanId = ref(null);

const savedPlans = ref([]);
const userChildren = ref([]);
const fallbackChildAgesByPlan = ref({});

const showReusePrompt = ref(true);
const isLoading = ref(false);
const errorMessage = ref('');

const whyPlanLoading = ref(false);
const whyPlanError = ref('');
const whyPlanExplanations = ref({});
const whyPlanMealExplanations = ref({});

const weeklyPlans = computed(() => {
  return savedPlans.value.filter((plan) => plan.type === 'weekly');
});

const sortedWeeklyPlans = computed(() => {
  return [...weeklyPlans.value].sort((a, b) => {
    const dateA = new Date(a.createdAt).getTime();
    const dateB = new Date(b.createdAt).getTime();

    return (Number.isNaN(dateB) ? 0 : dateB) - (Number.isNaN(dateA) ? 0 : dateA);
  });
});

const selectedReusePlan = computed(() => {
  if (!selectedReusePlanId.value) return null;

  return sortedWeeklyPlans.value.find(
    (plan) => String(plan.id) === String(selectedReusePlanId.value),
  );
});

const selectedWhyPlan = computed(() => {
  if (!selectedWhyPlanId.value) return null;

  return weeklyPlans.value.find(
    (plan) => String(plan.id) === String(selectedWhyPlanId.value),
  );
});

const currentWhyPlanExplanation = computed(() => {
  if (!selectedWhyPlanId.value) return '';

  return whyPlanExplanations.value[String(selectedWhyPlanId.value)] || '';
});

const currentMealExplanations = computed(() => {
  if (!selectedWhyPlanId.value) return [];

  return whyPlanMealExplanations.value[String(selectedWhyPlanId.value)] || [];
});

const buildWhyTags = (plan) => {
  const tags = [];

  if (plan.children?.length > 1) tags.push('Multi-child');
  if (plan.varietyPreference) tags.push(String(plan.varietyPreference));
  if (plan.mealStyle) tags.push(String(plan.mealStyle));
  if (plan.season) tags.push(String(plan.season));
  tags.push(`${plan.cookingFrequency}x cook days/week`);

  return tags.filter(Boolean).slice(0, 5);
};

const formatWhyPlanDescription = (plan) => {
  const d = new Date(plan.createdAt);
  const sessions = plan.batches?.length ?? 0;

  if (Number.isNaN(d.getTime())) {
    return `${sessions} cooking session${sessions === 1 ? '' : 's'}`;
  }

  const label = d.toLocaleDateString('en-AU', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return `Saved ${label} · ${sessions} cooking session${sessions === 1 ? '' : 's'}`;
};

const whyPlanDisplayList = computed(() => {
  return sortedWeeklyPlans.value.map((plan) => ({
    id: String(plan.id),
    name: plan.name,
    description: formatWhyPlanDescription(plan),
    tags: buildWhyTags(plan),
    image: plan.batches?.[0]?.recipe?.image || PLAN_IMAGE_FALLBACK,
  }));
});

const handleSelectWhyPlan = (planId) => {
  selectedWhyPlanId.value = String(planId);
  whyPlanError.value = '';
};

const parseTags = (tags) => {
  if (Array.isArray(tags)) return tags;
  if (!tags) return [];

  return String(tags)
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean);
};

const parseAgeNumber = (value) => {
  if (value === null || value === undefined || value === '') return null;

  const numberValue = Number(value);

  if (Number.isFinite(numberValue) && numberValue > 0) {
    return Math.round(numberValue);
  }

  const match = String(value).match(/\d+/);
  if (!match) return null;

  const parsed = Number(match[0]);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : null;
};

const parseAgeFromBand = (value) => {
  if (!value) return null;

  const numbers = String(value)
    .match(/\d+/g)
    ?.map((item) => Number(item))
    .filter((item) => Number.isFinite(item) && item > 0);

  if (!numbers || numbers.length === 0) return null;

  if (numbers.length === 1) return numbers[0];

  return Math.round((numbers[0] + numbers[1]) / 2);
};

const normaliseName = (value) => {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[^a-z0-9\u4e00-\u9fa5 ]/g, '');
};

const isLikelySameChildName = (profileName, planName) => {
  const nameA = normaliseName(profileName);
  const nameB = normaliseName(planName);

  if (!nameA || !nameB) return false;

  if (nameA === nameB) return true;

  if (nameA.includes(nameB) || nameB.includes(nameA)) return true;

  const partsA = nameA.split(' ').filter(Boolean);
  const partsB = nameB.split(' ').filter(Boolean);

  return partsA.some((partA) => partsB.some((partB) => partA === partB));
};

const getManualAgeForPlan = (planId) => {
  if (!planId) return null;

  return parseAgeNumber(fallbackChildAgesByPlan.value[String(planId)]);
};

const setManualAgeForPlan = (planId, age) => {
  if (!planId) return;

  fallbackChildAgesByPlan.value = {
    ...fallbackChildAgesByPlan.value,
    [String(planId)]: age,
  };

  whyPlanError.value = '';
};

const normalizeChild = (child, index = 0) => {
  if (typeof child === 'string') {
    return {
      id: null,
      fallbackId: `child-${index}-${child}`,
      displayName: child,
      age: null,
      ageBand: '',
    };
  }

  const age =
    parseAgeNumber(child?.age) ||
    parseAgeNumber(child?.child_age) ||
    parseAgeNumber(child?.age_years) ||
    parseAgeNumber(child?.childAge) ||
    parseAgeFromBand(child?.age_band) ||
    parseAgeFromBand(child?.ageBand) ||
    parseAgeFromBand(child?.band_name);

  const ageBand =
    child?.age_band ||
    child?.ageBand ||
    child?.band_name ||
    child?.age_group ||
    '';

  return {
    id:
      child?.child_id ??
      child?.id ??
      child?.user_child_id ??
      null,
    fallbackId: `child-${index}-${child?.child_name || child?.name || 'unknown'}`,
    displayName:
      child?.child_name ||
      child?.name ||
      child?.childName ||
      child?.displayName ||
      `Child ${index + 1}`,
    age,
    ageBand,
  };
};

const normalizeChildren = (children) => {
  if (!Array.isArray(children)) return [];

  return children.map(normalizeChild).filter((child) => child.displayName);
};

const getChildrenLabel = (children) => {
  if (!Array.isArray(children) || children.length === 0) {
    return 'your family';
  }

  return children.map((child) => child.displayName).join(', ');
};

const extractAgeFromChildProfile = (child) => {
  if (!child) return null;

  return (
    parseAgeNumber(child.age) ||
    parseAgeNumber(child.child_age) ||
    parseAgeNumber(child.age_years) ||
    parseAgeNumber(child.childAge) ||
    parseAgeFromBand(child.age_band) ||
    parseAgeFromBand(child.ageBand) ||
    parseAgeFromBand(child.band_name) ||
    parseAgeFromBand(child.age_group)
  );
};

const findAgeFromUserChildrenByName = (plan) => {
  if (!userChildren.value.length) return null;
  if (!plan?.children?.length) return null;

  for (const planChild of plan.children) {
    const planChildName =
      planChild.displayName ||
      planChild.child_name ||
      planChild.name ||
      planChild.childName ||
      '';

    if (!planChildName) continue;

    const matchedChild = userChildren.value.find((child) => {
      const profileName =
        child.child_name ||
        child.name ||
        child.childName ||
        child.displayName ||
        '';

      return isLikelySameChildName(profileName, planChildName);
    });

    const matchedAge = extractAgeFromChildProfile(matchedChild);

    if (matchedAge) return matchedAge;
  }

  return null;
};

const getResolvedPlanChildAge = (plan) => {
  if (!plan?.id) return null;

  const ageFromName = findAgeFromUserChildrenByName(plan);
  if (ageFromName) return ageFromName;

  const manualAge = getManualAgeForPlan(plan.id);
  if (manualAge) return manualAge;

  return null;
};

const getPlanAgeDisplay = (plan) => {
  if (!plan?.id) return 'Not available for this weekly plan';

  const ageFromName = findAgeFromUserChildrenByName(plan);
  if (ageFromName) return `${ageFromName} years old (matched by child name)`;

  const manualAge = getManualAgeForPlan(plan.id);
  if (manualAge) return `${manualAge} years old (selected manually for this plan)`;

  return 'Not available for this weekly plan';
};

const normalizeLunchbox = (meal, index = 0) => {
  const lunchbox = meal.lunchbox || {};
  const items = lunchbox.items || meal.items || meal.lunchbox_items || [];

  return {
    id:
      lunchbox.id ||
      meal.reference_food_id ||
      meal.lunchbox_id ||
      meal.source_id ||
      `db-${index}`,
    reference_food_id: lunchbox.reference_food_id || meal.reference_food_id || null,
    title:
      lunchbox.title ||
      meal.meal_title ||
      meal.mealName ||
      meal.lunchbox_title ||
      'Database Lunchbox',
    nutritionFocus: parseTags(lunchbox.nutritionFocus || meal.nutrition_tags || meal.tags),
    whyThisMeal: lunchbox.whyThisMeal || meal.whyThisMeal || '',
    items: Array.isArray(items) ? items : [],
  };
};

const normalizeRecipe = (meal) => {
  const recipe = meal.recipe || {};

  return {
    id: recipe.id || meal.recipe_id || meal.recipeId || null,
    title:
      recipe.title ||
      meal.recipe_title ||
      meal.recipeName ||
      (meal.recipe_id ? `Recipe #${meal.recipe_id}` : 'Recipe Inspiration'),
    image:
      recipe.image ||
      recipe.heroImage ||
      recipe.mealImage ||
      meal.image_url ||
      meal.heroImage ||
      meal.mealImage ||
      '',
    category: recipe.category || meal.category || '',
    area: recipe.area || meal.area || '',
    nutritionFocus: parseTags(recipe.nutritionFocus || meal.recipe_tags),
    whyThisMeal: recipe.whyThisMeal || meal.recipe_note || '',
  };
};

const normalizeMeal = (meal, index = 0) => ({
  id: meal.meal_id || meal.id || `meal-${index}`,
  cookDay: meal.cook_day || meal.cookDay || meal.title || `Cook Session ${index + 1}`,
  coverDays: meal.cover_days || meal.coverDays || meal.covers || 'Selected days',
  prepTime: meal.prep_time_minutes ? `${meal.prep_time_minutes} mins` : meal.prepTime || '30 mins',
  lunchbox: normalizeLunchbox(meal, index),
  recipe: normalizeRecipe(meal),
});

const getSeasonNameFromId = (seasonId) =>
  ({
    1: 'Spring',
    2: 'Summer',
    3: 'Autumn',
    4: 'Winter',
  })[Number(seasonId)] || '';

const normalizePlan = (plan) => {
  const meals = plan.meals || plan.batches || [];

  return {
    id: plan.plan_id || plan.id,
    type: 'weekly',
    name: plan.plan_name || plan.name || 'Untitled Weekly Plan',
    cookingFrequency: plan.cook_frequency || plan.cookingFrequency || meals.length || 0,
    varietyPreference: plan.variety_preference || plan.varietyPreference || '',
    mealStyle: plan.meal_style || plan.mealStyle || '',
    season: plan.season || plan.season_name || getSeasonNameFromId(plan.season_id) || 'Seasonal',
    children: normalizeChildren(plan.children),
    batches: Array.isArray(meals) ? meals.map(normalizeMeal) : [],
    createdAt: plan.created_at || plan.createdAt || new Date().toISOString(),
  };
};

const resolvePlanAgeBeforeAi = async (plan) => {
  const ageFromName = findAgeFromUserChildrenByName(plan);

  if (ageFromName) {
    return {
      plan,
      age: ageFromName,
      ageSource: 'matched by child name',
    };
  }

  const manualAge = getManualAgeForPlan(plan.id);

  if (manualAge) {
    return {
      plan,
      age: manualAge,
      ageSource: 'selected manually for this plan',
    };
  }

  return {
    plan,
    age: null,
    ageSource: '',
  };
};

const getBatchMealName = (batch) => {
  return (
    batch?.lunchbox?.title ||
    batch?.recipe?.title ||
    batch?.meal_title ||
    'Lunchbox meal'
  );
};

const getBatchRecipeName = (batch) => {
  return batch?.recipe?.title || '';
};

const getPlanMealNames = (plan) => {
  if (!plan?.batches?.length) return [];

  return plan.batches.map(getBatchMealName).filter(Boolean);
};

const getPlanRecipeNames = (plan) => {
  if (!plan?.batches?.length) return [];

  return plan.batches.map(getBatchRecipeName).filter(Boolean);
};

const getPlanAiPromptMealName = (plan) => {
  const mealNames = getPlanMealNames(plan);
  const recipeNames = getPlanRecipeNames(plan);

  const combined = [...new Set([...mealNames, ...recipeNames])].filter(Boolean);

  if (combined.length === 0) {
    return plan?.name || 'Saved weekly lunchbox plan';
  }

  return combined.slice(0, 6).join(', ');
};

const buildMealPayload = ({ plan, batch, index, resolvedAge }) => {
  const childAge = resolvedAge || getResolvedPlanChildAge(plan);
  const mealName = getBatchMealName(batch);
  const recipeName = getBatchRecipeName(batch);

  const promptMealName = [
    `Meal ${index + 1}: ${mealName}`,
    recipeName ? `Recipe inspiration: ${recipeName}` : '',
    batch.cookDay ? `Cook day: ${batch.cookDay}` : '',
    batch.coverDays ? `Covers: ${batch.coverDays}` : '',
    plan.season ? `Season: ${plan.season}` : '',
    plan.mealStyle ? `Meal style: ${plan.mealStyle}` : '',
    plan.varietyPreference ? `Variety preference: ${plan.varietyPreference}` : '',
    plan.children?.length ? `Children: ${getChildrenLabel(plan.children)}` : '',
    childAge ? `Child age: ${childAge}` : '',
  ]
    .filter(Boolean)
    .join('. ');

  return {
    meal_name: promptMealName,
    child_age: childAge,
    allergens: [],
    dietary_restrictions: [],
    season: plan.season || 'seasonal',
    meal_type: 'weekly lunchbox meal',
  };
};

const generateWhyThisPlan = async () => {
  if (!selectedWhyPlan.value) return;

  whyPlanLoading.value = true;
  whyPlanError.value = '';

  try {
    const originalPlan = selectedWhyPlan.value;
    const { plan, age, ageSource } = await resolvePlanAgeBeforeAi(originalPlan);

    if (!age) {
      whyPlanError.value =
        'Child age was not found by child name. Please select an age for this weekly plan first.';
      return;
    }

    const planKey = String(plan.id);
    const batches = Array.isArray(plan.batches) ? plan.batches : [];

    if (batches.length === 0) {
      whyPlanError.value = 'This plan does not have any meals to explain.';
      return;
    }

    const mealResults = [];

    for (const [index, batch] of batches.entries()) {
      const mealName = getBatchMealName(batch);
      const recipeName = getBatchRecipeName(batch);
      const payload = buildMealPayload({
        plan,
        batch,
        index,
        resolvedAge: age,
      });

      try {
        const data = await getWhyThisMeal(payload);

        mealResults.push({
          id: batch.id || `${planKey}-${index}`,
          title: mealName,
          recipeTitle: recipeName,
          cookDay: batch.cookDay || `Meal ${index + 1}`,
          explanation:
            data.explanation ||
            data.ai_feedback ||
            data.message ||
            'This meal supports a practical and balanced lunchbox routine.',
        });
      } catch (mealError) {
        mealResults.push({
          id: batch.id || `${planKey}-${index}`,
          title: mealName,
          recipeTitle: recipeName,
          cookDay: batch.cookDay || `Meal ${index + 1}`,
          explanation:
            mealError.message ||
            'Could not generate an AI explanation for this meal.',
          hasError: true,
        });
      }
    }

    const successfulMeals = mealResults.filter((meal) => !meal.hasError);
    const mealTitles = successfulMeals.map((meal) => meal.title).join(', ');
    const childAgeDisplay = `${age} years old${ageSource ? ` (${ageSource})` : ''}`;

    const summaryText =
      successfulMeals.length > 0
        ? `This weekly plan includes ${successfulMeals.length} explained meal${successfulMeals.length === 1 ? '' : 's'}: ${mealTitles}. The explanations were generated meal by meal, using the saved recipe inspirations, ${plan.season || 'seasonal'} planning context, ${plan.cookingFrequency || batches.length} cooking day(s), and child age information. Child age used: ${childAgeDisplay}.`
        : 'AI explanations could not be generated for this plan. Please try again later.';

    whyPlanMealExplanations.value = {
      ...whyPlanMealExplanations.value,
      [planKey]: mealResults,
    };

    whyPlanExplanations.value = {
      ...whyPlanExplanations.value,
      [planKey]: summaryText,
    };
  } catch (error) {
    whyPlanError.value =
      error.message || 'Could not generate AI explanation for this plan.';
  } finally {
    whyPlanLoading.value = false;
  }
};

const modifySelectedWhyPlan = () => {
  if (!selectedWhyPlanId.value) {
    router.push('/weekly-plan');
    return;
  }

  const plan = weeklyPlans.value.find(
    (p) => String(p.id) === String(selectedWhyPlanId.value),
  );

  if (plan) {
    router.push(`/weekly-plan?mode=edit&planId=${plan.id}`);
  } else {
    router.push('/weekly-plan');
  }
};

const closeWhyPlanExplanation = () => {
  selectedWhyPlanId.value = null;
  whyPlanError.value = '';
};

const goToWeeklyPlanFromWhy = () => {
  router.push('/weekly-plan');
};

const scrollToWhyThisPlanAnchor = () => {
  if (route.hash !== '#why-this-plan') return;

  nextTick(() => {
    document
      .getElementById('why-this-plan')
      ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
};

const loadSavedPlans = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';

    const [plans, children] = await Promise.all([
      getWeeklyPlans(),
      getChildren().catch(() => []),
    ]);

    savedPlans.value = Array.isArray(plans) ? plans.map(normalizePlan) : [];
    userChildren.value = Array.isArray(children) ? children : [];

    if (sortedWeeklyPlans.value.length > 0 && !selectedReusePlanId.value) {
      selectedReusePlanId.value = String(sortedWeeklyPlans.value[0].id);
    }

    if (sortedWeeklyPlans.value.length > 0 && !selectedWhyPlanId.value) {
      selectedWhyPlanId.value = String(sortedWeeklyPlans.value[0].id);
    }
  } catch (error) {
    console.error('Failed to load saved plans:', error);
    errorMessage.value = error.message || 'Failed to load saved plans.';
    savedPlans.value = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => loadSavedPlans());

watch([() => route.hash, isLoading, whyPlanDisplayList], () => {
  if (route.hash !== '#why-this-plan') return;
  if (isLoading.value) return;

  scrollToWhyThisPlanAnchor();
}, { flush: 'post' });

watch(sortedWeeklyPlans, (plans) => {
  if (plans.length === 0) {
    selectedReusePlanId.value = null;
    selectedWhyPlanId.value = null;
    return;
  }

  const reuseStillExists = plans.some(
    (plan) => String(plan.id) === String(selectedReusePlanId.value),
  );

  if (!reuseStillExists) {
    selectedReusePlanId.value = String(plans[0].id);
  }

  const whyStillExists = plans.some(
    (plan) => String(plan.id) === String(selectedWhyPlanId.value),
  );

  if (!whyStillExists) {
    selectedWhyPlanId.value = String(plans[0].id);
  }
});

const formatDate = (dateString) => {
  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) return 'Recently';

  const diffDays = Math.floor(Math.abs(new Date() - date) / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;

  return date.toLocaleDateString('en-AU', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

// ── Actions ───────────────────────────
const handleViewPlan = (plan) => router.push(`/weekly-plan?mode=view&planId=${plan.id}`);
const handleEditPlan = (plan) => router.push(`/weekly-plan?mode=edit&planId=${plan.id}`);
const handleReusePlan = (plan) => router.push(`/weekly-plan?mode=reuse&planId=${plan.id}`);
const handleAdjustPlan = (plan) => router.push(`/weekly-plan?mode=adjust&planId=${plan.id}`);

const handleDuplicatePlan = async (plan) => {
  try {
    errorMessage.value = '';
    await duplicateWeeklyPlan(plan.id);
    await loadSavedPlans();
  } catch (error) {
    errorMessage.value = error.message || 'Duplicate failed.';
  }
};

const handleDeletePlan = async (planId) => {
  if (!confirm('Are you sure you want to delete this plan?')) return;

  try {
    errorMessage.value = '';
    await deleteWeeklyPlan(planId);
    savedPlans.value = savedPlans.value.filter(
      (plan) => String(plan.id) !== String(planId),
    );
  } catch (error) {
    errorMessage.value = error.message || 'Failed to delete plan.';
  }
};

const handleImageError = (event) => {
  if (event.target.src !== PLAN_IMAGE_FALLBACK) {
    event.target.src = PLAN_IMAGE_FALLBACK;
  }
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.whitespace-pre-line {
  white-space: pre-line;
}
</style>