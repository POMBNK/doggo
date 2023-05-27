function start(){
	var state = $(document.getElementsByTagName('div')[0]).attr('var')
	var buttons = document.getElementsByTagName('button');

	for(var i = 0, len = buttons.length; i < len; i++) {
		if (buttons[i].className == state){
			$(buttons[i]).attr('aria-pressed', true);
		}
	  }
};

window.onload = start;

$(function(){
	$('button').click(function(){
		var cl=event.target.className;
		var ids=$(this).id

		var buttons = document.getElementsByTagName('button');

		for(var i = 0, len = buttons.length; i < len; i++) {   
			if (buttons[i].id != ids){
				$(buttons[i]).attr('aria-pressed', false);
			}
		  }

		if (event.target.getAttribute('aria-pressed') == "false"){
			$(this).attr('aria-pressed', true);
		}else{
			$(this).attr('aria-pressed', false);
		}

		if (cl == "forward"){
			$.ajax({
				url: '/forward',
				data: $('form').serialize(),
				type: 'POST',
				success: function(response){
					console.log(response);
				},
				error: function(error){
					console.log(error);
				}
			});
		}else if (cl == "left"){
			$.ajax({
				url: '/left',
				data: $('form').serialize(),
				type: 'POST',
				success: function(response){
					console.log(response);
				},
				error: function(error){
					console.log(error);
				}
			});
		}else if (cl == "backward"){
			$.ajax({
				url: '/backward',
				data: $('form').serialize(),
				type: 'POST',
				success: function(response){
					console.log(response);
				},
				error: function(error){
					console.log(error);
				}
			});
		}else if (cl == "idle"){
			$.ajax({
				url: '/idle',
				data: $('form').serialize(),
				type: 'POST',
				success: function(response){
					console.log(response);
				},
				error: function(error){
					console.log(error);
				}
			});
		}else if (cl == "right"){
			$.ajax({
				url: '/right',
				data: $('form').serialize(),
				type: 'POST',
				success: function(response){
					console.log(response);
				},
				error: function(error){
					console.log(error);
				}
			});
		}
	});
});