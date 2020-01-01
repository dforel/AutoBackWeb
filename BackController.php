<?php 

class BackController{
	#配置加密的盐值保持和back.py的一致
	private $salt = "test123456";
	#配置临时目录
	private $tmp_path = "/tmp/upload/";
	
	function index(){
		
		if($this->is_zip($_FILES["file"]) && $this->valid_secret() ){
			
			$remotepath =  '/webBack/'.date('Ym/');
			$remotefile = $remotepath.$_FILES["file"]['name']; 
			if (!is_dir($this->tmp_path)){  
				mkdir( $this->tmp_path ,0755,true); 
			}
			move_uploaded_file($_FILES["file"]["tmp_name"], $this->tmp_path . $_FILES["file"]["name"]);
			$local_name = $this->tmp_path . $_FILES["file"]['name'];
			$this->add_task($local_name,$remotefile); 
			 
			$model = new UploadController();
    	    echo $model->task($remotefile);  
			echo "is add to task ";
			return;
		}
		echo "error:";
		return;
		
	}
	
	

	function is_zip($file){
		$config = array("exts"=>[1=>"zip"]);
		$ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
		//if(!in_array($ext,$config['exts'])){
		//	echo 'not in exts';
		//	return false;
		//}
		// 限制文件大小为500M
		if($file['size'] > 524288000 || $file['size'] == 0){
			echo 'so big:'.$file['size'] ;
			return false;
		}

		return true;
	}
	
	private function valid_secret(){
		$secret = $_SERVER['HTTP_VALID']; 
		$here_secret = md5( $_FILES["file"]['name'].$this->salt ); 
		if( $here_secret == $secret ){ 
			return true;
		}
		echo("secret error!");
		return false;
	}
	
	private function add_task($localfile, $remotefile){
	    $task = array(
			'localfile'=>$localfile,
			'remotepath' => $remotefile,
			'filesize'=>onedrive::_filesize($localfile),
			'upload_type'=>'web',
			'update_time'=>0,
	    );

	    $uploads = (array)config('@upload');
	    if(empty($uploads[$remotefile])){
		    $uploads[$remotefile] = $task;
		    config('@upload', $uploads);
	    }
	}
	
	
	 
}
