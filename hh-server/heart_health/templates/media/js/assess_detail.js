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
    // Only show the description on the first step
    if(this.currentStepIdx == 0){
        $('#description-text').removeClass('hidden');
    } else {
        $('#description-text').addClass('hidden');
    }

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
       
        // If the next step has the class wizard-skip-step, skip it by adding 1 again to the step idex
        if($('#' + wizard.steps[this.currentStepIdx].inputDivId).hasClass('wizard-skip-step')){
            this.currentStepIdx += 1;
        }

        this.showCurrentStep();
    }
}
wizard.showPreviousStep = function(){
    oldStep = $('#' + wizard.steps[this.currentStepIdx].inputDivId).addClass('hidden');
    oldStep.removeClass('error');
    oldStep.find('.help-inline').addClass('hidden');
    this.currentStepIdx -= 1;

    // If the previous step has the class wizard-skip-step, skip it by subtracting 1 again to the step idex
    if($('#' + wizard.steps[this.currentStepIdx].inputDivId).hasClass('wizard-skip-step')){
        this.currentStepIdx -= 1;
    }

    this.showCurrentStep();
}

// Push all of the steps and their arrays
wizard.steps.push(new wizardStep('bp-meds-group', function(){
    if($('#bp-meds-group select').val() == 'true'){
        $('#bp-meds-count-group').removeClass('wizard-skip-step');
    } else {
        $('#bp-meds-count-group').addClass('wizard-skip-step');
    }

    return true;
}));
wizard.steps.push(new wizardStep('bp-meds-count-group', function(){
    return true;
}));
wizard.steps.push(new wizardStep('cholesterol-med-group', function(){
    return true;
}));
wizard.steps.push(new wizardStep('aspirin-group', function(){
        return true;
}));
wizard.steps.push(new wizardStep('moderate-exercise-group', function(){
    var validated = validateTextNumericInRange($('#moderate-exercise-group input').val(), 0, 59);
    if(!validated){
        $('#moderate-exercise-group').addClass('error');
        $('#moderate-exercise-group .help-inline').removeClass('hidden');
    } else {
        $('#moderate-exercise-group').removeClass('error');
        $('#moderate-exercise-group .help-inline').addClass('hidden');
    }
    return validated;
}));
wizard.steps.push(new wizardStep('vigorous-exercise-group', function(){
    var validated = validateTextNumericInRange($('#vigorous-exercise-group input').val(), 0, 29);
    if(!validated){
        $('#vigorous-exercise-group').addClass('error');
        $('#vigorous-exercise-group .help-inline').removeClass('hidden');
    } else {
        $('#vigorous-exercise-group').removeClass('error');
        $('#vigorous-exercise-group .help-inline').addClass('hidden');
    }
    return validated;
}));
wizard.steps.push(new wizardStep('family-risk-group', function(){
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
