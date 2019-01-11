# grader-reminder
上海科技大学研究生成绩提醒工具

### 运行方法

##### ！！！注意：只能运行在python3环境中

#### 创建conda虚拟环境并激活
```bash
conda create -n grade_reminder pip
conda activate grade_reminder
```

#### 安装依赖包
```bash
pip install requests bs4 schedule 
```
#### 设置参数
参数设置在`config.py`文件里，各个参数都有注释，仔细看

#### 运行脚本
```bash
python remind_grade.py &
```
