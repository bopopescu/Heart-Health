// Select the right pill for the menu
$('#results-pill').addClass('active');

$(document).ready(function (){
    $.ajax({
        url: '/results/get/',
        type: "POST",
        success: function(data){
           response = JSON.parse(data);
           if(response.success == false){
               $('#initial-loading').hide();
               $('#problem-message').append('<p class="center-text">' + response.message + '</p>');  
           } else {
               window.location.href = response.redirect;
           }
        },
        error: function(data){
           $('#initial-loading').hide();
           $('#problem-message').append('<p class="center-text"> An error has occurred, please try again later. </p>');  
        },
    });
});
