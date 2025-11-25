# 在Service Workers中测试跨域Fetch（仅V3扩展）

有专家指出，只要配置了正确的`host_permissions`，V3版本的Chrome扩展应该能通过`fetch` API加载所有资源。以下是具体说明：


## 1. 配置文件（manifest.json）
创建一个名为`manifest.json`的文件，内容如下：
```json
{
  "name": "CORTester",
  "version": "0.0.0.1",
  "description": "测试从Service Workers发起跨域Fetch请求",
  "host_permissions": ["<all_urls>"],  // 允许访问所有网址
  "background": { "service_worker": "stub.js" },  // 关联服务工作线程文件
  "manifest_version": 3  // 明确使用V3版本
}
```


## 2. 服务工作线程（stub.js）
创建一个名为`stub.js`的文件（和`manifest.json`放在同一文件夹），它的作用只是确认自己已加载：
```javascript
console.log("服务工作线程已加载。");
```


## 3. 如何测试
按照以下步骤操作，测试扩展能否发起跨域请求：

1. 打开Chrome浏览器，访问`chrome://serviceworker-internals`（服务工作线程管理页面）。
2. 再打开一个新标签，访问`chrome://extensions`（扩展管理页面）。
3. 开启右上角的“开发者模式”，然后把存放`manifest.json`和`stub.js`的文件夹拖进这个页面，加载扩展。
4. 记下扩展的ID（一串小写字母组成的长字符串，类似`deadbeefdeadbeefdeadbeefdeadbeef`）。
5. 回到`chrome://serviceworker-internals`页面，找到与你的扩展ID匹配的服务工作线程。
6. 如果它没在运行，点击“Start”启动。
7. 启动后点击“Inspect”，会弹出一个调试窗口。
8. 在调试窗口切换到“Console”（控制台）标签，会看到“服务工作线程已加载”的提示，说明准备就绪。


## 4. 测试案例1：被CORS阻止的请求
在控制台输入以下代码，尝试请求一个不支持跨域的资源：
```javascript
fetch("https://phistuck-app.appspot.com").then(r=>r.arrayBuffer()).then(console.log);
```

### 预期结果：
理论上应该返回该网站的HTML内容（以`<!doctype html>`开头）。

### 实际结果：
请求被CORS策略阻止，控制台会显示类似错误：
```
从源地址'chrome-extension://你的扩展ID'访问'https://phistuck-app.appspot.com/'的请求被CORS策略阻止：请求的资源上没有'Access-Control-Allow-Origin'头。如果只需要不透明响应，可以将请求模式设为'no-cors'来禁用CORS。

Uncaught (in promise) TypeError: 无法获取资源
```


## 5. 测试案例2：支持CORS的资源请求
在控制台输入以下代码，请求一个支持跨域的资源：
```javascript
fetch("https://widgets.pinterest.com/v1/urls/count.json?url=https%3A%2F%2Fwww.flickr.com%2Fphotos%2Fkentbrew%2F6851755809%2F").then(r=>r.text()).then(console.log);
```

### 实际结果：
请求成功，控制台会显示返回的内容：
```
receiveCount({"url":"https://www.flickr.com/photos/kentbrew/6851755809/","count":65326})
```


说明：V3扩展能否成功发起跨域请求，主要取决于目标资源是否支持CORS（即是否返回`Access-Control-Allow-Origin`头），即使扩展配置了`host_permissions`也无法绕过这一限制。