<template>
  <div class="min-h-screen bg-[#FAF9F6] flex">
    <!-- Left Panel - Illustration/Brand -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] relative overflow-hidden flex-col justify-between p-12">
      <!-- Background decorative circles -->
      <div class="absolute top-[-80px] right-[-80px] w-80 h-80 bg-white/10 rounded-full" />
      <div class="absolute bottom-[-60px] left-[-60px] w-64 h-64 bg-white/10 rounded-full" />
      <div class="absolute top-1/2 left-1/3 w-40 h-40 bg-white/5 rounded-full" />

      <!-- Logo -->
      <div class="flex items-center gap-3 relative z-10">
        <div class="w-10 h-10 bg-white/30 rounded-full flex items-center justify-center">
          <Heart class="w-5 h-5 text-white" />
        </div>
        <span class="text-2xl font-semibold text-white">LittleWell</span>
      </div>

      <!-- Center Content -->
      <div class="relative z-10">
        <h2 class="text-4xl font-light text-white leading-snug mb-4">
          Nourishing little ones,<br />one lunchbox at a time.
        </h2>
        <p class="text-white/80 text-lg leading-relaxed">
          Science-backed nutrition plans tailored to your child's unique needs, made simple for busy families.
        </p>

        <!-- Feature pills -->
        <div class="flex flex-wrap gap-2 mt-8">
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">🥗 Seasonal recipes</span>
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">🧒 Age-appropriate</span>
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">⚡ Allergy safe</span>
          <span class="bg-white/20 text-white text-sm rounded-full px-4 py-1.5">📅 Weekly plans</span>
        </div>
      </div>

      <!-- Bottom quote -->
      <p class="relative z-10 text-white/60 text-sm">
        Trusted by families across Australia
      </p>
    </div>

    <!-- Right Panel - Login Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
      <div class="w-full max-w-md">
        <!-- Mobile logo -->
        <div class="flex items-center gap-2 mb-8 lg:hidden">
          <div class="w-9 h-9 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center">
            <Heart class="w-4 h-4 text-white" />
          </div>
          <span class="text-xl font-semibold text-[#2C5F2D]">LittleWell</span>
        </div>

        <h1 class="text-3xl font-semibold text-gray-800 mb-2">Welcome back</h1>
        <p class="text-gray-500 mb-8">Sign in to your account to continue</p>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email address</label>
            <div class="relative">
              <Mail class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                v-model="form.email"
                type="email"
                placeholder="you@example.com"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-sm font-medium text-gray-700">Password</label>
              <button
                type="button"
                class="text-sm text-[#2C5F2D] hover:underline"
                @click="handleForgotPassword"
              >
                Forgot password?
              </button>
            </div>

            <div class="relative">
              <Lock class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                v-model="form.password"
                type="password"
                placeholder="Enter your password"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />
            </div>
          </div>

          <!-- Remember me -->
          <div class="flex items-center gap-2">
            <input
              id="remember"
              v-model="form.rememberMe"
              type="checkbox"
              class="w-4 h-4 rounded border-gray-300 text-[#A8D5BA] focus:ring-[#A8D5BA] accent-[#A8D5BA]"
            />
            <label for="remember" class="text-sm text-gray-600">Remember me for 30 days</label>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] font-semibold py-3 rounded-xl transition-colors"
          >
            Sign in
          </button>
        </form>

        <!-- Divider -->
        <div class="flex items-center gap-3 my-6">
          <div class="flex-1 h-px bg-gray-200" />
          <span class="text-sm text-gray-400">or</span>
          <div class="flex-1 h-px bg-gray-200" />
        </div>

        <!-- Register link -->
        <p class="text-center text-gray-600">
          Don't have an account?
          <router-link to="/register" class="text-[#2C5F2D] font-medium hover:underline ml-1">
            Create one for free
          </router-link>
        </p>

        <!-- Back to home -->
        <div class="mt-6 text-center">
          <router-link to="/" class="text-sm text-gray-400 hover:text-gray-600 flex items-center justify-center gap-1">
            <ArrowLeft class="w-3.5 h-3.5" />
            Back to home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import {
  Heart,
  Mail,
  Lock,
  ArrowLeft,
} from 'lucide-vue-next';

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
});

const handleLogin = () => {
  alert('Login function will be added later.');
};

const handleForgotPassword = () => {
  alert('Password reset coming soon. Please contact support.');
};
</script>