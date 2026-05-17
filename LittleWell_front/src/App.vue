<template>
  <div class="min-h-screen bg-[#FAF9F6] flex flex-col">
    <AppNavbar v-if="showLayout" />

    <main :class="['flex flex-1 flex-col', showLayout ? 'pt-16 lg:pt-20' : '']">
      <router-view />
    </main>

    <AppFooter v-if="showLayout" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import AppNavbar from './components/AppNavbar.vue';
import AppFooter from './components/AppFooter.vue';

const route = useRoute();

const hiddenLayoutPaths = [
  '/project-access',
];

const showLayout = computed(() => {
  return !hiddenLayoutPaths.includes(route.path);
});
</script>