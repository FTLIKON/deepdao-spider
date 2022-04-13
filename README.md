
---

# **deepdao数据爬虫+入库**

## 代码结构
```
├── anal.py -> 将数据解析至本地txt
├── main.py -> 爬虫主代码
└── todb.py -> 将本地txt数据入库
└── README.md
```

## 依赖环境
- python 3.6.4
- requests
- pymysql

## 项目运行
1. 拉取本项目，进入项目目录。
2. 开始抓取。抓取过程中会在当前目录下生成几个解析的txt，便于备份数据以及校验。
```bash
python3 main.py
```
3. 等待抓取完成后，确认生成了6个txt文件（分别对应6个数据表），即可开始执行入库脚本。
```bash
python3 todb.py
```