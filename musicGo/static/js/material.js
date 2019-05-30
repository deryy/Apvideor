$(document).ready(function(){

	$("#imageUpload").initUpload({
        "uploadUrl":"musicGo/imageSave",//上传文件信息地址
        "size":81920,//文件大小限制，单位kb,默认不限制
        "maxFileNumber":20,//文件个数限制，为整数
        //"filelSavePath":"",//文件上传地址，后台设置的根目录
        //"onUpload":onUploadFun，//在上传后执行的函数
        //autoCommit:true,//文件是否自动上传
        "fileType":['png','PNG','jpg','JPG','mp4']//文件类型限制，默认不限制，注意写的是文件后缀
    });

    function onUploadFun(opt,data){
        alert(data);
        uploadTools.uploadError(opt);//显示上传错误
        uploadTools.uploadSuccess(opt);//显示上传成功
    }
    
    
    function testUpload(){
    	var opt = uploadTools.getOpt("imageUpload");
    	uploadEvent.uploadFileEvent(opt);
    }

    
    
});
