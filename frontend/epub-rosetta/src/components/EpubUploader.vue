<template>
  <div class="show-epub">
    <div
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
    <p>拖拽文件到此处或点击选择文件</p>
    <button @click="selectFile">选择文件</button>
    
  </div>
  <EpubReader v-if="file" :file="file"/>
    </div>


  
</template>

<script>
import EpubReader from "./EpubReader.vue";
import EventBus from '../event-bus';
export default {
  components: {
    EpubReader,
  },
  data() {
    return {
      fileInput: null,
      file: null,
    };
  },
  mounted() {
    this.fileInput = this.$refs.fileInput;
    EventBus.on('send-success', this.loadEpubFromUrl);
  },
  methods: {
    handleDrop(event) {
      const files = event.dataTransfer.files;
      if (files.length) {
        this.handleFile(files[0]);
      }
    },
    handleFileSelect(event) {
      const files = event.target.files;
      if (files.length) {
        this.handleFile(files[0]);
      }
    },
    selectFile() {
      this.fileInput.click();
    },
    handleFile(file) {
      console.log("Selected file:", file);
      this.file = file;
      this.$emit("file-selected", file);
      // 在这里处理文件上传逻辑
    },
    loadEpubFromUrl(url) {
      this.file = url;
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
}
.uploader {
  position: relative;
  border: 1px dashed #ccc;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 5px;
  width: 100%;
}
.uploader p {
  margin: 0;
  font-size: 16px;
}
.uploader button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
}
</style>
