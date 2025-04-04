# yz-jmcomic
一个适用于yunzai的jm查本单js
> [!WARNING]
> 爱护jm，不要爬那么多本，西门
> -- 官网地址: https://18comic.vip

## 想说的
- 本项目基于[Python API For JMComic (禁漫天堂)](https://github.com/hect0x7/JMComic-Crawler-Python/tree/master)简单改造而来
- 使用简单，容易上手
- 一键部署插件包已经开发：[戳我](https://github.com/excellen114514/jmcomic-plugin)
  
## 食用方法
- js文件直接下载后放到到example文件夹即可
- 随便找一个文件夹存放api,下载bat文件直接运行,会使用git下载
  ```shell
  ./run.bat
  ```
- 启动api
  ```shell
  python3 app.py
  ```
- 然后对bot发送 #jm查{本子号} (仅允许私聊)

## 注意事项
- 需要准备python>=3.7环境 [戳我下载](https://www.python.org/downloads/)
- 安装jmcomic库和Flask(依赖文件)
  ```python
  pip install -r requirements.txt
  ```
- yunzai根目录执行
  ``` node
  pnpm install axios -w
  ```
- 塞了简单的配置文件，如需自己更改可 [戳此查看](https://github.com/hect0x7/JMComic-Crawler-Python/blob/master/assets/docs/sources/option_file_syntax.md)
- ~~对大小添加了限制，大于30mb的仅发送官网地址~~
- 现在在icqq环境下可以发送pdf格式的文件了
- api会每隔一小时删除一次工作目录下除了long和pdf文件夹的所有文件夹
- 脚本有简单的崩溃重启，非正常退出(0 code)会重新执行命令
- ~~由于路径硬编码写入，所以需自己修改py文件和配置文件的路径喵~~
- 支持了.env环境变量了喵,现在你只需要在.env自定义你存放的目录就好了奥

## 原理
- 使用Flask创建一个简单的webapi，并在node中用fetch请求和捕获异常
- 启动后本地地址应为 http://127.0.0.1:8000/jmd?jm=
- pdf请求地址为 http://127.0.0.1:8000/jmdp?jm=
- jmcomic库会先把本子下载，再进行长图拼接

## 许可证
本项目使用[MIT](https://zh.wikipedia.org/zh-hk/MIT%E8%A8%B1%E5%8F%AF%E8%AD%89)作为开源许可证

## 感谢
[Python API For JMComic (禁漫天堂)](https://github.com/hect0x7/JMComic-Crawler-Python/tree/master)
