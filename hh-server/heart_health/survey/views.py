from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from survey.models import Survey
import simplejson as json

def index(request):
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def assess_basic(request):
	return render_to_response('assess_basic.html', locals(), context_instance=RequestContext(request))

def assess_basic_save(request):
    # reject calls that do not have a logged in user
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    
    if not hasattr(request.user.userprofile, 'survey'):
       request.user.userprofile.survey = Survey()

    request.user.userprofile.survey.age = request.POST['age']
    request.user.userprofile.survey.gender = request.POST['gender'] 
    request.user.userprofile.survey.height = request.POST['height']
    request.user.userprofile.survey.weight = request.POST['weight']
    request.user.userprofile.survey.smoker = request.POST['smoker'] == "true"
    request.user.userprofile.survey.stroke = request.POST['stroke'] == "true"
    request.user.userprofile.survey.mi = request.POST['mi'] == "true"
    request.user.userprofile.survey.diabetes = request.POST['diabetes'] == "true"

    request.user.userprofile.survey.save()
    request.user.userprofile.save()
    return HttpResponseRedirect('/results/')    

def results_basic(request):
    if not request.user.userprofile.survey.has_basic_results():
        return render_to_response('results_loading.html', locals(), context_instance=RequestContext(request))
    else:
        return render_to_response('basic_results.html', locals(), context_instance=RequestContext(request))

def results(request):
	return render_to_response('results_loading.html', locals(), context_instance=RequestContext(request))

def get_results(request):
    # reject calls that do not have a logged in user
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"success": False, "message": 'You have not taken the assessment yet, please <a href="/assess/basic/"> take the assessment</a> or <a href="/login/"> log in </a> to see your results.'}))

    if not hasattr(request.user.userprofile, 'survey'):
        return HttpResponse(json.dumps({"success": False, "message": 'You have not taken the assessment yet, please <a href="/assess/basic/"> take the assessment</a> or <a href="/login/"> log in </a> to see your results.'}))

    if not request.user.userprofile.survey.has_basic_input():
        return HttpResponse(json.dumps({"success": False, "message": 'You have not entered enough information to calculate results, please <a href="/assess/basic/"> take the assessment</a> to see your results.'}))
  
    # We have basic input, so get basic results if we don't have them yet 

    # TODO remove this, I'm forcing a refresh for testing purposes
    request.user.userprofile.survey.get_basic_results()
    if not request.user.userprofile.survey.has_basic_results():
        request.user.userprofile.survey.get_basic_results()
        return HttpResponse(json.dumps({"success": True, "redirect": "/results/basic/"}))
    else:
        return HttpResponse(json.dumps({"success": True, "redirect": "/results/basic/"}))
