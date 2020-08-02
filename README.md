# salary_email

此项目为一个简易的工资条邮箱发送GUI小工具，支持读取excel文件，批量发送工资条邮件。

程序入口： SalaryEmailRun.py

建议使用pyinstaller等打包工具打包为可执行程序使用
#### 打包成exe命令
```
pyinstaller --icon=./icon.ico --noconsole -p 自定义路径 -D SalaryEmailRun.py 
```
### 工资条表格说明
支持的文件格式为xls,xlsx文件，文件第一行为工资条事项，第一列为姓名，最后一列为邮箱地址，中间列可自行随意增减。如：

![avatar](static/exc.png)


### 主界面
![avatar](static/mainw1.png)
![avatar](static/mainw2.png)

### 发件邮箱登陆设置
![avatar](static/ac.png)

### 邮箱smtp设置
![avatar](static/smtp.png)

### 邮件底部落款设置
![avatar](static/sign.png)

### 发送线程设置
![avatar](static/th.png)