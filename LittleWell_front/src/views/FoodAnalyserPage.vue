<template>
  <div class="min-h-screen bg-[#FAF9F6]">
    <!-- Header: no internal nav, use global NavigationBar -->
    <section class="pt-24 lg:pt-28 bg-white border-b border-gray-100">
      <div class="container mx-auto px-4 sm:px-6 max-w-6xl py-8 sm:py-10">
        <div class="flex flex-col sm:flex-row sm:items-center gap-4">
          <div
            class="w-14 h-14 bg-[#A8D5BA] rounded-full flex items-center justify-center shrink-0"
          >
            <Camera class="w-7 h-7 text-white" />
          </div>

          <div>
            <h1 class="text-2xl sm:text-3xl font-semibold text-[#2C5F2D] leading-tight">
              Lunchbox Food Analyser
            </h1>
            <p class="mt-2 text-sm sm:text-base text-gray-500 leading-relaxed">
              Upload a photo of your child's lunchbox for AI-powered nutrition insights.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main class="container mx-auto px-4 sm:px-6 max-w-6xl py-6 sm:py-10">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
        <!-- Left Panel -->
        <aside class="lg:col-span-1 space-y-5">
          <!-- Child Details -->
          <section class="bg-white rounded-2xl shadow-sm border p-5">
            <h2 class="font-semibold text-[#2C5F2D] mb-4">
              Child Details
            </h2>

            <div class="space-y-4">
              <div>
                <label class="text-xs text-gray-500 mb-1 block">
                  Child's name
                </label>
                <input
                  v-model="childName"
                  type="text"
                  placeholder="e.g. Arya"
                  class="w-full border border-gray-200 rounded-lg px-3 py-3 sm:py-2 text-sm focus:outline-none focus:border-[#A8D5BA] focus:ring-1 focus:ring-[#A8D5BA]"
                />
              </div>

              <div>
                <label class="text-xs text-gray-500 mb-1 block">
                  Age (years)
                </label>
                <select
                  v-model="childAge"
                  class="w-full border border-gray-200 rounded-lg px-3 py-3 sm:py-2 text-sm bg-white focus:outline-none focus:border-[#A8D5BA] focus:ring-1 focus:ring-[#A8D5BA]"
                >
                  <option
                    v-for="age in allowedAges"
                    :key="age"
                    :value="age"
                  >
                    {{ age }} years old
                  </option>
                </select>
              </div>
            </div>
          </section>

          <!-- Upload Card -->
          <section class="bg-white rounded-2xl shadow-sm border p-5">
            <h2 class="font-semibold text-[#2C5F2D] mb-4">
              Lunchbox Photo
            </h2>

            <div
              @click="triggerPhotoUpload"
              @dragover.prevent
              @drop.prevent="onPhotoDrop"
              :class="[
                'border-2 border-dashed rounded-xl p-5 sm:p-6 text-center cursor-pointer transition-colors',
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
          </section>

          <!-- Tips -->
          <section class="bg-[#CDE7F0]/30 rounded-2xl border border-[#CDE7F0] p-5">
            <h2 class="text-sm font-semibold text-[#1B4965] mb-3">
              Tips for best results
            </h2>

            <ul class="space-y-2 text-xs sm:text-sm text-[#1B4965] leading-relaxed">
              <li>• Good lighting helps identify more foods</li>
              <li>• Spread food out so all items are visible</li>
              <li>• Photograph from directly above the lunchbox</li>
              <li>• Enter your child's correct age for accurate scoring</li>
            </ul>
          </section>
        </aside>

        <!-- Right Panel -->
        <section class="lg:col-span-2">
          <!-- Empty State -->
          <div
            v-if="!result && !loading"
            class="bg-white rounded-2xl shadow-sm border p-8 sm:p-12 text-center flex flex-col items-center justify-center gap-4 min-h-[280px] sm:min-h-[360px]"
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
            class="bg-white rounded-2xl shadow-sm border p-8 sm:p-12 text-center flex flex-col items-center justify-center gap-4 min-h-[280px] sm:min-h-[360px]"
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
            <section class="bg-white rounded-2xl shadow-sm border p-5 sm:p-6">
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
            <section class="bg-white rounded-2xl shadow-sm border p-5 sm:p-6">
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
            class="bg-white rounded-2xl shadow-sm border border-red-100 p-5 sm:p-6 text-center mt-4"
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
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {
  Camera,
  Upload,
  X,
  Leaf,
} from 'lucide-vue-next';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const allowedAges = [5, 6, 7, 8, 9, 10, 11, 12];

const childName = ref('');
const childAge = ref(7);
const error = ref(null);

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