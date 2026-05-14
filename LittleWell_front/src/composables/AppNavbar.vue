<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm"
    aria-label="Main navigation"
  >
    <div class="mx-auto px-8 max-w-[1440px]">
      <div class="flex items-center justify-between h-20 gap-8">
        <!-- Logo -->
        <button
          class="flex items-center shrink-0"
          aria-label="LittleHelp home"
          type="button"
          @click="router.push('/')"
        >
          <img
            :src="littleHelpLogo"
            alt="LittleHelp logo"
            class="h-12 w-auto object-contain"
          />
        </button>

        <!-- Desktop Navigation Links -->
        <div class="flex items-center justify-end gap-2 flex-1" role="navigation">
          <button @click="goHomeSection('child-profiles')" class="nav-link" type="button">
            Lunchbox Plan
          </button>

          <button @click="goProtected('/weekly-plan')" class="nav-link" type="button">
            Weekly Plan
          </button>

          <button @click="goProtected('/my-plans')" class="nav-link" type="button">
            My Plans
          </button>

          <button
            @click="router.push('/knowledge-hub-prototype')"
            class="nav-link"
            type="button"
          >
            Knowledge Hub
          </button>

          <button @click="router.push('/about')" class="nav-link" type="button">
            About Us
          </button>

          <!-- Accessibility Dropdown -->
          <div ref="accessibilityMenuRef" class="relative">
            <button
              @click="toggleAccessibilityMenu"
              class="nav-link inline-flex items-center gap-1"
              type="button"
              :aria-expanded="showAccessibilityMenu"
              aria-haspopup="true"
              aria-controls="accessibility-menu"
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
              id="accessibility-menu"
              role="menu"
              class="absolute right-0 mt-2 w-72 rounded-2xl border border-[#D6E7DC] bg-white shadow-xl p-4 z-50"
            >
              <p class="text-sm font-semibold text-[#2C5F2D]">
                Accessibility
              </p>

              <div class="h-px bg-[#E5E7EB] my-3" aria-hidden="true"></div>

              <!-- Only show this on HomePage -->
              <button
                v-if="isHomePage"
                type="button"
                role="menuitem"
                @click="openHomeGuide"
                class="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors text-[#2C5F2D] hover:bg-[#F8F5EC]"
              >
                Interactive Guide
              </button>

              <button
                type="button"
                role="menuitem"
                @click="toggleLargeTextMode"
                :aria-pressed="largeTextMode"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors',
                  isHomePage ? 'mt-2' : '',
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
            </div>
          </div>

          <!-- Auth Buttons -->
          <template v-if="isLoggedIn">
            <span
              class="text-sm text-muted-foreground px-2 whitespace-nowrap"
              aria-live="polite"
            >
              Hi, {{ username }}
            </span>

            <button @click="handleLogout" class="nav-outline-button" type="button">
              Logout
            </button>
          </template>

          <template v-else>
            <button
              @click="router.push('/login')"
              class="nav-link nav-signin-link"
              type="button"
            >
              Sign in
            </button>

            <button
              @click="router.push('/register')"
              class="nav-primary-button"
              type="button"
            >
              Create account
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { ChevronDown } from 'lucide-vue-next';
import { useAuthStore } from '../stores/auth';
import { useAccessibility } from '../composables/useAccessibility';
import littleHelpLogo from '../assets/littlehelp-logo.jpg';

const router = useRouter();
const authStore = useAuthStore();

const {
  largeTextMode,
  highContrastMode,
  showAccessibilityMenu,
  accessibilityMenuRef,
  toggleLargeTextMode,
  toggleHighContrastMode,
  toggleAccessibilityMenu,
} = useAccessibility();

const isLoggedIn = computed(() => authStore.isAuthenticated);
const username = computed(() => authStore.user?.username || 'User');

const isHomePage = computed(() => router.currentRoute.value.path === '/');

const openHomeGuide = () => {
  window.dispatchEvent(new CustomEvent('open-home-user-guide'));
  showAccessibilityMenu.value = false;
};

const goProtected = (path) => {
  if (!isLoggedIn.value) {
    router.push({
      path: '/login',
      query: { redirect: path },
    });
    return;
  }

  router.push(path);
};

const goHomeSection = (sectionId) => {
  if (router.currentRoute.value.path === '/') {
    const section = document.getElementById(sectionId);
    section?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    return;
  }

  router.push({
    path: '/',
    hash: `#${sectionId}`,
  });
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}

.nav-link {
  color: #2C5F2D;
  padding: 0.55rem 0.85rem;
  border-radius: 0.65rem;
  font-size: 0.92rem;
  line-height: 1.2;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(168, 213, 186, 0.12);
}

.nav-signin-link {
  text-decoration: underline;
  text-decoration-color: #2C5F2D;
  text-underline-offset: 3px;
}

.nav-primary-button {
  background-color: #A8D5BA;
  color: #2C5F2D;
  padding: 0.65rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.92rem;
  font-weight: 600;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.nav-primary-button:hover {
  background-color: #8FC2A4;
}

.nav-outline-button {
  background-color: white;
  border: 1px solid #A8D5BA;
  color: #2C5F2D;
  padding: 0.6rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.92rem;
  font-weight: 600;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.nav-outline-button:hover {
  background-color: rgba(168, 213, 186, 0.12);
}
</style>