import { onMounted, onUnmounted } from 'vue'

/**
 * 给页面里所有 .reveal 元素加"滚动到视口时才出现"的效果。
 */
export function useReveal() {
  let io

  onMounted(() => {
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'))
      return
    }

    io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
            io.unobserve(entry.target)   // 出现一次后不再监听
          }
        })
      },
      { threshold: 0.15 }
    )

    document.querySelectorAll('.reveal').forEach((el) => io.observe(el))
  })

  onUnmounted(() => io?.disconnect())
}
