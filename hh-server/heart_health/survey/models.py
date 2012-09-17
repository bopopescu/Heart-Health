from django.db import models
from accounts.models import UserProfile
from django.contrib import admin
import urllib, urllib2
import uuid

INDIGO_URL = "https://demo-indigo4health.archimedesmodel.com/IndiGO4Health/IndiGO4Health"

class Survey(models.Model):
    user_profile = models.OneToOneField(UserProfile, verbose_name="The user that owns this survey")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="When the survey was created")
    age = models.IntegerField(null=True)

    # tracking ID 
    trackingid = uuid.uuid1() 

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, default='MALE', max_length=6)

    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    smoker = models.NullBooleanField()
    mi = models.NullBooleanField(verbose_name="Has the user had an MI?")
    stroke = models.NullBooleanField(verbose_name="Has the user had a stroke?")
    diabetes = models.NullBooleanField(verbose_name="Does the user have diabetes?")

    # pharmacy testing info
    systolic = models.IntegerField(null=True, verbose_name="systolic blood pressure")
    diastolic = models.IntegerField(null=True, verbose_name="diastolic blood pressure")
    cholesterol = models.IntegerField(null=True, verbose_name="total cholesterol")
    hdl = models.IntegerField(null=True)
    ldl = models.IntegerField(null=True)
    hba1c = models.FloatField(null=True, verbose_name="If diabetic, HbA1c")

    # optional info
    cholesterolmeds = models.NullBooleanField(verbose_name="Does the user take cholesterol meds?")
    bloodpressuremeds = models.NullBooleanField(verbose_name="Does the user take blood pressure meds?")
    bloodpressuremedcount = models.IntegerField(null=True, verbose_name="The number of blood pressure meds the user takes")
    aspirin = models.NullBooleanField(verbose_name="Does the user take aspirin regularly?")
    moderateexercise = models.IntegerField(null=True, verbose_name="How many hours of moderate exercise per week?")
    vigorousexercise = models.IntegerField(null=True, verbose_name="How many hours of vigorous exercise per week?")
    familymihistory = models.NullBooleanField(verbose_name="Is there an immediate family history of MI before 55?")

    # Upper bound CVD risk
    u_risk = models.FloatField(null=True)
    u_risk_percentile = models.IntegerField(null=True)
    u_comparison_risk = models.FloatField(null=True)
    u_rating_for_age = models.IntegerField(null=True)
    u_rating = models.IntegerField(null=True)
    
    # Lower bound CVD risk
    l_risk = models.FloatField(null=True)
    l_risk_percentile = models.IntegerField(null=True)
    l_comparison_risk = models.FloatField(null=True)
    l_rating_for_age = models.IntegerField(null=True)
    l_rating = models.IntegerField(null=True)

    # Accurate CVD risk
    risk = models.FloatField(null=True)
    risk_percentile = models.IntegerField(null=True)
    comparison_risk = models.FloatField(null=True)
    rating_for_age = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)

    # Additional Info
    recommendation = models.IntegerField(null=True, verbose_name="Pharmacy test recommendation")
    doctor_recommendation = models.IntegerField(null=True, verbose_name="Doctor visit recommendation")
    increase_in_risk = models.FloatField(null=True, verbose_name="Increase in risk if user stops meds")
    percent_reduc_with_medication = models.FloatField(null=True, verbose_name="Percent risk reduction with meds")
    percent_reduc_with_moderate_exercise = models.FloatField(null=True, verbose_name="Reduction with 3 extra hrs moderate exercise")
    percent_reduc_with_vigorous_exercise = models.FloatField(null=True, verbose_name="Reduction with 3 extra hrs moderate exercise")
    percent_reduc_with_weight_loss = models.FloatField(null=True, verbose_name="Reduction with weight loss specified")
    pounds_of_weight_loss_required = models.FloatField(null=True, verbose_name="Pounds of weight loss, 5% body weight")
    percent_reduc_with_no_smoking = models.FloatField(null=True, verbose_name="Reduction if the user stops smoking")
    percent_reduc_with_all = models.FloatField(null=True, verbose_name="Reduction if all suggestions are followed")
    elevated_blood_pressure = models.NullBooleanField(verbose_name="The user may have elevated blood pressure")
    elevated_cholesterol = models.NullBooleanField(verbose_name="The user may have elevated cholesterol")
    warning = models.IntegerField(null=True, verbose_name="The code for a warning message")

    def has_basic_input(self):
        return (self.age is not None and
                self.gender is not None and
                self.height is not None and
                self.weight is not None and 
                self.smoker is not None and
                self.mi is not None and
                self.diabetes is not None and
                self.stroke is not None)

    def has_basic_results(self):
        return (self.u_risk is not None and
                self.u_risk_percentile is not None and
                self.u_comparison_risk is not None and
                self.u_rating_for_age is not None and 
                self.u_rating is not None and
                self.l_risk is not None and
                self.l_risk_percentile is not None and
                self.l_comparison_risk is not None and
                self.l_rating_for_age is not None and 
                self.l_rating is not None and 
                self.recommendation is not None)

    def get_basic_results(self):
        gender_string = ""
        if self.gender == 'MALE':
            gender_string = 'M'
        else:
            gender_string = 'F'

        params = {'age': self.age, 'gender': str(self.gender).lower(), 'height': self.height, 'weight': self.weight, 'smoker': str(self.smoker).lower(), 'mi': str(self.mi).lower(), 'diabetes': str(self.diabetes).lower(), 'stroke': str(self.stroke).lower()}  
        encoded_args = urllib.urlencode(params)
        print urllib2.urlopen(INDIGO_URL, encoded_args).read()         
        
    class Admin:
        pass

admin.site.register(Survey)


class Notification(models.Model):
    user = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
    send_time = models.DateTimeField(verbose_name="The time at which the notification should be sent")
    message_type = models.IntegerField(default=0, verbose_name="Code for type of message to send")
    # Indicates whether this is an email notification (0) or a native notification for an app (1)
    notification_type = models.IntegerField(default=0, verbose_name="Code for email or native type")

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance = models.FloatField()
    name = models.CharField(max_length=75)
    address1 = models.CharField(max_length=75)
    address2 = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=25)
    url = models.CharField(max_length=255)
