# BJTU Homework to Microsoft ToDo

本项目基于 Microsoft Graph api 开发,支持一键将未完成的作业上传至 Microsoft ToDo。

## Before use this app

在app.py目录下创建 config.cfg 内容如下，需要填写你的学号:

``` text
[azure]
clientId = 822c6036-dd15-4f7f-86f8-6e54218319f7
graphUserScopes = User.Read Mail.Read Mail.Send

[gethw]
xqCode = 2024202502
studentId = <填写你的学号>
savePath = ./
jsonFile = homework.json
```

目前仅支持默认密码

添加参数 -a 自动同步作业

## Notification

1. homework.json 会在程序运行中自动创建，这个文件非常重要！！！大家别轻易动它

2. 如果有任何报错请先检查有无创建config.cfg并且填写学号， 学期代码（2024202502 代表2024-2025第二学期），

## Usage

创建环境:
``` bash
git clone https://github.com/kaguramena/BJTU-homework-todo.git
cd BJTU-homework-todo.git
conda create -n "BJTU-homework-todo" python=3.10
conda activate BJTU-homework-todo
pip install -r requirements.txt
```

运行程序:

``` bash
python app.py -a
```

## 如果你真的还有问题

直接发邮件到 kaguramena@outlook.com, 解答世间万物