# BJTU Homework to Microsoft ToDo

本项目基于 Microsoft Graph api 开发,支持一键将未完成的作业上传至 Microsoft ToDo。

## Usage

在根目录下创建 config.cfg 内容如下:

``` text
[azure]
clientId = 822c6036-dd15-4f7f-86f8-6e54218319f7
graphUserScopes = User.Read Mail.Read Mail.Send
clientSecret = 

[gethw]
xqCode = 2024202502 (学期代码)
studentId = 22281110 （学号）
```

目前仅支持默认密码

添加参数 -a 自动同步作业