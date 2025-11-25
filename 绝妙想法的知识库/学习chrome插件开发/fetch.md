好消息！这个问题似乎已于2020年2月7日修复（相关链接：https://bugs.chromium.org/p/chromium/issues/detail?id=661827）。我会保留这些内容，以防问题再次出现。


# Fetch API 行为不一致问题

之前在11月的一篇帖子中，我提到过在 Manifest V3 环境下，使用 Fetch API 加载跨域资源（配置了"<all_urls>"或"*://*/*"权限）时遇到的困难。

目前我认为，这其实是 Service Worker（服务工作线程）的问题，而非 Manifest V3 本身的问题。


## 代码示例

### 两个测试中用到的 `background.js` 代码完全相同：
```javascript
fetch("https://www.example.com/")
  .then(r => r.text())
  .then(console.log);
```


### Service Worker 版本的 `manifest.json` 配置：
```json
{
  "name": "SW Fetch",
  "description": "Service Worker Fetch Test",
  "version": "0.1.1",
  "permissions": ["<all_urls>"],
  "background": {
    "service_worker": "background.js"  // 使用 Service Worker 作为后台
  },
  "manifest_version": 2
}
```


## 测试结果

当使用普通后台脚本（非 Service Worker）时，能成功获取 example.com 的内容；但使用 Service Worker 版本时，会因“跨域资源共享（CORS）政策”而失败。

测试环境为 Chrome Canary 80.0.3987.0 版本；在稳定版 Chrome 中，可能会提示“background.service_worker 尚未正式支持”的错误。

看起来这可能是一个存在已久的已知bug：https://bugs.chromium.org/p/chromium/issues/detail?id=661827