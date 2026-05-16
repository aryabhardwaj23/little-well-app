<template>
  <footer
    class="relative bg-[#F4F1EA] border-t border-[#D8D2C4] shadow-[0_-8px_24px_rgba(44,95,45,0.06)] pt-12 sm:pt-16 pb-10 sm:pb-12"
  >
    <div class="container mx-auto px-4 sm:px-6 max-w-6xl relative z-10">
      <div class="grid gap-10 md:grid-cols-[1.4fr,1fr,1fr]">
        <!-- Brand -->
        <div>
          <button
            type="button"
            @click="goHome"
            class="text-left"
            aria-label="Go to LittleHelp home page"
          >
            <p class="text-2xl font-semibold text-[#2C5F2D]">LittleHelp</p>
          </button>

          <p class="mt-4 text-muted-foreground max-w-md leading-relaxed text-sm sm:text-base">
            Helping families create practical, balanced, and child-friendly
            lunchbox plans through science-backed nutrition guidance.
          </p>

          <p class="mt-4 text-xs text-muted-foreground leading-relaxed max-w-md">
            LittleHelp provides educational food guidance only and is not a replacement
            for professional medical or dietetic advice.
          </p>
        </div>

        <!-- Navigation -->
        <nav aria-label="Footer navigation">
          <p class="text-sm font-semibold uppercase tracking-wide text-[#2C5F2D] mb-4">
            Explore
          </p>

          <div class="space-y-3 text-sm">
            <button
              type="button"
              @click="goHome"
              class="footer-link"
            >
              Home
            </button>

            <button
              type="button"
              @click="goProtected('/weekly-plan')"
              class="footer-link"
            >
              Weekly Plan
            </button>

            <button
              type="button"
              @click="goProtected('/my-plans')"
              class="footer-link"
            >
              My Plans
            </button>

            <button
              type="button"
              @click="goTo('/knowledge-hub-prototype')"
              class="footer-link"
            >
              Knowledge Hub
            </button>

            <button
              type="button"
              @click="goTo('/about')"
              class="footer-link"
            >
              About Us
            </button>
          </div>
        </nav>

        <!-- CTA -->
        <div>
          <p class="text-sm font-semibold uppercase tracking-wide text-[#2C5F2D] mb-4">
            Get started
          </p>

          <p class="text-sm text-muted-foreground leading-relaxed mb-5">
            Create a child profile to receive more personalised lunchbox ideas based
            on age, allergies, dietary needs, and nutrition focus.
          </p>

          <div class="flex flex-col gap-3">
            <button
              type="button"
              @click="goProtected('/child-info')"
              class="w-full sm:w-auto bg-[#A8D5BA] hover:bg-[#8FC2A4] text-[#2C5F2D] rounded-lg px-6 py-3 font-semibold transition-colors"
            >
              Start Planning
            </button>

            <button
              type="button"
              @click="goTo('/quick-start')"
              class="w-full sm:w-auto bg-white hover:bg-[#FAF9F6] text-[#2C5F2D] border border-[#A8D5BA] rounded-lg px-6 py-3 font-semibold transition-colors"
            >
              Try Quick Start
            </button>
          </div>
        </div>
      </div>

      <div
        class="mt-10 pt-6 border-t border-[#D8D2C4] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-muted-foreground"
      >
        <p>© 2026 LittleHelp. All rights reserved.</p>

        <button
          type="button"
          @click="scrollToTop"
          class="text-[#2C5F2D] hover:underline"
        >
          Back to top
        </button>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';
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

const goTo = async (path) => {
  await router.push(path);
  scrollToTop();
};

const goHome = async () => {
  await router.push('/');
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

  await router.push(path);
  scrollToTop();
};
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}

.footer-link {
  display: block;
  color: #2C5F2D;
  transition:
    color 0.2s ease,
    transform 0.2s ease;
}

.footer-link:hover {
  color: #214B24;
  text-decoration: underline;
  transform: translateX(2px);
}
</style>