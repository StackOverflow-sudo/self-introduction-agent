<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<template>
  <div class="layout">
    <AppHeader />

    <main class="page">
      <router-view />
    </main>

    <AppFooter />
  </div>
</template>

<style>
/* 全局样式在 src/style.css，这里只管布局 */
.layout {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}

.page {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>