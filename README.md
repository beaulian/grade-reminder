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

#### 遇到的bug
之前遇到`由于目标计算机积极拒绝，无法连接`之类的错误，猜想是ip被封了。现在经过排查，
是研究生系统网站不稳定导致的，所以我现在把程序改了一下，连接研究生系统的时候尝试10次。

#### 写在后面的话
我写这个的初衷是为了方便大家查成绩，乱改程序，对研究生系统进行洪水攻击等行为均和本人无关，一切后果自负！

#### 联系
有问题联系我 <guanjw@shanghaitech.edu.cn>
