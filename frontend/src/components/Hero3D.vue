<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '3D 模型' },
})

const root = ref(null)
const ready = ref(false)     // model-viewer 是否已注册
const loaded = ref(false)    // 模型是否加载完成
const failed = ref(false)    // 加载失败

let io

async function load() {
  if (ready.value || failed.value) return
  try {
    // 动态引入：model-viewer 约 1MB，不进主包
    await import('@google/model-viewer')
    ready.value = true
  } catch (e) {
    console.error('[Hero3D] model-viewer 加载失败', e)
    failed.value = true
  }
}

onMounted(() => {
  // 进入视口附近才加载，避免一次挂载多个 WebGL 上下文
  if (!('IntersectionObserver' in window)) {
    load()
    return
  }
  io = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        load()
        io.disconnect()
      }
    },
    { rootMargin: '300px' }
  )
  if (root.value) io.observe(root.value)
})

onUnmounted(() => io?.disconnect())

function onLoad() { loaded.value = true }
function onError(e) {
  console.warn('[Hero3D] 模型加载失败', props.src, e)
  failed.value = true
}
</script>

<template>
  <div ref="root" class="hero3d">
    <!-- 背景光晕（模型没出来时就是它） -->
    <div class="glow" :class="{ dim: loaded }"></div>

    <model-viewer
      v-if="ready && !failed"
      :src="src"
      :alt="alt"
      camera-controls
      auto-rotate
      auto-rotate-delay="5000"
      rotation-per-second="9deg"
      interaction-prompt="none"
      min-field-of-view="2deg"
      shadow-intensity="0"
      class="viewer"
      @load="onLoad"
      @error="onError"
    />

    <div v-if="ready && !loaded && !failed" class="hint">模型加载中…</div>
  </div>
</template>

<style scoped>
.hero3d {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  max-height: 380px;
  display: grid;
  place-items: center;
}

.glow {
  position: absolute;
  inset: 14%;
  border-radius: 50%;
  background: radial-gradient(
    circle at 32% 28%,
    rgba(199, 210, 254, 0.9) 0%,
    rgba(165, 180, 252, 0.7) 35%,
    rgba(129, 140, 248, 0.4) 65%,
    rgba(99, 102, 241, 0) 100%
  );
  filter: blur(6px);
  animation: float 7s ease-in-out infinite;
  transition: opacity 0.6s ease;
  pointer-events: none;
}
.glow.dim { opacity: 0.3; }

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50%      { transform: translateY(-12px) scale(1.04); }
}

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

@media (max-width: 860px) {
  .hero3d { max-height: 300px; }
}

@media (prefers-reduced-motion: reduce) {
  .glow { animation: none; }
}
</style>
