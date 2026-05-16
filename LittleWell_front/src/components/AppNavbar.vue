<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm"
    aria-label="Main navigation"
  >
    <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-[1440px]">
      <div class="flex items-center justify-between h-16 lg:h-20 gap-4">
        <!-- Logo -->
        <button
          class="flex items-center shrink-0"
          aria-label="LittleHelp home"
          type="button"
          @click="goHome"
        >
          <img
            :src="littleHelpLogo"
            alt="LittleHelp logo"
            class="h-10 lg:h-12 w-auto object-contain"
          />
        </button>

        <!-- Desktop Navigation Links -->
        <div class="hidden lg:flex items-center justify-end gap-2 flex-1" role="navigation">
          <button
            @click="goProtected('/weekly-plan')"
            :class="['nav-link', { 'nav-link-active': isRouteActive('/weekly-plan') }]"
            :aria-current="isRouteActive('/weekly-plan') ? 'page' : undefined"
            type="button"
          >
            Weekly Plan
          </button>

          <button
            @click="goProtected('/my-plans')"
            :class="['nav-link', { 'nav-link-active': isRouteActive('/my-plans') }]"
            :aria-current="isRouteActive('/my-plans') ? 'page' : undefined"
            type="button"
          >
            My Plans
          </button>

          <button
            @click="router.push('/knowledge-hub-prototype')"
            :class="['nav-link', { 'nav-link-active': isRouteActive('/knowledge-hub-prototype') }]"
            :aria-current="isRouteActive('/knowledge-hub-prototype') ? 'page' : undefined"
            type="button"
          >
            Knowledge Hub
          </button>

          <button
            @click="router.push('/about')"
            :class="['nav-link', { 'nav-link-active': isRouteActive('/about') }]"
            :aria-current="isRouteActive('/about') ? 'page' : undefined"
            type="button"
          >
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
              :class="[
                'nav-link nav-signin-link',
                { 'nav-link-active': isRouteActive('/login') },
              ]"
              :aria-current="isRouteActive('/login') ? 'page' : undefined"
              type="button"
            >
              Sign in
            </button>

            <button
              @click="router.push('/register')"
              :class="[
                'nav-primary-button',
                { 'nav-primary-button-active': isRouteActive('/register') },
              ]"
              :aria-current="isRouteActive('/register') ? 'page' : undefined"
              type="button"
            >
              Create account
            </button>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <button
          class="lg:hidden inline-flex items-center justify-center w-10 h-10 rounded-lg text-[#2C5F2D] hover:bg-[#A8D5BA]/10 transition-colors"
          type="button"
          aria-label="Open main menu"
          :aria-expanded="showMobileMenu"
          aria-controls="mobile-menu"
          @click="toggleMobileMenu"
        >
          <Menu v-if="!showMobileMenu" class="w-6 h-6" aria-hidden="true" />
          <X v-else class="w-6 h-6" aria-hidden="true" />
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div
      v-if="showMobileMenu"
      id="mobile-menu"
      class="lg:hidden border-t border-gray-200 bg-white shadow-lg"
    >
      <div class="px-4 py-4 space-y-2">
        <button
          @click="handleMobileAction(() => goProtected('/weekly-plan'))"
          :class="['mobile-nav-link', { 'mobile-nav-link-active': isRouteActive('/weekly-plan') }]"
          :aria-current="isRouteActive('/weekly-plan') ? 'page' : undefined"
          type="button"
        >
          Weekly Plan
        </button>

        <button
          @click="handleMobileAction(() => goProtected('/my-plans'))"
          :class="['mobile-nav-link', { 'mobile-nav-link-active': isRouteActive('/my-plans') }]"
          :aria-current="isRouteActive('/my-plans') ? 'page' : undefined"
          type="button"
        >
          My Plans
        </button>

        <button
          @click="handleMobileAction(() => router.push('/knowledge-hub-prototype'))"
          :class="['mobile-nav-link', { 'mobile-nav-link-active': isRouteActive('/knowledge-hub-prototype') }]"
          :aria-current="isRouteActive('/knowledge-hub-prototype') ? 'page' : undefined"
          type="button"
        >
          Knowledge Hub
        </button>

        <button
          @click="handleMobileAction(() => router.push('/about'))"
          :class="['mobile-nav-link', { 'mobile-nav-link-active': isRouteActive('/about') }]"
          :aria-current="isRouteActive('/about') ? 'page' : undefined"
          type="button"
        >
          About Us
        </button>

        <div class="pt-3 mt-3 border-t border-gray-200">
          <p class="px-3 pb-2 text-sm font-semibold text-[#2C5F2D]">
            Accessibility
          </p>

          <button
            v-if="isHomePage"
            @click="handleMobileAction(openHomeGuide)"
            class="mobile-nav-link"
            type="button"
          >
            Interactive Guide
          </button>

          <button
            @click="toggleLargeTextMode"
            :aria-pressed="largeTextMode"
            :class="[
              'mobile-nav-link',
              largeTextMode ? 'bg-[#F8F5EC] font-semibold' : '',
            ]"
            type="button"
          >
            Large Text Mode
            <span v-if="largeTextMode" class="ml-2 text-xs">(on)</span>
          </button>

          <button
            @click="toggleHighContrastMode"
            :aria-pressed="highContrastMode"
            :class="[
              'mobile-nav-link',
              highContrastMode ? 'bg-[#F8F5EC] font-semibold' : '',
            ]"
            type="button"
          >
            High Contrast Mode
            <span v-if="highContrastMode" class="ml-2 text-xs">(on)</span>
          </button>
        </div>

        <div class="pt-3 mt-3 border-t border-gray-200">
          <template v-if="isLoggedIn">
            <p class="px-3 py-2 text-sm text-muted-foreground">
              Hi, {{ username }}
            </p>

            <button
              @click="handleMobileAction(handleLogout)"
              class="mobile-outline-button"
              type="button"
            >
              Logout
            </button>
          </template>

          <template v-else>
            <button
              @click="handleMobileAction(() => router.push('/login'))"
              :class="[
                'mobile-nav-link underline underline-offset-4',
                { 'mobile-nav-link-active': isRouteActive('/login') },
              ]"
              :aria-current="isRouteActive('/login') ? 'page' : undefined"
              type="button"
            >
              Sign in
            </button>

            <button
              @click="handleMobileAction(() => router.push('/register'))"
              :class="[
                'mobile-primary-button',
                { 'mobile-primary-button-active': isRouteActive('/register') },
              ]"
              :aria-current="isRouteActive('/register') ? 'page' : undefined"
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
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ChevronDown, Menu, X } from 'lucide-vue-next';
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

const showMobileMenu = ref(false);

const isLoggedIn = computed(() => authStore.isAuthenticated);
const username = computed(() => authStore.user?.username || 'User');

const currentPath = computed(() => router.currentRoute.value.path);
const isHomePage = computed(() => currentPath.value === '/');

const isRouteActive = (path) => {
  if (path === '/') {
    return currentPath.value === '/';
  }

  return currentPath.value === path || currentPath.value.startsWith(`${path}/`);
};

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

const closeMobileMenu = () => {
  showMobileMenu.value = false;
};

const handleMobileAction = (action) => {
  closeMobileMenu();
  action();
};

const goHome = () => {
  closeMobileMenu();
  router.push('/');
};

const openHomeGuide = () => {
  window.dispatchEvent(new CustomEvent('open-home-user-guide'));
  showAccessibilityMenu.value = false;
  closeMobileMenu();
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
  position: relative;
  color: #2C5F2D;
  padding: 0.55rem 0.85rem;
  border-radius: 0.65rem;
  font-size: 0.92rem;
  line-height: 1.2;
  white-space: nowrap;
  transition:
    background-color 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(168, 213, 186, 0.12);
}

.nav-link-active {
  background-color: rgba(168, 213, 186, 0.22);
  color: #214B24;
  font-weight: 700;
  box-shadow: inset 0 0 0 1px rgba(44, 95, 45, 0.12);
}

.nav-link-active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0.25rem;
  width: 1.25rem;
  height: 0.18rem;
  border-radius: 999px;
  background-color: #2C5F2D;
  transform: translateX(-50%);
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
  transition:
    background-color 0.2s ease,
    box-shadow 0.2s ease;
}

.nav-primary-button:hover {
  background-color: #8FC2A4;
}

.nav-primary-button-active {
  background-color: #8FC2A4;
  box-shadow: 0 0 0 2px rgba(44, 95, 45, 0.18);
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

.mobile-nav-link {
  width: 100%;
  display: block;
  text-align: left;
  color: #2C5F2D;
  padding: 0.8rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.95rem;
  line-height: 1.2;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}

.mobile-nav-link:hover {
  background-color: rgba(168, 213, 186, 0.12);
}

.mobile-nav-link-active {
  background-color: rgba(168, 213, 186, 0.22);
  color: #214B24;
  font-weight: 700;
  border-left: 4px solid #2C5F2D;
  padding-left: 0.95rem;
}

.mobile-primary-button {
  width: 100%;
  display: block;
  text-align: center;
  background-color: #A8D5BA;
  color: #2C5F2D;
  padding: 0.85rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

.mobile-primary-button:hover {
  background-color: #8FC2A4;
}

.mobile-primary-button-active {
  background-color: #8FC2A4;
  box-shadow: 0 0 0 2px rgba(44, 95, 45, 0.18);
}

.mobile-outline-button {
  width: 100%;
  display: block;
  text-align: center;
  background-color: white;
  border: 1px solid #A8D5BA;
  color: #2C5F2D;
  padding: 0.85rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

.mobile-outline-button:hover {
  background-color: rgba(168, 213, 186, 0.12);
}
</style>