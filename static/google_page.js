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
			var str = arr[1]=='0'?'':'_'+arr[1]

			ele.attr('href',location.href.replace(/(_\d\d)*\.html$/,str+'.html'))
		}

	})
})

// $(window).ready(function(){
// 	$('#gs_n a').each(function(i,ele){
// 		ele = $(ele);
// 		var href = ele.attr('href')
// 		if(href){
// 			ele.attr('href',"https://scholar.google.com"+href).attr('target','_blank')
// 		}

// 	})
// })