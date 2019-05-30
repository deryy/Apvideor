$(document).ready(function(){
    // $("#share").click(function(){
    //  $("#qrcode").html('');
    //     $("#qrcode").qrcode(window.location.href);
    //     $("#qrcode").css("background","white");
    // });
    var material_dirname = getUrlParam('set');
    var music_id = getUrlParam('music');
    // music_path = '/static/apvideor/'+music_id+'.mp3';
    // music_path = '1.mp3';
    var video_url = ''

    post_data={music_path:music_id,material_path:material_dirname}
    $.post("musicGo/getVideo",post_data,function(data,status){
        if(status=="success"){

            video_url = material_dirname+'_result.mp4';
            $("#result_video").append('<source id="result_video" src='+'/static/'+video_url+' type="video/mp4">'); 
            $(".cover").css("display","none");
	    $("#download").attr('href','/static/'+video_url);
            
        }
        else alert("ajax failure");
        
    });

    

    $("#again").click(function(){
        window.location.href = "/musicGo";
    });
    
    //{
    //    if(video_url==''){
    //        alert("请耐心等待视频生成...");
    //    }
    //    else{
    //        window.open('/static/'+video_url);    
    //    }
        
    //});

 
});

function FullScreen() {
    var ele = document.documentElement;
    if (ele .requestFullscreen) {
        ele .requestFullscreen();
    } else if (ele .mozRequestFullScreen) {
        ele .mozRequestFullScreen();
    } else if (ele .webkitRequestFullScreen) {
        ele .webkitRequestFullScreen();
    }
}

function exitFullscreen() {
    var de = document;
    if (de.exitFullscreen) {
        de.exitFullscreen();
    } else if (de.mozCancelFullScreen) {
        de.mozCancelFullScreen();
    } else if (de.webkitCancelFullScreen) {
        de.webkitCancelFullScreen();
    }
}

//获取url中的参数
function getUrlParam(name) {
 var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
 var r = window.location.search.substr(1).match(reg); //匹配目标参数
 if (r != null) return unescape(r[2]); return null; //返回参数值
}
