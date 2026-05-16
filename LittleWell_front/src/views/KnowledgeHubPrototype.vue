<template>
  <div class="min-h-screen bg-[#FAF9F6]">
    <div class="pt-10 pb-8">
      <div class="container mx-auto px-6 max-w-4xl text-center">
        <h1 class="text-4xl md:text-5xl mb-3 text-[#2C5F2D]">Knowledge Hub</h1>
        <p class="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          Learn about serving sizes, food groups, and what to watch out for in everyday foods.
        </p>
      </div>
    </div>

    <div class="relative py-10 pb-24">
      <div class="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true">
        <div class="absolute inset-0 bg-[#FAF9F6]"></div>
        <div
          class="absolute inset-0 bg-center bg-cover bg-fixed opacity-55"
          style="background-image: url('https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1600');"
        ></div>
        <div class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-b from-[#FAF9F6] via-[#FAF9F6]/75 to-transparent z-[1]"></div>
        <div class="absolute bottom-0 left-0 right-0 h-28 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6]/80 to-transparent z-[1]"></div>
      </div>

      <div class="container relative z-10 mx-auto max-w-5xl px-6">
        <!-- Tabs -->
        <div
          role="tablist"
          aria-label="Knowledge Hub sections"
          class="flex flex-wrap justify-center gap-2 mb-5"
        >
          <div
            v-for="tab in hubTabs"
            :key="tab.id"
            class="relative group"
          >
            <button
              type="button"
              role="tab"
              :aria-selected="activeHubTab === tab.id"
              :aria-controls="`panel-${tab.id}`"
              :id="`tab-${tab.id}`"
              @click="onHubTabActivate($event, tab.id)"
              :class="[
                'px-5 py-2.5 rounded-full text-sm font-medium transition-all border',
                activeHubTab === tab.id
                  ? 'bg-[#2C5F2D] text-white border-[#2C5F2D] shadow-sm'
                  : 'bg-white text-[#2C5F2D] border-[#D6E7DC] hover:border-[#A8D5BA] hover:bg-[#A8D5BA]/10',
              ]"
            >
              {{ tab.label }}
            </button>

            <div
              role="tooltip"
              class="absolute bottom-full left-1/2 z-40 mb-3 hidden w-max max-w-[min(22rem,calc(100vw-2rem))] -translate-x-1/2 rounded-xl border border-[#A8D5BA]/40 bg-white p-4 text-left text-sm leading-relaxed text-muted-foreground shadow-lg opacity-0 pointer-events-none transition-all duration-200 translate-y-1 group-hover:translate-y-0 group-hover:opacity-100 md:block"
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
          class="bg-white rounded-3xl border border-[#E8E4DC] shadow-sm p-6 md:p-10"
        >
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-5 mb-8">
            <div>
              <h2 class="text-2xl md:text-3xl text-[#2C5F2D] mb-1">
                Serving Size Calculator
              </h2>
              <p class="text-muted-foreground max-w-2xl">
                Choose one of your child profiles, then review age-based daily serves with personalised guidance.
              </p>
            </div>

            <div class="rounded-2xl bg-[#F8F5EC] border border-[#E8E4DC] px-4 py-3 text-sm max-w-sm">
              <p class="font-semibold text-[#2C5F2D] mb-1">Personalised calculation</p>
              <p class="text-muted-foreground leading-relaxed">
                Base targets come from age-band serving data. Notes are adjusted using saved nutrition focus, allergies, and dietary needs.
              </p>
            </div>
          </div>

          <p class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide mb-3">
            Step 1 — Select your child
          </p>

          <div
            v-if="USE_STEP1_LOGIN_GATE && !isLoggedIn"
            class="bg-white border border-gray-200 rounded-2xl p-5 text-center shadow-sm max-w-2xl mx-auto"
          >
            <p class="text-muted-foreground">
              Sign in to save child profiles, weekly plans, and personalised recommendations.
            </p>
            <div class="flex flex-wrap justify-center gap-3 mt-4">
              <button
                type="button"
                @click="goToLogin"
                class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg px-6 py-2 transition-colors"
              >
                Sign in
              </button>
              <button
                type="button"
                @click="goToRegister"
                class="bg-white border border-[#A8D5BA] text-[#2C5F2D] rounded-lg px-6 py-2 hover:bg-[#A8D5BA]/10 transition-colors"
              >
                Create account
              </button>
            </div>
          </div>

          <div
            v-else-if="isLoggedIn && (isLoadingProfiles || isLoadingServingTargets)"
            class="p-4 rounded-xl border bg-[#FAF9F6] text-center text-muted-foreground text-sm"
            aria-live="polite"
            aria-busy="true"
          >
            Loading your child profiles and serving targets…
          </div>

          <div v-else class="flex gap-4 overflow-x-auto pb-2 -mx-1 px-1 snap-x snap-mandatory">
            <button
              v-for="p in step1Profiles"
              :key="p.id"
              type="button"
              @click="selectedChildId = p.id"
              :aria-pressed="selectedChildId === p.id"
              :class="[
                'flex-shrink-0 w-[min(100%,280px)] snap-start text-left rounded-2xl border-2 p-5 transition-all',
                selectedChildId === p.id
                  ? 'border-[#2C5F2D] bg-[#A8D5BA]/15 shadow-md'
                  : 'border-gray-200 bg-[#FAF9F6] hover:border-[#A8D5BA]/60',
              ]"
            >
              <div class="flex items-center gap-3 mb-2">
                <div
                  class="w-12 h-12 rounded-full bg-[#CDE7F0]/50 flex items-center justify-center text-[#1B4965] font-semibold text-lg"
                  aria-hidden="true"
                >
                  {{ initials(p.name) }}
                </div>
                <div>
                  <p class="font-semibold text-[#111827]">{{ p.name }}</p>
                  <p class="text-sm text-muted-foreground">{{ p.ageGroup || 'Age on file' }}</p>
                </div>
              </div>

              <p
                v-if="p.allergies?.length"
                class="text-xs text-amber-800 bg-amber-50 rounded-lg px-2 py-1 mt-2"
              >
                Allergies: {{ p.allergies.join(', ') }}
              </p>

              <p
                v-if="p.dietaryRestriction"
                class="text-xs text-[#1B4965] bg-[#CDE7F0]/40 rounded-lg px-2 py-1 mt-2"
              >
                {{ p.dietaryRestriction }}
              </p>

              <p
                v-if="p.isDemo"
                class="text-[10px] uppercase tracking-wide text-muted-foreground mt-2"
              >
                Demo profile
              </p>

              <p
                v-else
                class="text-[10px] uppercase tracking-wide text-[#2C5F2D] mt-2"
              >
                Saved profile
              </p>
            </button>
          </div>

          <p v-if="isShowingDemoProfiles" class="text-xs text-muted-foreground mt-3 max-w-2xl">
            Preview mode: these sample profiles show how the calculator works. Sign in to use your saved child profiles and receive personalised serving guidance.
          </p>

          <p
            v-if="servingTargetError"
            class="text-xs text-red-600 mt-3 max-w-2xl"
          >
            {{ servingTargetError }}
          </p>

          <template v-if="selectedChild && dailyServeRows.length">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mt-10 mb-4">
              <p class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide">
                Step 2 — Recommended daily serves
              </p>

              <div
                class="inline-flex items-center gap-2 rounded-full border border-[#D6E7DC] bg-[#F8F5EC] px-3 py-1 text-xs text-[#2C5F2D] w-fit"
              >
                <Info class="w-3.5 h-3.5" aria-hidden="true" />
                <span>{{ servingDataSourceLabel }}</span>
              </div>
            </div>

            <div class="grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <div
                v-for="row in dailyServeRows"
                :key="row.group"
                class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4 flex flex-col"
              >
                <div class="w-10 h-10 rounded-full bg-white border border-[#D6E7DC] flex items-center justify-center mb-3 text-[#2C5F2D]" aria-hidden="true">
                  <component :is="row.icon" class="w-5 h-5" />
                </div>

                <h3 class="font-semibold text-[#2C5F2D]">{{ row.group }}</h3>

                <p class="text-2xl font-bold text-[#111827] mt-1">
                  {{ formatServe(row.serves) }}
                  <span class="text-sm font-normal text-muted-foreground">serves</span>
                </p>

                <p class="text-sm font-semibold text-[#2C5F2D] mt-1">
                  ≈ {{ row.estimatedGrams }} g/day
                </p>

                <p class="text-xs text-muted-foreground mt-2 leading-snug flex-1">
                  {{ row.example }}
                </p>

                <p
                  v-if="row.personalisedNote"
                  class="mt-3 rounded-xl bg-white border border-[#D6E7DC] px-3 py-2 text-xs text-[#2C5F2D] leading-relaxed"
                >
                  {{ row.personalisedNote }}
                </p>
              </div>
            </div>

            <div class="mt-8 flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-[#2C5F2D] text-white px-5 py-4">
              <span class="text-sm font-medium flex items-center gap-2">
                Total daily target
                <span class="inline-flex" title="Educational serving target based on age band; not medical advice.">
                  <Info class="w-4 h-4 opacity-80" aria-label="Educational serving target based on age band; not medical advice." />
                </span>
              </span>
              <span class="text-lg font-semibold tabular-nums text-right">
                {{ totalDailyServes }} serves
                <span v-if="totalEstimatedGrams">
                  · ≈ {{ totalEstimatedGrams }} g/day
                </span>
              </span>
            </div>

            <div
              v-if="personalisedFocusNotes.length"
              class="mt-8 rounded-2xl border border-[#D6E7DC] bg-[#F8F5EC]/80 p-5"
            >
              <p class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide mb-3">
                Step 3 — Personalised notes for {{ selectedChild.name }}
              </p>

              <ul class="space-y-2 text-sm text-muted-foreground leading-relaxed">
                <li
                  v-for="note in personalisedFocusNotes"
                  :key="note.label + note.message"
                  class="flex gap-2"
                >
                  <span class="text-[#2C5F2D] mt-0.5" aria-hidden="true">•</span>
                  <span>
                    <strong class="text-[#2C5F2D]">{{ note.label }}:</strong>
                    {{ note.message }}
                  </span>
                </li>
              </ul>
            </div>

            <p class="text-xs text-muted-foreground mt-3">
              Serve targets are based on the selected child's age band. Gram values are estimated using standard grams per serve by food group, because actual grams can vary by food type and preparation method.
            </p>
          </template>

          <p v-else-if="step1Profiles.length && !selectedChild" class="mt-8 text-center text-muted-foreground text-sm">
            Tap a child card above to load serving targets.
          </p>
        </section>

        <!-- Food Group Guide -->
        <section
          :id="`panel-guide`"
          role="tabpanel"
          aria-labelledby="tab-guide"
          v-show="activeHubTab === 'guide'"
          class="flex flex-col md:flex-row gap-6 md:gap-8"
        >
          <aside class="w-full md:w-56 shrink-0 rounded-2xl border border-[#E8E4DC] bg-white shadow-sm overflow-hidden">
            <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wider px-4 pt-4 pb-2">
              Food groups
            </p>
            <nav aria-label="Food group navigation">
              <button
                v-for="g in foodGroupCatalog"
                :key="g.id"
                type="button"
                @click="selectedFoodGroupId = g.id"
                :aria-pressed="selectedFoodGroupId === g.id"
                :class="[
                  'w-full flex items-center justify-between px-4 py-3 text-left text-sm transition-colors border-l-4',
                  selectedFoodGroupId === g.id
                    ? 'bg-[#A8D5BA]/20 border-l-[#2C5F2D] text-[#2C5F2D] font-medium'
                    : 'border-l-transparent hover:bg-[#FAF9F6] text-gray-700',
                ]"
              >
                {{ g.label }}
                <ChevronRight class="w-4 h-4 text-muted-foreground shrink-0" aria-hidden="true" />
              </button>
            </nav>
          </aside>

          <div class="flex-1 min-w-0 rounded-3xl border border-[#E8E4DC] bg-white shadow-sm p-6 md:p-10">
            <template v-if="activeFoodGroup">
              <div class="flex items-center gap-1.5 mb-6">
                <span class="text-4xl md:text-5xl leading-none select-none shrink-0 -translate-y-0.5" aria-hidden="true">
                  {{ activeFoodGroup.emoji }}
                </span>
                <h2 class="text-2xl md:text-3xl text-[#2C5F2D]">
                  {{ activeFoodGroup.label }}
                </h2>
              </div>

              <h3 class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide mb-2">Why it matters</h3>
              <p class="text-muted-foreground leading-relaxed mb-8">{{ activeFoodGroup.why }}</p>

              <h3 class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide mb-3">Serving guide (per day)</h3>

              <div class="overflow-x-auto rounded-xl border border-[#E5E7EB]">
                <table class="w-full text-sm">
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
                      <td class="px-4 py-3 whitespace-nowrap">{{ r.age }}</td>
                      <td class="px-4 py-3">{{ r.servings }}</td>
                      <td class="px-4 py-3 text-muted-foreground">{{ r.examples }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <p class="text-xs text-muted-foreground mt-3">{{ activeFoodGroup.footnote }}</p>
            </template>
          </div>
        </section>

        <!-- Additive Awareness Guide -->
        <section
          :id="`panel-heatmap`"
          role="tabpanel"
          aria-labelledby="tab-heatmap"
          v-show="activeHubTab === 'heatmap'"
          class="bg-white rounded-3xl border border-[#E8E4DC] shadow-sm p-6 md:p-10"
        >
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6 mb-8">
            <div>
              <h2 class="text-2xl md:text-3xl text-[#2C5F2D] mb-1">
                {{ additiveGuide?.title || 'Additive Awareness Guide' }}
              </h2>
              <p class="text-muted-foreground max-w-3xl leading-relaxed">
                {{ additiveGuide?.description || 'Explore how often added sugar, preservatives, and artificial colours appear across packaged food categories in our database.' }}
              </p>
            </div>
            <div class="rounded-2xl bg-[#F8F5EC] border border-[#E8E4DC] px-4 py-3 text-sm text-[#2C5F2D] max-w-sm">
              <p class="font-semibold mb-1">Why this matters</p>
              <p class="text-muted-foreground leading-relaxed">
                This guide helps parents decide which packaged food categories may need closer label checking.
              </p>
            </div>
          </div>

          <div
            v-if="isLoadingAdditive"
            class="p-5 rounded-2xl border bg-[#FAF9F6] text-center text-muted-foreground"
            aria-live="polite"
            aria-busy="true"
          >
            Loading additive insights...
          </div>

          <div
            v-else-if="additiveError"
            role="alert"
            class="p-5 rounded-2xl border border-red-200 bg-red-50 text-red-700 text-sm"
          >
            {{ additiveError }}
          </div>

          <template v-else>
            <div v-if="additiveSummary" class="grid md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Highest added sugar</p>
                <p
                  class="text-lg font-semibold text-[#2C5F2D] mt-2"
                  :title="additiveSummary.highest_added_sugar?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_added_sugar?.category) }}
                </p>
                <p class="text-2xl font-bold text-[#111827] mt-1">{{ additiveSummary.highest_added_sugar?.percent ?? 0 }}%</p>
              </div>

              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Highest preservatives</p>
                <p
                  class="text-lg font-semibold text-[#2C5F2D] mt-2"
                  :title="additiveSummary.highest_preservatives?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_preservatives?.category) }}
                </p>
                <p class="text-2xl font-bold text-[#111827] mt-1">{{ additiveSummary.highest_preservatives?.percent ?? 0 }}%</p>
              </div>

              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Highest colours</p>
                <p
                  class="text-lg font-semibold text-[#2C5F2D] mt-2"
                  :title="additiveSummary.highest_artificial_colours?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_artificial_colours?.category) }}
                </p>
                <p class="text-2xl font-bold text-[#111827] mt-1">{{ additiveSummary.highest_artificial_colours?.percent ?? 0 }}%</p>
              </div>

              <div class="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                <p class="text-xs font-semibold text-amber-800 uppercase tracking-wide">Highest label-check priority</p>
                <p
                  class="text-lg font-semibold text-amber-950 mt-2"
                  :title="additiveSummary.highest_overall_priority?.category"
                >
                  {{ getFriendlyCategoryName(additiveSummary.highest_overall_priority?.category) }}
                </p>
                <p class="text-sm text-amber-900 mt-1">
                  {{ simplifyLabelPriority(additiveSummary.highest_overall_priority?.label_priority) }}
                </p>
              </div>
            </div>

            <div v-if="additiveGuide?.disclaimer" class="mb-8 rounded-2xl border border-[#D6E7DC] bg-[#F8F5EC]/70 p-4">
              <p class="text-sm text-muted-foreground leading-relaxed">{{ additiveGuide.disclaimer }}</p>
            </div>

            <!-- Desktop Table -->
            <div class="hidden md:block overflow-x-auto rounded-xl border border-[#E5E7EB]">
              <table class="w-full text-sm min-w-[760px] table-fixed">
                <thead>
                  <tr class="bg-[#FAF9F6]">
                    <th scope="col" class="px-3 py-3 text-left font-semibold text-[#374151] w-[22%]">Category</th>
                    <th scope="col" class="px-3 py-3 text-left font-semibold text-[#374151] w-[18%]">Label priority</th>
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
                    <td class="px-3 py-3 font-medium text-gray-800 align-middle">
                      <div :title="row.category">
                        <p class="text-[#111827] font-semibold">
                          {{ getFriendlyCategoryName(row.category) }}
                        </p>

                        <p
                          v-if="getShortCategoryDescription(row.category)"
                          class="text-xs text-muted-foreground mt-1 leading-snug"
                        >
                          {{ getShortCategoryDescription(row.category) }}
                        </p>

                        <p class="text-xs text-muted-foreground mt-1">
                          {{ row.total_products }} products
                        </p>
                      </div>
                    </td>

                    <td class="px-3 py-3 align-middle">
                      <div class="rounded-xl bg-[#FAF9F6] border border-[#E5E7EB] p-3">
                        <p class="font-semibold text-[#2C5F2D]">
                          {{ simplifyLabelPriority(row.label_priority) }}
                        </p>
                        <p class="text-xs text-muted-foreground mt-1">Score: {{ row.risk_score }}</p>
                      </div>
                    </td>

                    <td v-for="col in additiveColumns" :key="col.key" class="px-3 py-2 align-middle text-center">
                      <div
                        :class="[
                          'relative rounded-xl px-4 py-3 font-semibold tabular-nums border w-full min-h-[3.5rem] flex items-center justify-center',
                          heatCellClass(row[col.key]?.level),
                        ]"
                      >
                        <AlertTriangle
                          v-if="row[col.key]?.level === 'warning'"
                          class="pointer-events-none absolute top-1/2 left-[calc(50%-2.1rem)] z-0 w-4 h-4 -translate-y-1/2 text-amber-700"
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
            <div class="md:hidden space-y-4">
              <article v-for="row in additiveRows" :key="row.category" class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <h3 class="font-semibold text-[#2C5F2D]" :title="row.category">
                      {{ getFriendlyCategoryName(row.category) }}
                    </h3>

                    <p
                      v-if="getShortCategoryDescription(row.category)"
                      class="text-xs text-muted-foreground mt-0.5 leading-snug"
                    >
                      {{ getShortCategoryDescription(row.category) }}
                    </p>

                    <p class="text-xs text-muted-foreground mt-1">{{ row.total_products }} products</p>
                  </div>

                  <span class="text-xs rounded-full bg-white border border-[#D6E7DC] px-3 py-1 text-[#2C5F2D]">
                    {{ simplifyLabelPriority(row.label_priority) }}
                  </span>
                </div>

                <div class="space-y-2">
                  <div
                    v-for="col in additiveColumns"
                    :key="col.key"
                    class="flex items-center justify-between rounded-xl bg-white border border-[#E5E7EB] px-3 py-2"
                  >
                    <span class="text-sm text-gray-700">{{ col.label }}</span>
                    <span :class="['text-sm font-semibold rounded-lg px-2 py-1 border', heatCellClass(row[col.key]?.level)]">
                      {{ row[col.key]?.percent ?? 0 }}%
                    </span>
                  </div>
                </div>

                <p class="text-xs text-muted-foreground mt-3 leading-relaxed">
                  {{ getSimpleAdditiveTip(row) }}
                </p>
              </article>
            </div>

            <div v-if="!additiveRows.length" class="mt-6 p-5 rounded-2xl border bg-[#FAF9F6] text-center text-muted-foreground">
              No additive records are available yet.
            </div>

            <div class="grid lg:grid-cols-2 gap-6 mt-8">
              <div class="rounded-2xl border border-[#E5E7EB] bg-white p-5">
                <p class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide mb-3">How to read this</p>
                <div class="space-y-3">
                  <div v-for="item in additiveHowToRead" :key="item.level" class="flex items-start gap-3">
                    <span :class="['w-10 h-5 rounded border shrink-0 mt-0.5', heatCellClass(item.level)]" aria-hidden="true"></span>
                    <div>
                      <p class="text-sm font-semibold text-gray-800">{{ item.label }}</p>
                      <p class="text-xs text-muted-foreground leading-relaxed">{{ item.meaning }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="rounded-2xl border border-[#E5E7EB] bg-white p-5">
                <p class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide mb-3">Parent tips</p>
                <ul class="space-y-2 text-sm text-muted-foreground leading-relaxed">
                  <li v-for="tip in additiveTips" :key="tip" class="flex gap-2">
                    <span class="text-[#2C5F2D] mt-0.5" aria-hidden="true">•</span>
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
      return 'Milk or dairy restriction detected. Choose safe calcium-fortified alternatives instead of regular dairy.';
    }

    if (hasNutritionFocus('calcium') || hasNutritionFocus('vitamin_d')) {
      return 'This profile has calcium or vitamin D support selected. Prioritise dairy or fortified alternatives when suitable.';
    }
  }

  if (groupKey === 'protein') {
    if (hasAllergy('peanut') || hasAllergy('tree nuts') || hasRestriction('excludes_nuts')) {
      return 'Nut allergy or nut restriction detected. Avoid nut-based snacks and choose safe protein options such as egg, tuna, chicken, beans, lentils, or tofu.';
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
    personalisedNote: row.personalised_note || buildGroupPersonalisedNote(key),
  };
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
  };
};

const dailyServeRows = computed(() => {
  const backendRows = selectedServingTarget.value?.recommended_serves;

  if (Array.isArray(backendRows) && backendRows.length > 0) {
    return backendRows.map(mapBackendServeRow);
  }

  return (servePresets[ageBandKey.value] || servePresets.mid).map(mapPresetServeRow);
});

const totalDailyServes = computed(() => {
  if (selectedServingTarget.value?.total_daily_serves != null) {
    return Number(selectedServingTarget.value.total_daily_serves).toFixed(1);
  }

  if (selectedServingTarget.value?.total_daily_target != null) {
    return Number(selectedServingTarget.value.total_daily_target).toFixed(1);
  }

  const total = dailyServeRows.value.reduce(
    (sum, r) => sum + Number(r.serves || 0),
    0,
  );

  return total.toFixed(1);
});

const totalEstimatedGrams = computed(() => {
  if (selectedServingTarget.value?.total_estimated_grams != null) {
    return Number(selectedServingTarget.value.total_estimated_grams);
  }

  const total = dailyServeRows.value.reduce(
    (sum, r) => sum + Number(r.estimatedGrams || 0),
    0,
  );

  return total || null;
});

const servingDataSourceLabel = computed(() => {
  if (selectedServingTarget.value?.recommended_serves?.length) {
    return 'Loaded from database age-band guideline table';
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