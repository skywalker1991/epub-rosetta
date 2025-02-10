<template>
  <div class="settings">
    <div class="setting-item">
      <el-slider 
      v-model="corpusFrequency" 
      :min="1000" 
      :max="10000" 
      :marks="marks"
      ></el-slider>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      useTextFrequency: false,
      textFrequency: 30,
      useCorpusFrequency: false,
      corpusFrequency: 2000,
      marks: {
        1500: '初级',
        3000: '中级',
        5000: '高级',


      }
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
  width: 300px;
  margin-left: 10px;
}
.setting-item {

  height: 80px;
  padding: 20px;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 1px solid #e0e0e0;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.range-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 5px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1em;
  text-align: left;
  border-radius: 10px;
}

th, td {
  padding: 12px 15px;
  border: 1px solid #ddd;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}
</style>