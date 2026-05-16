<template>
  <div class="min-h-screen bg-[#FAF9F6]">

    <!-- Nav (matches HomePage exactly) -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="container mx-auto px-6 max-w-6xl">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-2 cursor-pointer" @click="router.push('/')">
            <div class="w-10 h-10 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center">
              <Heart class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-semibold text-[#2C5F2D]">LittleWell</span>
          </div>
          <div class="hidden md:flex items-center gap-6">
            <button @click="router.push('/')" class="text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg px-4 py-2 transition-colors">
              Lunchbox Plan
            </button>
            <button class="text-[#2C5F2D] bg-[#A8D5BA]/20 rounded-lg px-4 py-2 font-medium">
              <ScanLine class="w-4 h-4 inline mr-2" />Food Analyser
            </button>
            <button @click="router.push('/')" class="text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-lg px-4 py-2 transition-colors">
              About Us
            </button>
          </div>
          <button class="md:hidden p-2" @click="router.push('/')">
            <Menu class="w-5 h-5" />
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <div class="pt-16 bg-white border-b border-gray-100">
      <div class="container mx-auto px-6 max-w-6xl py-12">
        <div class="flex items-center gap-4 mb-4">
          <div class="w-14 h-14 bg-[#F7B267] rounded-full flex items-center justify-center">
            <ScanLine class="w-7 h-7 text-white" />
          </div>
          <div>
            <h1 class="text-3xl font-semibold text-[#2C5F2D]">Food Analyser</h1>
            <p class="text-muted-foreground">AI-powered nutrition insights for your child's food</p>
          </div>
        </div>

        <!-- Mode Toggle -->
        <div class="flex gap-3 mt-6">
          <button
            @click="mode = 'photo'"
            :class="[
              'flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all text-sm',
              mode === 'photo'
                ? 'bg-[#A8D5BA] text-[#2C5F2D] shadow-sm'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            <Camera class="w-4 h-4" />
            Lunchbox Photo
          </button>
          <button
            @click="mode = 'product'"
            :class="[
              'flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all text-sm',
              mode === 'product'
                ? 'bg-[#F7B267] text-white shadow-sm'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            <Barcode class="w-4 h-4" />
            Product Scanner
          </button>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-6 max-w-6xl py-10">
      <div class="grid md:grid-cols-3 gap-8">

        <!-- LEFT: Input Panel -->
        <div class="md:col-span-1 space-y-5">

          <!-- Child details card -->
          <div class="bg-white rounded-2xl shadow-sm border p-5">
            <h3 class="font-semibold text-[#2C5F2D] mb-4 flex items-center gap-2">
              <User class="w-4 h-4" /> Child Details
            </h3>
            <div class="space-y-3">
              <div>
                <label class="text-xs text-muted-foreground mb-1 block">Child's name</label>
                <input
                  v-model="childName"
                  type="text"
                  placeholder="e.g. Arya"
                  class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#A8D5BA] focus:ring-1 focus:ring-[#A8D5BA]"
                />
              </div>
              <div>
                <label class="text-xs text-muted-foreground mb-1 block">Age (years)</label>
                <select
                  v-model="childAge"
                  class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#A8D5BA]"
                >
                  <option v-for="a in 14" :key="a" :value="a">{{ a }} year{{ a > 1 ? 's' : '' }} old</option>
                </select>
              </div>
            </div>
          </div>

          <!-- PHOTO MODE upload -->
          <div v-if="mode === 'photo'" class="bg-white rounded-2xl shadow-sm border p-5">
            <h3 class="font-semibold text-[#2C5F2D] mb-4 flex items-center gap-2">
              <Camera class="w-4 h-4" /> Lunchbox Photo
            </h3>
            <div
              @click="triggerPhotoUpload"
              @dragover.prevent
              @drop.prevent="onPhotoDrop"
              :class="[
                'border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors',
                photoPreview ? 'border-[#A8D5BA]' : 'border-gray-200 hover:border-[#A8D5BA]'
              ]"
            >
              <input ref="photoInput" type="file" accept="image/*" class="hidden" @change="onPhotoSelected" />
              <div v-if="!photoPreview" class="space-y-2">
                <div class="w-12 h-12 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center mx-auto">
                  <Upload class="w-6 h-6 text-[#2C5F2D]" />
                </div>
                <p class="text-sm text-[#2C5F2D] font-medium">Upload or drag a photo</p>
                <p class="text-xs text-muted-foreground">JPG, PNG up to 5MB</p>
              </div>
              <div v-else class="relative">
                <img :src="photoPreview" class="w-full rounded-lg object-cover max-h-48" />
                <button
                  @click.stop="clearPhoto"
                  class="absolute top-2 right-2 bg-white rounded-full p-1 shadow hover:bg-gray-50"
                >
                  <X class="w-4 h-4 text-gray-500" />
                </button>
              </div>
            </div>
            <button
              v-if="photoPreview"
              @click="analysePhoto"
              :disabled="photoLoading"
              class="w-full mt-4 bg-[#A8D5BA] hover:bg-[#8FC2A4] disabled:opacity-50 text-[#2C5F2D] font-medium rounded-xl py-3 flex items-center justify-center gap-2 transition-colors"
            >
              <span v-if="!photoLoading">✨ Analyse Nutrition</span>
              <span v-else class="flex items-center gap-2">
                <span class="w-4 h-4 border-2 border-[#2C5F2D] border-t-transparent rounded-full animate-spin"></span>
                Analysing…
              </span>
            </button>
          </div>

          <!-- PRODUCT MODE -->
          <div v-if="mode === 'product'" class="bg-white rounded-2xl shadow-sm border p-5">
            <h3 class="font-semibold text-[#2C5F2D] mb-4 flex items-center gap-2">
              <Barcode class="w-4 h-4" /> Scan Product
            </h3>

            <!-- Tabs: photo or manual -->
            <div class="flex gap-2 mb-4">
              <button
                @click="productTab = 'barcode'"
                :class="['text-xs px-3 py-1.5 rounded-lg transition-colors', productTab === 'barcode' ? 'bg-[#F7B267] text-white' : 'bg-gray-100 text-gray-600']"
              >Photo barcode</button>
              <button
                @click="productTab = 'manual'"
                :class="['text-xs px-3 py-1.5 rounded-lg transition-colors', productTab === 'manual' ? 'bg-[#F7B267] text-white' : 'bg-gray-100 text-gray-600']"
              >Enter barcode</button>
            </div>

            <div v-if="productTab === 'barcode'">
              <div
                @click="triggerProductUpload"
                @dragover.prevent
                @drop.prevent="onProductDrop"
                :class="[
                  'border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-colors',
                  productPreview ? 'border-[#F7B267]' : 'border-gray-200 hover:border-[#F7B267]'
                ]"
              >
                <input ref="productInput" type="file" accept="image/*" class="hidden" @change="onProductSelected" />
                <div v-if="!productPreview" class="space-y-2">
                  <div class="w-12 h-12 bg-[#F7B267]/20 rounded-full flex items-center justify-center mx-auto">
                    <Barcode class="w-6 h-6 text-[#F7B267]" />
                  </div>
                  <p class="text-sm text-gray-700 font-medium">Photo of product barcode</p>
                  <p class="text-xs text-muted-foreground">Point camera at barcode</p>
                </div>
                <div v-else class="relative">
                  <img :src="productPreview" class="w-full rounded-lg object-cover max-h-40" />
                  <button @click.stop="clearProduct" class="absolute top-2 right-2 bg-white rounded-full p-1 shadow">
                    <X class="w-4 h-4 text-gray-500" />
                  </button>
                </div>
              </div>
            </div>

            <div v-if="productTab === 'manual'" class="space-y-3">
              <div>
                <label class="text-xs text-muted-foreground mb-1 block">Barcode number (EAN/UPC)</label>
                <input
                  v-model="manualBarcode"
                  type="text"
                  placeholder="e.g. 9300617781452"
                  class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#F7B267] focus:ring-1 focus:ring-[#F7B267]"
                  @keyup.enter="scanByBarcode"
                />
              </div>
              <p class="text-xs text-muted-foreground">Find the barcode number printed under the stripes on any packaged food product.</p>
            </div>

            <button
              @click="productTab === 'manual' ? scanByBarcode() : scanProduct()"
              :disabled="productLoading || (productTab === 'barcode' && !productPreview) || (productTab === 'manual' && !manualBarcode)"
              class="w-full mt-4 bg-[#F7B267] hover:bg-[#E5A156] disabled:opacity-50 text-white font-medium rounded-xl py-3 flex items-center justify-center gap-2 transition-colors"
            >
              <span v-if="!productLoading">🔍 Scan Product</span>
              <span v-else class="flex items-center gap-2">
                <span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Scanning…
              </span>
            </button>
          </div>

          <!-- Tips card -->
          <div class="bg-[#CDE7F0]/30 rounded-2xl border border-[#CDE7F0] p-5">
            <h4 class="text-sm font-semibold text-[#1B4965] mb-3">💡 Tips for best results</h4>
            <ul class="space-y-1.5 text-xs text-[#1B4965]">
              <li v-if="mode === 'photo'">• Good lighting helps identify more foods</li>
              <li v-if="mode === 'photo'">• Spread food out so items are visible</li>
              <li v-if="mode === 'product'">• Photograph the barcode on a flat surface</li>
              <li v-if="mode === 'product'">• Australian products work best (Open Food Facts)</li>
              <li>• Enter your child's correct age for accurate scoring</li>
            </ul>
          </div>
        </div>

        <!-- RIGHT: Results Panel -->
        <div class="md:col-span-2">

          <!-- Empty state -->
          <div v-if="!photoResult && !productResult && !photoLoading && !productLoading"
            class="bg-white rounded-2xl shadow-sm border p-12 text-center h-full flex flex-col items-center justify-center gap-4">
            <div class="w-20 h-20 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center">
              <Leaf class="w-10 h-10 text-[#A8D5BA]" />
            </div>
            <h3 class="text-lg font-medium text-[#2C5F2D]">Ready to analyse</h3>
            <p class="text-muted-foreground text-sm max-w-xs">
              {{ mode === 'photo'
                ? 'Upload a photo of your child\'s lunchbox to get AI-powered nutrition feedback'
                : 'Scan a packaged product barcode to see if it\'s suitable for your child' }}
            </p>
          </div>

          <!-- Loading state -->
          <div v-if="photoLoading || productLoading"
            class="bg-white rounded-2xl shadow-sm border p-12 text-center flex flex-col items-center justify-center gap-4">
            <div class="w-16 h-16 bg-[#A8D5BA]/20 rounded-full flex items-center justify-center animate-pulse">
              <span class="text-2xl">🤖</span>
            </div>
            <h3 class="text-lg font-medium text-[#2C5F2D]">AI is analysing…</h3>
            <p class="text-sm text-muted-foreground">{{ mode === 'photo' ? 'Detecting foods and scoring nutrition' : 'Looking up product and generating verdict' }}</p>
            <div class="flex gap-1 mt-2">
              <span class="w-2 h-2 bg-[#A8D5BA] rounded-full animate-bounce" style="animation-delay:0ms"></span>
              <span class="w-2 h-2 bg-[#A8D5BA] rounded-full animate-bounce" style="animation-delay:150ms"></span>
              <span class="w-2 h-2 bg-[#A8D5BA] rounded-full animate-bounce" style="animation-delay:300ms"></span>
            </div>
          </div>

          <!-- PHOTO RESULT -->
          <div v-if="photoResult && !photoLoading" class="space-y-5">

            <!-- Score card -->
            <div class="bg-white rounded-2xl shadow-sm border p-6">
              <div class="flex items-start justify-between mb-5">
                <div>
                  <h3 class="text-xl font-semibold text-[#2C5F2D]">Nutrition Score</h3>
                  <p class="text-sm text-muted-foreground">for {{ childName || 'your child' }}, age {{ childAge }}</p>
                </div>
                <div class="text-right">
                  <div :class="['text-4xl font-bold', scoreColor]">
                    {{ photoResult.nutrition_score.overall_score }}
                    <span class="text-lg text-muted-foreground font-normal">/100</span>
                  </div>
                  <span :class="['text-sm font-medium px-3 py-1 rounded-full', gradeBadge]">
                    {{ photoResult.nutrition_score.grade }}
                  </span>
                </div>
              </div>

              <!-- Score bar -->
              <div class="w-full bg-gray-100 rounded-full h-3 mb-5">
                <div
                  :class="['h-3 rounded-full transition-all duration-700', scoreBarColor]"
                  :style="{ width: photoResult.nutrition_score.overall_score + '%' }"
                ></div>
              </div>

              <!-- Detected foods -->
              <div class="mb-5">
                <p class="text-xs text-muted-foreground mb-2">Detected foods</p>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="food in photoResult.detected_foods"
                    :key="food"
                    class="bg-[#A8D5BA]/20 text-[#2C5F2D] text-xs rounded-full px-3 py-1 capitalize"
                  >
                    {{ food }}
                  </span>
                </div>
              </div>

              <!-- Note if no AUSNUT -->
              <div v-if="photoResult.nutrition_score.note" class="bg-[#CDE7F0]/30 rounded-xl p-3 mb-4 text-xs text-[#1B4965]">
                ℹ️ {{ photoResult.nutrition_score.note }}
              </div>
            </div>

            <!-- AI Feedback card -->
            <div class="bg-white rounded-2xl shadow-sm border p-6">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-9 h-9 bg-[#A8D5BA] rounded-full flex items-center justify-center">
                  <span class="text-sm">✨</span>
                </div>
                <div>
                  <h3 class="font-semibold text-[#2C5F2D]">AI Nutritionist Feedback</h3>
                  <p class="text-xs text-muted-foreground">Powered by Groq LLaMA</p>
                </div>
              </div>
              <p class="text-sm text-gray-700 leading-relaxed">{{ photoResult.ai_feedback }}</p>
            </div>

            <!-- Try again -->
            <button
              @click="clearPhoto(); photoResult = null"
              class="w-full border border-[#A8D5BA] text-[#2C5F2D] hover:bg-[#A8D5BA]/10 rounded-xl py-3 text-sm font-medium transition-colors"
            >
              Analyse Another Photo
            </button>
          </div>

          <!-- PRODUCT RESULT -->
          <div v-if="productResult && !productLoading" class="space-y-5">

            <!-- Product header -->
            <div class="bg-white rounded-2xl shadow-sm border p-6">
              <div class="flex items-start gap-4">
                <img v-if="productResult.image_url" :src="productResult.image_url"
                  class="w-20 h-20 object-contain rounded-xl border bg-gray-50 p-1" />
                <div class="w-20 h-20 rounded-xl border bg-gray-50 flex items-center justify-center flex-shrink-0" v-else>
                  <Barcode class="w-8 h-8 text-gray-300" />
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="font-semibold text-[#2C5F2D] text-lg leading-tight">{{ productResult.product_name }}</h3>
                  <p class="text-sm text-muted-foreground">{{ productResult.brand }}</p>
                  <p class="text-xs text-muted-foreground mt-1">Barcode: {{ productResult.barcode }}</p>
                  <div class="flex items-center gap-2 mt-2">
                    <span v-if="productResult.nutriscore"
                      :class="['text-xs font-bold px-2 py-0.5 rounded', nutriscoreClass(productResult.nutriscore)]">
                      Nutri-Score {{ productResult.nutriscore }}
                    </span>
                    <span v-if="productResult.nova_group" class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                      NOVA {{ productResult.nova_group }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Verdict -->
            <div :class="['rounded-2xl shadow-sm border p-6', verdictBg]">
              <div class="flex items-center gap-3 mb-4">
                <span class="text-2xl">{{ verdictEmoji }}</span>
                <div>
                  <h3 class="font-semibold" :class="verdictTextColor">
                    {{ verdictLabel }}
                  </h3>
                  <p class="text-sm" :class="verdictTextColor + ' opacity-80'">
                    {{ productResult.verdict?.summary }}
                  </p>
                </div>
              </div>

              <div class="grid md:grid-cols-2 gap-4">
                <div v-if="productResult.verdict?.pros?.length">
                  <p class="text-xs font-semibold text-[#2C5F2D] mb-2">✅ Good for your child</p>
                  <ul class="space-y-1">
                    <li v-for="pro in productResult.verdict.pros" :key="pro"
                      class="text-sm text-gray-700 flex items-start gap-2">
                      <span class="text-[#A8D5BA] mt-0.5 flex-shrink-0">•</span>{{ pro }}
                    </li>
                  </ul>
                </div>
                <div v-if="productResult.verdict?.cons?.length">
                  <p class="text-xs font-semibold text-[#8B4513] mb-2">⚠️ Watch out for</p>
                  <ul class="space-y-1">
                    <li v-for="con in productResult.verdict.cons" :key="con"
                      class="text-sm text-gray-700 flex items-start gap-2">
                      <span class="text-[#F7B267] mt-0.5 flex-shrink-0">•</span>{{ con }}
                    </li>
                  </ul>
                </div>
              </div>

              <div v-if="productResult.verdict?.tip" class="mt-4 bg-white/60 rounded-xl p-3">
                <p class="text-xs font-semibold text-[#1B4965] mb-1">💡 Parent tip</p>
                <p class="text-sm text-gray-700">{{ productResult.verdict.tip }}</p>
              </div>
            </div>

            <!-- Nutrition table -->
            <div class="bg-white rounded-2xl shadow-sm border p-6">
              <h3 class="font-semibold text-[#2C5F2D] mb-4">Nutrition per 100g</h3>
              <div class="grid grid-cols-2 gap-3">
                <div v-for="(val, key) in productResult.nutriments" :key="key"
                  class="bg-[#FAF9F6] rounded-xl p-3">
                  <p class="text-xs text-muted-foreground capitalize">{{ formatNutrientName(key) }}</p>
                  <p class="text-sm font-semibold text-[#2C5F2D]">{{ formatNutrientVal(key, val) }}</p>
                </div>
              </div>
            </div>

            <!-- Allergens -->
            <div v-if="productResult.allergens?.length" class="bg-[#F7B267]/10 border border-[#F7B267]/30 rounded-2xl p-5">
              <p class="text-sm font-semibold text-[#8B4513] mb-2">⚠️ Allergens</p>
              <div class="flex flex-wrap gap-2">
                <span v-for="a in productResult.allergens" :key="a"
                  class="bg-[#F7B267]/20 text-[#8B4513] text-xs rounded-full px-3 py-1 capitalize">
                  {{ a.replace('en:', '').replace('-', ' ') }}
                </span>
              </div>
            </div>

            <!-- Try again -->
            <button
              @click="productResult = null; productPreview = null; manualBarcode = ''"
              class="w-full border border-[#F7B267] text-[#8B4513] hover:bg-[#F7B267]/10 rounded-xl py-3 text-sm font-medium transition-colors"
            >
              Scan Another Product
            </button>
          </div>

          <!-- Error -->
          <div v-if="error" class="bg-white rounded-2xl shadow-sm border border-red-100 p-6 text-center">
            <p class="text-red-500 text-sm">{{ error }}</p>
            <button @click="error = null" class="mt-3 text-xs text-muted-foreground underline">Dismiss</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Heart, ScanLine, Camera, Barcode, Upload, X, Leaf, Menu, User } from 'lucide-vue-next'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const router = useRouter()

// shared state
const mode = ref('photo')
const childName = ref('')
const childAge = ref(7)
const error = ref(null)

// photo analyser
const photoInput = ref(null)
const photoPreview = ref(null)
const photoFile = ref(null)
const photoLoading = ref(false)
const photoResult = ref(null)

// product scanner
const productInput = ref(null)
const productPreview = ref(null)
const productFile = ref(null)
const productLoading = ref(false)
const productResult = ref(null)
const productTab = ref('manual')
const manualBarcode = ref('')

// ── Photo analyser ──────────────────────────────────────
function triggerPhotoUpload() { photoInput.value.click() }

function onPhotoSelected(e) {
  const file = e.target.files[0]
  if (!file) return
  photoFile.value = file
  photoPreview.value = URL.createObjectURL(file)
  photoResult.value = null
  error.value = null
}

function onPhotoDrop(e) {
  const file = e.dataTransfer.files[0]
  if (!file) return
  photoFile.value = file
  photoPreview.value = URL.createObjectURL(file)
  photoResult.value = null
}

function clearPhoto() {
  photoFile.value = null
  photoPreview.value = null
  if (photoInput.value) photoInput.value.value = ''
}

async function analysePhoto() {
  if (!photoFile.value) return
  photoLoading.value = true
  error.value = null
  try {
    const form = new FormData()
    form.append('file', photoFile.value)
    form.append('child_age', childAge.value)
    form.append('child_name', childName.value || 'your child')
    const res = await fetch(`${API_BASE}/photo/analyse`, { method: 'POST', body: form })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Analysis failed')
    }
    photoResult.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    photoLoading.value = false
  }
}

// ── Product scanner ─────────────────────────────────────
function triggerProductUpload() { productInput.value.click() }

function onProductSelected(e) {
  const file = e.target.files[0]
  if (!file) return
  productFile.value = file
  productPreview.value = URL.createObjectURL(file)
  productResult.value = null
  error.value = null
}

function onProductDrop(e) {
  const file = e.dataTransfer.files[0]
  if (!file) return
  productFile.value = file
  productPreview.value = URL.createObjectURL(file)
}

function clearProduct() {
  productFile.value = null
  productPreview.value = null
  if (productInput.value) productInput.value.value = ''
}

async function scanProduct() {
  if (!productFile.value) return
  productLoading.value = true
  error.value = null
  try {
    const form = new FormData()
    form.append('file', productFile.value)
    form.append('child_age', childAge.value)
    form.append('child_name', childName.value || 'your child')
    const res = await fetch(`${API_BASE}/product/scan`, { method: 'POST', body: form })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Scan failed')
    }
    productResult.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    productLoading.value = false
  }
}

async function scanByBarcode() {
  if (!manualBarcode.value.trim()) return
  productLoading.value = true
  error.value = null
  try {
    const res = await fetch(
      `${API_BASE}/product/lookup?barcode=${manualBarcode.value.trim()}&child_age=${childAge.value}&child_name=${encodeURIComponent(childName.value || 'your child')}`
    )
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Product not found')
    }
    productResult.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    productLoading.value = false
  }
}

// ── Computed display helpers ─────────────────────────────
const scoreColor = computed(() => {
  const s = photoResult.value?.nutrition_score?.color
  return s === 'green' ? 'text-green-600' : s === 'blue' ? 'text-blue-600' : s === 'amber' ? 'text-amber-500' : 'text-red-500'
})

const scoreBarColor = computed(() => {
  const s = photoResult.value?.nutrition_score?.color
  return s === 'green' ? 'bg-green-400' : s === 'blue' ? 'bg-blue-400' : s === 'amber' ? 'bg-amber-400' : 'bg-red-400'
})

const gradeBadge = computed(() => {
  const s = photoResult.value?.nutrition_score?.color
  return s === 'green' ? 'bg-green-100 text-green-700' : s === 'blue' ? 'bg-blue-100 text-blue-700' : s === 'amber' ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700'
})

const verdictBg = computed(() => {
  const v = productResult.value?.verdict?.verdict
  return v === 'good' ? 'bg-[#A8D5BA]/10 border-[#A8D5BA]' : v === 'avoid' ? 'bg-red-50 border-red-200' : 'bg-[#F7B267]/10 border-[#F7B267]/40'
})

const verdictTextColor = computed(() => {
  const v = productResult.value?.verdict?.verdict
  return v === 'good' ? 'text-[#2C5F2D]' : v === 'avoid' ? 'text-red-700' : 'text-[#8B4513]'
})

const verdictLabel = computed(() => {
  const v = productResult.value?.verdict?.verdict
  return v === 'good' ? 'Great choice for your child' : v === 'avoid' ? 'Best to avoid this one' : 'Okay occasionally'
})

const verdictEmoji = computed(() => {
  const v = productResult.value?.verdict?.verdict
  return v === 'good' ? '✅' : v === 'avoid' ? '🚫' : '⚠️'
})

function nutriscoreClass(score) {
  const map = { A: 'bg-green-500 text-white', B: 'bg-lime-400 text-white', C: 'bg-yellow-400 text-gray-800', D: 'bg-orange-400 text-white', E: 'bg-red-500 text-white' }
  return map[score] || 'bg-gray-200 text-gray-700'
}

function formatNutrientName(key) {
  return key.replace(/_g$/, ' (g)').replace(/_mg$/, ' (mg)').replace(/_kj$/, ' (kj)').replace(/_/g, ' ')
}

function formatNutrientVal(key, val) {
  if (val === null || val === undefined) return '—'
  const v = parseFloat(val)
  if (isNaN(v)) return '—'
  return key.endsWith('_mg') ? v.toFixed(1) + ' mg' : key.endsWith('_kj') ? v.toFixed(0) + ' kj' : v.toFixed(1) + ' g'
}
</script>

<style scoped>
.text-muted-foreground { color: #6b7280; }
</style>
