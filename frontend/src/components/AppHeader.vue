<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="header">
    <RouterLink to="/" class="logo">自我介绍网站，您好！</RouterLink>

    <nav class="nav">
      <RouterLink to="/" active-class="" exact-active-class="router-link-active">首页</RouterLink>
      <RouterLink to="/agent">Agent 开发方向</RouterLink>
      <RouterLink to="/ml">机器学习方向</RouterLink>
      <RouterLink to="/about">自我评价</RouterLink>
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

  /* ---------- 磨砂玻璃三件套 ---------- */
  background: rgba(255, 255, 255, 0.75);                    /* 半透明（越低越透）*/
  backdrop-filter: blur(20px) saturate(180%);               /* 模糊 + 提饱和 */
  -webkit-backdrop-filter: blur(20px) saturate(180%);       /* Safari */
  border-bottom: 1px solid rgba(255, 255, 255, 0.65);       /* 半透明分隔线 */

  box-shadow:
    0 4px 24px rgba(30, 41, 59, 0.07),                      /* 下方投影 */
    inset 0 1px 0 rgba(255, 255, 255, 0.7);                 /* 顶部高光（玻璃边缘）*/

  position: sticky;
  top: 0;
  z-index: 50;
}

.logo {
  font-weight: 800;
  font-size: clamp(13px, 2vw, 15px);
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