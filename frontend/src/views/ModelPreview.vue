<script setup>
import '@google/model-viewer'

const models = [
  { key: 'waijing', label: 'waijing_final1.glb（17.8 MB）', src: '/models/waijing_final1.glb' },
  // { key: 'zhuguan', label: 'zhuguan_final.glb（63.6 MB）', src: '/models/zhuguan_final.glb' },
  { key: 'che', label: '汽车展厅 - 副本.glb（54.5 MB）', src: encodeURI('/models/汽车展厅 - 副本.glb') },
]
</script>

<template>
  <div class="container preview">
    <h1>模型预览</h1>
    <p class="sub">看哪个是哪个，把名字记下来（加载大模型需要几秒）</p>

    <div class="grid">
      <div v-for="m in models" :key="m.key" class="card">
        <h3>{{ m.label }}</h3>

        <model-viewer
          :src="m.src"
          :alt="m.label"
          camera-controls
          auto-rotate
          auto-rotate-delay="6000"
          rotation-per-second="8deg"
          interaction-prompt="none"
          min-field-of-view="1deg"
          shadow-intensity="1"
          style="width: 100%; height: 380px; border-radius: 12px;"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.preview {
  padding-block: clamp(24px, 5vw, 48px);
}
.sub { color: var(--text-dim); margin-bottom: 24px; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 380px), 1fr));
  gap: clamp(16px, 3vw, 28px);
}

.card {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 8px 28px rgba(30, 41, 59, 0.08);
}
.card h3 {
  font-size: 15px;
  margin: 0 0 12px;
  word-break: break-all;
}

/* 3D 画布透明，露出页面渐变背景 */
model-viewer {
  background: transparent;
  --poster-color: transparent;
  --progress-bar-color: transparent;
}
</style>
