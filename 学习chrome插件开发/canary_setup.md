# 在Chrome Canary上测试Manifest V3扩展（Mac版）
核心目的是让Chrome Canary（测试版）和正式版Chrome同时运行，互不干扰，专门用来测试Manifest V3扩展，不影响你日常用的正式版Chrome。


## 1. 下载并安装Chrome Canary
1. 打开链接下载：[https://www.google.com/chrome/canary/](https://www.google.com/chrome/canary/)
2. 直接安装即可，它不会覆盖你已有的正式版Chrome。
3. 验证是否安装成功：
   - 打开「终端」，输入命令 `cd /Applications` 并回车（进入应用程序文件夹）。
   - 再输入 `ls "Google Chrome*"` 并回车，能看到两个文件：`Google Chrome Canary.app`（测试版）和 `Google Chrome.app`（正式版），就说明安装好了。


## 2. 新建开发者专用配置文件
为了让Canary的设置不跟正式版混淆，需要给它建一个独立配置：
1. 保持「终端」还在 `/Applications` 目录下，输入命令：  
   `open -a "Google Chrome Canary" --args --user-data-dir=/dev/null`  
   回车后，会打开一个全新的Chrome Canary（没有任何你正式版的书签、插件）。
2. 点击Canary窗口右上角的「三个点」菜单，新建一个配置文件（比如命名为“Canary测试”，默认红色小鸟图标就行），然后切换到这个新配置。


## 3. 固定到 Dock 方便后续使用
右键点击 Dock 栏里的黄色Chrome Canary图标，选择「保留在程序坞」，之后直接点图标就能打开，不用再输终端命令。


## 4. 测试是否能正常用（关键：测V3扩展）
1. 先关闭所有Chrome窗口（包括正式版和Canary），然后分别重新打开。
2. 此时会出现两个独立的Chrome窗口：一个是你日常用的正式版，一个是刚设置好的Canary测试版。
3. 测试V3扩展：把你的Manifest V3测试扩展拖进Canary的「chrome://extensions」页面（打开扩展页需先开启右上角“开发者模式”），安装成功后，去正式版的「chrome://extensions」里看，不会出现这个扩展——说明两者完全独立，你可以安心在Canary里测V3功能了。
