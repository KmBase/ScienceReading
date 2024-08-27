# 安装

Setup安装包[ScienceReading.exe](https://github.com/KmBase/ScienceReading/releases/download/release/ScienceReading-1.0.0e-Setup-Windows-64.exe)

# 使用

## 启动界面

![launch.png](https://raw.githubusercontent.com/KmBase/ScienceReading/master/docs/launch.png)

## 搜索

搜索框输入关键词，点击搜索按钮或回车。

![example01.png](https://raw.githubusercontent.com/KmBase/ScienceReading/master/docs/example01.png)

![example02.png](https://raw.githubusercontent.com/KmBase/ScienceReading/master/docs/example02.png)

## 下载

双击下载，已限制下载次数，请勿频繁下载。

![example03.png](https://raw.githubusercontent.com/KmBase/ScienceReading/master/docs/example03.png)


## 取消

右键双击取消搜索或下载。

![example04.png](https://raw.githubusercontent.com/KmBase/ScienceReading/master/docs/example04.png)


## 其他

左键双击打开下载目录。

![example05.png](https://raw.githubusercontent.com/KmBase/ScienceReading/master/docs/example04.png)

# 二次开发

**注意**：核心代码未开源，此部分仅为二次开发示例

## 创建并激活venv

```bash
cd ScienceReading
python -m venv venv
venv\Scripts\activate.bat
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 执行脚本

```bash
python main.py
```

## 打包脚本

```bash
python build.py
```
