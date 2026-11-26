<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import ProjectCard from '../components/ProjectCard.vue'
import { useReveal } from '../composables/useReveal'
import { listProjects } from '../api/projects'

useReveal()

const route = useRoute()
const track = computed(() => route.meta.track || 'agent')
const info = computed(() => route.meta.info || {})

const projects = ref([])
const loading = ref(true)
const error = ref('')

async function load() {
  loading.value = true
  error.value = ''
  try {
    const all = await listProjects()
    projects.value = all.filter((p) => (p.categories || []).includes(track.value))
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

// 同一个组件在 /agent 和 /ml 之间切换时要重新加载
watch(track, load, { immediate: true })
</script>

<template>
  <div class="container track">
    <header class="head reveal">
      <p class="eyebrow">{{ info.eyebrow }}</p>
      <h1>{{ info.title }}</h1>
      <p class="intro">{{ info.intro }}</p>
    </header>

    <section class="section reveal">
      <h2>相关项目</h2>

      <p v-if="loading" class="state">加载中…</p>
      <p v-else-if="error" class="state error">加载失败：{{ error }}</p>
      <p v-else-if="!projects.length" class="state">暂无项目</p>

      <div v-else class="grid">
        <ProjectCard v-for="p in projects" :key="p.id" :project="p" />
      </div>
    </section>

    <section class="section reveal">
      <h2>相关技能</h2>

      <div class="skills">
        <div v-for="g in info.skills || []" :key="g.group" class="skill-group">
          <h3>{{ g.group }}</h3>
          <div class="tags">
            <span v-for="s in g.items" :key="s" class="tag">{{ s }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.track { padding-block: clamp(32px, 6vw, 72px); }

.head { margin-bottom: clamp(24px, 4vw, 48px); }
.eyebrow {
  color: var(--accent);
  font-size: clamp(12px, 1.5vw, 14px);
  font-weight: 600;
  letter-spacing: 0.08em;
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
  line-height: 1.8;
  max-width: 60ch;
}

.section { padding-block: clamp(24px, 5vw, 56px); }
.section h2 { margin-bottom: clamp(16px, 2.5vw, 28px); }

.state { color: var(--text-dim); font-size: 14px; }
.state.error { color: #dc2626; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: clamp(14px, 2.5vw, 24px);
}

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
.tags { display: flex; flex-wrap: wrap; gap: 8px; }
.tag {
  font-size: 13px;
  padding: 5px 12px;
  border-radius: 999px;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.18);
  color: #4f46e5;
}
</style>
