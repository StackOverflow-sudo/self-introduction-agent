<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useReveal } from '../composables/useReveal'
import ProjectCard from '../components/ProjectCard.vue'
import BiliPlayer from '../components/BiliPlayer.vue'
import { listProjects } from '../api/projects'

useReveal()

/* ---------- 作品集：从后端数据库读取 ---------- */
const projects = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    projects.value = await listProjects()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

// 有 bvid 的项目才显示演示视频
const demos = computed(() => projects.value.filter((p) => p.bvid))

const timeline = [
  { year: '2026', title: 'AI Agent 全栈开发', desc: '从零搭建 FastAPI + Vue + LangGraph 的个人 Agent 平台，并部署上线。' },
  { year: '2025', title: '后端开发', desc: 'Java / Spring Boot 后端开发，熟悉分层架构与接口设计。' },
  { year: '2024', title: '打基础', desc: 'Linux、数据库、计算机网络等基础。' },
]

const skills = [
  { group: '后端', items: ['Python', 'FastAPI', 'SQLAlchemy', 'MySQL', 'PostgreSQL'] },
  { group: '前端', items: ['Vue 3', 'Vite', 'CSS'] },
  { group: 'AI', items: ['LangChain', 'LangGraph', 'RAG', 'Milvus', 'Prompt'] },
  { group: '运维', items: ['Linux', 'Docker', 'Nginx'] },
]
</script>

<template>
  <div class="home">
    <!-- ① 自我评价 -->
    <section class="hero reveal">
      <div class="container hero-inner">
        <div class="hero-text">
          <p class="eyebrow">你好，我是</p>
          <h1>[你的名字]</h1>
          <p class="tagline">后端工程师 · AI Agent 开发者</p>
          <p class="intro">
            写 Java 出身，现在用 Python 构建 AI Agent 全栈应用。
            喜欢把复杂的东西拆开、讲清楚、再落地成能跑的系统。
          </p>

          <div class="cta">
            <RouterLink to="/projects" class="btn primary">看作品</RouterLink>
            <RouterLink to="/chat" class="btn">和我的数字分身聊聊 →</RouterLink>
          </div>
        </div>

        <!-- 3D 模型占位（后面接 model-viewer） -->
        <div class="hero-visual">
          <div class="orb"></div>
        </div>
      </div>
    </section>

    <!-- 演示视频 -->
    <section v-if="demos.length" class="section reveal">
      <div class="container">
        <h2>项目演示</h2>
        <p class="section-sub">点击封面播放（B 站）</p>

        <div class="demos">
          <BiliPlayer
            v-for="(p, i) in demos"
            :key="p.id"
            :bvid="p.bvid"
            :title="`演示 ${i + 1} · ${p.name}`"
          />
        </div>
      </div>
    </section>

    <!-- ② 作品集（数据来自后端 /api/projects） -->
    <section class="section reveal">
      <div class="container">
        <h2>作品集</h2>
        <p class="section-sub">点开卡片看技术栈和链接</p>

        <p v-if="loading" class="state">加载中…</p>
        <p v-else-if="error" class="state error">加载失败：{{ error }}</p>
        <p v-else-if="!projects.length" class="state">暂无作品</p>

        <div v-else class="grid">
          <ProjectCard v-for="p in projects" :key="p.id" :project="p" />
        </div>
      </div>
    </section>

    <!-- ③ 学习经历 -->
    <section class="section reveal">
      <div class="container">
        <h2>学习经历</h2>

        <ol class="timeline">
          <li v-for="t in timeline" :key="t.year">
            <span class="year">{{ t.year }}</span>
            <div class="tl-body">
              <h3>{{ t.title }}</h3>
              <p>{{ t.desc }}</p>
            </div>
          </li>
        </ol>
      </div>
    </section>

    <!-- ④ 技术栈 -->
    <section class="section reveal">
      <div class="container">
        <h2>技术栈</h2>

        <div class="skills">
          <div v-for="g in skills" :key="g.group" class="skill-group">
            <h3>{{ g.group }}</h3>
            <div class="tags">
              <span v-for="s in g.items" :key="s" class="tag">{{ s }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home { width: 100%; }

/* ---------- 通用区块间距 ---------- */
.section {
  padding-block: clamp(48px, 8vw, 96px);
}
.section h2 {
  margin-bottom: 8px;
}
.section-sub {
  color: var(--text-dim);
  font-size: clamp(13px, 1.6vw, 15px);
  margin-bottom: clamp(20px, 3vw, 32px);
}

/* 加载 / 错误状态 */
.state {
  color: var(--text-dim);
  font-size: 14px;
  padding: 24px 0;
}
.state.error { color: #dc2626; }

/* ---------- ① Hero ---------- */
.hero {
  padding-block: clamp(48px, 10vh, 120px);
}
.hero-inner {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: clamp(24px, 5vw, 64px);
  align-items: center;
}

.eyebrow {
  color: var(--text-dim);
  font-size: clamp(13px, 1.6vw, 15px);
  margin: 0 0 8px;
}
.hero h1 {
  margin: 0 0 12px;
  background: var(--grad);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.tagline {
  font-size: clamp(15px, 2.2vw, 20px);
  font-weight: 600;
  color: var(--accent);
  margin: 0 0 16px;
}
.intro {
  color: var(--text-dim);
  line-height: 1.8;
  max-width: 46ch;
  margin: 0 0 28px;
}

.cta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.btn {
  padding: 11px 22px;
  border-radius: 12px;
  font-size: 14px;
  text-decoration: none;
  color: var(--text);
  background: var(--glass-strong);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.btn.primary {
  background: var(--grad);
  border-color: transparent;
  color: #fff;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
}
.btn.primary:hover {
  box-shadow: 0 12px 30px rgba(99, 102, 241, 0.45);
}

/* Hero 右侧视觉（3D 占位） */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 240px;
}
.orb {
  width: clamp(140px, 22vw, 240px);
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #c7d2fe 0%, #a5b4fc 35%, #818cf8 65%, #6366f1 100%);
  box-shadow:
    0 20px 60px rgba(99, 102, 241, 0.35),
    inset -10px -10px 30px rgba(255, 255, 255, 0.5);
  animation: float 6s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-14px); }
}

/* ---------- ② 演示视频 ---------- */
.demos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 420px), 1fr));
  gap: clamp(16px, 3vw, 28px);
}

/* ---------- ③ 作品集网格 ---------- */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: clamp(14px, 2.5vw, 24px);
}

/* ---------- ③ 时间线 ---------- */
.timeline {
  list-style: none;
  margin: 0;
  padding: 0 0 0 clamp(16px, 3vw, 28px);
  border-left: 2px solid rgba(99, 102, 241, 0.18);
  display: flex;
  flex-direction: column;
  gap: clamp(20px, 3vw, 32px);
}
.timeline li {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: 6px 20px;
}
.timeline li::before {
  content: '';
  position: absolute;
  left: calc(-1 * clamp(16px, 3vw, 28px) - 6px);
  top: 7px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--grad);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.12);
}
.year {
  color: var(--accent);
  font-size: clamp(13px, 1.6vw, 14px);
  font-weight: 700;
  min-width: 48px;
}
.tl-body h3 {
  margin: 0 0 4px;
  font-size: clamp(15px, 1.9vw, 17px);
}
.tl-body p {
  margin: 0;
  color: var(--text-dim);
  font-size: clamp(13px, 1.6vw, 14px);
  line-height: 1.7;
}

/* ---------- ④ 技术栈 ---------- */
.skills {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr));
  gap: clamp(16px, 3vw, 28px);
}
.skill-group h3 {
  font-size: 14px;
  color: var(--text-dim);
  font-weight: 600;
  margin: 0 0 10px;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  font-size: 13px;
  padding: 5px 12px;
  border-radius: 999px;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.18);
  color: #4f46e5;
}

/* ---------- 响应式 ---------- */
@media (max-width: 768px) {
  .hero-inner {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .intro { margin-inline: auto; }
  .cta { justify-content: center; }
  .hero-visual { order: -1; min-height: 190px; }
}
</style>
