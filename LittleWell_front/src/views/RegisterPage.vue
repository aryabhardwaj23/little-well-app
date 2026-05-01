<template>
  <div class="min-h-screen bg-[#FAF9F6] flex">
    <!-- Left Panel -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] relative overflow-hidden flex-col justify-between p-12">
      <div class="absolute top-[-80px] right-[-80px] w-80 h-80 bg-white/10 rounded-full" />
      <div class="absolute bottom-[-60px] left-[-60px] w-64 h-64 bg-white/10 rounded-full" />

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
          Start your family's<br />nutrition journey today.
        </h2>
        <p class="text-white/80 text-lg leading-relaxed">
          Create your free account and build personalised lunchbox plans your kids will actually love.
        </p>

        <!-- Steps -->
        <div class="mt-8 space-y-4">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/30 flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm font-semibold">1</span>
            </div>
            <p class="text-white/90 text-sm">Create your free account</p>
          </div>

          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/30 flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm font-semibold">2</span>
            </div>
            <p class="text-white/90 text-sm">Add your children's profiles</p>
          </div>

          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/30 flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm font-semibold">3</span>
            </div>
            <p class="text-white/90 text-sm">Get personalised meal plans instantly</p>
          </div>
        </div>
      </div>

      <p class="relative z-10 text-white/60 text-sm">
        Free forever • No credit card required
      </p>
    </div>

    <!-- Right Panel - Register Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12 overflow-y-auto">
      <div class="w-full max-w-md">
        <!-- Mobile logo -->
        <div class="flex items-center gap-2 mb-8 lg:hidden">
          <div class="w-9 h-9 bg-gradient-to-br from-[#A8D5BA] to-[#8FC2A4] rounded-full flex items-center justify-center">
            <Heart class="w-4 h-4 text-white" />
          </div>
          <span class="text-xl font-semibold text-[#2C5F2D]">LittleWell</span>
        </div>

        <h1 class="text-3xl font-semibold text-gray-800 mb-2">Create your account</h1>
        <p class="text-gray-500 mb-8">Free forever. No credit card needed.</p>

        <!-- Form -->
        <form @submit.prevent="handleRegister" class="space-y-5">
          <!-- Name row -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">First name</label>
              <input
                v-model="form.firstName"
                type="text"
                placeholder="Jane"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Last name</label>
              <input
                v-model="form.lastName"
                type="text"
                placeholder="Smith"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />
            </div>
          </div>

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
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Password</label>
            <div class="relative">
              <Lock class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                v-model="form.password"
                type="password"
                placeholder="At least 8 characters"
                required
                minlength="8"
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Confirm password</label>
            <div class="relative">
              <Lock class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                v-model="form.confirmPassword"
                type="password"
                placeholder="Repeat your password"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 bg-white focus:outline-none focus:ring-2 focus:ring-[#A8D5BA] focus:border-transparent transition-all"
              />
            </div>
          </div>

          <!-- Terms -->
          <div class="flex items-start gap-2">
            <input
              id="terms"
              v-model="form.acceptTerms"
              type="checkbox"
              required
              class="w-4 h-4 mt-0.5 rounded border-gray-300 accent-[#A8D5BA]"
            />
            <label for="terms" class="text-sm text-gray-600 leading-relaxed">
              I agree to the
              <a href="#" class="text-[#2C5F2D] hover:underline">Terms of Service</a>
              and
              <a href="#" class="text-[#2C5F2D] hover:underline">Privacy Policy</a>
            </label>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            class="w-full bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] font-semibold py-3 rounded-xl transition-colors"
          >
            Create account
          </button>
        </form>

        <!-- Login link -->
        <p class="text-center text-gray-600 mt-6">
          Already have an account?
          <router-link to="/login" class="text-[#2C5F2D] font-medium hover:underline ml-1">
            Sign in
          </router-link>
        </p>

        <!-- Back to home -->
        <div class="mt-4 text-center">
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
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
});

const handleRegister = () => {
  alert('Register function will be added later.');
};
</script>