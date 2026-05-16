<template>
  <div class="min-h-screen bg-[#FAF9F6]">
    <!-- Header -->
    <div class="pt-7 pb-5 sm:pt-10 sm:pb-8">
      <div class="container mx-auto max-w-4xl px-4 text-center sm:px-6">
        <h1 class="mb-3 text-3xl font-semibold leading-tight text-[#2C5F2D] sm:text-4xl md:text-5xl">
          Knowledge Hub
        </h1>
        <p class="mx-auto max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-lg md:text-xl">
          Learn about serving sizes, food groups, and what to watch out for in everyday foods.
        </p>
      </div>
    </div>

    <div class="relative py-5 pb-16 sm:py-10 sm:pb-24">
      <!-- Background -->
      <div class="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true">
        <div class="absolute inset-0 bg-[#FAF9F6]"></div>
        <div
          class="absolute inset-0 bg-center bg-cover opacity-35 sm:opacity-55"
          style="background-image: url('https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1600');"
        ></div>
        <div class="absolute top-0 left-0 right-0 z-[1] h-16 bg-gradient-to-b from-[#FAF9F6] via-[#FAF9F6]/80 to-transparent sm:h-20"></div>
        <div class="absolute bottom-0 left-0 right-0 z-[1] h-20 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6]/85 to-transparent sm:h-28"></div>
      </div>

      <div class="container relative z-10 mx-auto max-w-5xl px-4 sm:px-6">
        <!-- Tabs -->
        <div
          role="tablist"
          aria-label="Knowledge Hub sections"
          class="-mx-4 mb-4 flex gap-2 overflow-x-auto px-4 pb-2 sm:mx-0 sm:mb-5 sm:flex-wrap sm:justify-center sm:overflow-visible sm:px-0 sm:pb-0"
        >
          <div
            v-for="tab in hubTabs"
            :key="tab.id"
            class="relative shrink-0 group"
          >
            <button
              type="button"
              role="tab"
              :aria-selected="activeHubTab === tab.id"
              :aria-controls="`panel-${tab.id}`"
              :id="`tab-${tab.id}`"
              @click="onHubTabActivate($event, tab.id)"
              :class="[
                'whitespace-nowrap rounded-full border px-4 py-2.5 text-sm font-medium transition-all sm:px-5',
                activeHubTab === tab.id
                  ? 'bg-[#2C5F2D] text-white border-[#2C5F2D] shadow-sm'
                  : 'bg-white text-[#2C5F2D] border-[#D6E7DC] hover:border-[#A8D5BA] hover:bg-[#A8D5BA]/10',
              ]"
            >
              {{ tab.label }}
            </button>

            <div
              role="tooltip"
              class="absolute bottom-full left-1/2 z-40 mb-3 hidden w-max max-w-[min(22rem,calc(100vw-2rem))] -translate-x-1/2 translate-y-1 rounded-xl border border-[#A8D5BA]/40 bg-white p-4 text-left text-sm leading-relaxed text-muted-foreground opacity-0 shadow-lg transition-all duration-200 pointer-events-none group-hover:translate-y-0 group-hover:opacity-100 md:block"
            >
              {{ tab.hint }}
            </div>
          </div>
        </div>

        <!-- Serving Size Calculator -->
        <section
          :id="`panel-serving`"
          role="tabpanel"
          aria-labelledby="tab-serving"
          v-show="activeHubTab === 'serving'"
          class="rounded-3xl border border-[#E8E4DC] bg-white p-5 shadow-sm sm:p-6 md:p-10"
        >
          <div class="mb-7 flex flex-col gap-4 lg:mb-8 lg:flex-row lg:items-start lg:justify-between lg:gap-5">
            <div>
              <h2 class="mb-1 text-2xl font-semibold leading-tight text-[#2C5F2D] md:text-3xl">
                Serving Size Calculator
              </h2>
              <p class="max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-base">
                Choose one child profile, then see an age-based serving guide personalised with saved child information.
              </p>
            </div>

            <div class="max-w-sm rounded-2xl border border-[#E8E4DC] bg-[#F8F5EC] px-4 py-3 text-sm">
              <p class="mb-1 font-semibold text-[#2C5F2D]">How this is personalised</p>
              <p class="leading-relaxed text-muted-foreground">
                Serving amounts come from the age-band guideline. Notes and safer choices are adjusted using allergies, dietary needs, and nutrition focus.
              </p>
            </div>
          </div>

          <p class="mb-3 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
            Step 1 — Select your child
          </p>

          <div
            v-if="USE_STEP1_LOGIN_GATE && !isLoggedIn"
            class="mx-auto max-w-2xl rounded-2xl border border-gray-200 bg-white p-5 text-center shadow-sm"
          >
            <p class="text-sm text-muted-foreground sm:text-base">
              Sign in to save child profiles, weekly plans, and personalised recommendations.
            </p>
            <div class="mt-4 flex flex-col justify-center gap-3 sm:flex-row sm:flex-wrap">
              <button
                type="button"
                @click="goToLogin"
                class="rounded-lg bg-[#A8D5BA] px-6 py-3 text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:py-2"
              >
                Sign in
              </button>
              <button
                type="button"
                @click="goToRegister"
                class="rounded-lg border border-[#A8D5BA] bg-white px-6 py-3 text-[#2C5F2D] transition-colors hover:bg-[#A8D5BA]/10 sm:py-2"
              >
                Create account
              </button>
            </div>
          </div>

          <div
            v-else-if="isLoggedIn && (isLoadingProfiles || isLoadingServingTargets)"
            class="rounded-xl border bg-[#FAF9F6] p-4 text-center text-sm text-muted-foreground"
            aria-live="polite"
            aria-busy="true"
          >
            Loading your child profiles and serving targets…
          </div>

          <div v-else class="-mx-1 flex snap-x snap-mandatory gap-3 overflow-x-auto px-1 pb-2 sm:gap-4">
            <button
              v-for="p in step1Profiles"
              :key="p.id"
              type="button"
              @click="selectedChildId = p.id"
              :aria-pressed="selectedChildId === p.id"
              :class="[
                'w-[82vw] max-w-[280px] shrink-0 snap-start rounded-2xl border-2 p-4 text-left transition-all sm:w-[280px] sm:p-5',
                selectedChildId === p.id
                  ? 'border-[#2C5F2D] bg-[#A8D5BA]/15 shadow-md'
                  : 'border-gray-200 bg-[#FAF9F6] hover:border-[#A8D5BA]/60',
              ]"
            >
              <div class="mb-2 flex items-center gap-3">
                <div
                  class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#CDE7F0]/50 text-base font-semibold text-[#1B4965] sm:h-12 sm:w-12 sm:text-lg"
                  aria-hidden="true"
                >
                  {{ initials(p.name) }}
                </div>
                <div class="min-w-0">
                  <p class="truncate font-semibold text-[#111827]">{{ p.name }}</p>
                  <p class="text-sm text-muted-foreground">{{ p.ageGroup || 'Age on file' }}</p>
                </div>
              </div>

              <p
                v-if="p.allergies?.length"
                class="mt-2 rounded-lg bg-amber-50 px-2 py-1 text-xs text-amber-800"
              >
                Allergies: {{ p.allergies.join(', ') }}
              </p>

              <p
                v-if="p.dietaryRestriction"
                class="mt-2 rounded-lg bg-[#CDE7F0]/40 px-2 py-1 text-xs text-[#1B4965]"
              >
                {{ p.dietaryRestriction }}
              </p>

              <p
                v-if="p.isDemo"
                class="mt-2 text-[10px] uppercase tracking-wide text-muted-foreground"
              >
                Demo profile
              </p>

              <p
                v-else
                class="mt-2 text-[10px] uppercase tracking-wide text-[#2C5F2D]"
              >
                Saved profile
              </p>
            </button>
          </div>

          <p v-if="isShowingDemoProfiles" class="mt-3 max-w-2xl text-xs leading-relaxed text-muted-foreground">
            Preview mode: these sample profiles show how the calculator works. Sign in to use your saved child profiles and receive personalised serving guidance.
          </p>

          <p
            v-if="servingTargetError"
            class="mt-3 max-w-2xl text-xs text-red-600"
          >
            {{ servingTargetError }}
          </p>

          <template v-if="selectedChild && dailyServeRows.length">
            <div class="mt-8 mb-4 flex flex-col gap-3 md:mt-10 md:flex-row md:items-center md:justify-between">
              <div>
                <p class="text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
                  Step 2 — Personalised daily serves
                </p>
                <p class="mt-1 text-xs leading-relaxed text-muted-foreground">
                  Serving amounts use the age-band guideline. Personalised tags and notes come from the selected child profile.
                </p>
              </div>

              <div
                class="inline-flex w-fit items-center gap-2 rounded-full border border-[#D6E7DC] bg-[#F8F5EC] px-3 py-1 text-xs text-[#2C5F2D]"
              >
                <Info class="h-3.5 w-3.5" aria-hidden="true" />
                <span>{{ servingDataSourceLabel }}</span>
              </div>
            </div>

            <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4 lg:grid-cols-5">
              <div
                v-for="row in dailyServeRows"
                :key="row.groupKey"
                class="flex flex-col rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4"
              >
                <div class="mb-3 flex items-start justify-between gap-3">
                  <div
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-[#D6E7DC] bg-white text-[#2C5F2D]"
                    aria-hidden="true"
                  >
                    <component :is="row.icon" class="h-5 w-5" />
                  </div>

                  <span
                    v-if="row.personalisedTags?.length"
                    class="whitespace-nowrap rounded-full border border-[#D6E7DC] bg-white px-2 py-1 text-[10px] text-[#2C5F2D]"
                  >
                    Personalised
                  </span>
                </div>

                <h3 class="font-semibold leading-tight text-[#2C5F2D]">
                  {{ row.group }}
                </h3>

                <p class="mt-2 text-2xl font-bold text-[#111827]">
                  {{ formatServe(row.serves) }}
                  <span class="text-sm font-normal text-muted-foreground">serves</span>
                </p>

                <p class="mt-1 text-sm font-semibold text-[#2C5F2D]">
                  ≈ {{ row.estimatedGrams }} g/day
                </p>

                <div
                  v-if="row.personalisedTags?.length"
                  class="mt-3 flex flex-wrap gap-1"
                >
                  <span
                    v-for="tag in row.personalisedTags"
                    :key="tag"
                    class="rounded-full border border-[#D6E7DC] bg-white px-2 py-1 text-[11px] text-[#2C5F2D]"
                  >
                    {{ tag }}
                  </span>
                </div>

                <p class="mt-3 flex-1 text-xs leading-snug text-muted-foreground">
                  {{ row.example }}
                </p>

                <p
                  v-if="row.personalisedNote"
                  class="mt-3 rounded-xl border border-[#D6E7DC] bg-white px-3 py-2 text-xs leading-relaxed text-[#2C5F2D]"
                >
                  {{ row.personalisedNote }}
                </p>
              </div>
            </div>

            <div class="mt-6 flex flex-col gap-2 rounded-2xl bg-[#2C5F2D] px-5 py-4 text-white sm:mt-8 sm:flex-row sm:items-center sm:justify-between sm:gap-3">
              <span class="flex items-center gap-2 text-sm font-medium">
                Total daily target
                <span class="inline-flex" title="Educational serving target based on age band; not medical advice.">
                  <Info class="h-4 w-4 opacity-80" aria-label="Educational serving target based on age band; not medical advice." />
                </span>
              </span>
              <span class="text-left text-lg font-semibold tabular-nums sm:text-right">
                {{ totalDailyServes }} serves
                <span v-if="totalEstimatedGrams">
                  · ≈ {{ totalEstimatedGrams }} g/day
                </span>
              </span>
            </div>

            <div
              v-if="personalisedFocusNotes.length"
              class="mt-6 rounded-2xl border border-[#D6E7DC] bg-[#F8F5EC]/80 p-5 sm:mt-8"
            >
              <p class="mb-3 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
                Step 3 — Profile-based guidance for {{ selectedChild.name }}
              </p>

              <ul class="space-y-2 text-sm leading-relaxed text-muted-foreground">
                <li
                  v-for="note in personalisedFocusNotes"
                  :key="note.label + note.message"
                  class="flex gap-2"
                >
                  <span class="mt-0.5 text-[#2C5F2D]" aria-hidden="true">•</span>
                  <span>
                    <strong class="text-[#2C5F2D]">{{ note.label }}:</strong>
                    {{ note.message }}
                  </span>
                </li>
              </ul>
            </div>

            <p class="mt-3 text-xs leading-relaxed text-muted-foreground">
              Serve targets are based on the selected child's age band. Gram values are estimated using standard grams per serve by food group, because actual grams can vary by food type and preparation method.
            </p>
          </template>

          <p v-else-if="step1Profiles.length && !selectedChild" class="mt-8 text-center text-sm text-muted-foreground">
            Tap a child card above to load serving targets.
          </p>
        </section>

        <!-- Food Group Guide -->
        <section
          :id="`panel-guide`"
          role="tabpanel"
          aria-labelledby="tab-guide"
          v-show="activeHubTab === 'guide'"
          class="flex flex-col gap-4 md:flex-row md:gap-8"
        >
          <aside class="w-full shrink-0 overflow-hidden rounded-2xl border border-[#E8E4DC] bg-white shadow-sm md:w-56">
            <p class="px-4 pt-4 pb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Food groups
            </p>
            <nav
              aria-label="Food group navigation"
              class="flex gap-2 overflow-x-auto px-3 pb-3 md:block md:gap-0 md:overflow-visible md:px-0 md:pb-0"
            >
              <button
                v-for="g in foodGroupCatalog"
                :key="g.id"
                type="button"
                @click="selectedFoodGroupId = g.id"
                :aria-pressed="selectedFoodGroupId === g.id"
                :class="[
                  'flex shrink-0 items-center justify-between rounded-full border px-4 py-2.5 text-left text-sm transition-colors md:w-full md:rounded-none md:border-0 md:border-l-4 md:px-4 md:py-3',
                  selectedFoodGroupId === g.id
                    ? 'bg-[#A8D5BA]/20 border-[#2C5F2D] text-[#2C5F2D] font-medium md:border-l-[#2C5F2D]'
                    : 'border-[#D6E7DC] text-gray-700 hover:bg-[#FAF9F6] md:border-l-transparent',
                ]"
              >
                {{ g.label }}
                <ChevronRight class="ml-2 hidden h-4 w-4 shrink-0 text-muted-foreground md:block" aria-hidden="true" />
              </button>
            </nav>
          </aside>

          <div class="min-w-0 flex-1 rounded-3xl border border-[#E8E4DC] bg-white p-5 shadow-sm sm:p-6 md:p-10">
            <template v-if="activeFoodGroup">
              <div class="mb-5 flex items-center gap-2 sm:mb-6">
                <span class="-translate-y-0.5 shrink-0 select-none text-4xl leading-none md:text-5xl" aria-hidden="true">
                  {{ activeFoodGroup.emoji }}
                </span>
                <h2 class="text-2xl font-semibold text-[#2C5F2D] md:text-3xl">
                  {{ activeFoodGroup.label }}
                </h2>
              </div>

              <h3 class="mb-2 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
                Why it matters
              </h3>
              <p class="mb-6 text-sm leading-relaxed text-muted-foreground sm:mb-8 sm:text-base">
                {{ activeFoodGroup.why }}
              </p>

              <h3 class="mb-3 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
                Serving guide (per day)
              </h3>

              <div class="overflow-x-auto rounded-xl border border-[#E5E7EB]">
                <table class="w-full min-w-[560px] text-sm">
                  <thead>
                    <tr class="bg-[#FAF9F6] text-left text-[#374151]">
                      <th scope="col" class="px-4 py-3 font-semibold">Age (years)</th>
                      <th scope="col" class="px-4 py-3 font-semibold">Servings</th>
                      <th scope="col" class="px-4 py-3 font-semibold">Examples</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(r, idx) in activeFoodGroup.table"
                      :key="idx"
                      class="border-t border-[#E5E7EB] text-gray-800"
                    >
                      <td class="whitespace-nowrap px-4 py-3">{{ r.age }}</td>
                      <td class="px-4 py-3">{{ r.servings }}</td>
                      <td class="px-4 py-3 text-muted-foreground">{{ r.examples }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <p class="mt-3 text-xs leading-relaxed text-muted-foreground">
                {{ activeFoodGroup.footnote }}
              </p>
            </template>
          </div>
        </section>

        <!-- Additive Awareness Guide -->
        <section
          :id="`panel-heatmap`"
          role="tabpanel"
          aria-labelledby="tab-heatmap"
          v-show="activeHubTab === 'heatmap'"
          class="rounded-3xl border border-[#E8E4DC] bg-white p-5 shadow-sm sm:p-6 md:p-10"
        >
          <div class="mb-7 flex flex-col gap-4 lg:mb-8 lg:flex-row lg:items-start lg:justify-between lg:gap-6">
            <div>
              <h2 class="mb-1 text-2xl font-semibold leading-tight text-[#2C5F2D] md:text-3xl">
                {{ additiveGuide?.title || 'Additive Awareness Guide' }}
              </h2>
              <p class="max-w-3xl text-sm leading-relaxed text-muted-foreground sm:text-base">
                {{ additiveGuide?.description || 'Explore how often added sugar, preservatives, and artificial colours appear across packaged food categories in our database.' }}
              </p>
            </div>
            <div class="max-w-sm rounded-2xl border border-[#E8E4DC] bg-[#F8F5EC] px-4 py-3 text-sm text-[#2C5F2D]">
              <p class="mb-1 font-semibold">Why this matters</p>
              <p class="leading-relaxed text-muted-foreground">
                This guide helps parents decide which packaged food categories may need closer label checking.
              </p>
            </div>
          </div>

          <div
            v-if="isLoadingAdditive"
            class="rounded-2xl border bg-[#FAF9F6] p-5 text-center text-muted-foreground"
            aria-live="polite"
            aria-busy="true"
          >
            Loading additive insights...
          </div>

          <div
            v-else-if="additiveError"
            role="alert"
            class="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700"
          >
            {{ additiveError }}
          </div>

          <template v-else>
            <div v-if="additiveSummary" class="mb-7 grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4 xl:grid-cols-4 xl:mb-8">
              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Highest added sugar</p>
                <p
                  class="mt-2 text-lg font-semibold text-[#2C5F2D]"
                  :title="additiveSummary.highest_added_sugar?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_added_sugar?.category) }}
                </p>
                <p class="mt-1 text-2xl font-bold text-[#111827]">{{ additiveSummary.highest_added_sugar?.percent ?? 0 }}%</p>
              </div>

              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Highest preservatives</p>
                <p
                  class="mt-2 text-lg font-semibold text-[#2C5F2D]"
                  :title="additiveSummary.highest_preservatives?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_preservatives?.category) }}
                </p>
                <p class="mt-1 text-2xl font-bold text-[#111827]">{{ additiveSummary.highest_preservatives?.percent ?? 0 }}%</p>
              </div>

              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Highest colours</p>
                <p
                  class="mt-2 text-lg font-semibold text-[#2C5F2D]"
                  :title="additiveSummary.highest_artificial_colours?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_artificial_colours?.category) }}
                </p>
                <p class="mt-1 text-2xl font-bold text-[#111827]">{{ additiveSummary.highest_artificial_colours?.percent ?? 0 }}%</p>
              </div>

              <div class="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                <p class="text-xs font-semibold uppercase tracking-wide text-amber-800">Highest label-check priority</p>
                <p
                  class="mt-2 text-lg font-semibold text-amber-950"
                  :title="additiveSummary.highest_overall_priority?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_overall_priority?.category) }}
                </p>
                <p class="mt-1 text-sm text-amber-900">
                  {{ simplifyLabelPriority(additiveSummary.highest_overall_priority?.label_priority) }}
                </p>
              </div>
            </div>

            <div v-if="additiveGuide?.disclaimer" class="mb-7 rounded-2xl border border-[#D6E7DC] bg-[#F8F5EC]/70 p-4 sm:mb-8">
              <p class="text-sm leading-relaxed text-muted-foreground">{{ additiveGuide.disclaimer }}</p>
            </div>

            <!-- Desktop Table -->
            <div class="hidden overflow-x-auto rounded-xl border border-[#E5E7EB] md:block">
              <table class="w-full min-w-[760px] table-fixed text-sm">
                <thead>
                  <tr class="bg-[#FAF9F6]">
                    <th scope="col" class="w-[22%] px-3 py-3 text-left font-semibold text-[#374151]">Category</th>
                    <th scope="col" class="w-[18%] px-3 py-3 text-left font-semibold text-[#374151]">Label priority</th>
                    <th
                      v-for="col in additiveColumns"
                      :key="col.key"
                      scope="col"
                      class="px-3 py-3 text-center font-semibold text-[#374151]"
                    >
                      {{ col.label }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in additiveRows" :key="row.category" class="border-t border-[#E5E7EB]">
                    <td class="px-3 py-3 align-middle font-medium text-gray-800">
                      <div :title="row.category">
                        <p class="font-semibold text-[#111827]">
                          {{ getFriendlyCategoryName(row.category) }}
                        </p>

                        <p
                          v-if="getShortCategoryDescription(row.category)"
                          class="mt-1 text-xs leading-snug text-muted-foreground"
                        >
                          {{ getShortCategoryDescription(row.category) }}
                        </p>

                        <p class="mt-1 text-xs text-muted-foreground">
                          {{ row.total_products }} products
                        </p>
                      </div>
                    </td>

                    <td class="px-3 py-3 align-middle">
                      <div class="rounded-xl border border-[#E5E7EB] bg-[#FAF9F6] p-3">
                        <p class="font-semibold text-[#2C5F2D]">
                          {{ simplifyLabelPriority(row.label_priority) }}
                        </p>
                        <p class="mt-1 text-xs text-muted-foreground">Score: {{ row.risk_score }}</p>
                      </div>
                    </td>

                    <td v-for="col in additiveColumns" :key="col.key" class="px-3 py-2 text-center align-middle">
                      <div
                        :class="[
                          'relative flex min-h-[3.5rem] w-full items-center justify-center rounded-xl border px-4 py-3 font-semibold tabular-nums',
                          heatCellClass(row[col.key]?.level),
                        ]"
                      >
                        <AlertTriangle
                          v-if="row[col.key]?.level === 'warning'"
                          class="pointer-events-none absolute top-1/2 left-[calc(50%-2.1rem)] z-0 h-4 w-4 -translate-y-1/2 text-amber-700"
                          aria-label="High prevalence"
                        />
                        <span class="relative z-10 text-center">{{ row[col.key]?.percent ?? 0 }}%</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Mobile Cards -->
            <div class="space-y-3 md:hidden">
              <article
                v-for="row in additiveRows"
                :key="row.category"
                class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4"
              >
                <div class="mb-3 flex flex-col gap-2">
                  <div>
                    <h3 class="font-semibold leading-tight text-[#2C5F2D]" :title="row.category">
                      {{ getFriendlyCategoryName(row.category) }}
                    </h3>

                    <p
                      v-if="getShortCategoryDescription(row.category)"
                      class="mt-0.5 text-xs leading-snug text-muted-foreground"
                    >
                      {{ getShortCategoryDescription(row.category) }}
                    </p>

                    <p class="mt-1 text-xs text-muted-foreground">{{ row.total_products }} products</p>
                  </div>

                  <span class="w-fit rounded-full border border-[#D6E7DC] bg-white px-3 py-1 text-xs text-[#2C5F2D]">
                    {{ simplifyLabelPriority(row.label_priority) }}
                  </span>
                </div>

                <div class="space-y-2">
                  <div
                    v-for="col in additiveColumns"
                    :key="col.key"
                    class="flex items-center justify-between gap-3 rounded-xl border border-[#E5E7EB] bg-white px-3 py-2"
                  >
                    <span class="text-sm text-gray-700">{{ col.label }}</span>
                    <span :class="['rounded-lg border px-2 py-1 text-sm font-semibold', heatCellClass(row[col.key]?.level)]">
                      {{ row[col.key]?.percent ?? 0 }}%
                    </span>
                  </div>
                </div>

                <p class="mt-3 text-xs leading-relaxed text-muted-foreground">
                  {{ getSimpleAdditiveTip(row) }}
                </p>
              </article>
            </div>

            <div v-if="!additiveRows.length" class="mt-6 rounded-2xl border bg-[#FAF9F6] p-5 text-center text-muted-foreground">
              No additive records are available yet.
            </div>

            <div class="mt-7 grid gap-4 lg:mt-8 lg:grid-cols-2 lg:gap-6">
              <div class="rounded-2xl border border-[#E5E7EB] bg-white p-5">
                <p class="mb-3 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
                  How to read this
                </p>
                <div class="space-y-3">
                  <div v-for="item in additiveHowToRead" :key="item.level" class="flex items-start gap-3">
                    <span :class="['mt-0.5 h-5 w-10 shrink-0 rounded border', heatCellClass(item.level)]" aria-hidden="true"></span>
                    <div>
                      <p class="text-sm font-semibold text-gray-800">{{ item.label }}</p>
                      <p class="text-xs leading-relaxed text-muted-foreground">{{ item.meaning }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="rounded-2xl border border-[#E5E7EB] bg-white p-5">
                <p class="mb-3 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
                  Parent tips
                </p>
                <ul class="space-y-2 text-sm leading-relaxed text-muted-foreground">
                  <li v-for="tip in additiveTips" :key="tip" class="flex gap-2">
                    <span class="mt-0.5 text-[#2C5F2D]" aria-hidden="true">•</span>
                    <span>{{ tip }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </template>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import {
  Carrot,
  Apple,
  Wheat,
  Drumstick,
  Milk,
  Info,
  ChevronRight,
  AlertTriangle,
} from 'lucide-vue-next';
import {
  getChildren,
  getKnowledgeAdditiveAwareness,
  getKnowledgeChildrenServes,
} from '../services/api';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

const isLoggedIn = computed(() => authStore.isAuthenticated);

// ── Tabs ────────────────────────────────────────────────────────────────────
const activeHubTab = ref('serving');

const hubTabs = [
  {
    id: 'serving',
    label: 'Serving Size Calculator',
    hint: 'Pick a child profile, then see age-based serving targets with personalised notes from saved child information.',
  },
  {
    id: 'guide',
    label: 'Food Group Guide',
    hint: 'Choose a food group to read why it matters and scan age-based serving suggestions with everyday examples.',
  },
  {
    id: 'heatmap',
    label: 'Additive Awareness Guide',
    hint: 'Compare how often added sugar, preservatives and artificial colours appear across packaged food categories in our database.',
  },
];

function onHubTabActivate(e, tabId) {
  activeHubTab.value = tabId;
  if (e.detail > 0 && e.currentTarget instanceof HTMLElement) {
    e.currentTarget.blur();
  }
}

// ── Profiles ────────────────────────────────────────────────────────────────
const profiles = ref([]);
const isLoadingProfiles = ref(false);
const selectedChildId = ref(null);

const servingTargets = ref({});
const isLoadingServingTargets = ref(false);
const servingTargetError = ref('');

const USE_STEP1_LOGIN_GATE = false;

const MOCK_STEP1_CHILDREN = [
  {
    id: 'demo-emma',
    name: 'Emma',
    ageGroup: '7-9 years',
    allergies: [],
    nutritionFocus: ['calcium', 'variety'],
    dietaryRestriction: '',
    restrictionFlags: {},
    isDemo: true,
  },
  {
    id: 'demo-oliver',
    name: 'Oliver',
    ageGroup: '5-6 years',
    allergies: ['Peanuts'],
    nutritionFocus: ['iron'],
    dietaryRestriction: '',
    restrictionFlags: {},
    isDemo: true,
  },
  {
    id: 'demo-maya',
    name: 'Maya',
    ageGroup: '10-12 years',
    allergies: ['Milk'],
    nutritionFocus: ['vitamin_d'],
    dietaryRestriction: 'Dairy-free',
    restrictionFlags: { excludes_dairy: true },
    isDemo: true,
  },
];

const step1Profiles = computed(() => {
  if (USE_STEP1_LOGIN_GATE && !isLoggedIn.value) return [];

  if (isLoggedIn.value && profiles.value.length > 0) {
    return profiles.value.map((p) => ({ ...p, isDemo: false }));
  }

  return MOCK_STEP1_CHILDREN;
});

const isShowingDemoProfiles = computed(() => {
  if (USE_STEP1_LOGIN_GATE && !isLoggedIn.value) return false;
  return !(isLoggedIn.value && profiles.value.length > 0);
});

const allowedAgeGroups = ['5-6 years', '7-9 years', '10-12 years'];

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

const isActiveStatus = (value) => {
  return value === 1 || value === '1' || value === true;
};

const mapAllergiesToNames = (allergies) => {
  if (!Array.isArray(allergies)) return [];

  return allergies.map((allergy) => {
    if (typeof allergy === 'string' && Number.isNaN(Number(allergy))) {
      return allergy;
    }

    return allergenIdToName[Number(allergy)] || `Allergen #${allergy}`;
  });
};

const mapNutritionFocus = (child) => {
  const focus = [];

  if (isActiveStatus(child.iron_status)) focus.push('iron');
  if (isActiveStatus(child.calcium_status)) focus.push('calcium');
  if (isActiveStatus(child.vitamin_d_status)) focus.push('vitamin_d');
  if (isActiveStatus(child.variety_status)) focus.push('variety');

  return focus;
};

const mapRestrictionFlags = (child) => {
  return {
    excludes_meat: isActiveStatus(child.excludes_meat),
    excludes_fish: isActiveStatus(child.excludes_fish),
    excludes_dairy: isActiveStatus(child.excludes_dairy),
    excludes_egg: isActiveStatus(child.excludes_egg),
    excludes_pork: isActiveStatus(child.excludes_pork),
    excludes_shellfish: isActiveStatus(child.excludes_shellfish),
    excludes_gluten: isActiveStatus(child.excludes_gluten),
    excludes_nuts: isActiveStatus(child.excludes_nuts),
  };
};

const mapChildToProfile = (child) => {
  const normalizedAgeGroup = normalizeAgeGroup(child.age_band);

  return {
    id: child.child_id,
    name: child.child_name,
    ageGroup: normalizedAgeGroup || child.age_band || '',
    allergies: mapAllergiesToNames(child.allergies),
    nutritionFocus: mapNutritionFocus(child),
    dietaryRestriction: child.restriction_name || '',
    restrictionFlags: mapRestrictionFlags(child),
    isSupportedAge: allowedAgeGroups.includes(normalizedAgeGroup),
  };
};

const loadProfiles = async () => {
  if (!isLoggedIn.value) {
    profiles.value = [];
    return;
  }

  try {
    isLoadingProfiles.value = true;
    const children = await getChildren();
    const list = Array.isArray(children) ? children.map(mapChildToProfile) : [];
    profiles.value = list.filter((p) => p.isSupportedAge);

    if (profiles.value.length && !profiles.value.some((p) => p.id === selectedChildId.value)) {
      selectedChildId.value = profiles.value[0].id;
    }
  } catch (e) {
    console.error('Failed to load child profiles:', e);
    profiles.value = [];
  } finally {
    isLoadingProfiles.value = false;
  }
};

const loadServingTargets = async () => {
  if (!isLoggedIn.value) {
    servingTargets.value = {};
    servingTargetError.value = '';
    return;
  }

  try {
    isLoadingServingTargets.value = true;
    servingTargetError.value = '';

    const data = await getKnowledgeChildrenServes();
    const children = Array.isArray(data.children) ? data.children : [];

    servingTargets.value = children.reduce((acc, child) => {
      acc[String(child.child_id)] = child;
      return acc;
    }, {});
  } catch (error) {
    console.error('Failed to load serving targets:', error);
    servingTargetError.value =
      error.message || 'Failed to load serving size data.';
    servingTargets.value = {};
  } finally {
    isLoadingServingTargets.value = false;
  }
};

const selectedChild = computed(() =>
  step1Profiles.value.find((p) => p.id === selectedChildId.value) || null,
);

const selectedServingTarget = computed(() => {
  if (!selectedChildId.value) return null;
  return servingTargets.value[String(selectedChildId.value)] || null;
});

const ageBandKey = computed(() => {
  const g = selectedChild.value?.ageGroup || '';
  if (g === '5-6 years') return 'young';
  if (g === '7-9 years') return 'mid';
  return 'older';
});

const foodGroupDisplayMap = {
  vegetables: {
    label: 'Vegetables',
    icon: Carrot,
    example: 'e.g. ½ cup cooked vegetables or 1 cup salad',
    gramsPerServe: 75,
  },
  fruit: {
    label: 'Fruit',
    icon: Apple,
    example: 'e.g. 1 medium piece or 1 cup diced fruit',
    gramsPerServe: 150,
  },
  grains: {
    label: 'Grains',
    icon: Wheat,
    example: 'e.g. 1 slice bread or ½ cup cooked rice',
    gramsPerServe: 40,
  },
  protein: {
    label: 'Protein',
    icon: Drumstick,
    example: 'e.g. lean meat, eggs, beans, tofu, or fish',
    gramsPerServe: 65,
  },
  dairy: {
    label: 'Dairy / Alternatives',
    icon: Milk,
    example: 'e.g. milk, yoghurt, cheese, or fortified alternatives',
    gramsPerServe: 250,
  },
};

const normaliseFoodGroupKey = (name = '') => {
  const lower = String(name).toLowerCase();

  if (lower.includes('vegetable') || lower.includes('legume')) return 'vegetables';
  if (lower.includes('fruit')) return 'fruit';
  if (lower.includes('grain') || lower.includes('cereal')) return 'grains';
  if (
    lower.includes('protein') ||
    lower.includes('lean meat') ||
    lower.includes('meat') ||
    lower.includes('egg') ||
    lower.includes('tofu') ||
    lower.includes('nut') ||
    lower.includes('seed')
  ) {
    return 'protein';
  }
  if (
    lower.includes('dairy') ||
    lower.includes('milk') ||
    lower.includes('cheese') ||
    lower.includes('yoghurt') ||
    lower.includes('yogurt')
  ) {
    return 'dairy';
  }

  return lower;
};

const hasAllergy = (keyword) => {
  const allergies = selectedChild.value?.allergies || [];
  return allergies.some((item) =>
    String(item).toLowerCase().includes(keyword.toLowerCase()),
  );
};

const hasNutritionFocus = (focus) => {
  return selectedChild.value?.nutritionFocus?.includes(focus);
};

const hasRestriction = (flag) => {
  return Boolean(selectedChild.value?.restrictionFlags?.[flag]);
};

const buildGroupPersonalisedNote = (groupKey) => {
  if (!selectedChild.value) return '';

  if (groupKey === 'dairy') {
    if (hasAllergy('milk') || hasRestriction('excludes_dairy')) {
      return 'Milk or dairy restriction detected. Choose calcium-fortified alternatives that are safe for this child.';
    }

    if (hasNutritionFocus('calcium') || hasNutritionFocus('vitamin_d')) {
      return 'Prioritise dairy or fortified alternatives because this profile has calcium or vitamin D support selected.';
    }
  }

  if (groupKey === 'protein') {
    if (hasAllergy('peanut') || hasAllergy('tree nuts') || hasRestriction('excludes_nuts')) {
      return 'Nut allergy or nut restriction detected. Avoid nut-based snacks and choose safe protein options.';
    }

    if (hasRestriction('excludes_meat')) {
      return 'This profile avoids meat. Try beans, lentils, tofu, eggs, yoghurt, or other suitable protein options.';
    }

    if (hasNutritionFocus('iron')) {
      return 'Iron support selected. Include iron-rich protein options such as lean meat, eggs, beans, lentils, tofu, or fortified grains.';
    }
  }

  if (groupKey === 'grains') {
    if (hasRestriction('excludes_gluten') || hasAllergy('wheat')) {
      return 'Gluten or wheat restriction detected. Choose suitable grain options such as rice, corn, quinoa, or gluten-free bread.';
    }
  }

  if (groupKey === 'vegetables') {
    if (hasNutritionFocus('variety')) {
      return 'Food variety support selected. Try rotating colours and textures across the week.';
    }
  }

  if (groupKey === 'fruit') {
    if (hasNutritionFocus('variety')) {
      return 'Use different fruit colours across the week to support variety and acceptance.';
    }
  }

  return '';
};

const buildPersonalisedTags = (groupKey) => {
  const tags = [];

  if (groupKey === 'dairy') {
    if (hasAllergy('milk') || hasRestriction('excludes_dairy')) {
      tags.push('Dairy-safe option');
    }

    if (hasNutritionFocus('calcium')) {
      tags.push('Calcium focus');
    }

    if (hasNutritionFocus('vitamin_d')) {
      tags.push('Vitamin D support');
    }
  }

  if (groupKey === 'protein') {
    if (hasAllergy('peanut') || hasAllergy('tree nuts') || hasRestriction('excludes_nuts')) {
      tags.push('Nut-safe choices');
    }

    if (hasRestriction('excludes_meat')) {
      tags.push('Meat-free protein');
    }

    if (hasNutritionFocus('iron')) {
      tags.push('Iron focus');
    }
  }

  if (groupKey === 'grains') {
    if (hasAllergy('wheat') || hasRestriction('excludes_gluten')) {
      tags.push('Gluten-free options');
    }
  }

  if (groupKey === 'vegetables' || groupKey === 'fruit') {
    if (hasNutritionFocus('variety')) {
      tags.push('Variety focus');
    }
  }

  return tags;
};

const mapBackendServeRow = (row) => {
  const key = normaliseFoodGroupKey(row.food_group_name);
  const display = foodGroupDisplayMap[key] || {
    label: row.food_group_name || 'Food group',
    icon: Info,
    example: row.example || 'Use this as a general daily serving guide.',
    gramsPerServe: 100,
  };

  const serves = Number(row.recommended_serves || 0);
  const gramsPerServe = Number(row.grams_per_serve || display.gramsPerServe || 100);
  const estimatedGrams = Number(row.estimated_grams || Math.round(serves * gramsPerServe));

  return {
    group: display.label,
    groupKey: key,
    serves,
    gramsPerServe,
    estimatedGrams,
    example: row.example || display.example,
    icon: display.icon,
    personalisedNote: buildGroupPersonalisedNote(key),
    personalisedTags: buildPersonalisedTags(key),
  };
};

const buildAgeBasedPersonalisedServeRows = (rows = []) => {
  const order = ['vegetables', 'fruit', 'grains', 'protein', 'dairy'];

  const grouped = rows.reduce((acc, row) => {
    const key = row.groupKey || normaliseFoodGroupKey(row.group);

    if (!acc[key]) {
      acc[key] = {
        ...row,
        servesList: [],
        gramsList: [],
      };
    }

    acc[key].servesList.push(Number(row.serves || 0));
    acc[key].gramsList.push(Number(row.estimatedGrams || 0));

    return acc;
  }, {});

  return order
    .map((key) => grouped[key])
    .filter(Boolean)
    .map((row) => {
      const averageServes =
        row.servesList.reduce((sum, value) => sum + value, 0) /
        row.servesList.length;

      const averageGrams =
        row.gramsList.reduce((sum, value) => sum + value, 0) /
        row.gramsList.length;

      return {
        ...row,
        serves: Math.round(averageServes * 2) / 2,
        estimatedGrams: Math.round(averageGrams),
        personalisedNote: buildGroupPersonalisedNote(row.groupKey),
        personalisedTags: buildPersonalisedTags(row.groupKey),
      };
    });
};

const servePresets = {
  young: [
    { group: 'Vegetables', groupKey: 'vegetables', serves: 4.5, icon: Carrot },
    { group: 'Fruit', groupKey: 'fruit', serves: 1.5, icon: Apple },
    { group: 'Grains', groupKey: 'grains', serves: 4, icon: Wheat },
    { group: 'Protein', groupKey: 'protein', serves: 1.5, icon: Drumstick },
    { group: 'Dairy / Alternatives', groupKey: 'dairy', serves: 2, icon: Milk },
  ],
  mid: [
    { group: 'Vegetables', groupKey: 'vegetables', serves: 5, icon: Carrot },
    { group: 'Fruit', groupKey: 'fruit', serves: 2, icon: Apple },
    { group: 'Grains', groupKey: 'grains', serves: 5, icon: Wheat },
    { group: 'Protein', groupKey: 'protein', serves: 2.5, icon: Drumstick },
    { group: 'Dairy / Alternatives', groupKey: 'dairy', serves: 2.5, icon: Milk },
  ],
  older: [
    { group: 'Vegetables', groupKey: 'vegetables', serves: 5.5, icon: Carrot },
    { group: 'Fruit', groupKey: 'fruit', serves: 2, icon: Apple },
    { group: 'Grains', groupKey: 'grains', serves: 6, icon: Wheat },
    { group: 'Protein', groupKey: 'protein', serves: 2.5, icon: Drumstick },
    { group: 'Dairy / Alternatives', groupKey: 'dairy', serves: 3, icon: Milk },
  ],
};

const mapPresetServeRow = (row) => {
  const display = foodGroupDisplayMap[row.groupKey] || foodGroupDisplayMap.vegetables;
  const gramsPerServe = display.gramsPerServe;
  const estimatedGrams = Math.round(Number(row.serves || 0) * gramsPerServe);

  return {
    ...row,
    example: display.example,
    gramsPerServe,
    estimatedGrams,
    personalisedNote: buildGroupPersonalisedNote(row.groupKey),
    personalisedTags: buildPersonalisedTags(row.groupKey),
  };
};

const dailyServeRows = computed(() => {
  const backendRows = selectedServingTarget.value?.recommended_serves;

  if (Array.isArray(backendRows) && backendRows.length > 0) {
    const mappedRows = backendRows.map(mapBackendServeRow);
    return buildAgeBasedPersonalisedServeRows(mappedRows);
  }

  return (servePresets[ageBandKey.value] || servePresets.mid).map(mapPresetServeRow);
});

const totalDailyServes = computed(() => {
  const total = dailyServeRows.value.reduce(
    (sum, row) => sum + Number(row.serves || 0),
    0,
  );

  return total.toFixed(1);
});

const totalEstimatedGrams = computed(() => {
  const total = dailyServeRows.value.reduce(
    (sum, row) => sum + Number(row.estimatedGrams || 0),
    0,
  );

  return total || null;
});

const servingDataSourceLabel = computed(() => {
  if (selectedServingTarget.value?.recommended_serves?.length) {
    return 'Age-based guideline personalised with child profile';
  }

  return 'Preview estimate';
});

const formatServe = (value) => {
  const number = Number(value);

  if (Number.isNaN(number)) return value;

  return Number.isInteger(number) ? String(number) : number.toFixed(1);
};

const personalisedFocusNotes = computed(() => {
  const child = selectedChild.value;

  if (!child) return [];

  const notes = [];

  if (child.isDemo) {
    notes.push({
      label: 'Preview mode',
      message: 'These notes show how saved nutrition focus, allergies, and dietary restrictions can change guidance.',
    });
  }

  if (hasNutritionFocus('iron')) {
    notes.push({
      label: 'Iron support',
      message: 'Include iron-rich foods such as lean meat, eggs, beans, lentils, tofu, or fortified grains.',
    });
  }

  if (hasNutritionFocus('calcium')) {
    notes.push({
      label: 'Calcium support',
      message: 'Dairy or calcium-fortified alternatives are important for this profile.',
    });
  }

  if (hasNutritionFocus('vitamin_d')) {
    notes.push({
      label: 'Vitamin D support',
      message: 'Consider vitamin D supportive foods such as eggs, oily fish, fortified milk, or fortified alternatives.',
    });
  }

  if (hasNutritionFocus('variety')) {
    notes.push({
      label: 'Food variety',
      message: 'Rotate colours, textures, and food groups across the school week.',
    });
  }

  if (hasAllergy('milk')) {
    notes.push({
      label: 'Milk allergy',
      message: 'Use safe calcium-fortified alternatives instead of regular dairy foods.',
    });
  }

  if (hasAllergy('peanut') || hasAllergy('tree nuts')) {
    notes.push({
      label: 'Nut allergy',
      message: 'Avoid nut-based snacks and choose safe protein options.',
    });
  }

  if (hasAllergy('wheat') || hasRestriction('excludes_gluten')) {
    notes.push({
      label: 'Gluten or wheat restriction',
      message: 'Choose suitable grain options such as rice, corn, quinoa, or gluten-free bread.',
    });
  }

  if (hasRestriction('excludes_meat')) {
    notes.push({
      label: 'Meat-free profile',
      message: 'Use beans, lentils, tofu, eggs, yoghurt, or other suitable protein alternatives.',
    });
  }

  if (hasRestriction('excludes_dairy')) {
    notes.push({
      label: 'Dairy-free profile',
      message: 'Choose calcium-fortified alternatives where suitable.',
    });
  }

  if (!notes.length) {
    notes.push({
      label: 'Balanced lunchbox',
      message: 'No special restriction was detected, so the calculator shows general age-based guidance.',
    });
  }

  return notes;
});

const foodGroupCatalog = [
  {
    id: 'vegetables',
    label: 'Vegetables',
    emoji: '🥦',
    why: 'Vegetables provide vitamins, minerals, fibre and antioxidants that help your child grow strong and stay healthy.',
    table: [
      { age: '4 – 8', servings: '2 – 2½ cups', examples: 'Carrots, spinach, broccoli, beans' },
      { age: '9 – 13', servings: '2½ – 3 cups', examples: 'Mixed vegetables, sweet potato, peas' },
    ],
    footnote: '* 1 cup = 1 cup raw leafy vegetables or ½ cup cooked vegetables.',
  },
  {
    id: 'fruits',
    label: 'Fruits',
    emoji: '🍎',
    why: 'Fruit adds vitamin C, potassium and fibre, and naturally sweet flavours that can replace discretionary snacks.',
    table: [
      { age: '4 – 8', servings: '1 – 1½', examples: 'Apple, banana, berries, melon wedges' },
      { age: '9 – 13', servings: '1½ – 2', examples: 'Stone fruit, citrus, frozen fruit in yoghurt' },
    ],
    footnote: '* One serve ≈ 1 medium fruit or 1 cup diced fruit.',
  },
  {
    id: 'grains',
    label: 'Grains',
    emoji: '🌾',
    why: 'Whole grains supply steady energy and B vitamins to fuel school days and active play.',
    table: [
      { age: '4 – 8', servings: '4 – 5', examples: 'Wholegrain bread, oats, brown rice, pasta' },
      { age: '9 – 13', servings: '5 – 6', examples: 'Quinoa wraps, high-fibre cereals, barley soups' },
    ],
    footnote: '* One serve ≈ 1 slice bread or ½ cup cooked grains.',
  },
  {
    id: 'protein',
    label: 'Protein foods',
    emoji: '🍗',
    why: 'Protein supports muscle repair, immune function and growth spurts in school-aged children.',
    table: [
      { age: '4 – 8', servings: '1½ – 2', examples: 'Lean meat, tofu, eggs, lentils' },
      { age: '9 – 13', servings: '2 – 2½', examples: 'Fish twice weekly, chickpeas, nut-free dips' },
    ],
    footnote: '* One serve ≈ 65–80 g cooked meat or plant equivalent.',
  },
  {
    id: 'dairy',
    label: 'Dairy',
    emoji: '🥛',
    why: 'Dairy and fortified alternatives supply calcium for bones and teeth during rapid growth.',
    table: [
      { age: '4 – 8', servings: '1½ – 2', examples: 'Milk on cereal, cheese sticks, yoghurt tubs' },
      { age: '9 – 13', servings: '2 – 3', examples: 'Smoothies, fortified soy drink, cottage cheese' },
    ],
    footnote: '* One serve ≈ 1 cup milk or 2 slices cheese; choose unsweetened options where possible.',
  },
];

const selectedFoodGroupId = ref('vegetables');

const activeFoodGroup = computed(() =>
  foodGroupCatalog.find((g) => g.id === selectedFoodGroupId.value) || foodGroupCatalog[0],
);

// ── Additive Awareness ───────────────────────────────────────────────────────
const additiveColumns = [
  { key: 'added_sugar', label: 'Added sugar' },
  { key: 'preservatives', label: 'Preservatives' },
  { key: 'artificial_colours', label: 'Artificial colours' },
];

const additiveGuide = ref(null);
const isLoadingAdditive = ref(false);
const additiveError = ref('');

const additiveRows = computed(() => additiveGuide.value?.heatmap || []);
const additiveSummary = computed(() => additiveGuide.value?.summary || null);
const additiveTips = computed(() => additiveGuide.value?.parent_tips || []);
const additiveHowToRead = computed(() => additiveGuide.value?.how_to_read || []);

const loadAdditiveAwareness = async () => {
  try {
    isLoadingAdditive.value = true;
    additiveError.value = '';
    additiveGuide.value = await getKnowledgeAdditiveAwareness();
  } catch (error) {
    console.error('Failed to load additive awareness guide:', error);
    additiveError.value = error.message || 'Failed to load additive awareness guide.';
  } finally {
    isLoadingAdditive.value = false;
  }
};

const getFriendlyCategoryName = (category = '') => {
  const text = String(category).trim();
  const lower = text.toLowerCase();

  const rules = [
    { keywords: ['ice creams', 'ice cream'], label: 'Ice creams' },
    { keywords: ['breakfast cereals'], label: 'Breakfast cereals' },
    { keywords: ['candies', 'confectioneries'], label: 'Candies' },
    { keywords: ['biscuits'], label: 'Biscuits' },
    { keywords: ['crackers'], label: 'Crackers' },
    { keywords: ['breads'], label: 'Breads' },
    { keywords: ['yogurts', 'yoghurt', 'yoghurts'], label: 'Yogurts' },
    { keywords: ['chocolate candies', 'bars covered with chocolate', 'chocolate'], label: 'Chocolate bars' },
    { keywords: ['honeys', 'sweeteners', 'sweet spreads'], label: 'Honey / sweet spreads' },
    { keywords: ['condiments'], label: 'Condiments' },
    { keywords: ['baking'], label: 'Baking products' },
    { keywords: ['snacks'], label: 'Snacks' },
  ];

  const matched = rules.find((rule) =>
    rule.keywords.some((keyword) => lower.includes(keyword)),
  );

  if (matched) return matched.label;

  const parts = text
    .split(',')
    .map((part) => part.trim())
    .filter(Boolean);

  return parts[parts.length - 1] || 'Other category';
};

const getShortCategoryDescription = (category = '') => {
  const text = String(category).trim();
  const parts = text
    .split(',')
    .map((part) => part.trim())
    .filter(Boolean);

  if (parts.length <= 1) return '';

  return parts.slice(0, -1).slice(-2).join(' / ');
};

const getSimpleAdditiveTip = (row) => {
  const name = getFriendlyCategoryName(row.category);

  const sugar = row.added_sugar?.percent || 0;
  const preservatives = row.preservatives?.percent || 0;
  const colours = row.artificial_colours?.percent || 0;

  const highest = Math.max(sugar, preservatives, colours);

  if (highest === sugar && sugar >= 60) {
    return `${name} often contains added sugar in the available records. Compare labels and choose lower-sugar options when possible.`;
  }

  if (highest === colours && colours >= 40) {
    return `${name} often contains artificial colours. Check the ingredient list before choosing regular lunchbox items.`;
  }

  if (highest === preservatives && preservatives >= 30) {
    return `${name} may need closer preservative checking. Compare simpler ingredient lists when possible.`;
  }

  return `${name} shows a lower additive signal, but it is still useful to compare labels.`;
};

const simplifyLabelPriority = (priority = '') => {
  const text = String(priority).toLowerCase();

  if (text.includes('high')) return 'High priority';
  if (text.includes('moderate')) return 'Moderate';
  if (text.includes('low')) return 'Low priority';

  return priority || 'No signal';
};

function heatCellClass(level) {
  if (level === 'low') return 'bg-white border-[#E5E7EB] text-gray-800';
  if (level === 'medium') return 'bg-[#A8D5BA]/25 border-[#A8D5BA]/40 text-[#1a3d1c]';
  if (level === 'high') return 'bg-[#A8D5BA]/45 border-[#8FC2A4] text-[#142f16]';
  return 'bg-amber-100 border-amber-300 text-amber-950';
}

const initials = (name) => {
  if (!name || typeof name !== 'string') return '?';

  const parts = name.trim().split(/\s+/);

  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();

  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

const goToLogin = () => {
  window.location.href = '/login?redirect=/knowledge-hub-prototype';
};

const goToRegister = () => {
  window.location.href = '/register';
};

// ── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(() => {
  loadProfiles();
  loadServingTargets();
  loadAdditiveAwareness();
});

watch(
  step1Profiles,
  (list) => {
    if (!list.length) {
      selectedChildId.value = null;
      return;
    }

    if (!selectedChildId.value || !list.some((p) => p.id === selectedChildId.value)) {
      selectedChildId.value = list[0].id;
    }
  },
  { immediate: true },
);

watch(() => authStore.token, () => {
  loadProfiles();
  loadServingTargets();
});

watch(isLoggedIn, (v) => {
  if (v) {
    loadProfiles();
    loadServingTargets();
  } else {
    profiles.value = [];
    servingTargets.value = {};
  }
});
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>