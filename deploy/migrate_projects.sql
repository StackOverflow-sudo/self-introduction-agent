-- 作品集表迁移（本地 → 线上）
-- 在云服务器执行：
--   docker exec -i sa-mariadb mariadb -uapp -p'你的DB_PASSWORD' insurance < migrate_projects.sql

ALTER TABLE projects
  ADD COLUMN summary    VARCHAR(255) NOT NULL DEFAULT '',
  ADD COLUMN github     VARCHAR(255) NOT NULL DEFAULT '',
  ADD COLUMN demo       VARCHAR(255) NOT NULL DEFAULT '',
  ADD COLUMN bvid       VARCHAR(64)  NOT NULL DEFAULT '',
  ADD COLUMN cover      VARCHAR(255) NOT NULL DEFAULT '',
  ADD COLUMN sort_order INT          NOT NULL DEFAULT 0;

UPDATE projects SET
  summary     = '全栈个人网站：FastAPI + Vue + LangGraph，支持 RAG 引用溯源与会话记忆。',
  description = '从零搭建的个人数字分身平台：FastAPI 后端 + Vue 3 前端 + LangGraph 多 Agent 编排，支持意图路由、父子块 RAG 检索、引用溯源、PostgreSQL 会话记忆，Docker 部署到阿里云。',
  tech_stack  = 'FastAPI,Vue 3,LangGraph,Milvus,Docker',
  github      = 'https://github.com/StackOverflow-sudo/self-introduction-agent',
  demo        = 'http://47.93.204.199',
  bvid        = 'BV16AadecEYv',
  cover       = '',
  sort_order  = 1
WHERE id = 1;

UPDATE projects SET
  summary     = '基于 RAG 的多 Agent 保险咨询系统，按意图路由到闲聊 / 推荐 / 查询子 Agent。',
  description = '主图负责意图识别与路由，子图分别处理寒暄、保险推荐、产品查询，配合 Milvus 向量检索与结构化输出分类。',
  tech_stack  = 'FastAPI,Milvus,LangGraph',
  github      = '',
  demo        = '',
  bvid        = 'BV1CK4y1B7xt',
  cover       = '',
  sort_order  = 2
WHERE id = 2;

SELECT id, name, summary, bvid, sort_order FROM projects ORDER BY sort_order;
