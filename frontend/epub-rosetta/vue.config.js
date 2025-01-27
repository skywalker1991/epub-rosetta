module.exports = {
    devServer: {
      proxy: {
        '/api': {
          target: 'https://your-backend-api.com', // 后端服务器地址
          changeOrigin: true,
          pathRewrite: { '^/api': '' }
        }
      }
    }
  };