<script setup>
import { useReveal } from '../composables/useReveal'

useReveal()

const strengths = [
  {
    icon: '🧩',
    title: '把复杂问题拆成可验证的步骤',
    desc: '毕设里把 LLM 行为树的不确定性拆成"格式校验 → 符号验证 → 物理仿真 → 候选排序"，每一步都能单独量化、单独失败、单独改进。',
  },
  {
    icon: '📊',
    title: '习惯用数字说话',
    desc: '仿真后 regret 0.034（人工权重 3.182）、ROC-AUC 0.942、验证集 F2 0.9315——比起"效果不错"，我更愿意给出可复现的指标。',
  },
  {
    icon: '🛠️',
    title: '能独立把想法做成产品',
    desc: '从模型训练到 FastAPI 后端、Vue 前端、Docker 部署上线，全流程自己走一遍，知道每一层会在哪里出问题。',
  },
]

const honesty = [
  '有时过度追求指标，需要提醒自己"业务价值优先"。',
  '英语口语仍在提升（IELTS 6.5），全英文汇报能完成，但不够流畅自然。',
  '工程经验集中在个人项目和课程项目，还没经历过高并发、多人协作的线上系统。',
]

const goals = [
  { k: '短期', v: '在 LLM Agent 的可靠性评估与工程化方向做深，补齐线上运维、可观测性经验。' },
  { k: '长期', v: '成为能把 LLM 能力稳定落地到真实产品里的工程师。' },
]
</script>

<template>
  <div class="container about">
    <header class="head reveal">
      <p class="eyebrow">ABOUT ME</p>
      <h1>自我评价</h1>
      <p class="intro">
        一个把"能跑起来、能量化"当作完成标准的工程师。
      </p>
    </header>

    <!-- 优势 -->
    <section class="section reveal">
      <h2>我的优势</h2>
      <div class="cards">
        <article v-for="s in strengths" :key="s.title" class="card">
          <div class="icon">{{ s.icon }}</div>
          <h3>{{ s.title }}</h3>
          <p>{{ s.desc }}</p>
        </article>
      </div>
    </section>

    <!-- 不足 -->
    <section class="section reveal">
      <h2>需要改进的地方</h2>
      <ul class="list">
        <li v-for="h in honesty" :key="h">{{ h }}</li>
      </ul>
    </section>

    <!-- 目标 -->
    <section class="section reveal">
      <h2>职业目标</h2>
      <div class="goals">
        <div v-for="g in goals" :key="g.k" class="goal">
          <span class="k">{{ g.k }}</span>
          <p>{{ g.v }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about { padding-block: clamp(32px, 6vw, 72px); }

.head { margin-bottom: clamp(24px, 4vw, 48px); }
.eyebrow {
  color: var(--accent);
  font-size: clamp(12px, 1.5vw, 14px);
  font-weight: 600;
  letter-spacing: 0.12em;
  margin: 0 0 8px;
}
.head h1 {
  margin: 0 0 16px;
  background: var(--grad);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.intro {
  color: var(--text-dim);
  font-size: clamp(14px, 2vw, 17px);
  line-height: 1.8;
}

.section { padding-block: clamp(24px, 4vw, 48px); }
.section h2 { margin-bottom: clamp(16px, 2.5vw, 24px); }

/* 优势卡片 */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
  gap: clamp(14px, 2.5vw, 24px);
}
.card {
  background: rgba(255, 255, 255, 0.68);
  -webkit-backdrop-filter: blur(16px);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 18px;
  padding: clamp(16px, 2.5vw, 24px);
  box-shadow: 0 8px 28px rgba(30, 41, 59, 0.08);
}
.card .icon { font-size: 24px; margin-bottom: 10px; }
.card h3 { font-size: clamp(15px, 1.9vw, 17px); margin: 0 0 8px; }
.card p {
  margin: 0;
  color: var(--text-dim);
  font-size: clamp(13px, 1.6vw, 14px);
  line-height: 1.7;
}

/* 不足列表 */
.list {
  margin: 0;
  padding-left: 1.2em;
  color: var(--text-dim);
  line-height: 1.9;
  font-size: clamp(13px, 1.7vw, 15px);
}

/* 目标 */
.goals { display: grid; gap: 16px; }
.goal {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: clamp(14px, 2vw, 20px);
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 14px;
  box-shadow: 0 6px 20px rgba(30, 41, 59, 0.06);
}
.goal .k {
  flex-shrink: 0;
  font-size: 12px;
  font-weight: 700;
  color: #4f46e5;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 999px;
  padding: 3px 12px;
}
.goal p { margin: 0; color: var(--text-dim); line-height: 1.7; font-size: clamp(13px, 1.6vw, 15px); }
</style>
