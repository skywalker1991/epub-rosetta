<template>
  <div class="banner">
    <h1 class="title">EPUB-Rosetta</h1>
    <p class="subtitle">将原版EPUB更加容易阅读</p>
  </div>
</template>

<script>
export default {
  name: 'Banner'
}
</script>

<style scoped>
.banner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
  z-index: 1000;
}

.title {
  font-size: 2.5em;
  margin: 20px 0 10px;
}
.subtitle {
  font-size: 1.2em;
  color: #666;
}
</style>