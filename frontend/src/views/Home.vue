<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useReveal } from '../composables/useReveal'
import ProjectSection from '../components/ProjectSection.vue'
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

/* 教育经历：按阶段分组（研究生 / 本科），阶段内按时间倒序 */
const educationStages = [
  {
    stage: '研究生阶段',
    period: '2025.09 – 2026.11',
    school: '南安普顿大学 ｜ 人工智能 硕士',
    note: '深度学习技术、计算机视觉、NLP、智能体/博弈论；多门课程项目担任团队负责人。',
    items: [
      {
        kind: 'project',
        label: '项目',
        date: '2026.06 – 2026.09',
        title: 'LLM 行为树候选选择框架（硕士毕设）',
        desc: '多候选生成 → KIOS 符号验证 → Isaac Gym 物理仿真 → Transformer 排序；110 组任务、660 个候选，仿真后重排序 regret 0.034。',
      },
      {
        kind: 'project',
        label: '项目',
        date: '2026.04 – 2026.06',
        title: '亚马逊卫星图像多标签分类',
        desc: '40,479 张图像 / 17 类标签，对比三种骨干并做 TTA 与概率融合，验证集 F2 0.9315。',
      },
      {
        kind: 'contest',
        label: '竞赛',
        date: '2025.11 – 2026.01',
        title: '海事运输市场自适应竞价智能体 · 课程竞赛第一名',
        desc: '基于 MABLE 模拟器打通报价与排程决策，多起点插入估边际成本 + EWMA 调价；课程成绩 82.5。',
      },
    ],
  },
  {
    stage: '本科阶段',
    period: '2021.09 – 2025.06',
    school: '浙江理工大学 ｜ 计算机科学与技术 学士',
    note: 'C++ / Python 程序设计、数据结构与算法、软件工程、操作系统、计算机网络。',
    items: [
      {
        kind: 'intern',
        label: '实习',
        date: '2024.07 – 2024.08',
        title: '阿里巴巴 · AI 算法实习生',
        desc: 'YOLOv9 对照 SSD 做交通视频目标检测；RFS / E-IRFS 长尾采样 + 定向增强，整体 Precision +5pp、少数类 Recall +10pp。',
      },
      {
        kind: 'contest',
        label: '竞赛',
        date: '2024.02 – 2024.07',
        title: '御影智心 · 服务外包创新创业大赛 国家三等奖',
        desc: '队长兼主要开发者：三维前端（Vue 3 / Three.js）、Blender 建模、ChatGLM-6B 部署、数字人集成、约 50% Spring Boot 后端；完成 Web 与小程序上线。',
      },
      {
        kind: 'campus',
        label: '校园',
        date: '2021.10 – 2023.10',
        title: '学院学风建设指导中心 · 宣传部部长',
        desc: '带 10 人团队运营"学风建设"公众号；个人撰写推文 20 篇，部门累计 50 余篇，获当届干事评选第一名。',
      },
      {
        kind: 'honor',
        label: '荣誉',
        date: '2022.12',
        title: '浙江理工大学 优秀学生二等奖学金',
        desc: '',
      },
      {
        kind: 'campus',
        label: '校园',
        date: '2021.10 – 2022.10',
        title: '校博物馆宣讲团 · 英文讲解员',
        desc: '为外宾提供丝绸博物馆英文导览，背诵 1 万余字英文讲解稿，并运营博物馆公众号。',
      },
    ],
  },
]

const skills = [
  {
    group: '编程与工程',
    items: ['Python', 'C++（基础）', 'Java', 'Git', 'Linux', 'Docker', 'Nginx'],
  },
  {
    group: '模型与视觉',
    items: ['PyTorch', 'Transformer', 'YOLO', 'ResNet', 'ConvNeXt', 'OpenCV'],
  },
  {
    group: 'LLM & Agent',
    items: ['LangChain', 'LangGraph', 'RAG', 'Milvus', 'Prompt', 'ChatGLM-6B'],
  },
  {
    group: '数据与后端',
    items: ['NumPy', 'pandas', 'Matplotlib', 'FastAPI', 'SQLAlchemy', 'MySQL', 'PostgreSQL', 'Spring Boot'],
  },
]
</script>

<template>
  <div class="home">
    <!-- ① 自我评价 -->
    <section class="hero reveal">
      <div class="container hero-inner">
        <div class="hero-text">
          <p class="eyebrow">您好，我是</p>
          <h1>王瑞琦</h1>
          <p class="tagline">多模态算法工程师 · LLM Agent 研发</p>
          <p class="intro">
            南安普顿大学人工智能硕士，关注 LLM Agent 的可靠性与工程化落地。
            做过 LLM 行为树可靠性评估、卫星图像多标签分类、大模型数字人交互平台；
            相信"能跑起来、能量化"才算真正做完。
          </p>

          <div class="cta">
            <RouterLink to="/agent" class="btn primary">看 AI Agent 方向</RouterLink>
            <RouterLink to="/ml" class="btn primary">看机器学习方向</RouterLink>
            <RouterLink to="/chat" class="btn">和数字分身聊聊</RouterLink>
          </div>
        </div>

        <!-- Hero 视觉：大光球 -->
        <div class="hero-visual">
          <div class="orb"></div>
        </div>
      </div>
    </section>

    <!-- 演示视频 -->
    <!-- <section v-if="demos.length" class="section reveal">
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
    </section> -->

    <!-- ② 作品集（数据来自后端 /api/projects） -->
    <section class="section reveal">
      <div class="container">
        <h2>作品集</h2>
        <!-- <p class="section-sub">点开卡片看技术栈和链接</p> -->

        <p v-if="loading" class="state">加载中…</p>
        <p v-else-if="error" class="state error">加载失败：{{ error }}</p>
        <p v-else-if="!projects.length" class="state">暂无作品</p>

        <div v-else class="list">
          <ProjectSection
            v-for="(p, i) in projects"
            :key="p.id"
            :project="p"
            :index="i"
          />
        </div>
      </div>
    </section>

    <!-- ③ 教育经历（完整时间线） -->
    <section class="section reveal">
      <div class="container">
        <h2>教育经历</h2>
        <p class="section-sub">教育 · 实习 · 竞赛 · 项目 · 校园 · 荣誉</p>

        <div class="stages">
          <section
            v-for="(g, gi) in educationStages"
            :key="g.stage"
            class="stage"
            :class="{ sep: gi > 0 }"
          >
            <header class="stage-head">
              <h3>{{ g.stage }}</h3>
              <span class="stage-period">{{ g.period }}</span>
            </header>
            <p class="stage-school">{{ g.school }}</p>
            <p v-if="g.note" class="stage-note">{{ g.note }}</p>

            <div class="tl">
              <div
                v-for="t in g.items"
                :key="t.title"
                class="tl-item"
                :class="`k-${t.kind}`"
              >
                <div class="tl-head">
                  <span class="tl-date">{{ t.date }}</span>
                  <span class="tl-tag">{{ t.label }}</span>
                </div>
                <h3>{{ t.title }}</h3>
                <p v-if="t.desc">{{ t.desc }}</p>
              </div>
            </div>
          </section>
        </div>
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

/* Hero 右侧视觉（大光球） */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 240px;
}
.orb {
  width: clamp(160px, 26vw, 300px);
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(
    circle at 32% 28%,
    #e0e7ff 0%,
    #c7d2fe 25%,
    #a5b4fc 50%,
    #818cf8 75%,
    #6366f1 100%
  );
  box-shadow:
    0 24px 80px rgba(99, 102, 241, 0.45),
    0 0 120px rgba(129, 140, 248, 0.35),
    inset -12px -12px 40px rgba(255, 255, 255, 0.55);
  animation: float 6s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50%      { transform: translateY(-16px) scale(1.03); }
}

/* ---------- ② 演示视频 ---------- */
.demos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 420px), 1fr));
  gap: clamp(16px, 3vw, 28px);
}

/* ---------- ③ 作品集：流式列表 ---------- */
.list {
  display: flex;
  flex-direction: column;
}

/* ---------- ③ 教育经历（按阶段分组） ---------- */
.stages { display: flex; flex-direction: column; }

.stage { position: relative; }

/* 阶段之间的分隔 */
.stage.sep {
  margin-top: clamp(34px, 5vw, 56px);
  padding-top: clamp(26px, 4vw, 42px);
}
.stage.sep::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    rgba(99, 102, 241, 0.35),
    rgba(168, 85, 247, 0.22),
    rgba(236, 72, 153, 0.12),
    transparent
  );
}

/* 阶段头 */
.stage-head {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 14px;
  margin-bottom: 8px;
}
.stage-head h3 {
  margin: 0;
  font-size: clamp(19px, 2.6vw, 24px);
  letter-spacing: 0.02em;
  background: var(--grad);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.stage-period {
  font-size: clamp(12px, 1.7vw, 13px);
  font-weight: 700;
  color: #fff;
  background: var(--grad);
  border-radius: 999px;
  padding: 3px 13px;
  letter-spacing: 0.03em;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  box-shadow: 0 5px 16px rgba(99, 102, 241, 0.26);
}

.stage-school {
  margin: 0 0 4px;
  color: var(--text);
  font-size: clamp(14px, 1.9vw, 16px);
  font-weight: 600;
}
.stage-note {
  margin: 0 0 20px;
  color: var(--text-dim);
  font-size: clamp(12.5px, 1.6vw, 14px);
  line-height: 1.7;
}

/* 阶段内时间线 */
.tl {
  position: relative;
  margin-left: 6px;
  padding-left: clamp(20px, 3.5vw, 34px);
  border-left: 2px solid rgba(99, 102, 241, 0.15);
}

.tl-item {
  position: relative;
  padding-bottom: clamp(22px, 3vw, 34px);
}
.tl-item:last-child { padding-bottom: 0; }

/* 节点 */
.tl-item::before {
  content: '';
  position: absolute;
  left: calc(-1 * clamp(20px, 3.5vw, 34px) - 6px);
  top: 9px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #a5b4fc;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.08);
}

.tl-head {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 10px;
  margin-bottom: 6px;
}

.tl-date {
  font-size: clamp(12px, 1.6vw, 13px);
  font-weight: 700;
  color: var(--accent);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.tl-tag {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 10px;
  border-radius: 999px;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

/* 类型配色 */
.k-edu .tl-tag { color: #4338ca; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.22); }
.k-intern .tl-tag { color: #0369a1; background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.22); }
.k-contest .tl-tag { color: #92400e; background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.26); }
.k-project .tl-tag { color: #6d28d9; background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.22); }
.k-campus .tl-tag { color: #047857; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.22); }
.k-honor .tl-tag { color: #be123c; background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.22); }

.tl-item h3 {
  margin: 0 0 4px;
  font-size: clamp(15px, 1.9vw, 17px);
  color: var(--text);
  line-height: 1.4;
}

.tl-item p {
  margin: 0;
  color: var(--text-dim);
  font-size: clamp(12.5px, 1.6vw, 14px);
  line-height: 1.75;
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
