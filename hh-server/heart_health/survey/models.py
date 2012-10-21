from django.db import models
from accounts.models import UserProfile
from django.contrib import admin
import urllib, urllib2
import simplejson as json
import uuid
import logging

INDIGO_URL = "https://demo-indigo4health.archimedesmodel.com/IndiGO4Health/IndiGO4Health"
logger = logging.getLogger(__name__)

class Survey(models.Model):
    user_profile = models.OneToOneField(UserProfile, verbose_name="The user that owns this survey")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="When the survey was created")
    age = models.IntegerField(null=True)

    # tracking ID 
    trackingid = models.CharField(default=uuid.uuid1(), max_length=75) 
    # Maintain if the data is stale or not
    is_stale = models.BooleanField(default=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, default='M', max_length=6)

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

    def gender_group_string(self):
        if self.gender == 'M':
            return 'men'
        else:
            return 'women'

    def risk_comparison_less_1(self):
        return 1 - self.comparison_risk

    def u_risk_comparison_less_1(self):
        return 1 - self.u_comparison_risk

    def has_basic_input(self):
        return (self.age is not None and
                self.gender is not None and
                self.height is not None and
                self.weight is not None and 
                self.smoker is not None and
                self.mi is not None and
                self.diabetes is not None and
                self.stroke is not None)

    def has_bio_input(self):
        return (self.systolic is not None and
                self.diastolic is not None and
                self.cholesterol is not None and
                self.hdl is not None and 
                self.ldl is not None)

    def has_detail_input(self):
        return (self.cholesterolmeds is not None and
                self.bloodpressuremeds is not None and
                self.bloodpressuremedcount is not None and
                self.aspirin is not None and 
                self.moderateexercise is not None and
                self.vigorousexercise is not None and
                self.familymihistory is not None)

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

    def has_full_results(self):
        return (self.risk is not None and
                self.risk_percentile is not None and
                self.comparison_risk is not None and
                self.rating_for_age is not None and 
                self.rating is not None and
                self.elevated_blood_pressure is not None and
                self.elevated_cholesterol is not None and
                self.doctor_recommendation is not None)

    def get_basic_results(self):
        params = {'age': self.age, 'gender': str(self.gender), 'height': self.height, 'weight': self.weight, 'smoker': str(self.smoker).lower(), 'mi': str(self.mi).lower(), 'diabetes': str(self.diabetes).lower(), 'stroke': str(self.stroke).lower(), 'trackingid': str(self.trackingid)}  
        encoded_args = urllib.urlencode(params)
        response = json.loads(urllib2.urlopen(INDIGO_URL, encoded_args).read())        
        if len(response['ErrorMessageHashMap']) > 1:
             logger.error('Error while getting basic results: ' + json.dumps(response['ErrorMessageHashMap'])) 

        risk_array = response['Risk']
        for risk_obj in risk_array:
            if risk_obj['riskType'] == 'UpperBoundCVD':
                self.u_risk = risk_obj['risk']
                self.u_risk_percentile = risk_obj['riskPercentile']
                self.u_comparison_risk = risk_obj['comparisonRisk']
                self.u_rating_for_age = risk_obj['ratingForAge']
                self.u_rating = risk_obj['rating']
            if risk_obj['riskType'] == 'LowerBoundCVD':
                self.l_risk = risk_obj['risk']
                self.l_risk_percentile = risk_obj['riskPercentile']
                self.l_comparison_risk = risk_obj['comparisonRisk']
                self.l_rating_for_age = risk_obj['ratingForAge']
                self.l_rating = risk_obj['rating']

        self.recommendation = response['Recommendation']

        self.is_stale = False

        self.save()

    # This function uses the saved values for the bio results and pulls in the new data about the user's risk.
    def get_bio_results(self):
        params = {'age': self.age, 'gender': str(self.gender), 'height': self.height, 'weight': self.weight, 'smoker': str(self.smoker).lower(), 'mi': str(self.mi).lower(), 'diabetes': str(self.diabetes).lower(), 'stroke': str(self.stroke).lower(), 'systolic': self.systolic, 'diastolic': self.diastolic, 'cholesterol': self.cholesterol, 'hdl': self.hdl, 'ldl': self.ldl, 'trackingid': str(self.trackingid)}  

        if self.hba1c:
            params['hba1c'] = self.hba1c

        if self.has_detail_input():
            params['cholesterolmeds'] = self.cholesterolmeds
            params['bloodpressuremeds'] = self.bloodpressuremeds
            params['bloodpressuremedcount'] = self.bloodpressuremedcount
            params['aspirin'] = self.aspirin
            params['moderateexercise'] = self.moderateexercise
            params['vigorousexercise'] = self.vigorousexercise
            params['familymihistory'] = self.familymihistory

        encoded_args = urllib.urlencode(params)
        response = json.loads(urllib2.urlopen(INDIGO_URL, encoded_args).read())
        print response

        if len(response['ErrorMessageHashMap']) > 1:
             logger.error('Error while getting bio results: ' + json.dumps(response['ErrorMessageHashMap'])) 

        risk_array = response['Risk']
        for risk_obj in risk_array:
            if risk_obj['riskType'] == 'CVD':
                self.risk = risk_obj['risk']
                self.risk_percentile = risk_obj['riskPercentile']
                self.comparison_risk = risk_obj['comparisonRisk']
                self.rating_for_age = risk_obj['ratingForAge']
                self.rating = risk_obj['rating']

        self.doctor_recommendation = response['DoctorRecommendation']
 
        # For these outputs, I'm not positive they will be returned, so I will use get() since it returns none
        # if the output doesn't exist
        self.warning = get_from_dict_or_none(response, 'WarningCode')
        self.recommendation = get_from_dict_or_none(response, 'Recommendation')
        
        if 'Interventions' in response:
           interventions = response['Interventions']
           self.increase_in_risk = get_from_dict_or_none(interventions, 'IncreaseInRisk')
           self.percent_reduc_with_medication = get_from_dict_or_none(interventions, 'PercentReductionInRiskWithMedication')
           self.percent_reduc_with_moderate_exercise = get_from_dict_or_none(interventions, 'PercentReductionInRiskWithAdditionalModerateExercise')
           self.percent_reduc_with_vigorous_exercise = get_from_dict_or_none(interventions, 'PercentReductionInRiskWithAdditionalVigorousExercise')
           self.percent_reduc_with_weight_loss = get_from_dict_or_none(interventions, 'PercentReductionInRiskWithWeightLoss')
           self.pounds_of_weight_loss_required = get_from_dict_or_none(interventions, 'PoundsOfWeightLossRequired')
           self.percent_reduc_with_no_smoking = get_from_dict_or_none(interventions, 'PercentReductionWithSmokingCessation')
           self.percent_reduc_with_all = get_from_dict_or_none(interventions, 'PercentReductionWithAllInterventions')
           
        self.elevated_blood_pressure = response.get('ElevatedBloodPressure')
        self.elevated_cholesterol = response.get('ElevatedCholesterol')

        self.is_stale = False

        self.save()

        
class Admin:
    pass

admin.site.register(Survey)

def get_from_dict_or_none(dictionary, key):
    result = dictionary.get(key)
    if(result == ''):
        return None
    else:
        return result


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
    name = models.CharField(max_length=75)
    address1 = models.CharField(max_length=75)
    address2 = models.CharField(max_length=75,default='',blank=True)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=75)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=25)
    url = models.CharField(max_length=255)
    url_caption = models.CharField(max_length=255,default='',blank=True)
    cross_street = models.CharField(max_length=255,default='',blank=True)
    description = models.CharField(max_length=255,default='',blank=True)
    is_result = models.BooleanField(default=False)

    def get_as_provider_json(self):
       return json.dumps(self.to_provider_dict())

    def to_provider_dict(self):
       """
       For a self model object instance,
       create a provider dictionary that contains the same information
       """
       provider = {}
       provider['lat'] = self.latitude
       provider['lon'] = self.longitude
       provider['name'] = self.name
       provider['address1'] = self.address1
       provider['address2'] = self.address2
       provider['city'] = self.city
       provider['state'] = self.state
       provider['zip'] = self.zip_code
       provider['phone'] = self.phone
       provider['url'] = self.url
       provider['urlCaption'] = self.url_caption
       provider['crossStreet'] = self.cross_street
       provider['description'] = self.description
       return provider 

    class Meta:
        unique_together = ['name', 'address1', 'address2', 'city', 'state', 'zip_code']

admin.site.register(Location)

