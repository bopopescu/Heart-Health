// Select the right pill for the menu
$('#assess-pill').addClass('active');

function wizardStep(inputDivId, validationFunction) {
    this.inputDivId = inputDivId;
    this.validationFunction = validationFunction;
}

var wizard = new Object();
wizard.steps = new Array();
wizard.currentStepIdx = 0;
wizard.showCurrentStep = function(){
    $('.wizard-button-group').each(function (){
        $(this).addClass('hidden');
    });

    // First step
    if(this.currentStepIdx == 0){
        $('#wizard-next-only').removeClass('hidden');
    } else if(this.currentStepIdx == this.steps.length - 1){
        $('#wizard-submit-group').removeClass('hidden');
    } else {
        $('#wizard-both-buttons').removeClass('hidden');
    }

    $('#' + wizard.steps[this.currentStepIdx].inputDivId).removeClass('hidden');
}
wizard.showNextStep = function(){
    if(wizard.steps[this.currentStepIdx].validationFunction()){
        $('#' + wizard.steps[this.currentStepIdx].inputDivId).addClass('hidden');
        this.currentStepIdx += 1;
        this.showCurrentStep();
    }
}
wizard.showPreviousStep = function(){
    oldStep = $('#' + wizard.steps[this.currentStepIdx].inputDivId).addClass('hidden');
    oldStep.removeClass('error');
    oldStep.find('.help-inline').addClass('hidden');
    this.currentStepIdx -= 1;
    this.showCurrentStep();
}

// Push all of the steps and their arrays
wizard.steps.push(new wizardStep('age-group', function(){
    var validated = validateTextNumericInRange($('#age-group input').val(), 18, 130);
    if(!validated){
        $('#age-group').addClass('error');
        $('#age-group .help-inline').removeClass('hidden');
    } else {
        $('#age-group').removeClass('error');
        $('#age-group .help-inline').addClass('hidden');
    }
    return validated;
}));
wizard.steps.push(new wizardStep('gender-group', function(){
   if($('#gender-group select').val() == "Not Selected"){
       $('#gender-group').addClass('error');
       $('#gender-group .help-inline').removeClass('hidden');
       return false;
   } else {
       $('#gender-group').removeClass('error');
       $('#gender-group .help-inline').addClass('hidden');
       return true;
   }
}));
wizard.steps.push(new wizardStep('height-group', function(){
    var validated = validateTextNumericInRange($('#height-group input').val(), 44, 87);
    if(!validated){
        $('#height-group').addClass('error');
        $('#height-group .help-inline').removeClass('hidden');
    } else {
        $('#height-group').removeClass('error');
        $('#height-group .help-inline').addClass('hidden');
    }
    return validated;
}));
wizard.steps.push(new wizardStep('weight-group', function(){
    var validated = validateTextNumericInRange($('#weight-group input').val(), 80, 600);
    if(!validated){
        $('#weight-group').addClass('error');
        $('#weight-group .help-inline').removeClass('hidden');
    } else {
        $('#weight-group').removeClass('error');
        $('#weight-group .help-inline').addClass('hidden');
    }
    return validated;
}));
wizard.steps.push(new wizardStep('smoke-group', function(){
   return true;
}));
wizard.steps.push(new wizardStep('heart-attack-group', function(){
   return true;
}));
wizard.steps.push(new wizardStep('stroke-group', function(){
   return true;
}));
wizard.steps.push(new wizardStep('diabetes-group', function(){
   return true;
}));

//Show the first step!
wizard.showCurrentStep();

// Pressing the enter key on each input checkbox should advance the form wizard
$('.control-group input').keyup(function(event){
        if(event.keyCode == 13){
            wizard.showNextStep();
        }
});

function validateTextNumericInRange(text, min, max) {
        var value = parseInt(text, 10);

        return (!isNaN(value) && !isNaN(text) && value >= min && value <= max);
}

function submitBasicQuestions(){
    var query = $('#basic-form').serializeArray(),
    inputData = {};

    for (i in query) {
        inputData[query[i].name] = query[i].value
    }

    $.ajax({
        url: 'save/',
        data: inputData,
        type: "POST",
        success: function(data){
            console.log('Success! Data is: ' + data);    
        },
        error: function(data){
            console.log('Failure :(');
        },
    });
}
