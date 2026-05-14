<template>
  <div class="min-h-screen bg-[#FAF9F6]">
    <AppNavbar />

    <main class="pt-20">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import AppNavbar from './components/AppNavbar.vue';
</script>