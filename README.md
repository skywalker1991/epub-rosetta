# epub-rosetta
>罗塞塔石碑(Rosetta stone)的发现，使得人类首次能够解读古埃及的象形文字。本项目的目标是提供可以对多种语言的epub电子书进行解析，翻译，标注和语言学习的工具。

## 项目结构
项目采用前后端分离架构，前端采用Vue.js，后端采用Django提供RESTful API。

**结构**如下：
```shell
epub-rosetta
├── README.md
├── backend # 后端代码
│   └── epubrosetta
│       ├── epubrosetta
│       ├── wordwise # 单词解析模块
│           ├── epub.py # epub解析模块 
│           ├── wordwise.py # 单词解析模块
│           ├── stardict.py # stardict词典解析模块 
│           ├── test.db # 测试数据库 文件较大，请自行下载链接付后
├── frontend # 前端代码
```


## 启动方法
### 后端
1. 进入`backend/epubrosetta`目录
2. 下载并解压'test.db'文件到`backend/epubrosetta/wordwise`目录
```shell
#字典数据链接
链接: https://pan.baidu.com/s/1GI_KCZmVS7igCgZ87IScmg?pwd=xbgc 提取码: xbgc 
```
3. 安装python依赖
```shell
pip install -r requirements.txt
```
1. 启动Django服务
```shell
python manage.py runserver
```

### 前端
1. 进入`frontend/epub-rosetta`目录
2. 安装依赖
```shell
npm install
```
3. 启动Vue服务
```shell
npm run dev
```
4. 访问vite服务地址，如`http://localhost:5173/`


## 进度

- 2025.2.10 初步功能完成

