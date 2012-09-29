$('.bp-help').popover({
    title: 'Blood Pressure',
    content: 'The first number in your blood pressure reading is your systolic blood pressure and the sceond number is your diastolic blood pressure. For example if your blood pressure is <strong>125/82</strong>, your systolic blood pressure is <strong>125</strong> and your diastolic pressure is <strong>82</strong>.'
});

function validateInputGroupInRange(id, low, high){
    var validated = validateTextNumericInRange($('#' + id + ' input').val(), low, high)
    if(!validated){
        $('#' + id).addClass('error');
        $('#' + id + ' .range-error').removeClass('hidden');
    } else {
        $('#' + id).removeClass('error');
        $('#' + id + ' .range-error').addClass('hidden');
    }
    return validated;
}

$('#bio-form').submit(function() {
    var validated = true;
    
    validated = validateInputGroupInRange('systolic', 80, 220) && validated;
    
    validated = validateInputGroupInRange('diastolic', 40, 130) && validated;
   
    validated = validateInputGroupInRange('cholesterol', 70, 500) && validated;
    
    validated = validateInputGroupInRange('hdl', 20, 130) && validated;
    
    validated = validateInputGroupInRange('ldl', 40, 400) && validated;
    
    if($('#hba1c').length > 0){
        if($('#hba1c input').val().length > 0){
            validated = validateInputGroupInRange('hba1c', 2, 16) && validated;
        }
    }
   
    var diastolic = $('#diastolic input').val();
    var systolic = $('#systolic input').val();
    // Diastolic must be less than systolic 
    if(!isNaN(diastolic) && !isNaN(systolic) && (parseInt(systolic) <= parseInt(diastolic))){
        validated = false;
        $('#diastolic').addClass('error')
        $('#diastolic-less-error').removeClass('hidden');
    } else {
        $('#diastolic-less-error').addClass('hidden');
    }

    // HDL + LDL must be less than total cholesterol
    var ldl = $('#ldl input').val();
    var hdl = $('#hdl input').val();
    var total = $('#cholesterol input').val();
    if(!isNaN(ldl) && !isNaN(hdl) && !isNaN(total) && ((parseInt(hdl) + parseInt(ldl)) > parseInt(total))){
        validated = false;
        $('#cholesterol,#hdl,#ldl').addClass('error');
        $('.cholesterol-combo-error').removeClass('hidden');
    } else {
        $('.cholesterol-combo-error').addClass('hidden')
    }

    return validated;
});

function validateTextNumericInRange(text, min, max) {
        var value = parseInt(text, 10);

        return (!isNaN(value) && !isNaN(text) && value >= min && value <= max);
}
