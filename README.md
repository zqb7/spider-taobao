# 闲鱼爬虫

## 提示
闲鱼网页端，官方已停止维护。此脚本已不能使用

## 准备环境

1. [Splash](https://splash.readthedocs.io/en/stable/):一个js渲染服务
```
docker run --name splash -d -p 8050:8050 scrapinghub/splash
```

2. 复制config.example.yml到与其同级目录为config.yml,替换其中的SPLASH和JServer的地址与端口
```
SPLASH:
  # It't docker image for scrapinghub/splash
  URL: 192.168.121.128
  PORT: 8050
```

## Quick start
```
python main.py
```
![运行效果](https://raw.githubusercontent.com/ngdyj/spider-taobao/master/docs/pic/p1.gif)
