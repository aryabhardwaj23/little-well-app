<template>
  <footer
    class="relative bg-[#F4F1EA] border-t border-[#D8D2C4] shadow-[0_-10px_28px_rgba(44,95,45,0.07)]"
  >
    <div class="h-1 bg-gradient-to-r from-[#A8D5BA] via-[#F7B267]/70 to-[#CDE7F0]"></div>

    <div class="container mx-auto px-4 sm:px-6 max-w-6xl py-10 sm:py-14">
      <div
        class="grid gap-10 lg:grid-cols-[minmax(0,1.3fr)_auto_minmax(0,1.1fr)_auto_minmax(0,0.9fr)] lg:items-start lg:gap-x-0"
      >
        <!-- Brand -->
        <section aria-label="LittleHelp summary" class="lg:pr-8">
          <button
            type="button"
            @click="goHome"
            class="inline-flex items-center gap-3 text-left group"
            aria-label="Go to LittleHelp home page"
          >
            <div
              class="w-11 h-11 rounded-2xl bg-white border border-[#D8D2C4] flex items-center justify-center shadow-sm group-hover:border-[#A8D5BA] transition-colors"
              aria-hidden="true"
            >
              <span class="text-xl">🥗</span>
            </div>

            <div>
              <p class="text-2xl font-semibold text-[#2C5F2D] leading-tight">
                LittleHelp
              </p>
              <p class="text-xs text-muted-foreground mt-0.5">
                Smarter lunchbox planning
              </p>
            </div>
          </button>

          <p class="mt-5 text-muted-foreground max-w-md leading-relaxed text-sm sm:text-base">
            Helping families create practical, balanced, and child-friendly
            lunchbox plans through science-backed nutrition guidance.
          </p>

          <div class="mt-5 max-w-md space-y-5">
            <div>
              <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D]">
                Educational guidance
              </p>
              <p class="text-xs leading-relaxed text-muted-foreground">
                LittleHelp provides educational food guidance only and is not a replacement
                for professional medical or dietetic advice.
              </p>
            </div>

            <div>
              <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-[#2C5F2D]">
                Data & attribution
              </p>
              <p class="text-xs leading-relaxed text-muted-foreground">
                Built with public food and nutrition references including OpenFoodFacts,
                AUSNUT, Australian Dietary Guidelines, and seasonal food resources.
              </p>
              <button
                type="button"
                @click="goTo('/about#data-sources')"
                class="group mt-2 inline-flex items-center gap-1.5 text-xs font-semibold text-[#2C5F2D]"
              >
                <span aria-hidden="true" class="text-[0.65rem] leading-none">→</span>
                <span class="underline underline-offset-[3px] decoration-[#2C5F2D]/70 group-hover:decoration-[#2C5F2D]">
                  View data sources
                </span>
              </button>
            </div>
          </div>
        </section>

        <div
          class="footer-column-divider hidden lg:flex lg:items-start lg:justify-center lg:px-8"
          aria-hidden="true"
        >
          <span class="mt-[4.25rem] h-44 w-px bg-[#6B7280]/70" />
        </div>

        <!-- CTA -->
        <section aria-label="Begin with LittleHelp" class="lg:px-8 lg:pt-[4.25rem]">
          <div>
            <p class="footer-heading mb-3">
              Begin with LittleHelp
            </p>

            <p class="text-sm leading-relaxed text-muted-foreground">
              Set up a child profile to receive simple, personalised lunchbox guidance
              for your family.
            </p>

            <div class="mt-5">
              <button
                type="button"
                @click="goProtected('/child-info')"
                class="footer-primary-button"
              >
                Start Planning
              </button>
            </div>
          </div>
        </section>

        <div
          class="footer-column-divider hidden lg:flex lg:items-start lg:justify-center lg:px-8"
          aria-hidden="true"
        >
          <span class="mt-[4.25rem] h-44 w-px bg-[#6B7280]/70" />
        </div>

        <!-- Navigation -->
        <nav aria-label="Footer navigation" class="lg:pl-0 lg:pt-[4.25rem]">
          <p class="footer-heading">
            Explore
          </p>

          <div class="mt-3.5 grid grid-cols-2 gap-x-6 gap-y-1 text-sm sm:grid-cols-1 sm:gap-y-1">
            <button type="button" @click="goHome" class="footer-link">
              Home
            </button>

            <button type="button" @click="goProtected('/weekly-plan')" class="footer-link">
              Weekly Plan
            </button>

            <button type="button" @click="goProtected('/my-plans')" class="footer-link">
              My Plans
            </button>

            <button type="button" @click="goTo('/knowledge-hub-prototype')" class="footer-link">
              Knowledge Hub
            </button>

            <button type="button" @click="goTo('/about')" class="footer-link">
              About Us
            </button>
          </div>
        </nav>
      </div>

      <div
        class="mt-10 pt-6 border-t border-[#D8D2C4] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-muted-foreground"
      >
        <p>© 2026 LittleHelp. All rights reserved.</p>

        <button
          type="button"
          @click="scrollToTop"
          class="inline-flex items-center gap-1 text-[#2C5F2D] hover:underline"
        >
          Back to top
          <span aria-hidden="true">↑</span>
        </button>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const isLoggedIn = computed(() => authStore.isAuthenticated);

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
};

const scrollToHash = async (hash) => {
  await nextTick();

  setTimeout(() => {
    const target = document.querySelector(hash);

    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
  }, 120);
};

const goTo = async (path) => {
  const [routePath, hashPart] = path.split('#');
  const hash = hashPart ? `#${hashPart}` : '';

  if (router.currentRoute.value.path !== routePath || router.currentRoute.value.hash !== hash) {
    await router.push({
      path: routePath,
      hash,
    });
  }

  if (hash) {
    await scrollToHash(hash);
    return;
  }

  scrollToTop();
};

const goHome = async () => {
  if (router.currentRoute.value.path !== '/') {
    await router.push('/');
  }

  scrollToTop();
};

const goProtected = async (path) => {
  if (!isLoggedIn.value) {
    await router.push({
      path: '/login',
      query: { redirect: path },
    });

    scrollToTop();
    return;
  }

  if (router.currentRoute.value.path !== path) {
    await router.push(path);
  }

  scrollToTop();
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}

.footer-heading {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #2C5F2D;
}

.footer-link {
  width: fit-content;
  display: inline-flex;
  align-items: center;
  color: #2C5F2D;
  padding: 0.2rem 0;
  border-radius: 0.5rem;
  transition:
    color 0.2s ease,
    transform 0.2s ease;
}

.footer-link:hover {
  color: #214B24;
  text-decoration: underline;
  transform: translateX(3px);
}

.footer-primary-button {
  width: 100%;
  background-color: #2C5F2D;
  color: #ffffff;
  border-radius: 0.5rem;
  padding: 0.75rem 1.75rem;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

.footer-primary-button:hover {
  background-color: #254F25;
}

.footer-secondary-button {
  width: 100%;
  background-color: white;
  color: #2C5F2D;
  border: 1px solid #A8D5BA;
  border-radius: 0.75rem;
  padding: 0.85rem 1.25rem;
  font-weight: 700;
  transition:
    background-color 0.2s ease,
    transform 0.2s ease;
}

.footer-secondary-button:hover {
  background-color: #FAF9F6;
  transform: translateY(-1px);
}
</style>