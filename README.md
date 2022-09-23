# Login_ele
Obtain the electricity bill data of the one-card platform developed by Zhengyuan Wisdom.
获取正源智慧开发的一卡平台电费数据
+ 此项目基于`正元智慧·一卡通`平台编写

+ 项目部署推荐使用`pipenv`进行包管理
  1. 设置永久 `pip` 源(windows)
  ```python
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  ```
  2. 安装 `Python` 包管理
  ```python
  pip install pipenv
  # 安装依赖
  pipenv requests ddddocr pymysql
  ```
  3. 配置项
  ```ini
  在 base_sql.save_to_mysql 中配置Mysql
  在 task_allele_data 中配置一卡通主机地址
  ```
---
## 未来发展
![develp](https://user-images.githubusercontent.com/99723642/191985727-da6a627f-025b-4a87-b174-d752ca5e0cec.png)
