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
        <img
          :src="logoUrl"
          alt=""
          class="h-12 w-auto object-contain rounded-lg"
        />
      </div>

      <div class="relative z-10">
        <h2 class="text-4xl font-light text-white leading-snug mb-4">
          Start your family's<br />nutrition journey today.
        </h2>

        <p class="text-white/80 text-lg leading-relaxed">
          Create your free account and build personalised lunchbox plans your kids will actually love.
        </p>

        <div class="mt-8 space-y-4">
          <div
            v-for="(step, i) in steps"
            :key="i"
            class="flex items-center gap-3"
          >
            <div class="w-8 h-8 rounded-full bg-white/30 flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm font-semibold">{{ i + 1 }}</span>
            </div>
            <p class="text-white/90 text-sm">{{ step }}</p>
          </div>
        </div>
      </div>

      <p class="relative z-10 text-white/60 text-sm">
        Free forever • No credit card required
      </p>
    </div>

    <!-- Right Panel -->
    <div class="w-full lg:w-1/2 flex items-center justify-center px-4 py-6 sm:px-6 sm:py-10 lg:py-12 overflow-y-auto">
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
              <p class="text-xs text-white/80">Free lunchbox planning account</p>
            </div>
          </div>

          <h2 class="text-2xl font-light leading-snug text-white">
            Start your family's nutrition journey today.
          </h2>

          <div class="mt-5 space-y-2">
            <div
              v-for="(step, i) in steps"
              :key="i"
              class="flex items-center gap-2"
            >
              <div class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white/25">
                <span class="text-xs font-semibold text-white">{{ i + 1 }}</span>
              </div>
              <p class="text-xs text-white/90">{{ step }}</p>
            </div>
          </div>
        </div>

        <!-- Form Card -->
        <div class="rounded-3xl bg-white p-5 shadow-sm border border-[#E8E4DC] sm:p-8 lg:border-0 lg:bg-transparent lg:p-0 lg:shadow-none">
          <h1 class="mb-2 text-3xl font-semibold text-gray-800">
            Create your account
          </h1>

          <p class="mb-6 text-sm text-gray-500 sm:mb-8 sm:text-base">
            Free forever. No credit card needed.
          </p>

          <div
            v-if="errorMessage"
            role="alert"
            aria-live="assertive"
            class="mb-5 flex items-start gap-2 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
          >
            <AlertCircle class="mt-0.5 h-4 w-4 flex-shrink-0" aria-hidden="true" />
            <span>{{ errorMessage }}</span>
          </div>

          <div
            v-if="successMessage"
            role="status"
            aria-live="polite"
            class="mb-5 flex items-start gap-2 rounded-xl border border-[#A8D5BA] bg-[#A8D5BA]/20 p-4 text-sm text-[#2C5F2D]"
          >
            <CheckCircle class="mt-0.5 h-4 w-4 flex-shrink-0" aria-hidden="true" />
            <span>{{ successMessage }}</span>
          </div>

          <form @submit.prevent="handleRegister" class="space-y-5" novalidate>
            <!-- Username -->
            <div>
              <label for="register-username" class="mb-1.5 block text-sm font-medium text-gray-700">
                Username
              </label>

              <div class="relative">
                <User
                  class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
                  aria-hidden="true"
                />

                <input
                  id="register-username"
                  v-model.trim="form.username"
                  type="text"
                  placeholder="Choose a username"
                  required
                  minlength="3"
                  autocomplete="username"
                  autocapitalize="none"
                  spellcheck="false"
                  class="w-full rounded-xl border border-gray-200 bg-white py-3.5 pl-10 pr-4 text-base text-gray-800 placeholder-gray-400 transition-all focus:border-transparent focus:outline-none focus:ring-2 focus:ring-[#A8D5BA]"
                />
              </div>
            </div>

            <!-- Password -->
            <div>
              <label for="register-password" class="mb-1.5 block text-sm font-medium text-gray-700">
                Password
              </label>

              <div class="relative">
                <Lock
                  class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
                  aria-hidden="true"
                />

                <input
                  id="register-password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="At least 8 characters"
                  required
                  minlength="8"
                  autocomplete="new-password"
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

              <div v-if="form.password" class="mt-2">
                <div class="flex gap-1">
                  <div
                    v-for="i in 4"
                    :key="i"
                    class="h-1 flex-1 rounded-full transition-all"
                    :class="passwordStrength >= i ? strengthColor : 'bg-gray-200'"
                  />
                </div>

                <p class="mt-1 text-xs" :class="strengthTextColor">
                  {{ strengthLabel }}
                </p>
              </div>
            </div>

            <!-- Confirm Password -->
            <div>
              <label for="register-confirm-password" class="mb-1.5 block text-sm font-medium text-gray-700">
                Confirm password
              </label>

              <div class="relative">
                <Lock
                  class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
                  aria-hidden="true"
                />

                <input
                  id="register-confirm-password"
                  v-model="form.confirmPassword"
                  :type="showConfirm ? 'text' : 'password'"
                  placeholder="Repeat your password"
                  required
                  autocomplete="new-password"
                  class="w-full rounded-xl border border-gray-200 bg-white py-3.5 pl-10 pr-12 text-base text-gray-800 placeholder-gray-400 transition-all focus:border-transparent focus:outline-none focus:ring-2 focus:ring-[#A8D5BA]"
                  :class="{ 'border-red-300 focus:ring-red-300': form.confirmPassword && !passwordsMatch }"
                  aria-describedby="confirm-password-error"
                />

                <button
                  type="button"
                  @click="showConfirm = !showConfirm"
                  class="absolute right-2 top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-lg text-gray-400 transition-colors hover:bg-gray-50 hover:text-gray-600"
                  :aria-label="showConfirm ? 'Hide confirm password' : 'Show confirm password'"
                  :aria-pressed="showConfirm"
                >
                  <Eye v-if="!showConfirm" class="h-4 w-4" aria-hidden="true" />
                  <EyeOff v-else class="h-4 w-4" aria-hidden="true" />
                </button>
              </div>

              <p
                v-if="form.confirmPassword && !passwordsMatch"
                id="confirm-password-error"
                class="mt-1 text-xs text-red-500"
              >
                Passwords don't match
              </p>
            </div>

            <!-- Terms -->
            <div class="flex items-start gap-3">
              <input
                id="terms"
                v-model="form.acceptTerms"
                type="checkbox"
                required
                class="mt-0.5 h-4 w-4 rounded border-gray-300 accent-[#A8D5BA]"
              />

              <label for="terms" class="text-sm leading-relaxed text-gray-600">
                I agree to the

                <button
                  type="button"
                  @click="openPolicyModal('terms')"
                  class="font-medium text-[#2C5F2D] hover:underline"
                >
                  Terms of Service
                </button>

                and

                <button
                  type="button"
                  @click="openPolicyModal('privacy')"
                  class="font-medium text-[#2C5F2D] hover:underline"
                >
                  Privacy Policy
                </button>
              </label>
            </div>

            <button
              type="submit"
              :disabled="isLoading || !canSubmit"
              class="flex w-full items-center justify-center gap-2 rounded-xl bg-[#A8D5BA] py-3.5 font-semibold text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] disabled:cursor-not-allowed disabled:opacity-60"
              :aria-busy="isLoading"
            >
              <Loader2 v-if="isLoading" class="h-4 w-4 animate-spin" aria-hidden="true" />
              <span>{{ isLoading ? 'Creating account...' : 'Create account' }}</span>
            </button>
          </form>

          <p class="mt-6 text-center text-sm text-gray-600 sm:text-base">
            Already have an account?
            <router-link
              to="/login"
              class="ml-1 font-medium text-[#2C5F2D] hover:underline"
            >
              Sign in
            </router-link>
          </p>

          <div class="mt-4 text-center">
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

    <!-- Policy Modal -->
    <div
      v-if="showPolicyModal"
      class="fixed inset-0 z-[100] flex items-end justify-center bg-black/40 px-4 py-4 sm:items-center"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="policyModalTitleId"
      @click.self="closePolicyModal"
    >
      <div class="w-full max-w-2xl overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-2xl">
        <div class="flex items-start justify-between gap-4 border-b border-gray-100 px-5 py-4 sm:px-6 sm:py-5">
          <div>
            <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D]">
              LittleHelp
            </p>

            <h2
              :id="policyModalTitleId"
              class="text-xl font-semibold text-[#2C5F2D] sm:text-2xl"
            >
              {{ activePolicyTitle }}
            </h2>
          </div>

          <button
            type="button"
            @click="closePolicyModal"
            class="flex h-10 w-10 items-center justify-center rounded-full text-2xl leading-none text-gray-500 transition-colors hover:bg-gray-100 hover:text-gray-700"
            aria-label="Close policy modal"
          >
            ×
          </button>
        </div>

        <div class="max-h-[62vh] overflow-y-auto px-5 py-4 sm:max-h-[65vh] sm:px-6 sm:py-5">
          <div
            v-if="activePolicy === 'terms'"
            class="space-y-4 text-sm leading-relaxed text-gray-600"
          >
            <p>
              By creating an account, you agree to use LittleHelp for educational and personal lunchbox planning support.
            </p>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                1. Educational purpose
              </h3>
              <p>
                LittleHelp provides general food and nutrition guidance. It does not replace professional medical, dietetic, or allergy advice.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                2. User responsibility
              </h3>
              <p>
                Parents and caregivers are responsible for checking ingredients, allergens, food labels, and suitability before preparing or serving meals.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                3. Account use
              </h3>
              <p>
                You should keep your login details secure and use the platform in a reasonable and lawful way.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                4. Data accuracy
              </h3>
              <p>
                We aim to provide helpful guidance, but food data, labels, and nutrition information may change over time.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                5. No emergency or medical use
              </h3>
              <p>
                LittleHelp should not be used for urgent medical decisions. For health, allergy, or diet concerns, seek professional advice.
              </p>
            </div>
          </div>

          <div
            v-else
            class="space-y-4 text-sm leading-relaxed text-gray-600"
          >
            <p>
              LittleHelp uses limited information to support personalised lunchbox planning.
            </p>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                1. Information we use
              </h3>
              <p>
                We may use account details and child profile information such as nickname, age band, allergies, dietary needs, and nutrition focus.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                2. Why we use it
              </h3>
              <p>
                This information is used to generate more relevant lunchbox suggestions, serving guidance, and weekly plans.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                3. Privacy-conscious design
              </h3>
              <p>
                LittleHelp is designed to work with minimal personal details. Families can use nicknames instead of full child names.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                4. Food safety and allergies
              </h3>
              <p>
                Allergy and dietary information should always be checked carefully by parents or caregivers before preparing food.
              </p>
            </div>

            <div>
              <h3 class="mb-1 font-semibold text-gray-800">
                5. Data source limitations
              </h3>
              <p>
                Public food and nutrition datasets may be updated by their original providers, and product information may change over time.
              </p>
            </div>
          </div>
        </div>

        <div class="flex justify-end border-t border-gray-100 px-5 py-4 sm:px-6">
          <button
            type="button"
            @click="closePolicyModal"
            class="w-full rounded-xl bg-[#A8D5BA] px-6 py-3 font-semibold text-[#2C5F2D] transition-colors hover:bg-[#8FC2A4] sm:w-auto sm:py-2"
          >
            I understand
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import {
  User,
  Lock,
  Eye,
  EyeOff,
  AlertCircle,
  CheckCircle,
  Loader2,
  ArrowLeft,
} from 'lucide-vue-next';
import { useAuthStore } from '../stores/auth';
import logoUrl from '../assets/littlehelp-logo.jpg';

const router = useRouter();
const authStore = useAuthStore();

const steps = [
  'Create your free account',
  "Add your children's profiles",
  'Get personalised meal plans instantly',
];

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
});

const showPassword = ref(false);
const showConfirm = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const showPolicyModal = ref(false);
const activePolicy = ref('terms');

const activePolicyTitle = computed(() => {
  return activePolicy.value === 'terms'
    ? 'Terms of Service'
    : 'Privacy Policy';
});

const policyModalTitleId = computed(() => {
  return activePolicy.value === 'terms'
    ? 'terms-modal-title'
    : 'privacy-modal-title';
});

const openPolicyModal = (type) => {
  activePolicy.value = type;
  showPolicyModal.value = true;
};

const closePolicyModal = () => {
  showPolicyModal.value = false;
};

const passwordsMatch = computed(() =>
  !form.confirmPassword || form.password === form.confirmPassword
);

const canSubmit = computed(() => {
  return (
    form.username.trim().length >= 3 &&
    form.password.length >= 8 &&
    form.confirmPassword.length > 0 &&
    passwordsMatch.value &&
    form.acceptTerms
  );
});

const passwordStrength = computed(() => {
  const p = form.password;

  if (!p) return 0;

  let score = 0;

  if (p.length >= 8) score++;
  if (/[A-Z]/.test(p)) score++;
  if (/[0-9]/.test(p)) score++;
  if (/[^A-Za-z0-9]/.test(p)) score++;

  return score;
});

const strengthColor = computed(() =>
  ['bg-red-400', 'bg-orange-400', 'bg-yellow-400', 'bg-[#A8D5BA]'][passwordStrength.value - 1] || 'bg-gray-200'
);

const strengthTextColor = computed(() =>
  ['text-red-500', 'text-orange-500', 'text-yellow-600', 'text-[#2C5F2D]'][passwordStrength.value - 1] || 'text-gray-400'
);

const strengthLabel = computed(() =>
  ['Weak', 'Fair', 'Good', 'Strong'][passwordStrength.value - 1] || ''
);

const handleRegister = async () => {
  if (!canSubmit.value || isLoading.value) return;

  errorMessage.value = '';
  successMessage.value = '';
  isLoading.value = true;

  try {
    await authStore.register({
      username: form.username.trim(),
      password: form.password,
    });

    successMessage.value = 'Account created! Redirecting...';
    setTimeout(() => router.push('/'), 1500);
  } catch (err) {
    errorMessage.value = err.message || 'Something went wrong. Please try again.';
  } finally {
    isLoading.value = false;
  }
};
</script>