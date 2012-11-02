from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from survey.models import Survey, Notification
from survey import locationMethods as location
from accounts.models import UserProfile
import uuid
import datetime
import simplejson as json
import survey.locationMethods as locationMethods

def index(request):
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def assess(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/assess/basic/')    

    if request.user.userprofile.survey.has_basic_input():
        if not request.user.userprofile.survey.has_bio_input():
            return HttpResponseRedirect('/assess/bio/')    
        else:
            return HttpResponseRedirect('/assess/detail/')    
    else:
        return HttpResponseRedirect('/assess/basic/')    

def assess_basic(request):
	return render_to_response('assess_basic.html', locals(), context_instance=RequestContext(request))

def assess_basic_save(request):
    create_user_if_anonymous(request)
    
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

    request.user.userprofile.survey.is_stale = True

    if request.user.userprofile.allow_notifications and not request.user.userprofile.is_anonymous:
        create_notifications(request.user)

    request.user.userprofile.survey.save()
    request.user.userprofile.save()
    return HttpResponseRedirect('/results/')    

def create_notifications(userObj):
    """ Creates three notifications for the user, at 1 week, 2 weeks, and 4 weeks. """
    now = datetime.datetime.utcnow().replace(tzinfo=utc)

    one_min = Notification(user=userObj)
    one_min.send_time = now + datetime.timedelta(0, 60)
    one_min.save()

    one_week = Notification(user=userObj)
    one_week.send_time = now + datetime.timedelta(7)
    one_week.save()

    two_weeks = Notification(user=userObj)
    two_weeks.send_time = now + datetime.timedelta(7)
    two_weeks.save()

    four_weeks = Notification(user=userObj)
    four_weeks.send_time = now + datetime.timedelta(7)
    four_weeks.save()

    userObj.userprofile.allow_notifications = False
    userObj.userprofile.save()

def assess_bio_save(request):
    create_user_if_anonymous(request)
    
    if not hasattr(request.user.userprofile, 'survey'):
       request.user.userprofile.survey = Survey()

    request.user.userprofile.survey.systolic = request.POST['systolic']
    request.user.userprofile.survey.diastolic = request.POST['diastolic'] 
    request.user.userprofile.survey.cholesterol = request.POST['cholesterol']
    request.user.userprofile.survey.hdl = request.POST['hdl']
    request.user.userprofile.survey.ldl = request.POST['ldl']
    if 'hba1c' in request.POST:
        request.user.userprofile.survey.hba1c = request.POST['hba1c']

    request.user.userprofile.survey.save()
    request.user.userprofile.save()

    request.user.userprofile.survey.get_bio_results()

    warning = str(request.user.userprofile.survey.warning)

    notifications = Notification.objects.filter(user=request.user)
    notifications.delete()

    return HttpResponse(json.dumps({"warningCode": warning}), mimetype="application/json")    


def assess_bio(request):
	return render_to_response('assess_bio.html', locals(), context_instance=RequestContext(request))

def assess_detail(request):
	return render_to_response('assess_detail.html', locals(), context_instance=RequestContext(request))

def assess_detail_save(request):
    create_user_if_anonymous(request)
    
    if not hasattr(request.user.userprofile, 'survey'):
       request.user.userprofile.survey = Survey()

    request.user.userprofile.survey.bloodpressuremeds = request.POST['bloodpressuremeds'] == 'true'
    if request.user.userprofile.survey.bloodpressuremeds:
        request.user.userprofile.survey.bloodpressuremedcount = request.POST['bloodpressuremedcount'] 
    else:
        request.user.userprofile.survey.bloodpressuremedcount = 0

    request.user.userprofile.survey.cholesterolmeds = request.POST['cholesterolmeds'] == 'true'
    request.user.userprofile.survey.aspirin = request.POST['aspirin'] == 'true'
    request.user.userprofile.survey.moderateexercise = request.POST['moderateexercise']
    request.user.userprofile.survey.vigorousexercise = request.POST['vigorousexercise']
    request.user.userprofile.survey.familymihistory = request.POST['familymihistory'] == "true"

    request.user.userprofile.survey.is_stale = True
    request.user.userprofile.survey.save()
    request.user.userprofile.save()
    return HttpResponseRedirect('/results/')    


def locate(request):
	return render_to_response('locate.html', locals(), context_instance=RequestContext(request))

def locate_get(request):
    locations = locationMethods.getScreeningLocations(request.GET['lat'], request.GET['lon'], request.GET['radius'])     
    return HttpResponse(json.dumps({'providers': locations}))

def locate_save_preferred(request):
    create_user_if_anonymous(request)

    preferred_location = location.get_and_save_location_from_provider_dict(request.POST) 
    request.user.userprofile.preferred_location = preferred_location
    request.user.userprofile.save()
    return HttpResponse(json.dumps({"success": True}))

def results_basic(request):
    if not hasattr(request.user, 'userprofile'):
        return render_to_response('results_loading.html', locals(), context_instance=RequestContext(request))
    if not request.user.userprofile.survey.has_basic_results():
        return render_to_response('results_loading.html', locals(), context_instance=RequestContext(request))
    else:
        return render_to_response('basic_results.html', locals(), context_instance=RequestContext(request))

def results_full(request):
    if not hasattr(request.user, 'userprofile'):
        return render_to_response('results_loading.html', locals(), context_instance=RequestContext(request))
    if not request.user.userprofile.survey.has_full_results():
        return render_to_response('results_loading.html', locals(), context_instance=RequestContext(request))
    else:
        return render_to_response('full_results.html', locals(), context_instance=RequestContext(request))

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
  
    # Now check for full input 
    if request.user.userprofile.survey.has_bio_input():
        if (not request.user.userprofile.survey.has_full_results()) or request.user.userprofile.survey.is_stale:
            request.user.userprofile.survey.get_bio_results()
        return HttpResponse(json.dumps({"success": True, "redirect": "/results/full/"}))

    if (not request.user.userprofile.survey.has_basic_results()) or request.user.userprofile.survey.is_stale:
        request.user.userprofile.survey.get_basic_results()
        return HttpResponse(json.dumps({"success": True, "redirect": "/results/basic/"}))
    else:
        return HttpResponse(json.dumps({"success": True, "redirect": "/results/basic/"}))

def create_user_if_anonymous(request):
    if not request.user.is_authenticated():
        anon_user = User(username=str(uuid.uuid4().hex[:30]), first_name="Anonymous", last_name="User") 
        anon_user.set_unusable_password()
        anon_user.save()

        anon_user.username = "user_" + str(anon_user.id)
        anon_user.userprofile.is_anonymous = True
        anon_user.save()


        anon_user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, anon_user)
