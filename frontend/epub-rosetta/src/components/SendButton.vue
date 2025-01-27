<template>
  <div class="send-button">
    <button @click="sendData">注释词汇</button>
  </div>
</template>

<script>
export default {
  props: {
    file: {
      type: File,
      required: true
    },
    useTextFrequency: {
      type: Boolean,
      required: true
    },
    textFrequency: {
      type: Number,
      required: true
    },
    useCorpusFrequency: {
      type: Boolean,
      required: true
    },
    corpusFrequency: {
      type: Number,
      required: true
    }
  },
  methods: {
    async sendData() {
      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('useTextFrequency', this.useTextFrequency);
      formData.append('textFrequency', this.textFrequency);
      formData.append('useCorpusFrequency', this.useCorpusFrequency);
      formData.append('corpusFrequency', this.corpusFrequency);

      try {
        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });
        const result = await response.json();
        console.log('上传成功:', result);
      } catch (error) {
        console.error('上传失败:', error);
      }
    }
  }
}
</script>

<style scoped>
.send-button {
  width: 300px;
  height: 300px;
  margin-left: 30px;
  margin-top: 10px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
}
</style>