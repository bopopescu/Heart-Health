$('#percentile-more-button').popover({
    title: 'About Percentiles',
    content: 'Your risk percentile relates your risk to other people of the same age and gender. If you are in the 90th percentile, then your risk of having a heart attack is greater than 90% of others with the same age and gender.'
});

function setUpperRatingMessage(){
  var messages = ['low', 'medium', 'high', 'very high', 'extremely high'] 
  $('#upper-rating').text(messages[absoluteRatingUpper]);
  
  var colorClass = 'text-success';
  if(absoluteRatingUpper <= 2){
      colorClass = 'text-success';
  } else if(absoluteRatingUpper == 3){
      colorClass = 'text-warning';
  } else if(absoluteRatingUpper <= 5){
      colorClass = 'text-error';
  }

  $('#upper-rating-text').addClass(colorClass);
}
setUpperRatingMessage();
