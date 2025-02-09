<template>
  <div v-if="isVisible" class="epub-reader">
    <div ref="viewer" class="viewer"></div>
    <div class="controls">
      <button class="btn" @click="prevPage">上一页</button>
      <button class="btn" @click="nextPage">下一页</button>
      <button class="btnred" @click="close">关闭</button>
    </div>
  </div>
</template>

<script>
import ePub from 'epubjs';
import EventBus from '../event-bus';

export default {
  props: {
    file: {
      type: [File, String],
      required: true
    }
  },
  data() {
    return {
      book: null,
      rendition: null,
      isVisible: true
    }
  },
  watch: {
    file: {
      immediate: true,
      handler(newFile) {
        if (newFile) {
          if (typeof newFile === 'string') {
            this.loadEpubFromUrl(newFile);
          } else {
            this.loadEpubFromFile(newFile);
          }
        }
      }
    }
  },

  methods: {
    loadEpubFromFile(file) {
      if (this.book) {
        this.book.destroy();
        this.book = null;
        this.rendition = null;
      }
      const reader = new FileReader();
      reader.onload = (event) => {
        this.book = ePub(event.target.result);
        this.rendition = this.book.renderTo(this.$refs.viewer, {
          method: 'default',
          width: '100%',
          height: '100%'
        });
        this.rendition.display();
        EventBus.emit('new-reader');
        this.applyCustomCss();
      };
      reader.readAsArrayBuffer(file);
    },
    loadEpubFromUrl(url) {
      if (this.book) {
        this.book.destroy();
        this.book = null;
        this.rendition = null;
      }
      this.book = ePub(url);
      this.rendition = this.book.renderTo(this.$refs.viewer, {
        method: 'default',
        width: '100%',
        height: '100%'
      });
      this.book.ready.then(() => {
        this.rendition.display();
      });
    },
    applyCustomCss() {
        const style = `
        ruby {
          ruby-position: over;
        }
        rt {
          font-size: 0.3em;
          color: #555;
        }
        rp {
          display: none;
        }
      `;
    },
    prevPage() {
      if (this.rendition) {
        this.rendition.prev();
      }
    },
    nextPage() {
      if (this.rendition) {
        this.rendition.next();
      }
    },
    close() {
      if (this.book) {
        this.book.destroy();
        this.book = null;
        this.rendition = null;
      }
      this.$emit('close');
      EventBus.emit('close-reader');
    }
  },
  beforeUnmount() {
    EventBus.off('send-success', this.loadEpubFromUrl);
  }

}
</script>

<style scoped>
.epub-reader {
  width: 600px;
  height: 900px;
  overflow: hidden;
  position: relative;
  background-color: #ffffff;
  border: 1px solid #d1d5da;
  border-radius: 6px;
}
.viewer {
  width: 100%;
  height: 100%;
}
.controls {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}
.btn {
  padding: 10px 20px;
  font-size: 14px;
  color: #fff;
  background-color: #0366d6;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.btn:hover {
  background-color: #005cc5;
}
</style>