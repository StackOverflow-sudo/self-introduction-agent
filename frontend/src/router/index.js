import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Chat from '../views/Chat.vue'
import Projects from '../views/Projects.vue'
import About from '../views/About.vue'
import NotFound from '../views/NotFound.vue'

/* 两个方向页共用 Track.vue，内容由 meta 决定 */
const AGENT_INFO = {
  eyebrow: '方向一',
  title: 'Agent 方向',
  intro:
    '聚焦 LLM Agent 的可靠性、编排与工程化落地：多 Agent 意图路由、父子块 RAG 检索、工具调用、会话记忆与线上部署。',
  skills: [
    { group: 'Agent 框架', items: ['LangChain', 'LangGraph', 'ReAct', '工具调用', '检查点记忆'] },
    { group: 'RAG', items: ['父子块检索', 'Milvus', 'bge-m3 / DashScope', '引用溯源'] },
    { group: '工程化', items: ['FastAPI', 'SSE 流式', 'Docker', 'Nginx', 'PostgreSQL'] },
  ],
}

const ML_INFO = {
  eyebrow: '方向二',
  title: '机器学习方向',
  intro:
    '聚焦模型训练与评测：目标检测、多标签分类、类别不平衡处理、TTA 与阈值分析，以及 LLM 生成结果的排序建模。',
  skills: [
    { group: '模型', items: ['PyTorch', 'Transformer', 'ResNet', 'ConvNeXt', 'YOLO'] },
    { group: '训练与评测', items: ['训练/验证划分', 'TTA', '阈值调优', 'mAP / F2 / ROC-AUC'] },
    { group: '数据处理', items: ['NumPy', 'pandas', 'Matplotlib', 'OpenCV'] },
  ],
}

const routes = [
  /* ---------- 顶部导航 4 项 ---------- */
  { path: '/', name: 'home', component: Home },
  {
    path: '/agent',
    name: 'agent',
    component: () => import('../views/Track.vue'),
    meta: { track: 'agent', info: AGENT_INFO },
  },
  {
    path: '/ml',
    name: 'ml',
    component: () => import('../views/Track.vue'),
    meta: { track: 'ml', info: ML_INFO },
  },
  { path: '/about', name: 'about', component: About },

  /* ---------- 其他页面（不在导航里）---------- */
  { path: '/chat', name: 'chat', component: Chat },
  { path: '/projects', name: 'projects', component: Projects },
  { path: '/preview', name: 'preview', component: () => import('../views/ModelPreview.vue') },

  { path: '/:pathMatch(.*)*', name: 'notfound', component: NotFound },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
