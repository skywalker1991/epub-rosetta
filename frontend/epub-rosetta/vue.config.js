module.exports = {
    devServer: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1', // 后端服务器地址
          changeOrigin: true,
          pathRewrite: { '^/api': '' }
        }
      }
    }
  };