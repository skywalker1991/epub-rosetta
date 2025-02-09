<template>
  <div class="banner">
    <div class="text-container">
      <h1 class="title">Epub-Rosetta</h1>
      <p class="subtitle">流畅你的外语阅读体验</p>
    </div>
\

  </div>
</template>

<script>
export default {
  name: 'Banner'
}
</script>

<style scoped>
.banner {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  text-align: left;
  padding: 20px;
  background-color: #0f6fd0;
  z-index: 1000;
  justify-content: space-between;
}

.title {
  font-size: 3.5em;
  margin: 20px 0 10px;
  color: #fafafa;
  font-weight: bold;
  margin-left: 150px;
}
.subtitle {
  margin-top: -10px;
  font-size: 2.0em;
  color: #e5e2e2;
  margin-left: 150px;
}


</style>