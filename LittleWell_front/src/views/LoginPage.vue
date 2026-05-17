<template>
  <div class="min-h-screen bg-[#FAF9F6] flex">
    <!-- Left Panel - Desktop only -->
    <div
      class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] relative overflow-hidden flex-col justify-between p-12"
      aria-hidden="true"
    >
      <div class="absolute top-[-80px] right-[-80px] w-80 h-80 bg-white/10 rounded-full" />
      <div class="absolute bottom-[-60px] left-[-60px] w-64 h-64 bg-white/10 rounded-full" />

      <div class="flex items-center relative z-10">
        <img :src="logoUrl" alt="" class="h-12 w-auto object-contain rounded-lg" />
      </div>

      <div class="relative z-10">
        <h2 class="text-4xl font-light text-white leading-snug mb-4">
          Nourishing little ones,<br />one lunchbox at a time.
        </h2>
        <p class="text-white/80 text-lg leading-relaxed">
          Science-backed nutrition plans tailored to your child's unique needs, made simple for busy families.
        </p>
        <div class="flex flex-wrap gap-2 mt-8">
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">🥗 Seasonal recipes</span>
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">🧒 Age-appropriate</span>
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">⚡ Allergy safe</span>
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">📅 Weekly plans</span>
        </div>
      </div>

      <p class="relative z-10 text-white/60 text-sm">
        Trusted by families across Australia
      </p>
    </div>

    <!-- Right Panel -->
    <div class="w-full lg:w-1/2 flex items-center justify-center px-4 py-6 sm:px-6 sm:py-10 lg:py-12">
      <div class="w-full max-w-md">
        <!-- Mobile Brand Card -->
        <div
          class="mb-6 rounded-3xl bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] p-5 shadow-sm lg:hidden"
        >
          <div class="flex items-center gap-3 mb-5">
            <img
              :src="logoUrl"
              alt="LittleHelp logo"
              class="h-11 w-11 rounded-2xl object-cover bg-white/80 p-1"
            />
            <div>
              <p class="text-lg font-semibold text-white">LittleHelp</p>
              <p class="text-xs text-white/80">Lunchbox planning made simple</p>
            </div>
          </div>

          <h2 class="text-2xl font-light leading-snug text-white">
            Welcome back to your family nutrition space.
          </h2>

          <div class="mt-5 flex flex-wrap gap-2">
            <span class="rounded-full bg-white/20 px-3 py-1 text-xs text-white">🥗 Seasonal</span>
            <span class="rounded-full bg-white/20 px-3 py-1 text-xs text-white">🧒 Age-based</span>
            <span class="rounded-full bg-white/20 px-3 py-1 text-xs text-white">⚡ Allergy safe</span>
          </div>
        </div>

        <!-- Form Card -->
        <div class="rounded-3xl bg-white p-5 shadow-sm border border-[#E8E4DC] sm:p-8 lg:border-0 lg:bg-transparent lg:p-0 lg:shadow-none">
          <h1 class="mb-2 text-3xl font-semibold text-gray-800">
            Welcome back
          </h1>
          <p class="mb-6 text-sm text-gray-500 sm:mb-8 sm:text-base">
            Sign in to your account to continue
          </p>

          <!-- Error message -->
          <div
            v-if="errorMessage"
            role="alert"
            aria-live="assertive"
            class="mb-5 flex items-start gap-2 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
          >
            <AlertCircle class="mt-0.5 h-4 w-4 flex-shrink-0" aria-hidden="true" />
            <span>{{ errorMessage }}</span>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-5" novalidate>
            <!-- Username -->
            <div>
              <label for="login-username" class="mb-1.5 block text-sm font-medium text-gray-700">
                Username
              </label>
              <div class="relative">
                <User
                  class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
                  aria-hidden="true"
                />
                <input
                  id="login-username"
                  v-model.trim="form.username"
                  type="text"
                  placeholder="Enter your username"
                  required
                  autocomplete="username"
                  autocapitalize="none"
                  spellcheck="false"
                  class="w-full rounded-xl border border-gray-200 bg-white py-3.5 pl-10 pr-4 text-base text-gray-800 placeholder-gray-400 transition-all focus:border-transparent focus:outline-none focus:ring-2 focus:ring-[#A8D5BA]"
                />
              </div>
            </div>

            <!-- Password -->
            <div>
              <label for="login-password" class="mb-1.5 block text-sm font-medium text-gray-700">
                Password
              </label>
              <div class="relative">
                <Lock
                  class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
                  aria-hidden="true"
                />
                <input
                  id="login-password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Enter your password"
                  required
                  autocomplete="current-password"
                  class="w-full rounded-xl border border-gray-200 bg-white py-3.5 pl-10 pr-12 text-base text-gray-800 placeholder-gray-400 transition-all focus:border-transparent focus:outline-none focus:ring-2 focus:ring-[#A8D5BA]"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-2 top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-lg text-gray-400 transition-colors hover:bg-gray-50 hover:text-gray-600"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  :aria-pressed="showPassword"
                >
                  <Eye v-if="!showPassword" class="h-4 w-4" aria-hidden="true" />
                  <EyeOff v-else class="h-4 w-4" aria-hidden="true" />
                </button>
              </div>
            </div>

            <button
              type="submit"
              :disabled="isLoading || !form.username || !form.password"
              class="flex w-full items-center justify-center gap-2 rounded-xl bg-[#A8D5BA] py-3.5 font-semibold text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-60"
              :aria-busy="isLoading"
            >
              <Loader2 v-if="isLoading" class="h-4 w-4 animate-spin" aria-hidden="true" />
              <span>{{ isLoading ? 'Signing in…' : 'Sign in' }}</span>
            </button>
          </form>

          <div class="my-6 flex items-center gap-3" aria-hidden="true">
            <div class="h-px flex-1 bg-gray-200" />
            <span class="text-sm text-gray-400">or</span>
            <div class="h-px flex-1 bg-gray-200" />
          </div>

          <p class="text-center text-sm text-gray-600 sm:text-base">
            Don't have an account?
            <router-link
              to="/register"
              class="ml-1 font-medium text-[#2C5F2D] hover:underline"
            >
              Create one for free
            </router-link>
          </p>

          <div class="mt-6 text-center">
            <router-link
              to="/"
              class="inline-flex items-center justify-center gap-1 text-sm text-gray-400 hover:text-gray-600"
            >
              <ArrowLeft class="h-3.5 w-3.5" aria-hidden="true" />
              Back to home
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { User, Lock, Eye, EyeOff, AlertCircle, Loader2, ArrowLeft } from 'lucide-vue-next';
import { useAuthStore } from '../stores/auth';
import logoUrl from '../assets/littlehelp-logo.jpg';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = reactive({
  username: '',
  password: '',
});

const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

const handleLogin = async () => {
  if (!form.username || !form.password || isLoading.value) return;

  errorMessage.value = '';
  isLoading.value = true;

  try {
    await authStore.login({
      username: form.username,
      password: form.password,
    });

    const rawRedirect = route.query.redirect;
    let destination = '/';
    if (typeof rawRedirect === 'string' && rawRedirect.startsWith('/') && !rawRedirect.startsWith('//')) {
      destination = rawRedirect;
    }

    const hashIndex = destination.indexOf('#');
    if (hashIndex !== -1) {
      router.push({
        path: destination.slice(0, hashIndex),
        hash: destination.slice(hashIndex),
      });
    } else {
      router.push(destination);
    }
  } catch (err) {
    errorMessage.value = err.message || 'Incorrect username or password.';
  } finally {
    isLoading.value = false;
  }
};
</script>