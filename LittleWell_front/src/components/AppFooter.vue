<template>
  <footer
    class="relative bg-[#F4F1EA] border-t border-[#D8D2C4] shadow-[0_-10px_28px_rgba(44,95,45,0.07)]"
  >
    <div class="h-1 bg-gradient-to-r from-[#A8D5BA] via-[#F7B267]/70 to-[#CDE7F0]"></div>

    <div class="container mx-auto px-4 sm:px-6 max-w-6xl py-10 sm:py-14">
      <div class="grid gap-10 lg:grid-cols-[1.3fr,0.9fr,1.1fr]">
        <!-- Brand -->
        <section aria-label="LittleHelp summary">
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

          <div class="mt-5 space-y-3 max-w-md">
            <div class="rounded-2xl border border-[#D8D2C4] bg-white/60 p-4">
              <p class="text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] mb-1">
                Educational guidance
              </p>
              <p class="text-xs text-muted-foreground leading-relaxed">
                LittleHelp provides educational food guidance only and is not a replacement
                for professional medical or dietetic advice.
              </p>
            </div>

            <div class="rounded-2xl border border-[#D8D2C4] bg-white/60 p-4">
              <p class="text-xs font-semibold uppercase tracking-wide text-[#2C5F2D] mb-1">
                Data & attribution
              </p>

              <p class="text-xs text-muted-foreground leading-relaxed">
                Built with public food and nutrition references including OpenFoodFacts,
                AUSNUT, Australian Dietary Guidelines, and seasonal food resources.
              </p>

              <button
                type="button"
                @click="goTo('/about#data-sources')"
                class="mt-2 text-xs font-semibold text-[#2C5F2D] hover:underline"
              >
                View data sources
              </button>
            </div>
          </div>
        </section>

        <!-- Navigation -->
        <nav aria-label="Footer navigation">
          <p class="footer-heading">
            Explore
          </p>

          <div class="grid grid-cols-2 sm:grid-cols-1 gap-2 text-sm">
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

        <!-- CTA -->
        <section aria-label="Get started">
          <div class="rounded-3xl bg-white border border-[#D8D2C4] p-5 sm:p-6 shadow-sm">
            <p class="footer-heading mb-3">
              Get started
            </p>

            <h2 class="text-xl font-semibold text-[#2C5F2D] leading-snug">
              Build a lunchbox plan that fits your child.
            </h2>

            <p class="mt-3 text-sm text-muted-foreground leading-relaxed">
              Create a child profile for personalised ideas based on age, allergies,
              dietary needs, and nutrition focus.
            </p>

            <div class="mt-5 flex flex-col gap-3">
              <button
                type="button"
                @click="goProtected('/child-info')"
                class="footer-primary-button"
              >
                Start Planning
              </button>

              <button
                type="button"
                @click="goTo('/quick-start')"
                class="footer-secondary-button"
              >
                Try Quick Start
              </button>
            </div>
          </div>
        </section>
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
  padding: 0.35rem 0;
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
  background-color: #A8D5BA;
  color: #2C5F2D;
  border-radius: 0.75rem;
  padding: 0.85rem 1.25rem;
  font-weight: 700;
  transition:
    background-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.footer-primary-button:hover {
  background-color: #8FC2A4;
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(44, 95, 45, 0.12);
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