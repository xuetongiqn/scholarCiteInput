$(window).ready(function(){
    $('[name=citeNum]').select().focus().on('keyup',function(e){
        var userInput = $(this).val();
        var id = $(this).attr('data-id');

        if(e.keyCode==13 && (!isNaN(userInput)){
            $.post('/submit/set_cite',{
                id : id,
                num : userInput
            },function(data){
                if(data.change==1){
                    location.href = '/goto/next?id='+id
                }else{
                    alert(data)
                }
            },'json')

        }else if(userInput == ""){
            location.href = '/goto/next?id='+id
        }
    });
})