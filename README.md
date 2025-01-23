# yz-jmcomic
一个适用于yunzai的jm查本单js

## 想说的
- 本项目基于[Python API For JMComic (禁漫天堂)](https://github.com/hect0x7/JMComic-Crawler-Python/tree/master)简单改造而来
- 使用简单，容易上手
  
## 食用方法
- 先启动api`python app1.py`
- #jm查422866(仅允许私聊)

## 注意事项
- 需要准备python>=3.7环境 [戳我下载](https://www.python.org/downloads/windows/)
- 安装jmcomic库和Flask
  ```
  pip install jmcomic -i https://pypi.org/project -U
  pip install Flask
  ```
- 塞了简单的配置文件，如需自己更改可 [戳此查看](https://github.com/hect0x7/JMComic-Crawler-Python/blob/master/assets/docs/sources/option_file_syntax.md)
- yunzai不支持发送大于30mb的图片，可能需自行解决长图大于30m的问题
- 由于路径硬编码写入，所以需自己修改py文件和配置文件的路径

## 原理
- 使用Flask创建一个简单的webapi，并在node中用fetch请求和捕获异常
- 启动后本地地址应为 http://127.0.0.1:8000/jmd?jm=
- jmcomic库会先把本子下载，再进行长图拼接

## 许可证
本项目使用[MIT](https://zh.wikipedia.org/zh-hk/MIT%E8%A8%B1%E5%8F%AF%E8%AD%89)作为开源许可证

