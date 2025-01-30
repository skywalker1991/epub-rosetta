<template>
  <div class="send-button">
    <button @click="sendData">
      <span v-if="isProcessing">处理中<span class="dots">...</span></span>
      <span v-else>注释词汇</span>
    </button>
    <a v-if="fileUrl" :href="fileUrl" download>下载处理后的文件</a>
  </div>
</template>

<script>

import EventBus from '../event-bus';

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
  data() {
    return {
      isProcessing: false,
      fileUrl: null,
    }
  },
  methods: {
    async sendData() {
      this.isProcessing = true;
      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('useTextFrequency', this.useTextFrequency);
      formData.append('textFrequency', this.textFrequency);
      formData.append('useCorpusFrequency', this.useCorpusFrequency);
      formData.append('corpusFrequency', this.corpusFrequency);

      try {
        const response = await fetch('http://127.0.0.1:8000/api/wordwise/', {
          method: 'POST',
          body: formData
        });
        if (response.status === 200) {
          console.log('上传成功',response);
          const data = await response.json();
          const file_url = data.file_url;
          EventBus.emit('send-success', file_url);
          console.log('file_url:', file_url);
          this.fileUrl = file_url;

        }
      } catch (error) {
        console.error('上传失败:', error);
      } finally {
        this.isProcessing = false;
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
  background-color: #007bff;
}


button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.dots::after {
  content: '';
  display: inline-block;
  width: 1em;
  text-align: left;
  animation: ellipsis steps(4, end) 900ms infinite;
}

@keyframes ellipsis {
  0%, 100% {
    content: '';
  }
  25% {
    content: '.';
  }
  50% {
    content: '..';
  }
  75% {
    content: '...';
  }
}
</style>