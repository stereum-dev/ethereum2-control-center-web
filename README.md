# ethereum2-control-center-web

## developer setup
### `ethereum2-control-center-web/frontend/vue.config.js`

add:
```
module.exports = {
  publicPath: "/public/",
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8082/",
        logLevel: "debug",
        changeOrigin: true
      }
    }
    }
};
```

### `ethereum2-control-center-web/frontend/public/index.html`

replace:
```
      window.ENTRY = '/control-center';
```

