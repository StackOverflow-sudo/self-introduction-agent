SET NAMES utf8mb4;
-- 线上 projects 表迁移（v2：category / period / award + 数据）
-- 用法：docker exec -i sa-mariadb mariadb -uapp -p'密码' insurance < migrate_projects_v2.sql

ALTER TABLE projects ADD COLUMN category VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE projects ADD COLUMN period   VARCHAR(64) NOT NULL DEFAULT '';
ALTER TABLE projects ADD COLUMN award    VARCHAR(128) NOT NULL DEFAULT '';

DELETE FROM projects;

INSERT INTO projects (id, name, summary, description, tech_stack, github, demo, bvid, cover, category, period, award, sort_order) VALUES (1, '个人 AI Agent 平台', '全栈个人网站：FastAPI + Vue 3 + LangGraph，支持意图路由、父子块 RAG 与引用溯源。', '独立开发的个人数字分身平台，目标是把"自我介绍"做成一个可以对话的产品，而不是静态页面。

后端用 FastAPI 分层（Router / Service / Repository / Model / Schema），SQLAlchemy 管理业务表；在 LangGraph 手写的 ReAct 图（模型节点 + ToolNode + 条件边）之上再加一层意图路由主图，把请求分发到闲聊 / 技能 / 作品 / 知识库分支，避免每一轮都让模型重新决策。

RAG 采用父子块策略：子块约 400 字进 Milvus 做向量检索，父块（整节）存 MariaDB 用于还原上下文；检索后按 parent_id 取回完整章节，并在流式响应中通过自定义 SSE 事件把引用来源推给前端，回答里用 [1][2] 标注出处。

会话记忆交给 PostgreSQL 的 LangGraph Checkpointer，按 thread_id 隔离；前端 Vue 3 + Vite 用 fetch + ReadableStream 解析 SSE 实现逐字输出；整套服务用 Docker Compose 部署在阿里云，前端静态文件走 Nginx。', 'FastAPI,Vue 3,LangGraph,Milvus,Docker,PostgreSQL', 'https://github.com/StackOverflow-sudo/self-introduction-agent', 'http://47.93.204.199', '', '', 'agent', '2026.10 – 至今', '', 1);
INSERT INTO projects (id, name, summary, description, tech_stack, github, demo, bvid, cover, category, period, award, sort_order) VALUES (2, '御影智心 ｜ 基于大模型与 AIGC 的电影园区数字化平台', '面向西安电影制片厂的数字化体验平台：三维园区漫游 + 数字人讲解 + 电影推荐，服务外包大赛国家三等奖。', '发包方"长安计算"针对西安电影制片厂的定制化数字化体验平台。核心问题：园区与电影博物馆的内容原本靠图文展示，远程用户难以感知空间与展陈，游客看到展品后也缺少即时提问和延伸了解电影的途径。

平台以三维园区为交互入口：用 Blender 制作园区与博物馆模型，Vue 3 + Three.js 实现场景浏览与展品交互，Spring Boot 提供内容与功能接口；电影推荐把 TMDB 5000、Netflix Prize 数据组织成 Neo4j 电影知识图谱，结合图谱相似度与协同过滤加权推荐，用电影间关系补充稀疏的用户行为。

数字人讲解在 RTX 3090 上本地部署 ChatGLM-6B，为场馆问答设置上下文，把文字、语音交互与 Unity 数字人的动作、口型驱动对接，打通从提问到讲解的完整流程。

我担任队长与主要开发者：拆解三维游览 / 电影推荐 / 数字人讲解 / 多端交付四块需求，个人主导整体 UI、园区与博物馆建模、三维前端、模型部署与数字人集成，完成约 50% 的 Spring Boot 后端代码，并负责 Neo4j 图谱实现。最终按"进入园区 — 点击展品 — 询问数字人 — 查看推荐"的路径联调，完成 Web 端展示与微信小程序上线。', 'Vue 3,Three.js,Blender,ChatGLM-6B,Unity,Spring Boot,Neo4j', 'https://github.com/StackOverflow-sudo/fwwbgs', '', 'BV16AadecEYv', '', 'agent,ml', '2024.02 – 2024.07', '国家三等奖 ｜ 位次 1/3', 2);
INSERT INTO projects (id, name, summary, description, tech_stack, github, demo, bvid, cover, category, period, award, sort_order) VALUES (3, '面向机器人任务规划的 LLM 行为树候选选择框架', '让 LLM 生成的行为树先过符号验证与物理仿真再择优；仿真后重排序 regret 0.034（人工权重方案 3.182）。', '硕士毕业项目。机器人接收"抓取、放置、堆叠"等自然语言指令后可由大模型生成行为树，但直接执行第一份结果存在风险：计划可能遗漏前置条件、选错操作对象，或在逻辑检查通过后仍因接触位置不稳定而仿真失败——单看文本或符号结果，无法判断是否真正适合执行。

系统做成"多候选生成 — 分层验证 — 排序选择 — 结果复核"的原型：为 GPT 定义统一的行为树 JSON 约束与解析适配层；先用 KIOS 检查目标达成、前置条件覆盖与无效动作，再转成 Isaac Gym 任务采集执行成功率、目标位置误差等物理结果；最后用行为树结构编码与符号特征训练轻量 Transformer 排序，并区分"仿真前预排序"与"仿真后重排序"两种模式。

工程上把系统拆成可独立运行的阶段，为每个候选保存标识、配置、状态与输出文件；配合任务清单、结果缓存、失败日志与断点续跑，避免 ROS/MoveIt 环境故障后重跑全部仿真。评估严格按任务与初始状态分组、整组来源留出测试，隔离仿真前输入与事后物理结果。

完成端到端原型与含 110 组任务状态、660 个候选的评测集；30 组来源留出测试中，仿真后重排序平均 regret 为 0.034（人工权重方案 3.182），选出成功计划的组数与评测上界一致。', 'Python,PyTorch,Transformer,KIOS,Isaac Gym,ROS Noetic', 'https://github.com/StackOverflow-sudo/BT_selector', '', '', '', 'agent,ml', '2026.06 – 2026.09', '', 3);
INSERT INTO projects (id, name, summary, description, tech_stack, github, demo, bvid, cover, category, period, award, sort_order) VALUES (4, '亚马逊卫星图像多标签分类', '40,479 张图像 / 17 类标签的多标签分类，验证集 sample-wise F2 0.9315。', '课程项目，担任组长与主要开发者。一张亚马逊卫星图像可能同时包含植被、农田、水域等信息，人工逐张识别效率低，且不同标签的样本数量差异很大。

基于 40,479 张图像搭建 PyTorch 训练与评估流程，固定 80/20 划分；对比 SimpleCNN、ResNet18、ConvNeXt-Tiny 三种骨干，集成阈值调整、四视图 TTA 与概率融合，最终验证集 sample-wise F2 达 0.9315。

项目难点是"多标签 + 稀有类"：提高稀有类识别容易拉低整体指标。通过采样与类别加权做消融，量化了稀有类宏平均 F2 从 0.3220 提升到 0.4602、整体 F2 从 0.9240 降到 0.9070 的取舍，为模型与阈值选择提供依据。', 'PyTorch,ResNet18,ConvNeXt-Tiny,OpenCV', 'https://github.com/StackOverflow-sudo/DLT_CW2', '', '', '', 'ml', '2026.04 – 2026.06', '', 4);
INSERT INTO projects (id, name, summary, description, tech_stack, github, demo, bvid, cover, category, period, award, sort_order) VALUES (5, '海事运输市场自适应竞价智能体', '基于 MABLE 模拟器的竞价智能体：订单估值 + 动态报价 + 中标后排程更新，课程竞赛第一名。', '课程项目，组长与主要开发者。海运公司通过竞拍获取运输合同，但低价中标不等于盈利——订单能否按时完成、需要增加多少航程与燃油成本，取决于船队当前的航线与排程。

基于学校提供的 MABLE 模拟器，打通"读取订单与船队状态 → 估算履约成本 → 生成报价 → 根据竞拍结果更新排程"的完整决策流程。

关键难点是竞价与排程相互影响：报价过低可能中标后亏损，而逐一求解最优排程又难以满足每轮决策的时间要求，同时对手报价不完全可见。做法是用多起点插入从可行排程中估算新订单的边际成本，利用竞拍反馈与指数加权移动平均（EWMA）调整报价；中标后再校验船舶运力、交付时限与预期利润，把订单插入现有排程。

在不同竞争强度与船队规模下对比课程基线，最终获课程竞赛第一名。', 'Python,约束排程,竞价策略,EWMA', 'https://github.com/StackOverflow-sudo/intelligent_agent_project', '', '', '', 'agent', '2025.11 – 2026.01', '课程竞赛第一名', 5);
INSERT INTO projects (id, name, summary, description, tech_stack, github, demo, bvid, cover, category, period, award, sort_order) VALUES (6, '曼舍湖畔 · 西湖民宿游戏化体验 App', '原生 Android 应用：把民宿展示做成游戏化虚拟游览，配手绘西湖地图与 AI 问答导览，多媒体竞赛省级三等奖。', '传统民宿宣传通常集中展示房间、价格和位置，用户很难在浏览信息时感受到民宿与西湖周边生活方式的联系。团队希望做一个更有参与感的移动应用，让用户在了解民宿的同时认识周边景点与文化特色。

目标有两个：用游戏化体验提升民宿展示的趣味性；同时解决游客抵达后"周边有什么、该怎么逛、遇到问题向谁问"的实际需求。

应用把民宿展示融入虚拟游览场景：用户可通过钓鱼、采茶等互动获取积分并培养虚拟宠物；出行时可以查看手绘风格的西湖地图，并通过 AI 对话查询游览信息。这样"民宿宣传 + 持续互动 + 周边导览"被串成一条完整的用户体验。

我担任主要开发者，负责整体 UI 与交互设计、Android 前端开发，以及大语言模型接口接入。难点在于把宣传、游戏互动和出行导览组织成自然的流程，而不是彼此独立的功能页面；做法是围绕"入住与探索周边"设计界面，用钓鱼、采茶和积分反馈承接日常互动，实现手绘地图展示并把 AI 问答接进应用，方便用户游览过程中随时查询。作品获浙江省大学生多媒体作品设计竞赛省级三等奖。', 'Android,UI 与交互设计,LLM API,手绘地图', '', '', 'BV1CK4y1B7xt', '', 'agent', '', '省级三等奖 ｜ 位次 2/5', 6);

SELECT id, name, period, award, LEFT(category,20) AS cat FROM projects ORDER BY sort_order;