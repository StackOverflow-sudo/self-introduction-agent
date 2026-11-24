<script setup>
import { ref, nextTick } from 'vue'

const input = ref('')
const messages = ref([])                                  // { role, content }
const threadId = ref(crypto.randomUUID())                 // 会话ID（浏览器生成）
const loading = ref(false)
const listEl = ref(null)

async function scrollToBottom() {
  await nextTick()
  if (listEl.value) listEl.value.scrollTop = listEl.value.scrollHeight
}

function newSession() {
  threadId.value = crypto.randomUUID()
  messages.value = []
}

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  scrollToBottom()

  // 先放一条空的 AI 消息，边收边填
  messages.value.push({ role: 'ai', content: '' })
  const aiMsg = messages.value[messages.value.length - 1]

  try {
    const resp = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, thread_id: threadId.value }),
    })
    if (!resp.ok) throw new Error('HTTP ' + resp.status)

    const reader = resp.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      // SSE 以空行分隔消息
      const parts = buffer.split('\n\n')
      buffer = parts.pop()                    // 最后一段可能不完整，留到下次

      for (const part of parts) {
        const line = part.trim()
        if (!line.startsWith('data:')) continue
        const data = line.slice(5).trim()
        if (data === '[DONE]') return

        try {
          const obj = JSON.parse(data)
          if (obj.text) {
            aiMsg.content += obj.text
            scrollToBottom()
          }
          if (obj.error) aiMsg.content += `\n[错误] ${obj.error}`
        } catch { /* 忽略不完整 JSON */ }
      }
    }
  } catch (e) {
    if (!aiMsg.content) aiMsg.content = '请求失败：' + e.message
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>

<template>
  <div class="app">
    <header>
      <div>
        <h1>我的数字分身</h1>
        <p class="conv">会话 {{ threadId.slice(0, 8) }}…</p>
      </div>
      <button class="new" @click="newSession">新会话</button>
    </header>

    <ul ref="listEl" class="messages">
      <li v-for="(m, i) in messages" :key="i" :class="m.role">
        <span>{{ m.content || (m.role === 'ai' ? '…' : '') }}</span>
      </li>
    </ul>

    <form class="input" @submit.prevent="send">
      <input
        v-model="input"
        placeholder="问点什么…（比如：你会什么技术？）"
        :disabled="loading"
      />
      <button type="submit" :disabled="loading">发送</button>
    </form>
  </div>
</template>

<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, sans-serif; background: #f5f5f7; }

.app {
  max-width: 720px; margin: 0 auto; height: 100vh;
  display: flex; flex-direction: column; padding: 16px;
}

header { display: flex; justify-content: space-between; align-items: flex-start; }
header h1 { font-size: 20px; margin: 0 0 4px; }
.conv { color: #888; font-size: 12px; margin: 0 0 12px; }
.new {
  padding: 6px 12px; border: 1px solid #ccc; background: #fff;
  border-radius: 8px; font-size: 13px; cursor: pointer;
}

.messages { flex: 1; overflow-y: auto; list-style: none; padding: 0; margin: 0 0 12px; }
.messages li { margin: 8px 0; display: flex; }
.messages li.user { justify-content: flex-end; }
.messages li span {
  display: inline-block; max-width: 80%; padding: 10px 14px;
  border-radius: 12px; white-space: pre-wrap; line-height: 1.5;
}
.messages li.user span { background: #1f6feb; color: #fff; }
.messages li.ai span { background: #fff; color: #222; border: 1px solid #e3e3e6; }

.input { display: flex; gap: 8px; }
.input input {
  flex: 1; padding: 10px 12px; border: 1px solid #ccc;
  border-radius: 10px; font-size: 14px;
}
.input button {
  padding: 10px 18px; border: none; border-radius: 10px;
  background: #1f6feb; color: #fff; font-size: 14px; cursor: pointer;
}
.input button:disabled { opacity: 0.5; cursor: not-allowed; }
</style>