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
        <div class="hidden lg:flex flex-1 items-center justify-end gap-2">
          <div
            ref="navLinksContainerRef"
            class="relative flex items-center gap-2"
            role="navigation"
          >
            <div
              class="nav-underline-indicator pointer-events-none absolute bottom-1 left-0 h-[2px] rounded-full bg-[#2C5F2D] transition-[transform,width,opacity] duration-300 ease-out"
              :style="navUnderlineStyle"
              aria-hidden="true"
            />

            <button
              v-for="item in desktopNavItems"
              :key="item.path"
              :ref="(el) => setNavLinkRef(item.path, el)"
              type="button"
              :class="['nav-link', { 'nav-link-active': isRouteActive(item.path) }]"
              :aria-current="isRouteActive(item.path) ? 'page' : undefined"
              @click="item.action()"
            >
              {{ item.label }}
            </button>
          </div>

          <!-- Desktop Accessibility Dropdown -->
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

        <!-- Mobile Actions -->
        <div class="lg:hidden flex items-center gap-2">
          <!-- Mobile Accessibility Button -->
          <div ref="mobileAccessibilityMenuRef" class="relative">
            <button
              type="button"
              class="mobile-accessibility-button"
              :aria-expanded="showMobileAccessibilityMenu"
              aria-haspopup="true"
              aria-controls="mobile-accessibility-popover"
              @click="toggleMobileAccessibilityMenu"
            >
              <span class="hidden xs:inline">Accessibility</span>
              <span class="xs:hidden">Access</span>
              <ChevronDown
                :class="[
                  'w-3.5 h-3.5 transition-transform duration-200',
                  showMobileAccessibilityMenu ? 'rotate-180' : 'rotate-0',
                ]"
                aria-hidden="true"
              />
            </button>

            <div
              v-if="showMobileAccessibilityMenu"
              id="mobile-accessibility-popover"
              class="absolute right-0 mt-2 w-64 rounded-2xl border border-[#D6E7DC] bg-white shadow-xl p-4 z-50"
            >
              <p class="text-sm font-semibold text-[#2C5F2D]">
                Accessibility
              </p>

              <div class="h-px bg-[#E5E7EB] my-3" aria-hidden="true"></div>

              <button
                v-if="isHomePage"
                type="button"
                @click="handleMobileAccessibilityAction(openHomeGuide)"
                class="accessibility-popover-button"
              >
                Interactive Guide
              </button>

              <button
                type="button"
                @click="toggleLargeTextMode"
                :aria-pressed="largeTextMode"
                :class="[
                  'accessibility-popover-button',
                  isHomePage ? 'mt-2' : '',
                  largeTextMode ? 'bg-[#F8F5EC] font-semibold' : '',
                ]"
              >
                Large Text Mode
                <span v-if="largeTextMode" class="ml-2 text-xs">(on)</span>
              </button>

              <button
                type="button"
                @click="toggleHighContrastMode"
                :aria-pressed="highContrastMode"
                :class="[
                  'accessibility-popover-button mt-2',
                  highContrastMode ? 'bg-[#F8F5EC] font-semibold' : '',
                ]"
              >
                High Contrast Mode
                <span v-if="highContrastMode" class="ml-2 text-xs">(on)</span>
              </button>
            </div>
          </div>

          <!-- Mobile Menu Button -->
          <button
            class="inline-flex items-center justify-center w-10 h-10 rounded-lg text-[#2C5F2D] hover:bg-[#A8D5BA]/10 transition-colors"
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

        <!-- Temporary Food Analyser entry -->
        <button
          @click="handleMobileAction(() => router.push('/food-analyser'))"
          :class="['mobile-nav-link', { 'mobile-nav-link-active': isRouteActive('/food-analyser') }]"
          :aria-current="isRouteActive('/food-analyser') ? 'page' : undefined"
          type="button"
        >
          Food Analyser
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
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue';
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
const showMobileAccessibilityMenu = ref(false);
const mobileAccessibilityMenuRef = ref(null);

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

const navLinksContainerRef = ref(null);
const navLinkRefs = ref({});
const navUnderlineStyle = ref({
  transform: 'translateX(0px)',
  width: '0px',
  opacity: '0',
});

let navResizeObserver = null;
let underlineRafId = null;

const setNavLinkRef = (path, el) => {
  if (el) {
    navLinkRefs.value[path] = el;
    return;
  }

  delete navLinkRefs.value[path];
};

const resetNavUnderline = () => {
  navUnderlineStyle.value = {
    transform: 'translateX(0px)',
    width: '0px',
    opacity: '0',
  };
};

const updateNavUnderline = () => {
  if (underlineRafId) {
    cancelAnimationFrame(underlineRafId);
  }

  underlineRafId = requestAnimationFrame(() => {
    const container = navLinksContainerRef.value;

    if (!container) {
      resetNavUnderline();
      return;
    }

    const activeItem = desktopNavItems.find((item) => isRouteActive(item.path));

    if (!activeItem) {
      resetNavUnderline();
      return;
    }

    const linkEl = navLinkRefs.value[activeItem.path];

    if (!linkEl) {
      resetNavUnderline();
      return;
    }

    const containerRect = container.getBoundingClientRect();
    const linkRect = linkEl.getBoundingClientRect();

    const underlineInset = 12;
    const left = linkRect.left - containerRect.left + underlineInset;
    const width = Math.max(24, linkRect.width - underlineInset * 2);

    navUnderlineStyle.value = {
      transform: `translateX(${left}px)`,
      width: `${width}px`,
      opacity: '1',
    };
  });
};

const updateNavUnderlineAfterLayout = async () => {
  await nextTick();

  requestAnimationFrame(() => {
    updateNavUnderline();

    requestAnimationFrame(() => {
      updateNavUnderline();
    });
  });
};

const setupNavResizeObserver = () => {
  if (!('ResizeObserver' in window)) {
    return;
  }

  if (navResizeObserver) {
    navResizeObserver.disconnect();
  }

  navResizeObserver = new ResizeObserver(() => {
    updateNavUnderlineAfterLayout();
  });

  if (navLinksContainerRef.value) {
    navResizeObserver.observe(navLinksContainerRef.value);
  }

  Object.values(navLinkRefs.value).forEach((el) => {
    if (el) {
      navResizeObserver.observe(el);
    }
  });
};

watch(currentPath, () => {
  updateNavUnderlineAfterLayout();
});

watch(
  [largeTextMode, highContrastMode, isLoggedIn, username],
  async () => {
    await updateNavUnderlineAfterLayout();
    setupNavResizeObserver();
  }
);

onMounted(() => {
  updateNavUnderlineAfterLayout();
  setupNavResizeObserver();

  window.addEventListener('resize', updateNavUnderlineAfterLayout);

  if (document.fonts?.ready) {
    document.fonts.ready.then(() => {
      updateNavUnderlineAfterLayout();
    });
  }
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateNavUnderlineAfterLayout);

  if (navResizeObserver) {
    navResizeObserver.disconnect();
    navResizeObserver = null;
  }

  if (underlineRafId) {
    cancelAnimationFrame(underlineRafId);
    underlineRafId = null;
  }
});

const closeMobileMenu = () => {
  showMobileMenu.value = false;
};

const closeMobileAccessibilityMenu = () => {
  showMobileAccessibilityMenu.value = false;
};

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;

  if (showMobileMenu.value) {
    closeMobileAccessibilityMenu();
  }
};

const toggleMobileAccessibilityMenu = () => {
  showMobileAccessibilityMenu.value = !showMobileAccessibilityMenu.value;

  if (showMobileAccessibilityMenu.value) {
    closeMobileMenu();
  }
};

const handleMobileAction = (action) => {
  closeMobileMenu();
  closeMobileAccessibilityMenu();
  action();
};

const handleMobileAccessibilityAction = (action) => {
  closeMobileAccessibilityMenu();
  closeMobileMenu();
  action();
};

const goHome = () => {
  closeMobileMenu();
  closeMobileAccessibilityMenu();
  router.push('/');
};

const openHomeGuide = () => {
  window.dispatchEvent(new CustomEvent('open-home-user-guide'));
  showAccessibilityMenu.value = false;
  closeMobileMenu();
  closeMobileAccessibilityMenu();
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

const desktopNavItems = [
  {
    path: '/weekly-plan',
    label: 'Weekly Plan',
    action: () => goProtected('/weekly-plan'),
  },
  {
    path: '/my-plans',
    label: 'My Plans',
    action: () => goProtected('/my-plans'),
  },
  {
    path: '/food-analyser',
    label: 'Food Analyser',
    action: () => router.push('/food-analyser'),
  },
  {
    path: '/knowledge-hub-prototype',
    label: 'Knowledge Hub',
    action: () => router.push('/knowledge-hub-prototype'),
  },
  {
    path: '/about',
    label: 'About Us',
    action: () => router.push('/about'),
  },
];

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
  color: #214B24;
  font-weight: 600;
}

.nav-signin-link::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0.25rem;
  width: 2.5rem;
  height: 2px;
  border-radius: 999px;
  background-color: #2C5F2D;
  transform: translateX(-50%);
  pointer-events: none;
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

.mobile-accessibility-button {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  color: #2C5F2D;
  padding: 0.55rem 0.7rem;
  border-radius: 0.65rem;
  font-size: 0.82rem;
  line-height: 1.2;
  font-weight: 600;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.mobile-accessibility-button:hover {
  background-color: rgba(168, 213, 186, 0.12);
}

.accessibility-popover-button {
  width: 100%;
  display: block;
  text-align: left;
  color: #2C5F2D;
  padding: 0.65rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.9rem;
  line-height: 1.2;
  transition: background-color 0.2s ease;
}

.accessibility-popover-button:hover {
  background-color: #F8F5EC;
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

@media (max-width: 360px) {
  .mobile-accessibility-button {
    padding-left: 0.55rem;
    padding-right: 0.55rem;
    font-size: 0.78rem;
  }
}
</style>