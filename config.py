#coding=utf-8
http_timeout = 15 # HTTP连接超时阈值
try_to_connect_times = 10 # HTTP连接尝试次数

# account
username = 'xxx'  # 学号
password = 'xxx'  # 密码

# email
mail_host = 'smtp.qq.com' # 这里采用的是qq邮箱，如果不清楚邮箱发送原理，建议就按默认的qq邮箱，不要修改
mail_sender = '123456@qq.com' # 发送者和接收者填同一个邮箱
mail_password = 'xxx' # qq邮箱授权码，如果不清楚什么是授权码，请百度
mail_receiver_list = ['123456@qq.com', ] # 接收者，默认就自己一个

# scheduler
# 这里填写的是时间提醒策略
# 严正声明！！！本人不支持时间间隔设置得太短。
# 一方面，时间太短会加重网站负担，导致程序被封；另一方面，时间设得太短没有必要。
# 当开始跑这个程序的时候可以用1分钟测试是否可行，后面请改掉，否则程序很容易被封。
strategy = {'hours': 1} # 每小时，如果需要其它小时数，把1换掉就行
# strategy = {'minutes': 30} # 每30分钟，如果需要其它分钟数，把30替换掉就行