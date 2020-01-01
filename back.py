#coding:utf-8

import os, zipfile
import time
import requests
import hashlib
import urllib3
# 禁用SSL提示
urllib3.disable_warnings()

strTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

# 要备份的目录
s_dir=r'/www/wwwroot/driver.kekeacg.com'
# 备份目录压缩的临时文件位置
zip_out=r'/www/wwwroot/webback/'
# 备份的文件名
back_name = 'driver.kekeacg.com'
# 保存地址
oneIndex_url='https://driver.kekeacg.com/?/back/'
# salt 加密的盐值，防止任何人都能上传，保持和BackController.php的一致
salt = 'test123456'

# 2020年1月1日 增加zip压缩包加密
ZIP_PASSWORD = 'xhvps.info'


#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
            zipf.write(pathfile, arcname)
    if ZIP_PASSWORD:
        zipf.setpassword(ZIP_PASSWORD)
    zipf.close()
    
def upload_file(zip_out,file_name):
    files = {'file': open(zip_out+file_name, 'rb')} 
    headers = {'valid': hashlib.md5( file_name + salt ).hexdigest()}
    response = requests.post(oneIndex_url, files=files, headers=headers, verify=False) 
    print response.text

def remove_file(file_name):
    if(os.path.exists(file_name)):
        os.remove(file_name)
        print 'remove success!'
    else:
        print "file not found！"

if __name__ == '__main__':
    
    if not os.path.exists(zip_out):
        os.makedirs(zip_out)
    file_name = strTime + back_name+'.zip'
    temp_file = zip_out + file_name
    make_zip(s_dir,temp_file)
    upload_file(zip_out,file_name)
    # 注释掉remove这句的话，可以备份一个在本地服务器。
    remove_file(temp_file)
    