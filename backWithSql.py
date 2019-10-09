#coding:utf-8

import os, zipfile
import time
import requests 
import datetime
import hashlib
import urllib3
# 禁用SSL提示
urllib3.disable_warnings()

strTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

# 要备份的目录
s_dir=r'/www/wwwroot/kekeacg.com'
# 备份目录压缩的临时文件位置
zip_out=r'/www/wwwroot/webback/'
# 备份的文件名
back_name = 'kekeacg.com'
# 保存地址
oneIndex_url='https://driver.kekeacg.com/?/back/'
# salt 加密的盐值，防止任何人都能上传，保持和BackController.php的一致
salt = 'test123456'

#定义服务器，用户名、密码、数据库名称（多个库分行放置）和备份的路径
DB_HOST = 'localhost'
DB_USER = 'kk'
DB_USER_PASSWD = '123456'
DB_NAME = 'kk'
BACKUP_PATH = '/www/wwwroot/kekeacg.com/db/'

DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH

#创建备份文件夹
if not os.path.exists(TODAYBACKUPPATH):
        os.makedirs(TODAYBACKUPPATH)

#定义执行备份脚本，读取文件中的数据库名称，注意按行读写，不校验是否存在该库
def run_backup_sql():
    dumpcmd = "mysqldump -u" +DB_USER + " -p"+DB_USER_PASSWD+" " +DB_NAME+" > "+TODAYBACKUPPATH +"/"+DATETIME+DB_NAME+".sql"
    print dumpcmd 
    os.system(dumpcmd)
        
def delete_sql(): 
    remove_file(TODAYBACKUPPATH +"/"+DATETIME+DB_NAME+".sql")

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED)
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
    
def upload_file(zip_out,file_name):
    files = {'file': open(zip_out+file_name, 'rb')}
    headers = {'valid': hashlib.md5( file_name + salt ).hexdigest()}
    response = requests.post(oneIndex_url, files=files, headers=headers, verify=False) 
    print response.text

def remove_file(file_name):
    if(os.path.exists(file_name)):
        os.remove(file_name)
        print 'remove ' + file_name +' success!'
    else:
        print "file not found！"

if __name__ == '__main__':
    
    if not os.path.exists(zip_out):
        os.makedirs(zip_out)
    file_name = strTime + back_name+'.zip'
    temp_file = zip_out+file_name
    #run_backup_sql()
    make_zip(s_dir,temp_file)
    upload_file(zip_out,file_name)
    # 注释掉remove这句的话，可以备份一个在本地服务器。
    #delete_sql()
    remove_file(temp_file)
    
