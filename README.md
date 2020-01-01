# 自动备份网站到oneIndex的脚本

## 我的博客
https://kekeacg.com/archives/27.html

## 缘由
以前买了个服务器，搬瓦工的，但是后来到期了，没有续费，等到再想弄博客的时候后悔莫及，因为文件都没有备份，那可是一点一点调出来的css，到最后都没有了。所以，这次要把网站自动保存到oneDriver上，希望能有个备份。

## 使用方法

`该备份方法需要配合oneIndex使用，oneIndex:https://github.com/donwa/oneindex`

`2020年1月1日增加了压缩分卷，记得修改controller运行分卷的扩展，我是直接删掉了扩展的校验！`

1、安装好oneIndex、python

2、将BackController.php放到oneIndex的controller目录。
```
	#配置加密的盐值保持和back.py的一致
	private $salt = "test123456";
	#配置临时目录
	private $tmp_path = "/tmp/upload/";
```

3、在oneIndex的index.php页面的第58行（列目录前面）增加一行
```
route::any('/back','BackController@index');
```

4、将back.py放到要备份的同级目录中，并且配置好以下参数
```
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
```
