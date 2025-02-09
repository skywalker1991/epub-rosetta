<template>
  <div class="send-button">
    <button class="btn" @click="sendData" :disabled="isProcessing || !file || isSended || isClose">
      <span v-if="isProcessing">处理中<span class="dots">...</span></span>
      <span v-else>注释词汇</span>
    </button>
    <div class="download">
      <a v-if="fileUrl" :href="fileUrl" download>下载处理后的文件</a>
    </div>
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
      isDisable: false,
      isSended: false,
      isClose: false
    }
  },
  mounted() {
    EventBus.on('send-success', () => {
      this.isSended = true;
    });
    EventBus.on('close-reader', () => {
      this.isClose = true;
      this.isSended = false;
      this.isProcessing = false;
      this.fileUrl = null;
    });
    EventBus.on('new-reader', () => {
      this.isClose = false;
      this.fileUrl = null;
    });
  },
  beforeUnmount() {
    EventBus.off('send-success', () => {
      this.isDisable = true;
    });
    EventBus.off('close-reader', () => {
      if (this.isDisable) {
        this.isDisable = false;
      } else {
        this.isDisable = true;
      }
    });
  },
  methods: {
    async sendData() {
      //如果this.file存在，则执行按钮
      
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
  margin-left: 10px;
  margin-top: 10px;
}
.btn {
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #0366d6;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
}
.btn:disabled {
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
.download {
  margin-top: 10px;
  align-items: center;
}
</style>