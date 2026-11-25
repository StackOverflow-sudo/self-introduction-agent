<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="header">
    <RouterLink to="/" class="logo">我的数字空间</RouterLink>

    <nav class="nav">
      <RouterLink to="/">首页</RouterLink>
      <RouterLink to="/projects">作品集</RouterLink>
      <RouterLink to="/chat">AI 对话</RouterLink>
      <RouterLink to="/about">关于我</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 16px;
  padding: clamp(10px, 2vw, 16px) var(--gutter);
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 14px rgba(30, 41, 59, 0.05);
  position: sticky;
  top: 0;
  z-index: 50;
}

.logo {
  font-weight: 800;
  font-size: clamp(15px, 2vw, 18px);
  background: var(--grad);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-decoration: none;
  white-space: nowrap;
}

.nav {
  display: flex;
  gap: clamp(10px, 2.5vw, 24px);
  flex-wrap: wrap;
}

.nav a {
  color: var(--text-dim);
  text-decoration: none;
  font-size: clamp(13px, 1.8vw, 14px);
  padding: 6px 2px;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
  white-space: nowrap;
}

.nav a:hover { color: var(--text); }

.nav a.router-link-active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

@media (max-width: 480px) {
  .header { justify-content: center; }
  .logo { width: 100%; text-align: center; }
  .nav { justify-content: center; }
}
</style>