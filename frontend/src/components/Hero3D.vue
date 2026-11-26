<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '3D 模型' },
})

const ready = ref(false)      // model-viewer 是否已注册
const loaded = ref(false)     // 模型是否加载完成
const failed = ref(false)     // 加载失败

onMounted(() => {
  // 首屏先渲染文字，等浏览器空闲再加载 model-viewer（1MB 脚本）
  const start = async () => {
    try {
      await import('@google/model-viewer')
      ready.value = true
    } catch (e) {
      console.error('[Hero3D] model-viewer 加载失败', e)
      failed.value = true
    }
  }

  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(start, { timeout: 2500 })
  } else {
    setTimeout(start, 1200)
  }
})

function onLoad() {
  loaded.value = true
}

function onError(e) {
  console.warn('[Hero3D] 模型加载失败', props.src, e)
  failed.value = true
}
</script>

<template>
  <div class="hero3d">
    <!-- 背景光晕（模型没加载出来时就是它） -->
    <div class="glow" :class="{ dim: loaded }"></div>

    <model-viewer
      v-if="ready && !failed"
      :src="src"
      :alt="alt"
      camera-controls
      auto-rotate
      auto-rotate-delay="5000"
      rotation-per-second="10deg"
      interaction-prompt="none"
      min-field-of-view="2deg"
      shadow-intensity="0"
      exposure="1"
      class="viewer"
      @load="onLoad"
      @error="onError"
    />

    <!-- 加载中的小提示 -->
    <div v-if="ready && !loaded && !failed" class="hint">模型加载中…</div>
  </div>
</template>

<style scoped>
.hero3d {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  max-height: 460px;
  display: grid;
  place-items: center;
}

/* 背景光晕（没有模型时的视觉主体） */
.glow {
  position: absolute;
  inset: 12%;
  border-radius: 50%;
  background: radial-gradient(
    circle at 32% 28%,
    rgba(199, 210, 254, 0.95) 0%,
    rgba(165, 180, 252, 0.75) 35%,
    rgba(129, 140, 248, 0.45) 65%,
    rgba(99, 102, 241, 0) 100%
  );
  filter: blur(6px);
  animation: float 7s ease-in-out infinite;
  transition: opacity 0.6s ease;
  pointer-events: none;
}
.glow.dim {
  opacity: 0.35;      /* 模型加载出来后让光晕退后 */
}

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50%      { transform: translateY(-14px) scale(1.04); }
}

/* 3D 画布 */
.viewer {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  background: transparent;
  --poster-color: transparent;
  --progress-bar-color: rgba(99, 102, 241, 0.4);
}

.hint {
  position: absolute;
  bottom: 4%;
  z-index: 2;
  font-size: 12px;
  color: var(--text-dim);
}

@media (max-width: 768px) {
  .hero3d { max-height: 320px; }
}
</style>
