<template>
  <div class="notfound">
    <h1>404</h1>
    <p>页面不存在</p>
    <RouterLink to="/">回首页</RouterLink>
  </div>
</template>

<style scoped>
.notfound {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: var(--gutter);
  text-align: center;
}
</style>
