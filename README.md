# 闲鱼爬虫

## 准备环境

1. [Splash](https://splash.readthedocs.io/en/stable/):一个js渲染服务
```
docker run --name splash -d -p 8050:8050 scrapinghub/splash
```

2. [Jserver](): 使用golang封装的js解释服务，把要执行的js脚本让服务器运行并返回结果。
```
docker run --name jserver -d -p 18080:8080 sadeye/jserver:slim
```

3. 复制config.example.yml到与其同级目录为config.yml,替换其中的SPLASH和JServer的地址与端口
```
SPLASH:
  # It't docker image for scrapinghub/splash
  URL: 192.168.121.128
  PORT: 8050

JServer:
  # It't docker image for sadeye/jserver:slim
  URL: 192.168.121.128
  PORT: 18080
```

## Quick start
```
python main.py
```
![运行效果](https://raw.githubusercontent.com/ngdyj/spider-taobao/master/docs/pic/p1.gif)
