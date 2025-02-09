<template>
  <div class="container">
    <Banner />
    <main>
      <div class="uploader">
        <EpubUploader @file-selected="handleFileSelect"/>
      </div>
      <div class="sidebar">
        <Settings @settings-change="handleSettingsChange" />
        <SendButton
          :file="file"
          :useTextFrequency="useTextFrequency"
          :textFrequency="textFrequency"
          :useCorpusFrequency="useCorpusFrequency"
          :corpusFrequency="corpusFrequency"
          @send-success="handleSendSuccess"
        />
      </div>
    </main>
    <footer>
      <p>© 2025 Epub-Rosetta</p>
    </footer>
  </div>
</template>


<script>
import Banner from './components/Banner.vue';
import EpubUploader from './components/EpubUploader.vue';
import Settings from './components/Settings.vue';
import SendButton from './components/SendButton.vue';

export default {
  components: {
    Banner,
    EpubUploader,
    Settings,
    SendButton
  },
  data() {
    return {
      file: null,
      useTextFrequency: false,
      textFrequency: 50,
      useCorpusFrequency: false,
      corpusFrequency: 50,
      fileUrl: null
     
    };
  },
  mounted() {
    document.title = 'Epub-Rosetta';
  },
  methods: {
    handleSettingsChange(settings) {
      console.log('Settings changed:', settings);
      this.useTextFrequency = settings.useTextFrequency;
      this.textFrequency = settings.textFrequency;
      this.useCorpusFrequency = settings.useCorpusFrequency;
      this.corpusFrequency = settings.corpusFrequency;
    },
    handleFileSelect(file) {
      console.log('Selected file:', file);
      this.file = file;
    },
    handleSendSuccess(file_url) {
      console.log('Send success:', file_url);
      this.fileUrl = file_url;
      
    }
  },

}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background-color: #ffffff;
}
/* header和main上下排列*/
main {
  width: 100%;
  display: flex;
  padding-top: 200px;
  align-items: flex-start;
  margin: 0 auto;

}

.uploader {
  position:relative;
  width: 700px;
  height: 900px;
  display: flex;
  border: 3px dashed #d1d5da;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  padding: 5px;
  background-color: #eae6e6;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.sidebar {
  display: flex;
  
  flex-direction: column;
  /* 内部元素垂直且靠近上方 */
  margin-left: 10px;
  height: 900px;
}

</style>
