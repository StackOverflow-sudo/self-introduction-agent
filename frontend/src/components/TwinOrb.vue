<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

// 已经在对话页就不显示（避免重复入口）
const visible = computed(() => route.path !== '/chat')
</script>

<template>
  <Transition name="orb">
    <RouterLink
      v-if="visible"
      to="/chat"
      class="twin-orb"
      aria-label="和我的数字分身聊聊"
    >
      <!-- 扩散光环 -->
      <span class="ring"></span>
      <span class="ring ring-2"></span>

      <!-- 核心 -->
      <span class="core">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" aria-hidden="true">
          <path
            d="M12 3c4.97 0 9 3.58 9 8s-4.03 8-9 8c-.9 0-1.77-.12-2.58-.34L5 20l1.2-3.3C4.83 15.36 3 13.35 3 11c0-4.42 4.03-8 9-8Z"
            stroke="currentColor"
            stroke-width="1.6"
            stroke-linejoin="round"
          />
          <circle cx="8.5" cy="11" r="1.1" fill="currentColor" />
          <circle cx="12" cy="11" r="1.1" fill="currentColor" />
          <circle cx="15.5" cy="11" r="1.1" fill="currentColor" />
        </svg>
      </span>

      <!-- 悬停提示 -->
      <span class="tip">和数字分身聊聊</span>
    </RouterLink>
  </Transition>
</template>

<style scoped>
.twin-orb {
  position: fixed;
  right: clamp(16px, 3vw, 36px);
  bottom: clamp(16px, 3vw, 36px);
  z-index: 120;

  width: clamp(56px, 7vw, 68px);
  height: clamp(56px, 7vw, 68px);
  border-radius: 50%;
  display: grid;
  place-items: center;
  text-decoration: none;
  color: #fff;

  background: var(--grad);
  box-shadow:
    0 12px 40px rgba(99, 102, 241, 0.45),
    inset 0 1px 2px rgba(255, 255, 255, 0.5);

  animation: breathe 3.2s ease-in-out infinite;
  transition: transform 0.2s ease;
}

.twin-orb:hover {
  transform: scale(1.08);
}

.core {
  position: relative;
  z-index: 2;
  display: grid;
  place-items: center;
}

/* ---------- 呼吸（核心缩放 + 光晕强弱）---------- */
@keyframes breathe {
  0%,
  100% {
    transform: scale(1);
    box-shadow:
      0 12px 40px rgba(99, 102, 241, 0.45),
      inset 0 1px 2px rgba(255, 255, 255, 0.5);
  }
  50% {
    transform: scale(1.06);
    box-shadow:
      0 16px 56px rgba(99, 102, 241, 0.65),
      inset 0 1px 2px rgba(255, 255, 255, 0.7);
  }
}

/* ---------- 扩散光环 ---------- */
.ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid rgba(129, 140, 248, 0.55);
  animation: pulse 3.2s ease-out infinite;
  pointer-events: none;
}

.ring-2 {
  animation-delay: 1.6s;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.7;
  }
  80% {
    transform: scale(1.7);
    opacity: 0;
  }
  100% {
    transform: scale(1.7);
    opacity: 0;
  }
}

/* ---------- 悬停提示 ---------- */
.tip {
  position: absolute;
  right: calc(100% + 12px);
  top: 50%;
  transform: translateY(-50%) translateX(6px);
  white-space: nowrap;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 10px;
  color: var(--text);
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 24px rgba(30, 41, 59, 0.12);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s, transform 0.2s;
}

.twin-orb:hover .tip {
  opacity: 1;
  transform: translateY(-50%) translateX(0);
}

/* ---------- 进出场 ---------- */
.orb-enter-active,
.orb-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.orb-enter-from,
.orb-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

/* 手机：缩小一点，避免挡内容 */
@media (max-width: 480px) {
  .twin-orb {
    width: 52px;
    height: 52px;
  }
  .tip { display: none; }
}

@media (prefers-reduced-motion: reduce) {
  .twin-orb { animation: none; }
  .ring { animation: none; opacity: 0.35; }
}
</style>
