$('[name=gotoPage]').on('keyup',function(e){
    var userInput = $(this).val()|0;
    if(e.keyCode==13){
        location.href="/list/" + userInput + "?type=" + $(this).attr('data-type')
    }
})