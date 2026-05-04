<template>
  <div class="min-h-screen bg-[#FAF9F6] flex items-center justify-center px-6">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <img
          :src="logoUrl"
          alt="LittleHelp logo"
          class="h-20 w-auto object-contain mx-auto mb-4"
        />

        <p class="text-gray-500">
          Private project access
        </p>
      </div>

      <!-- Card -->
      <div class="bg-white rounded-3xl shadow-xl border border-gray-100 p-8">
        <div class="mb-6">
          <h2 class="text-2xl font-semibold text-gray-800 mb-2">
            Enter access details
          </h2>

          <p class="text-sm text-gray-500 leading-relaxed">
            Please enter the project access username and password to continue.
          </p>
        </div>

        <div
          v-if="errorMessage"
          class="mb-5 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-start gap-2"
        >
          <AlertCircle class="w-4 h-4 mt-0.5 flex-shrink-0" />
          <span>{{ errorMessage }}</span>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- Username -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              Username
            </label>

            <div class="relative">
              <User class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />

              <input
                v-model="form.username"
                type="text"
                autocomplete="username"
                placeholder="Enter username"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              Password
            </label>

            <div class="relative">
              <Lock class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />

              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                placeholder="Enter password"
                required
                class="w-full pl-10 pr-12 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />

              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <Eye v-if="!showPassword" class="w-4 h-4" />
                <EyeOff v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <button
            type="submit"
            class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] font-semibold py-3 rounded-xl transition-colors"
          >
            Continue to LittleHelp
          </button>
        </form>

        <p class="text-xs text-gray-400 text-center mt-6">
          Access is required before viewing the website.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {
  User,
  Lock,
  Eye,
  EyeOff,
  AlertCircle,
} from 'lucide-vue-next';
import logoUrl from '../assets/littlehelp-logo.jpg';

const router = useRouter();
const route = useRoute();

const form = reactive({
  username: '',
  password: '',
});

const showPassword = ref(false);
const errorMessage = ref('');

const PROJECT_USERNAME =
  import.meta.env.VITE_PROJECT_ACCESS_USERNAME || 'littlehelp';

const PROJECT_PASSWORD =
  import.meta.env.VITE_PROJECT_ACCESS_PASSWORD || 'LH2026DEMO';

const handleSubmit = () => {
  errorMessage.value = '';

  const inputUsername = form.username.trim();
  const inputPassword = form.password;

  if (
    inputUsername === PROJECT_USERNAME &&
    inputPassword === PROJECT_PASSWORD
  ) {
    localStorage.setItem('littlewell_project_access', 'granted');

    const redirect = route.query.redirect || '/';
    router.push(String(redirect));
    return;
  }

  errorMessage.value = 'Incorrect access username or password.';
};
</script>