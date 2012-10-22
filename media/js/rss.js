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
	    update_sentiment(data);
	    $('#sentiment_analysis').hide().fadeIn('slow');
	    $('#review').hide().fadeIn('slow');
	},
	'json');
}


function update_sentiment(data) {
	var sentiment = data.sentiment;
        var badge_class = sentiment >= 0 ? 'success' : 'important';
	if (sentiment == 0) { badge_class = 'inverse';}
	$('#sentiment').html('<span class="badge badge-'+badge_class+'">'+sentiment+'</span>');
	var features = data.features.split('|');
        $('#features').empty();
	for (var i in features) {
	    var feature_tuple = features[i].split(',');
	    var feature = feature_tuple[0].replace(/^[()]/, '').replace(/'/g, '');
	    var polarity = parseInt(feature_tuple[1]);
	    var label_class = polarity >= 0 ? 'success' : 'important';
	    var class_ = 'label label-' + label_class;
	    var title = 'Polarity: ' + polarity
            if (!isNaN(polarity)) {
	      $('#features').append('<span title="'+title+'" class="'+class_+'">'+feature+'</span>&nbsp;');
	    }
	}
        $('.label').css('cursor', 'help');
}


function update_description(description) {
	$('#item').html(description);
	$('#review').show();
}


function clear_ui() {
	$('.item-title').css('font-weight', 'normal');
}

