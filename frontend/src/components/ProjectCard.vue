<script setup>
import { ref } from 'vue'
import BiliPlayer from './BiliPlayer.vue'

defineProps({
  project: {
    type: Object,
    required: true,
  },
})

const open = ref(false)
</script>

<template>
  <!-- 卡片 -->
  <article class="card" @click="open = true">
    <h3>{{ project.name }}</h3>
    <p class="summary">{{ project.summary }}</p>

    <div class="tags">
      <span v-for="t in project.tech" :key="t" class="tag">{{ t }}</span>
    </div>
  </article>

  <!-- 详情弹窗 -->
  <Teleport to="body">
    <div v-if="open" class="mask" @click.self="open = false">
      <div class="modal">
        <h2>{{ project.name }}</h2>
        <p class="desc">{{ project.summary }}</p>

        <template v-if="project.bvid">
          <h4>演示视频</h4>
          <BiliPlayer :bvid="project.bvid" />
        </template>

        <h4>技术栈</h4>
        <div class="tags">
          <span v-for="t in project.tech" :key="t" class="tag">{{ t }}</span>
        </div>

        <div class="actions">
          <a v-if="project.github" :href="project.github" target="_blank" rel="noopener" class="link">
            GitHub ↗
          </a>
          <a v-if="project.demo" :href="project.demo" target="_blank" rel="noopener" class="link">
            在线 Demo ↗
          </a>
          <button class="close" @click="open = false">关闭</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
/* ---------- 毛玻璃卡片 ---------- */
.card {
  background: rgba(255, 255, 255, 0.68);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 18px;
  padding: clamp(16px, 2.5vw, 22px);
  box-shadow: 0 8px 28px rgba(30, 41, 59, 0.08);
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 44px rgba(30, 41, 59, 0.14);
  border-color: rgba(99, 102, 241, 0.35);
}

.card h3 {
  margin: 0;
  font-size: clamp(16px, 2vw, 19px);
  color: var(--text);
}

.summary {
  margin: 0;
  color: var(--text-dim);
  font-size: clamp(13px, 1.6vw, 14px);
  line-height: 1.6;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: auto;
}

.tag {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.18);
  color: #4f46e5;
  white-space: nowrap;
}

/* ---------- 弹窗 ---------- */
.mask {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--gutter);
  background: rgba(15, 23, 42, 0.28);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

.modal {
  width: 100%;
  max-width: 560px;
  max-height: 85dvh;
  overflow-y: auto;
  padding: clamp(20px, 4vw, 32px);
  border-radius: 22px;
  color: var(--text);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 28px 70px rgba(30, 41, 59, 0.22);
}

.modal h2 {
  margin: 0 0 12px;
  font-size: clamp(18px, 3vw, 24px);
  background: var(--grad);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  display: inline-block;
}

.modal h4 {
  margin: 20px 0 8px;
  font-size: 13px;
  color: var(--text-dim);
  font-weight: 600;
}

.desc {
  color: var(--text-dim);
  line-height: 1.7;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-top: 24px;
}

.link {
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 13px;
  text-decoration: none;
  color: var(--accent);
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.2);
  transition: background 0.2s;
}
.link:hover { background: rgba(99, 102, 241, 0.16); }

.close {
  margin-left: auto;
  padding: 8px 16px;
  border-radius: 10px;
  border: 1px solid rgba(30, 41, 59, 0.15);
  background: transparent;
  color: var(--text);
  font-size: 13px;
  cursor: pointer;
}
.close:hover { background: rgba(30, 41, 59, 0.05); }
</style>
