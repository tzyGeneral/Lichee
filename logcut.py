import datetime
import os

DELETE_DAYS = 100  # 日志删除天数
FILE_TYPE = '.log'  # 日志文件后缀名

# 获取当前文件夹作为日志文件夹
log_file_path = os.getcwd()
# 拿到当前目录下的所有 log 文件
log_file_list = list(filter(None, [f if os.path.splitext(f)[1] == FILE_TYPE else '' for f in os.listdir(log_file_path)]))

today = datetime.date.today()
yesterdayFileName = 'log-' + str(today - datetime.timedelta(days=1)) + '.tar.gz'

# 删除日期文件名
deleteFileName = 'log-' + str(today - datetime.timedelta(days=DELETE_DAYS))+'.tar.gz'

# 压缩日志
try:
    os.system('tar -czvf ./%s %s' % (yesterdayFileName, ' '.join(log_file_list)))
except Exception as e:
    print("压缩日志出现错误-", e)

# 删除所有log,重新创建文件
os.system('rm -rf ./*%s && touch %s' % (FILE_TYPE, ' '.join(log_file_list)))

# 删除过期日志压缩包
if os.path.exists('./' + deleteFileName):
    os.system('rm -rf ./' + deleteFileName)

# nginx重读日志文件
os.system('nginx -s reopen')