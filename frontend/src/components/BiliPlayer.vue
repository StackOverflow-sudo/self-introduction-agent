<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  bvid: { type: String, required: true },
  page: { type: Number, default: 1 },
  cover: { type: String, default: '' },          // 可选封面图
  title: { type: String, default: '点击播放演示视频' },
})

const playing = ref(false)

// 点击后才把 autoplay=1 带上
const src = computed(() => {
  const p = new URLSearchParams({
    bvid: props.bvid,
    page: String(props.page),
    high_quality: '1',
    danmaku: '0',
    autoplay: playing.value ? '1' : '0',
  })
  return `https://player.bilibili.com/player.html?${p.toString()}`
})
</script>

<template>
  <div class="bili-wrap">
    <!-- 点击后：加载播放器 -->
    <iframe
      v-if="playing"
      :src="src"
      scrolling="no"
      frameborder="0"
      allowfullscreen="true"
      referrerpolicy="no-referrer"
      :title="title"
    />

    <!-- 点击前：封面 + 播放按钮（不加载任何 iframe） -->
    <button
      v-else
      class="cover"
      type="button"
      :style="cover ? { backgroundImage: `url(${cover})` } : {}"
      @click="playing = true"
    >
      <span class="play">▶</span>
      <span class="label">{{ title }}</span>
    </button>
  </div>
</template>

<style scoped>
.bili-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 16px;
  overflow: hidden;
  background: #0f172a;
  box-shadow: 0 14px 38px rgba(30, 41, 59, 0.18);
}

.bili-wrap iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

/* 封面 / 播放按钮 */
.cover {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
  padding: 0;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  color: #fff;
  background-color: #1e293b;
  background-image: linear-gradient(135deg, #6366f1 0%, #a855f7 55%, #ec4899 100%);
  background-size: cover;
  background-position: center;
  transition: filter 0.2s;
}

.cover::after {
  /* 图片封面时压暗，保证文字可读 */
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.28);
}

.cover:hover { filter: brightness(1.06); }

.play,
.label {
  position: relative;
  z-index: 1;
}

.play {
  width: clamp(52px, 8vw, 72px);
  height: clamp(52px, 8vw, 72px);
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: clamp(18px, 3vw, 24px);
  background: rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  transition: transform 0.2s, background 0.2s;
}

.cover:hover .play {
  transform: scale(1.08);
  background: rgba(255, 255, 255, 0.3);
}

.label {
  font-size: clamp(13px, 1.8vw, 15px);
  text-shadow: 0 1px 6px rgba(0, 0, 0, 0.4);
}
</style>
