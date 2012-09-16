from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from survey.models import Survey

def index(request):
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def basic(request):
	return render_to_response('begin.html', locals(), context_instance=RequestContext(request))

def basic_save(request):
    # reject calls that do not have a logged in user
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    
    if not hasattr(request.user.userprofile, 'survey'):
       request.user.userprofile.survey = Survey()

    request.user.userprofile.survey.age = request.POST['age']
    request.user.userprofile.survey.gender = request.POST['gender']
    request.user.userprofile.survey.height = request.POST['height']
    request.user.userprofile.survey.weight = request.POST['weight']
    request.user.userprofile.survey.smoker = request.POST['smoker']
    request.user.userprofile.survey.mi = request.POST['mi']
    request.user.userprofile.survey.diabetes = request.POST['diabetes']

    request.user.userprofile.survey.save()
    request.user.userprofile.save()
    return HttpResponseRedirect('/results/')    

def results_basic(request):
	return render_to_response('basic_results.html', locals(), context_instance=RequestContext(request))

