$(document).ready(function() {
	setup_ui();
});


function setup_ui() {
    $('.item-title').css('cursor', 'pointer');
    $(".item-title").bind('click',function(){
        clear_ui();
	$(this).css('font-weight','bold');
	var bottom_line = $(this).siblings('.item-bottom_line').html();
	var description = $(this).siblings('.item-description').html();
	sentiment_analisys(bottom_line);
	update_description(description);
    });
}


function sentiment_analisys(text) {
    $.post(
	'/sentiment/?',
	{'text':text},
	function(data) {
		console.log(data.sentiment);
		console.log(data.features);
		$('#sentiment').html(data.sentiment);
		$('#features').html(data.features);
		$('#sentiment').parent().hide().fadeIn('slow');
		$('#features').parent().hide().fadeIn('slow');
		$('#review').hide().fadeIn('slow');
	},
	'json');
}


function update_description(description) {
	$('#item').html(description);
	$('#review').show();
}


function clear_ui() {
	$('.item-title').css('font-weight', 'normal');
}

