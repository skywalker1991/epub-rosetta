<template>
  <div class="settings">
    <h2>参数设置</h2>
    <div class="setting-item">
      <label>
        <input type="checkbox" v-model="useTextFrequency" />
        只翻译文中出现次数小于该值的词（数值越小，词越稀有）
      </label>
    </div>
    <div class="setting-item" v-if="useTextFrequency">
      <label>词频选择</label>
      <input type="range" v-model="textFrequency" min="1" max="10" />
      <span>{{ textFrequency }}</span>
    </div>
    <div class="setting-item">
      <label>
        <input type="checkbox" v-model="useCorpusFrequency" />
        只翻译现代语料库中处于该值排名之后的词（数值越大，词越稀有）
      </label>
    </div>
    <div class="setting-item" v-if="useCorpusFrequency">
      <label>词频选择</label>
      <input type="range" v-model="corpusFrequency" min="1000" max="20000" />
      <span>{{ corpusFrequency }}</span>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      useTextFrequency: false,
      textFrequency: 50,
      useCorpusFrequency: false,
      corpusFrequency: 50
    };
  },
  methods:{
    emitSettingsChange() {
      this.$emit('settings-change', {
        useTextFrequency: this.useTextFrequency,
        textFrequency: this.textFrequency,
        useCorpusFrequency: this.useCorpusFrequency,
        corpusFrequency: this.corpusFrequency
      });
    }
  },
  watch: {
    useTextFrequency: 'emitSettingsChange',
    textFrequency: 'emitSettingsChange',
    useCorpusFrequency: 'emitSettingsChange',
    corpusFrequency: 'emitSettingsChange'
  }
}
</script>

<style scoped>
.settings {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
  height: 300px;
  margin-left: 30px;
}
.setting-item {
  margin-bottom: 20px;
}
</style>