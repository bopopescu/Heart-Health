// Select the right pill for the menu
$('#results-pill').addClass('active');

$('#percentile-more-button').popover({
    title: 'About Percentiles',
    content: 'Your risk percentile relates your risk to other people of the same age and gender. If you are in the 90th percentile, then your risk of having a heart attack is greater than 90% of others with the same age and gender.',
    placement: 'top'
}).click(function(evt) {
    var popover = $(this).data('popover');
    var shown = popover && popover.tip().is(':visible');
    evt.stopPropagation();
    if(shown) return;
    $(this).popover('show');
});

$('html').on('click', function () {
    $('#percentile-more-button').popover('hide');
});

function setUpperRatingMessage(){
  //var messages = ['Low', 'Medium', 'High', 'Very High', 'Extremely High'] 
  //$('#upper-rating').text(messages[absoluteRatingUpper - 1]);
  
  var colorClass = 'text-success';
  if(absoluteRatingUpper <= 2){
      colorClass = 'text-success';
  } else if(absoluteRatingUpper == 3){
      colorClass = 'text-warning';
  } else if(absoluteRatingUpper <= 5){
      colorClass = 'text-error';
  }

  $('#upper-rating-' + absoluteRatingUpper).addClass(colorClass).removeClass('hidden-phone').css('font-size', '30px');
  $('.rating-color').addClass(colorClass);
}
setUpperRatingMessage();

/*
function setUpperRatingBar(){
    var highestWidth = absoluteRatingUpper * 20;

    var colorClass = 'progress-success';
    
    if(absoluteRatingUpper <= 2){
      colorClass = 'progress-success';
    } else if(absoluteRatingUpper == 3){
      colorClass = 'progress-warning';
    } else if(absoluteRatingUpper <= 5){
      colorClass = 'progress-danger';
    }

    $('#rating-bar-container').addClass(colorClass);

    $('#rating-bar').css('width', highestWidth + "%");
}
setUpperRatingBar();
*/
