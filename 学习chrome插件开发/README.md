# Manifest V3 介绍

现在是时候认真了解 Manifest V3 了，以下是核心信息和官方参考链接，帮你快速掌握关键内容。

### 1. 官方迁移参考
想要深入学习或迁移到 Manifest V3，可以查看这两个核心官方文档：
- [Manifest V3 迁移指南](https://developer.chrome.com/extensions/migrating_to_manifest_v3)
- [Service Workers 迁移指南](https://developer.chrome.com/extensions/migrating_to_service_workers)


### 2. Manifest V3 的主要调整
这些是 Manifest V3 相比旧版本的关键变化，也是实际使用中需要重点注意的点：
- **权限拆分**：网站权限和 API 权限不再混为一谈，而是分成了两个独立的类别。
- **Service Workers 替代后台脚本**：不再支持持久化的后台脚本，需要优先使用 Service Workers 处理相关逻辑（比如之前用后台脚本做的内容脚本执行、右键菜单绑定等）。
- **背景环境无 DOM**：Manifest V3 的背景环境里没有 DOM，像“img.onload 后绘制到 canvas”这类依赖 DOM 的操作无法直接实现（目前该问题可能与 Service Workers 相关，而非 V3 本身的设计问题）。
- **本地存储的影响**：使用本地存储时，需要更合理地设计代码，同时要关注全局事件和系统的运行逻辑。
