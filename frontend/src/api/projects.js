import { request } from './http'

/** 作品集列表 */
export function listProjects() {
  return request('/api/projects')
}

/** 作品详情 */
export function getProject(id) {
  return request(`/api/projects/${id}`)
}
