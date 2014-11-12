(function(){
    var height = document.body.scrollHeight;
    var width = document.body.scrollWidth;
    var iframe = window.top.document.getElementsByTagName('iframe')[0]
    
    iframe.style.height = height + 'px';
    iframe.style.width = width + 'px';
})();
