$(document).ready(function(){
    // var set = getUrlParam('set');

    // $("#back_btn").click(function(){
    //     window.location.href = "/musicGo";
    // });
    
    $("#next_btn").click(function(){
        ds=$('select[name="dress_style"]').find("option:selected").text();
        var my_data = {'dress_style':ds};
        // alert(ds);
        $.ajax({
            type:"post",
            url:"musicGo/getMusicStyle",
            data:my_data,
            success:function(data){
                // window.location.href = "material?set="+set+"&list="+data[0].join('');
                window.location.href = "musicGo/material?list="+data[0].join('');
            },
            error:function(e){
                alert("ajax fail");
            }
        });

    });
});



