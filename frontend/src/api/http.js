/**
 * 极简 fetch 封装：统一 JSON、错误处理。
 */
export async function request(path, options = {}) {
  const resp = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!resp.ok) {
    let detail = ''
    try {
      const data = await resp.json()
      detail = data.detail || ''
    } catch {
      /* 忽略解析失败 */
    }
    throw new Error(detail || `HTTP ${resp.status}`)
  }

  if (resp.status === 204) return null
  return resp.json()
}
