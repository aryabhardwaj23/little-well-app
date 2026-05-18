<template>
  <div class="flex flex-1 flex-col bg-[#F4F1EA]">
    <!-- Header: no internal nav, use global NavigationBar -->
    <section class="bg-white">
      <div class="container mx-auto max-w-6xl px-4 pb-5 pt-7 sm:px-6 sm:pb-6 sm:pt-10">
        <div>
          <h1 class="text-3xl font-semibold leading-tight text-[#2C5F2D] sm:text-4xl md:text-5xl">
            Lunchbox Food Analyser
          </h1>
          <p class="mt-2 text-sm leading-relaxed text-gray-500 sm:text-base">
            Upload a photo of your child's lunchbox for AI-powered nutrition insights.
          </p>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="relative flex-1 pb-0">
      <div class="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true">
        <div class="absolute inset-0 bg-gradient-to-b from-[#FAF9F6] to-[#F4F1EA]"></div>
        <div
          class="absolute inset-0 bg-cover bg-center opacity-40 sm:opacity-50"
          style="background-image: url('https://images.pexels.com/photos/5949887/pexels-photo-5949887.jpeg?auto=compress&cs=tinysrgb&w=1600');"
        ></div>
        <div
          class="absolute inset-0 bg-gradient-to-br from-[#A8D5BA]/15 to-[#F4F1EA]/80"
        ></div>
        <div
          class="absolute left-0 right-0 top-0 z-[1] h-10 bg-gradient-to-b from-white from-0% via-white/90 via-[58%] to-transparent to-100% sm:h-14"
        ></div>
        <div
          class="absolute bottom-0 left-0 right-0 z-[1] h-16 bg-gradient-to-t from-[#F4F1EA] from-0% via-[#F4F1EA]/95 via-45% to-transparent to-100% sm:h-24"
        ></div>
      </div>

      <main class="container relative z-10 mx-auto max-w-6xl px-4 pb-16 pt-6 sm:px-6 sm:pb-24 sm:pt-10">
      <div class="flex flex-col gap-6 lg:gap-8">
        <div class="grid grid-cols-1 items-start gap-6 lg:grid-cols-12 lg:gap-8">
          <!-- Step 1 -->
          <section class="relative z-20 overflow-visible rounded-2xl border bg-white p-5 shadow-sm lg:z-30 lg:col-span-4">
            <p class="mb-3 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
              Step 1 — Select your child
            </p>

            <div
              class="child-picker-bubble rounded-2xl border border-gray-200 bg-white p-2 shadow-sm transition-[max-height] duration-300 ease-in-out"
              :class="
                childPickerOpen
                  ? 'max-h-[min(36rem,72vh)] overflow-y-auto'
                  : 'max-h-[14.5rem] overflow-hidden'
              "
              @mouseenter="openChildPicker"
              @mouseleave="closeChildPicker"
            >
              <div
                class="flex flex-col gap-2"
                role="listbox"
                aria-label="Child profiles"
              >
                  <button
                    v-for="profile in orderedProfiles"
                    :key="profile.id"
                    type="button"
                    role="option"
                    :aria-selected="selectedChildId === profile.id"
                    class="w-full shrink-0 rounded-2xl border-2 p-4 text-left transition-colors"
                    :class="
                      selectedChildId === profile.id
                        ? 'border-[#2C5F2D] bg-[#A8D5BA]/15 shadow-md'
                        : 'border-gray-200 bg-[#FAF9F6] hover:border-[#A8D5BA]/60'
                    "
                    @click="selectChildProfile(profile)"
                  >
                    <div class="mb-2 flex items-center gap-3">
                      <div
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#CDE7F0]/50 text-base font-semibold text-[#1B4965] sm:h-12 sm:w-12 sm:text-lg"
                        aria-hidden="true"
                      >
                        {{ profileInitials(profile.name) }}
                      </div>
                      <div class="min-w-0">
                        <p class="truncate font-semibold text-[#111827]">{{ profile.name }}</p>
                        <p class="text-sm text-muted-foreground">{{ profile.ageGroup }}</p>
                      </div>
                    </div>

                    <p
                      v-if="profile.allergies?.length"
                      class="mt-2 rounded-lg bg-amber-50 px-2 py-1 text-xs text-amber-800"
                    >
                      Allergies: {{ profile.allergies.join(', ') }}
                    </p>

                    <p
                      v-if="profile.dietaryRestriction"
                      class="mt-2 rounded-lg bg-[#CDE7F0]/40 px-2 py-1 text-xs text-[#1B4965]"
                    >
                      {{ profile.dietaryRestriction }}
                    </p>

                    <p class="mt-2 text-[10px] uppercase tracking-wide text-muted-foreground">
                      Demo profile
                    </p>
                  </button>
              </div>
            </div>

            <p class="mt-3 text-xs leading-relaxed text-muted-foreground">
              Mock profiles for UI preview. Child cards will be loaded from the backend later.
            </p>
          </section>

          <!-- Steps 2 & 3 — Upload, tips, and AI feedback (single white bubble) -->
          <section class="flex min-w-0 flex-col rounded-2xl border bg-white p-5 shadow-sm lg:col-span-8">
            <p class="mb-4 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
              Step 2 — Upload lunchbox photo
            </p>

            <div class="grid flex-1 grid-cols-1 gap-5 md:grid-cols-2 md:gap-6 lg:gap-8">
              <div class="flex min-w-0 flex-col">

            <div
              @click="triggerPhotoUpload"
              @dragover.prevent
              @drop.prevent="onPhotoDrop"
              :class="[
                'flex flex-1 flex-col justify-center border-2 border-dashed rounded-xl p-5 sm:p-6 text-center cursor-pointer transition-colors min-h-[10rem]',
                photoPreview
                  ? 'border-[#A8D5BA]'
                  : 'border-gray-200 hover:border-[#A8D5BA]'
              ]"
            >
              <input
                ref="photoInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onPhotoSelected"
              />

              <div v-if="!photoPreview" class="space-y-2">
                <div
                  class="w-12 h-12 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center mx-auto"
                >
                  <Upload class="w-6 h-6 text-[#2C5F2D]" />
                </div>

                <p class="text-sm text-[#2C5F2D] font-medium">
                  Upload or drag a photo
                </p>
                <p class="text-xs text-gray-500">
                  JPG, PNG up to 5MB
                </p>
              </div>

              <div v-else class="relative">
                <img
                  :src="photoPreview"
                  class="w-full rounded-lg object-cover max-h-56 sm:max-h-48"
                  alt="Lunchbox preview"
                />

                <button
                  @click.stop="clearPhoto"
                  class="absolute top-2 right-2 bg-white rounded-full p-2 shadow hover:bg-gray-50"
                  type="button"
                  aria-label="Remove uploaded photo"
                >
                  <X class="w-4 h-4 text-gray-500" />
                </button>
              </div>
            </div>

            <button
              v-if="photoPreview"
              @click="analysePhoto"
              :disabled="loading"
              class="w-full mt-4 bg-[#A8D5BA] hover:bg-[#8FC2A4] disabled:opacity-50 disabled:cursor-not-allowed text-[#2C5F2D] font-medium rounded-xl py-3.5 sm:py-3 flex items-center justify-center gap-2 transition-colors"
              type="button"
            >
              <span v-if="!loading">
                ✨ Analyse Nutrition
              </span>

              <span v-else class="flex items-center gap-2">
                <span
                  class="w-4 h-4 border-2 border-[#2C5F2D] border-t-transparent rounded-full animate-spin"
                ></span>
                Analysing...
              </span>
            </button>
              </div>

              <div
                class="flex flex-col border-t border-gray-200 pt-5 md:border-l md:border-t-0 md:pl-6 md:pt-0"
              >
                <h3 class="mb-3 text-sm font-semibold text-[#1B4965]">
                  Tips for best results
                </h3>

                <ul class="space-y-2 text-xs leading-relaxed text-[#1B4965] sm:text-sm">
                  <li>• Good lighting helps identify more foods</li>
                  <li>• Spread food out so all items are visible</li>
                  <li>• Photograph from directly above the lunchbox</li>
                  <li>• Select the correct child profile for accurate scoring</li>
                </ul>
              </div>
            </div>

            <!-- Step 3 — AI feedback -->
            <div class="mt-6 border-t border-gray-200 pt-6">
              <p class="mb-4 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] sm:text-sm">
                Step 3 — Get AI powered nutrition feedback
              </p>

              <!-- Empty State -->
              <div
                v-if="!result && !loading"
                class="flex min-h-[220px] flex-col items-center justify-center gap-4 rounded-xl bg-[#FAF9F6] p-8 text-center sm:min-h-[260px] sm:p-10"
              >
            <div
              class="w-18 h-18 sm:w-20 sm:h-20 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center"
            >
              <Leaf class="w-9 h-9 sm:w-10 sm:h-10 text-[#A8D5BA]" />
            </div>

            <h2 class="text-lg font-medium text-[#2C5F2D]">
              Ready to analyse
            </h2>

            <p class="text-gray-500 text-sm max-w-xs leading-relaxed">
              Upload a lunchbox photo to get AI-powered nutrition feedback tailored
              to your child's age.
            </p>
              </div>

              <!-- Loading State -->
              <div
                v-if="loading"
                class="flex min-h-[220px] flex-col items-center justify-center gap-4 rounded-xl bg-[#FAF9F6] p-8 text-center sm:min-h-[260px] sm:p-10"
              >
            <div
              class="w-16 h-16 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center"
            >
              <span class="text-3xl">🤖</span>
            </div>

            <h2 class="text-lg font-medium text-[#2C5F2D]">
              AI is analysing your lunchbox...
            </h2>

            <p class="text-sm text-gray-500 leading-relaxed">
              Detecting foods, scoring nutrition, and running the ML classifier.
            </p>

            <div class="flex gap-1 mt-2">
              <span
                class="w-2 h-2 bg-[#A8D5BA] rounded-full animate-bounce"
                style="animation-delay: 0ms"
              ></span>
              <span
                class="w-2 h-2 bg-[#A8D5BA] rounded-full animate-bounce"
                style="animation-delay: 150ms"
              ></span>
              <span
                class="w-2 h-2 bg-[#A8D5BA] rounded-full animate-bounce"
                style="animation-delay: 300ms"
              ></span>
            </div>
              </div>

              <!-- Result -->
              <div v-if="result && !loading" class="space-y-5">
            <!-- Nutrition Score -->
            <section class="rounded-xl border border-gray-100 bg-[#FAF9F6] p-5 sm:p-6">
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-4 gap-4">
                <div>
                  <h2 class="text-xl font-semibold text-[#2C5F2D]">
                    Nutrition Score
                  </h2>
                  <p class="text-sm text-gray-500 mt-1">
                    for {{ childName || 'your child' }}, age {{ childAge }}
                  </p>
                </div>

                <div class="text-left sm:text-right shrink-0">
                  <div :class="['text-4xl font-bold', scoreColor]">
                    {{ result.nutrition_score?.overall_score ?? 0 }}
                    <span class="text-lg text-gray-400 font-normal">/100</span>
                  </div>

                  <span
                    :class="['inline-block mt-1 text-sm font-medium px-3 py-1 rounded-full', gradeBadge]"
                  >
                    {{ result.nutrition_score?.grade || 'N/A' }}
                  </span>
                </div>
              </div>

              <div class="w-full bg-gray-100 rounded-full h-3 mb-5">
                <div
                  :class="['h-3 rounded-full transition-all duration-700', scoreBarColor]"
                  :style="{ width: `${result.nutrition_score?.overall_score || 0}%` }"
                ></div>
              </div>

              <!-- ML Classification -->
              <div
                v-if="
                  result.nutrition_score?.ml_classification &&
                  result.nutrition_score.ml_classification.class !== 'unknown'
                "
                class="flex flex-col sm:flex-row sm:items-center gap-3 mb-5 p-3 rounded-xl border"
                :class="{
                  'bg-green-50 border-green-200':
                    result.nutrition_score.ml_classification.color === 'green',
                  'bg-amber-50 border-amber-200':
                    result.nutrition_score.ml_classification.color === 'amber',
                  'bg-red-50 border-red-200':
                    result.nutrition_score.ml_classification.color === 'red',
                }"
              >
                <span class="text-2xl shrink-0">
                  {{ result.nutrition_score.ml_classification.emoji }}
                </span>

                <div class="flex-1">
                  <p
                    class="text-sm font-semibold flex items-center gap-2 flex-wrap"
                    :class="{
                      'text-green-700':
                        result.nutrition_score.ml_classification.color === 'green',
                      'text-amber-700':
                        result.nutrition_score.ml_classification.color === 'amber',
                      'text-red-700':
                        result.nutrition_score.ml_classification.color === 'red',
                    }"
                  >
                    ML Classification:
                    {{ result.nutrition_score.ml_classification.display_label }}

                    <span
                      class="font-normal text-xs bg-white/70 px-2 py-0.5 rounded-full"
                    >
                      {{ result.nutrition_score.ml_classification.confidence }}%
                      confidence
                    </span>
                  </p>

                  <p class="text-xs text-gray-500 mt-1 leading-relaxed">
                    {{ result.nutrition_score.ml_classification.message }}
                  </p>
                </div>
              </div>

              <!-- Detected Foods -->
              <p class="text-xs text-gray-500 mb-2">
                Detected foods
              </p>

              <div class="flex flex-wrap gap-2 mb-4">
                <span
                  v-for="food in result.detected_foods || []"
                  :key="food"
                  class="bg-[#A8D5BA]/20 text-[#2C5F2D] text-xs rounded-full px-3 py-1 capitalize"
                >
                  {{ food }}
                </span>
              </div>

              <div
                v-if="result.nutrition_score?.note"
                class="bg-[#CDE7F0]/30 rounded-xl p-3 text-xs text-[#1B4965] leading-relaxed"
              >
                ℹ️ {{ result.nutrition_score.note }}
              </div>
            </section>

            <!-- AI Feedback -->
            <section class="rounded-xl border border-gray-100 bg-[#FAF9F6] p-5 sm:p-6">
              <div class="flex items-center gap-3 mb-4">
                <div
                  class="w-9 h-9 bg-[#A8D5BA] rounded-full flex items-center justify-center shrink-0"
                >
                  <span class="text-sm">✨</span>
                </div>

                <div>
                  <h2 class="font-semibold text-[#2C5F2D]">
                    AI Nutritionist Feedback
                  </h2>
                  <p class="text-xs text-gray-500">
                    Powered by Groq LLaMA · Based on Australian Dietary Guidelines
                  </p>
                </div>
              </div>

              <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                {{ result.ai_feedback }}
              </p>
            </section>

            <button
              @click="resetAnalysis"
              class="w-full border border-[#A8D5BA] text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-xl py-3.5 sm:py-3 text-sm font-medium transition-colors"
              type="button"
            >
              Analyse Another Photo
            </button>
              </div>

              <!-- Error -->
              <div
                v-if="error"
                class="mt-4 rounded-xl border border-red-100 bg-red-50/50 p-5 text-center sm:p-6"
              >
                <p class="text-red-500 text-sm leading-relaxed">
                  {{ error }}
                </p>

                <button
                  @click="error = null"
                  class="mt-3 text-xs text-gray-400 underline"
                  type="button"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </section>
        </div>
      </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import {
  Upload,
  X,
  Leaf,
} from 'lucide-vue-next';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const childName = ref('');
const childAge = ref(7);
const error = ref(null);

const selectedChildId = ref('demo-emma');
const childPickerOpen = ref(false);

/** Mock child cards for UI preview — replace with backend-driven list later */
const MOCK_CHILD_PROFILES = [
  {
    id: 'demo-emma',
    name: 'Emma',
    ageGroup: '7-9 years',
    allergies: [],
    dietaryRestriction: '',
  },
  {
    id: 'demo-oliver',
    name: 'Oliver',
    ageGroup: '5-6 years',
    allergies: ['Peanuts'],
    dietaryRestriction: '',
  },
  {
    id: 'demo-maya',
    name: 'Maya',
    ageGroup: '10-12 years',
    allergies: ['Milk'],
    dietaryRestriction: 'Dairy-free',
  },
];

const orderedProfiles = computed(() => {
  const selected = MOCK_CHILD_PROFILES.find((p) => p.id === selectedChildId.value);
  const rest = MOCK_CHILD_PROFILES.filter((p) => p.id !== selectedChildId.value);

  return selected ? [selected, ...rest] : MOCK_CHILD_PROFILES;
});

const profileInitials = (name) => {
  if (!name || typeof name !== 'string') return '?';

  const parts = name.trim().split(/\s+/);

  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();

  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

const ageFromProfile = (profile) => {
  const group = profile?.ageGroup || '';

  if (group === '5-6 years') return 6;
  if (group === '7-9 years') return 8;
  if (group === '10-12 years') return 11;

  return 7;
};

const syncChildFromProfile = (profile) => {
  if (!profile) return;

  childName.value = profile.name;
  childAge.value = ageFromProfile(profile);
};

function openChildPicker() {
  childPickerOpen.value = true;
}

function closeChildPicker() {
  childPickerOpen.value = false;
}

function selectChildProfile(profile) {
  selectedChildId.value = profile.id;
  syncChildFromProfile(profile);
  childPickerOpen.value = false;
}

onMounted(() => {
  syncChildFromProfile(MOCK_CHILD_PROFILES[0]);
});

const photoInput = ref(null);
const photoPreview = ref(null);
const photoFile = ref(null);

const loading = ref(false);
const result = ref(null);

function triggerPhotoUpload() {
  if (photoInput.value) {
    photoInput.value.click();
  }
}

function setPhotoFile(file) {
  if (!file) return;

  const maxSizeMB = 5;
  const maxSizeBytes = maxSizeMB * 1024 * 1024;

  if (!file.type.startsWith('image/')) {
    error.value = 'Please upload an image file.';
    return;
  }

  if (file.size > maxSizeBytes) {
    error.value = `Please upload an image smaller than ${maxSizeMB}MB.`;
    return;
  }

  if (photoPreview.value) {
    URL.revokeObjectURL(photoPreview.value);
  }

  photoFile.value = file;
  photoPreview.value = URL.createObjectURL(file);
  result.value = null;
  error.value = null;
}

function onPhotoSelected(event) {
  const file = event.target.files?.[0];
  setPhotoFile(file);
}

function onPhotoDrop(event) {
  const file = event.dataTransfer.files?.[0];
  setPhotoFile(file);
}

function clearPhoto() {
  if (photoPreview.value) {
    URL.revokeObjectURL(photoPreview.value);
  }

  photoFile.value = null;
  photoPreview.value = null;

  if (photoInput.value) {
    photoInput.value.value = '';
  }
}

function resetAnalysis() {
  clearPhoto();
  result.value = null;
  error.value = null;
}

async function analysePhoto() {
  if (!photoFile.value) return;

  loading.value = true;
  error.value = null;

  try {
    const form = new FormData();
    form.append('file', photoFile.value);
    form.append('child_age', childAge.value);
    form.append('child_name', childName.value || 'your child');

    const response = await fetch(`${API_BASE}/photo/analyse`, {
      method: 'POST',
      body: form,
    });

    if (!response.ok) {
      let message = 'Analysis failed. Please try again.';

      try {
        const errorData = await response.json();
        message = errorData.detail || message;
      } catch {
        // keep default message
      }

      throw new Error(message);
    }

    result.value = await response.json();
  } catch (err) {
    error.value = err.message || 'Analysis failed. Please try again.';
  } finally {
    loading.value = false;
  }
}

const scoreColor = computed(() => {
  const color = result.value?.nutrition_score?.color;

  if (color === 'green') return 'text-green-600';
  if (color === 'blue') return 'text-blue-600';
  if (color === 'amber') return 'text-amber-500';

  return 'text-red-500';
});

const scoreBarColor = computed(() => {
  const color = result.value?.nutrition_score?.color;

  if (color === 'green') return 'bg-green-400';
  if (color === 'blue') return 'bg-blue-400';
  if (color === 'amber') return 'bg-amber-400';

  return 'bg-red-400';
});

const gradeBadge = computed(() => {
  const color = result.value?.nutrition_score?.color;

  if (color === 'green') return 'bg-green-100 text-green-700';
  if (color === 'blue') return 'bg-blue-100 text-blue-700';
  if (color === 'amber') return 'bg-amber-100 text-amber-700';

  return 'bg-red-100 text-red-700';
});
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>