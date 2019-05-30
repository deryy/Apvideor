$(document).ready(function(){
    
    
    
    $(this).removeClass('icon-play');
    $(this).addClass('icon-stop');
    var set = getUrlParam('set');
    var id_list_str = getUrlParam('list');
    var id_list = [];
    var len = id_list_str.length;
    
    for(var i=0;i*6<=len;i++){
        var start = 6*i;
        var end = 6*i+6;
        id_list.push(id_list_str.slice(start,end));
    }
    
    var music_url = ''
    var k=0;
    music_url = '/static/apvideor/'+id_list[k]+'.mp3';
    $("source")[0].src=music_url;
    audio_show();
    $("#stream")[0].play();
    post_data = {music_id:id_list[k]}
    $.post("/musicGo/getMusicName",post_data,function(data,status){
        if(status=="success"){

           // alert(data[0]);
           $("#music_name").html(data[0]);
            
        }
        else alert("ajax failure");    
    });
 
    
    $("#change_pre").click(function(){
        if(k-1>-1){
            k=k-1;
        }
        else{
            k=k-1+5;
        }
        music_url = '/static/apvideor/'+id_list[k]+'.mp3';
        $("source")[0].src=music_url;
        $("#stream")[0].load();
        $("#stream")[0].play();
        $("#control").removeClass('icon-play');
        $("#control").addClass('icon-stop');
        post_data = {music_id:id_list[k]}
        $.post("/musicGo/getMusicName",post_data,function(data,status){
            if(status=="success"){

               $("#music_name").html(data[0]);
                
            }
            else alert("ajax failure");
        });
        
    });
        
 
    $("#change_next").click(function(){
        if(k+1<5){
            k=k+1;  
        }
        else{
            k=k+1-5;
        }
        music_url = '/static/apvideor/'+id_list[k]+'.mp3';
        $("source")[0].src=music_url;
        $("#stream")[0].load();
        $("#stream")[0].play();
        $("#control").removeClass('icon-play');
        $("#control").addClass('icon-stop');
        post_data = {music_id:id_list[k]}
        $.post("/musicGo/getMusicName",post_data,function(data,status){
            if(status=="success"){

               // alert(data[0]);
               $("#music_name").html(data[0]);
                
            }
            else alert("ajax failure");    
        });
        
    });

	// $.ajax({
 //        type:"post",
 //        url:"/musicGo/generateCondition",
 //        data:my_data,
 //        success:function(data){
 //            // alert(data);
 //        },
 //        error:function(e){

 //        }
 //    });
    $('#stream')[0].addEventListener('ended',function(){
        $('#control').removeClass('icon-stop');
        $('#control').addClass('icon-play');
    });

    $('#control').click(function(){
        
        var audio = $('#stream')[0];
        if(audio.paused){
            $(this).removeClass('icon-play');
            $(this).addClass('icon-stop');
            
            audio.play();
        }
        else{
            $(this).removeClass('icon-stop');
            $(this).addClass('icon-play');
            audio.pause();
        }
    });
    $("#generate_btn").click(function(){
        window.location.href = "result?set="+set+"&music="+id_list[k];
    });

    

});

//获取url中的参数
function getUrlParam(name) {
 var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
 var r = window.location.search.substr(1).match(reg); //匹配目标参数
 if (r != null) return unescape(r[2]); return null; //返回参数值
}

