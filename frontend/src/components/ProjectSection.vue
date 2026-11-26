<script setup>
import { computed } from 'vue'
import BiliPlayer from './BiliPlayer.vue'
import Hero3D from './Hero3D.vue'

const props = defineProps({
  project: { type: Object, required: true },
  index: { type: Number, default: 0 },
})

const num = computed(() => String(props.index + 1).padStart(2, '0'))

// 有视频或封面才占媒体列
const hasMedia = computed(() => Boolean(props.project.bvid || props.project.cover))

const paragraphs = computed(() =>
  (props.project.description || '')
    .split(/\n\s*\n/)
    .map((s) => s.trim())
    .filter(Boolean)
)
</script>

<template>
  <article class="project" :class="{ reverse: index % 2 === 1 }">
    <!-- ===== 上半：视频 + 简介（左右） ===== -->
    <div class="top" :class="{ single: !hasMedia }">
      <div v-if="hasMedia" class="media">
        <BiliPlayer
          v-if="project.bvid"
          :bvid="project.bvid"
          :title="`${project.name} · 演示`"
        />
        <div
          v-else
          class="cover"
          :style="{ backgroundImage: `url(${project.cover})` }"
        ></div>
      </div>

      <div class="intro">
        <div class="meta">
          <span class="num">{{ num }}</span>
          <span v-if="project.period" class="period">{{ project.period }}</span>
          <span v-for="c in project.categories || []" :key="c" class="cat">{{ c }}</span>
        </div>

        <h3>{{ project.name }}</h3>

        <span v-if="project.award" class="award">🏆 {{ project.award }}</span>

        <p class="summary">{{ project.summary }}</p>

        <div class="tags">
          <span v-for="t in project.tech" :key="t" class="tag">{{ t }}</span>
        </div>

        <div class="links">
          <a v-if="project.github" :href="project.github" target="_blank" rel="noopener">
            GitHub ↗
          </a>
          <a v-if="project.demo" :href="project.demo" target="_blank" rel="noopener">
            在线 Demo ↗
          </a>
        </div>
      </div>
    </div>

    <!-- ===== 下半：详细描述（+ 可选 3D 模型） ===== -->
    <div v-if="paragraphs.length" class="detail-row" :class="{ 'no-model': !project.model_glb }">
      <div class="detail">
        <p v-for="(p, i) in paragraphs" :key="i">{{ p }}</p>
      </div>

      <div v-if="project.model_glb" class="model">
        <Hero3D :src="project.model_glb" :alt="`${project.name} 3D 展示`" />
      </div>
    </div>
  </article>
</template>

<style scoped>
.project {
  padding-block: clamp(40px, 7vw, 88px);
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}
.project:first-child { border-top: none; }

/* ---------- 上半：左右 ---------- */
.top {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: clamp(24px, 4vw, 56px);
  align-items: center;
}

/* 偶数项：媒体移到右侧 */
.project.reverse .media { order: 2; }

/* 没有视频/封面：单列，不占媒体位 */
.top.single {
  grid-template-columns: minmax(0, 1fr);
}

/* ---------- 媒体 ---------- */
.media { position: relative; width: 100%; }

.cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 18px;
  overflow: hidden;
  background-size: cover;
  background-position: center;
}

/* ---------- 简介 ---------- */
.intro { min-width: 0; }

.meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 10px;
  margin-bottom: 12px;
}

.num {
  font-size: 14px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  color: var(--accent);
  opacity: 0.55;
}

.period {
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  background: var(--grad);
  border-radius: 999px;
  padding: 3px 12px;
  letter-spacing: 0.03em;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.cat {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 9px;
  border-radius: 999px;
  color: #4f46e5;
  background: rgba(99, 102, 241, 0.09);
  border: 1px solid rgba(99, 102, 241, 0.18);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.intro h3 {
  margin: 0 0 10px;
  font-size: clamp(20px, 2.8vw, 27px);
  line-height: 1.3;
  color: var(--text);
}

.award {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 13px;
  margin-bottom: 14px;
  border-radius: 999px;
  color: #92400e;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid rgba(245, 158, 11, 0.32);
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.16);
}

.summary {
  margin: 0 0 18px;
  color: var(--text);
  font-size: clamp(14px, 1.75vw, 16px);
  line-height: 1.8;
}

/* ---------- 技术栈：胶囊 ---------- */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  font-size: 12.5px;
  padding: 5px 14px;
  border-radius: 999px;
  color: #4338ca;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.09), rgba(168, 85, 247, 0.07));
  border: 1px solid rgba(99, 102, 241, 0.18);
  white-space: nowrap;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.18);
}

.links {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-top: 18px;
  font-size: 14px;
}
.links a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
}
.links a:hover { text-decoration: underline; }

/* ---------- 下半：详细描述 + 3D 模型 ---------- */
.detail-row {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr);
  gap: clamp(20px, 4vw, 48px);
  align-items: start;
  margin-top: clamp(22px, 3.5vw, 40px);
}

/* 没有 3D 模型时：详细描述独占整行 */
.detail-row.no-model {
  grid-template-columns: minmax(0, 1fr);
}

.detail {
  padding-left: clamp(0px, 1vw, 12px);
  border-left: 2px solid rgba(99, 102, 241, 0.1);
}
.detail p {
  margin: 0 0 14px;
  padding-left: clamp(12px, 2vw, 20px);
  color: var(--text-dim);
  font-size: clamp(13px, 1.65vw, 14.5px);
  line-height: 1.95;
}
.detail p:last-child { margin-bottom: 0; }

/* 右侧 3D 模型：滚动时吸附 */
.model {
  position: sticky;
  top: 100px;
  display: flex;
  justify-content: center;
}

/* ---------- 响应式 ---------- */
@media (max-width: 860px) {
  .project { padding-block: clamp(32px, 5vw, 52px); }

  .top,
  .project.reverse {
    grid-template-columns: minmax(0, 1fr);
    gap: 18px;
  }
  .project.reverse .media { order: 0; }

  .detail { border-left: none; padding-left: 0; }
  .detail p { padding-left: 0; }

  .detail-row { grid-template-columns: minmax(0, 1fr); }
  .model { position: static; }
}
</style>
