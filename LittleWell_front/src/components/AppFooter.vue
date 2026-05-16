<template>
  <footer
    class="relative bg-[#FAF9F6] border-t border-gray-200 pt-12 sm:pt-16 pb-10 sm:pb-12 overflow-visible"
  >
    <div
      class="absolute -top-24 left-0 right-0 h-24 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6]/75 to-transparent pointer-events-none z-30"
      aria-hidden="true"
    ></div>

    <div
      class="container mx-auto px-4 sm:px-6 max-w-5xl text-center relative z-10"
    >
      <p class="text-2xl text-[#2C5F2D]">LittleHelp</p>

      <p
        class="mt-4 text-muted-foreground max-w-3xl mx-auto leading-relaxed text-sm sm:text-base"
      >
        Helping families create practical, balanced, and child-friendly
        lunchbox plans through science-backed nutrition guidance.
      </p>

      <nav
        class="mt-6 flex flex-wrap items-center justify-center gap-x-4 gap-y-2 text-sm text-[#2C5F2D]"
        aria-label="Footer navigation"
      >
        <button
          @click="goHomeSection('child-profiles')"
          type="button"
          class="hover:underline"
        >
          Lunchbox Plan
        </button>

        <button
          @click="goProtected('/weekly-plan')"
          type="button"
          class="hover:underline"
        >
          Weekly Plan
        </button>

        <button
          @click="goProtected('/my-plans')"
          type="button"
          class="hover:underline"
        >
          My Plans
        </button>

        <button
          @click="router.push('/knowledge-hub-prototype')"
          type="button"
          class="hover:underline"
        >
          Knowledge Hub
        </button>

        <button
          @click="router.push('/about')"
          type="button"
          class="hover:underline"
        >
          About Us
        </button>
      </nav>

      <p class="mt-6 text-xs text-muted-foreground">
        © 2026 LittleHelp. All rights reserved.
      </p>
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
</script>

<style scoped>
.text-muted-foreground {
  color: #6b7280;
}
</style>