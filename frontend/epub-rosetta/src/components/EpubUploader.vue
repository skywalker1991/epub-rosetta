<template>
  <div class="show-epub">
    <div
    v-if="!file"
    class="uploader"
    @dragover.prevent
    @dragenter.prevent
    @drop.prevent="handleDrop"
  >
    <input
      type="file"
      @change="handleFileSelect"
      ref="fileInput"
      accept=".epub"
      hidden
    />
    <img class="icon"    :src="bookIcon" alt="book" />
    <p class="dragtext">拖拽文件到此处释放</p>
    <button class="btn" @click="selectFile">从设备中选择文件</button>
    <p class="subtext">目前支持文件格式：.epub</p>
    <p class="subtext">目前只支持English,日本語努力开发中💪</p>
    <p class="subtext">文件大小不超过50MB</p>
    
  </div>
  <EpubReader v-if="file" :file="file" @close = "handleClose"/>
    </div>
</template>

<script>
import EpubReader from "./EpubReader.vue";
import EventBus from '../event-bus';
import bookIcon from '../assets/book.svg';

export default {
  components: {
    EpubReader,
  },
  data() {
    return {
      fileInput: null,
      file: null,
      bookIcon: bookIcon,
      errorMessages: null,
    };
  },
  mounted() {
    this.fileInput = this.$refs.fileInput;
    EventBus.on('send-success', this.loadEpubFromUrl);
  },
  methods: {
    handleDrop(event) {
      const files = event.dataTransfer.files;
      if (files.length>0) {
        const file = files[0];
        this.handleFile(files[0]);
        if (this.validateFile(file)) {
          this.handleFile(file);
        } else {
          alert('文件格式不正确');
          this.file = null;
        }
      }
    },
    handleFileSelect(event) {
      const files = event.target.files;
      if (files.length>0) {
        const file = files[0];
        if (this.validateFile(file)) {
          this.handleFile(file);
        } else {
          alert('文件格式不正确');
          this.file = null;
        }
      }
    },
    validateFile(file) {
      const maxSize = 50 * 1024 * 1024; // 50MB
      const allowedTypes = ['application/epub+zip'];

      if (file.size > maxSize) {
        this.errorMessage = '文件大小不能超过50MB';
        return false;
      }

      if (!allowedTypes.includes(file.type)) {
        this.errorMessage = '只支持EPUB文件格式';
        return false;
      }

      return true;
    },
    selectFile() {
      this.fileInput.click();
    },
    handleFile(file) {
      this.file = file;
      this.$emit("file-selected", file);
      // 在这里处理文件上传逻辑
    },

    loadEpubFromUrl(url) {
      this.file = url;
    },
    handleClose() {
      this.file = null;
    },
  },
};
</script>

<style scoped>
.show-epub {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  background-color: #ffffff00;
}

.icon {
  width: 50px;
  height: 50px;
  margin-bottom: 20px;
}

.uploader {
  position: relative;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  width: 100%;
  height: 100%;
}
.dragtext {
  margin: 0;
  font-size: 30px;
  color: #040404;
  font-weight: bold;
}
.uploader .btn {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  color: #070707;
  background-color: #f4d121;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.5s;
}
.uploader .btn:hover {
  background-color: #005cc5;
}

.subtext {
  font-size: 20px;
  color: #666;
  margin-top: 40px;
}
</style>
