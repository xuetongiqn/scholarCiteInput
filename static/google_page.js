(function(){
    var height = document.body.scrollHeight;
    var width = document.body.scrollWidth;
    var iframe = window.top.document.getElementsByTagName('iframe')[0]
    
    iframe.style.height = height + 'px';
    iframe.style.width = width + 'px';
})();


$(window).ready(function(){
	$('#gs_n a').each(function(i,ele){
		ele = $(ele);
		var arr = ele.attr('href').match(/\?start=(\d+)/);
		if(arr && arr.length==2){
			ele.attr('href',location.href.replace(/\.html$/,'_'+arr[1]+'.html'))
		}

	})
})