<template>
  <div class="min-h-screen bg-[#FAF9F6]">
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between h-16">
          <button @click="router.push('/')" class="flex items-center cursor-pointer" type="button" aria-label="Go to home">
            <img
              :src="logoUrl"
              alt="LittleHelp logo"
              class="h-10 w-auto object-contain"
            />
          </button>

          <div class="flex items-center gap-2">
            <button
              @click="router.push('/')"
              type="button"
              class="inline-flex items-center px-4 py-2 text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg transition-colors"
            >
              <ArrowLeft class="w-4 h-4 mr-2" aria-hidden="true" />
              Back to Home
            </button>

            <div ref="accessibilityMenuRef" class="relative">
              <button
                @click="toggleAccessibilityMenu"
                class="inline-flex items-center gap-1 px-4 py-2 text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg transition-colors"
                type="button"
                :aria-expanded="showAccessibilityMenu"
                aria-haspopup="true"
                aria-controls="kb-accessibility-menu"
              >
                Accessibility
                <ChevronDown
                  :class="[
                    'w-3.5 h-3.5 transition-transform duration-200 translate-y-[1px]',
                    showAccessibilityMenu ? 'rotate-180' : 'rotate-0',
                  ]"
                  aria-hidden="true"
                />
              </button>

              <div
                v-if="showAccessibilityMenu"
                id="kb-accessibility-menu"
                role="menu"
                class="absolute right-0 mt-2 w-72 rounded-2xl border border-[#D6E7DC] bg-white shadow-xl p-4 z-50"
              >
                <p class="text-sm font-semibold text-[#2C5F2D]">Accessibility</p>
                <div class="h-px bg-[#E5E7EB] my-3" aria-hidden="true"></div>

                <button
                  type="button"
                  role="menuitem"
                  @click="toggleLargeTextMode"
                  :aria-pressed="largeTextMode"
                  :class="[
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors',
                    largeTextMode
                      ? 'bg-[#F8F5EC] text-[#2C5F2D] font-semibold'
                      : 'bg-transparent text-[#2C5F2D] hover:bg-[#F8F5EC]',
                  ]"
                >
                  Large Text Mode
                  <span v-if="largeTextMode" class="ml-2 text-xs">(on)</span>
                </button>

                <button
                  type="button"
                  role="menuitem"
                  @click="toggleHighContrastMode"
                  :aria-pressed="highContrastMode"
                  :class="[
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors mt-2',
                    highContrastMode
                      ? 'bg-[#F8F5EC] text-[#2C5F2D] font-semibold'
                      : 'bg-transparent text-[#2C5F2D] hover:bg-[#F8F5EC]',
                  ]"
                >
                  High Contrast Mode
                  <span v-if="highContrastMode" class="ml-2 text-xs">(on)</span>
                </button>

                <div class="h-px bg-[#E5E7EB] my-3" aria-hidden="true"></div>
                <p class="text-xs text-muted-foreground leading-relaxed">
                  Accessibility settings can be changed anytime.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="pt-28 pb-8">
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
          <h2 class="text-2xl md:text-3xl text-[#2C5F2D] mb-1">
            Serving Size Calculator
          </h2>
          <p class="text-muted-foreground mb-8 max-w-2xl">
            Choose one of your child profiles, then review guideline daily serves matched to their age band.
          </p>

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
                @click="router.push({ path: '/login', query: { redirect: '/knowledge-hub-prototype' } })"
                class="bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg px-6 py-2 transition-colors"
              >
                Sign in
              </button>
              <button
                type="button"
                @click="router.push('/register')"
                class="bg-white border border-[#A8D5BA] text-[#2C5F2D] rounded-lg px-6 py-2 hover:bg-[#A8D5BA]/10 transition-colors"
              >
                Create account
              </button>
            </div>
          </div>

          <div
            v-else-if="isLoggedIn && isLoadingProfiles"
            class="p-4 rounded-xl border bg-[#FAF9F6] text-center text-muted-foreground text-sm"
            aria-live="polite"
            aria-busy="true"
          >
            Loading your child profiles…
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
                v-if="p.isDemo"
                class="text-[10px] uppercase tracking-wide text-muted-foreground mt-2"
              >
                Demo profile
              </p>
            </button>
          </div>

          <p v-if="isShowingDemoProfiles" class="text-xs text-muted-foreground mt-3 max-w-2xl">
            Showing sample child cards for preview. Sign in and add profiles under Child Information to use your own children here.
          </p>

          <template v-if="selectedChild && dailyServeRows.length">
            <p class="text-sm font-semibold text-[#2C5F2D] uppercase tracking-wide mt-10 mb-4">
              Step 2 — Recommended daily serves
            </p>

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
                  {{ row.serves }}
                  <span class="text-sm font-normal text-muted-foreground">serves</span>
                </p>
                <p class="text-xs text-muted-foreground mt-2 leading-snug flex-1">
                  {{ row.example }}
                </p>
              </div>
            </div>

            <div class="mt-8 flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-[#2C5F2D] text-white px-5 py-4">
              <span class="text-sm font-medium flex items-center gap-2">
                Total daily target (illustrative)
                <span class="inline-flex" title="Educational estimate based on age band; not medical advice.">
                  <Info class="w-4 h-4 opacity-80" aria-label="Educational estimate based on age band; not medical advice." />
                </span>
              </span>
              <span class="text-lg font-semibold tabular-nums">
                {{ totalDailyGrams }} g across all food groups
              </span>
            </div>

            <p class="text-xs text-muted-foreground mt-3">
              Figures follow general Australian-style children's guidelines for the selected age band. Adjust with your clinician for medical diets.
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
                <p class="text-lg font-semibold text-[#2C5F2D] mt-2">{{ additiveSummary.highest_added_sugar?.category || 'N/A' }}</p>
                <p class="text-2xl font-bold text-[#111827] mt-1">{{ additiveSummary.highest_added_sugar?.percent ?? 0 }}%</p>
              </div>
              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Highest preservatives</p>
                <p class="text-lg font-semibold text-[#2C5F2D] mt-2">{{ additiveSummary.highest_preservatives?.category || 'N/A' }}</p>
                <p class="text-2xl font-bold text-[#111827] mt-1">{{ additiveSummary.highest_preservatives?.percent ?? 0 }}%</p>
              </div>
              <div class="rounded-2xl border border-[#E5E7EB] bg-[#FAF9F6] p-4">
                <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Highest colours</p>
                <p class="text-lg font-semibold text-[#2C5F2D] mt-2">{{ additiveSummary.highest_artificial_colours?.category || 'N/A' }}</p>
                <p class="text-2xl font-bold text-[#111827] mt-1">{{ additiveSummary.highest_artificial_colours?.percent ?? 0 }}%</p>
              </div>
              <div class="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                <p class="text-xs font-semibold text-amber-800 uppercase tracking-wide">Highest label-check priority</p>
                <p class="text-lg font-semibold text-amber-950 mt-2">{{ additiveSummary.highest_overall_priority?.category || 'N/A' }}</p>
                <p class="text-sm text-amber-900 mt-1">{{ additiveSummary.highest_overall_priority?.label_priority || 'No signal' }}</p>
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
                    <th scope="col" class="px-3 py-3 text-left font-semibold text-[#374151] w-[22%]">Label priority</th>
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
                      {{ row.category }}
                      <p class="text-xs text-muted-foreground mt-1">{{ row.total_products }} products</p>
                    </td>
                    <td class="px-3 py-3 align-middle">
                      <div class="rounded-xl bg-[#FAF9F6] border border-[#E5E7EB] p-3">
                        <p class="font-semibold text-[#2C5F2D]">{{ row.label_priority }}</p>
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
                    <h3 class="font-semibold text-[#2C5F2D]">{{ row.category }}</h3>
                    <p class="text-xs text-muted-foreground">{{ row.total_products }} products</p>
                  </div>
                  <span class="text-xs rounded-full bg-white border border-[#D6E7DC] px-3 py-1 text-[#2C5F2D]">{{ row.label_priority }}</span>
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
                <p class="text-xs text-muted-foreground mt-3 leading-relaxed">{{ row.parent_tip }}</p>
              </article>
            </div>

            <div v-if="!additiveRows.length" class="mt-6 p-5 rounded-2xl border bg-[#FAF9F6] text-center text-muted-foreground">
              No additive records are available yet.
            </div>

            <!-- How to read + tips -->
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
import { useRouter } from 'vue-router';
import {
  ArrowLeft,
  ChevronDown,
  Carrot,
  Apple,
  Wheat,
  Drumstick,
  Milk,
  Info,
  ChevronRight,
  AlertTriangle,
} from 'lucide-vue-next';
import logoUrl from '../assets/littlehelp-logo.jpg';
import { getChildren, getKnowledgeAdditiveAwareness } from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useAccessibility } from '../composables/useAccessibility';

const router = useRouter();
const authStore = useAuthStore();

const isLoggedIn = computed(() => authStore.isAuthenticated);

// ── Accessibility (global) ──────────────────────────────────────────────────
const {
  largeTextMode,
  highContrastMode,
  showAccessibilityMenu,
  accessibilityMenuRef,
  toggleLargeTextMode,
  toggleHighContrastMode,
  toggleAccessibilityMenu,
} = useAccessibility();

// ── Tabs ────────────────────────────────────────────────────────────────────
const activeHubTab = ref('serving');

const hubTabs = [
  { id: 'serving', label: 'Serving Size Calculator', hint: 'Pick a child profile, then see guideline serves for vegetables, fruit, grains, protein and dairy—matched to their age band.' },
  { id: 'guide', label: 'Food Group Guide', hint: 'Choose a food group to read why it matters and scan age-based serving suggestions with everyday examples.' },
  { id: 'heatmap', label: 'Additive Awareness Guide', hint: 'Compare how often added sugar, preservatives and artificial colours appear across packaged food categories in our database.' },
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

const USE_STEP1_LOGIN_GATE = false;

const MOCK_STEP1_CHILDREN = [
  { id: 'demo-emma', name: 'Emma', ageGroup: '7-9 years', allergies: [], isDemo: true },
  { id: 'demo-oliver', name: 'Oliver', ageGroup: '5-6 years', allergies: ['Peanuts'], isDemo: true },
  { id: 'demo-maya', name: 'Maya', ageGroup: '10-12 years', allergies: [], isDemo: true },
];

const step1Profiles = computed(() => {
  if (USE_STEP1_LOGIN_GATE && !isLoggedIn.value) return [];
  if (isLoggedIn.value && profiles.value.length > 0) return profiles.value.map((p) => ({ ...p, isDemo: false }));
  return MOCK_STEP1_CHILDREN;
});

const isShowingDemoProfiles = computed(() => {
  if (USE_STEP1_LOGIN_GATE && !isLoggedIn.value) return false;
  return !(isLoggedIn.value && profiles.value.length > 0);
});

const allowedAgeGroups = ['5-6 years', '7-9 years', '10-12 years'];

const normalizeAgeGroup = (ageGroup) => {
  const mapping = { '5-6 years': '5-6 years', '7-9 years': '7-9 years', '10-12 years': '10-12 years', '3-6 years': '5-6 years', '6-9 years': '7-9 years', '9-12 years': '10-12 years', '12+ years': '10-12 years', '4-8': '7-9 years', '9-13': '10-12 years', '0-3 years': '', '2-3': '', '14-18': '' };
  return mapping[ageGroup] || '';
};

const mapAllergiesToNames = (allergies) => {
  if (!Array.isArray(allergies)) return [];
  return allergies.map((a) => typeof a === 'string' && Number.isNaN(Number(a)) ? a : `Allergen #${a}`);
};

const mapChildToProfile = (child) => {
  const normalizedAgeGroup = normalizeAgeGroup(child.age_band);
  return { id: child.child_id, name: child.child_name, ageGroup: normalizedAgeGroup || child.age_band || '', allergies: mapAllergiesToNames(child.allergies), isSupportedAge: allowedAgeGroups.includes(normalizedAgeGroup) };
};

const loadProfiles = async () => {
  if (!isLoggedIn.value) { profiles.value = []; return; }
  try {
    isLoadingProfiles.value = true;
    const children = await getChildren();
    const list = Array.isArray(children) ? children.map(mapChildToProfile) : [];
    profiles.value = list.filter((p) => p.isSupportedAge);
    if (profiles.value.length && !profiles.value.some((p) => p.id === selectedChildId.value)) {
      selectedChildId.value = profiles.value[0].id;
    }
  } catch (e) {
    console.error(e);
    profiles.value = [];
  } finally {
    isLoadingProfiles.value = false;
  }
};

const selectedChild = computed(() => step1Profiles.value.find((p) => p.id === selectedChildId.value) || null);
const ageBandKey = computed(() => { const g = selectedChild.value?.ageGroup || ''; if (g === '5-6 years') return 'young'; if (g === '7-9 years') return 'mid'; return 'older'; });

const servePresets = {
  young: [
    { group: 'Vegetables', serves: 4.5, example: 'e.g. ½ cup cooked vegetables', grams: 340, icon: Carrot },
    { group: 'Fruit', serves: 2, example: 'e.g. 1 medium apple or 2 small mandarins', grams: 300, icon: Apple },
    { group: 'Grains', serves: 5, example: 'e.g. 1 slice wholegrain bread per serve', grams: 600, icon: Wheat },
    { group: 'Protein', serves: 2, example: 'e.g. 65 g cooked lean meat per serve', grams: 260, icon: Drumstick },
    { group: 'Dairy', serves: 2, example: 'e.g. 1 cup milk or 2 slices cheese', grams: 500, icon: Milk },
  ],
  mid: [
    { group: 'Vegetables', serves: 5, example: 'e.g. ½ cup cooked veg or 1 cup salad', grams: 375, icon: Carrot },
    { group: 'Fruit', serves: 2, example: 'e.g. 1 medium piece or 1 cup diced fruit', grams: 320, icon: Apple },
    { group: 'Grains', serves: 6, example: 'e.g. ½ cup cooked rice = 1 serve', grams: 720, icon: Wheat },
    { group: 'Protein', serves: 2.5, example: 'e.g. 80 g fish or 2 eggs', grams: 325, icon: Drumstick },
    { group: 'Dairy', serves: 2.5, example: 'e.g. 200 g yoghurt + milk in cereal', grams: 625, icon: Milk },
  ],
  older: [
    { group: 'Vegetables', serves: 5.5, example: 'e.g. include leafy greens most days', grams: 400, icon: Carrot },
    { group: 'Fruit', serves: 2, example: 'e.g. whole fruit preferred over juice', grams: 320, icon: Apple },
    { group: 'Grains', serves: 6, example: 'e.g. mostly wholegrain varieties', grams: 720, icon: Wheat },
    { group: 'Protein', serves: 2.5, example: 'e.g. mix legumes, fish, lean meats', grams: 340, icon: Drumstick },
    { group: 'Dairy', serves: 3, example: 'e.g. fortified plant milks count if chosen', grams: 650, icon: Milk },
  ],
};

const dailyServeRows = computed(() => servePresets[ageBandKey.value] || servePresets.mid);
const totalDailyGrams = computed(() => dailyServeRows.value.reduce((sum, r) => sum + (r.grams || 0), 0));

const foodGroupCatalog = [
  { id: 'vegetables', label: 'Vegetables', emoji: '🥦', why: 'Vegetables provide vitamins, minerals, fibre and antioxidants that help your child grow strong and stay healthy.', table: [{ age: '4 – 8', servings: '2 – 2½ cups', examples: 'Carrots, spinach, broccoli, beans' }, { age: '9 – 13', servings: '2½ – 3 cups', examples: 'Mixed vegetables, sweet potato, peas' }], footnote: '* 1 cup = 1 cup raw leafy vegetables or ½ cup cooked vegetables.' },
  { id: 'fruits', label: 'Fruits', emoji: '🍎', why: 'Fruit adds vitamin C, potassium and fibre, and naturally sweet flavours that can replace discretionary snacks.', table: [{ age: '4 – 8', servings: '1 – 1½', examples: 'Apple, banana, berries, melon wedges' }, { age: '9 – 13', servings: '1½ – 2', examples: 'Stone fruit, citrus, frozen fruit in yoghurt' }], footnote: '* One serve ≈ 1 medium fruit or 1 cup diced fruit.' },
  { id: 'grains', label: 'Grains', emoji: '🌾', why: 'Whole grains supply steady energy and B vitamins to fuel school days and active play.', table: [{ age: '4 – 8', servings: '4 – 5', examples: 'Wholegrain bread, oats, brown rice, pasta' }, { age: '9 – 13', servings: '5 – 6', examples: 'Quinoa wraps, high-fibre cereals, barley soups' }], footnote: '* One serve ≈ 1 slice bread or ½ cup cooked grains.' },
  { id: 'protein', label: 'Protein foods', emoji: '🍗', why: 'Protein supports muscle repair, immune function and growth spurts in school-aged children.', table: [{ age: '4 – 8', servings: '1½ – 2', examples: 'Lean meat, tofu, eggs, lentils' }, { age: '9 – 13', servings: '2 – 2½', examples: 'Fish twice weekly, chickpeas, nut-free dips' }], footnote: '* One serve ≈ 65–80 g cooked meat or plant equivalent.' },
  { id: 'dairy', label: 'Dairy', emoji: '🥛', why: 'Dairy and fortified alternatives supply calcium for bones and teeth during rapid growth.', table: [{ age: '4 – 8', servings: '1½ – 2', examples: 'Milk on cereal, cheese sticks, yoghurt tubs' }, { age: '9 – 13', servings: '2 – 3', examples: 'Smoothies, fortified soy drink, cottage cheese' }], footnote: '* One serve ≈ 1 cup milk or 2 slices cheese; choose unsweetened options where possible.' },
];

const activeFoodGroup = computed(() => foodGroupCatalog.find((g) => g.id === selectedFoodGroupId.value) || foodGroupCatalog[0]);
const selectedFoodGroupId = ref('vegetables');

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

// ── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(() => {
  loadProfiles();
  loadAdditiveAwareness();
});

watch(step1Profiles, (list) => {
  if (!list.length) { selectedChildId.value = null; return; }
  if (!selectedChildId.value || !list.some((p) => p.id === selectedChildId.value)) {
    selectedChildId.value = list[0].id;
  }
}, { immediate: true });

watch(() => authStore.token, () => loadProfiles());
watch(isLoggedIn, (v) => { if (v) loadProfiles(); else profiles.value = []; });
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}

@media (max-width: 640px) {
  nav .container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>