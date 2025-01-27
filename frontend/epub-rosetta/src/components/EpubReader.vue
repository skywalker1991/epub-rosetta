<template>
  <div class="epub-reader">
    <div ref="viewer" class="viewer"></div>
    <div class="controls">
      <button @click="prevPage">上一页</button>
      <button @click="nextPage">下一页</button>
    </div>
  </div>
</template>

<script>
import ePub from 'epubjs';

export default {
  props: {
    file: {
      type: File,
      required: true
    }
  },
  data() {
    return {
      book: null,
      rendition: null
    }
  },
  watch: {
    file: {
      immediate: true,
      handler(newFile) {
        if (newFile) {
          this.loadEpub(newFile);
        }
      }
    }
  },

  methods: {
    loadEpub(file) {
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
        this.applyCustomCss();
      };
      reader.readAsArrayBuffer(file);
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
    }
  }

}
</script>

<style scoped>
.epub-reader {
  width: 600px;
  height: 900px;
  overflow: hidden;
  position: relative;
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
button {
  padding: 10px 20px;
  font-size: 10px;
  cursor: pointer;
}
</style>