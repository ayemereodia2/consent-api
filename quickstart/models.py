from django.db import models
from rest_framework import serializers

class Consent(models.Model):
    consent_title = models.CharField(max_length=256,blank=False, null=False)
    client_name = models.CharField(max_length=256,blank=False, null=False)
    name_on_health_card = models.CharField(max_length=256,blank=False, null=False)
    health_card_number = models.CharField(max_length=155,blank=False, null=False)
    date_of_birth = models.DateTimeField(auto_now=True)
    permission_to_communicate = models.BooleanField()
    email_to_communicate_with = models.CharField(max_length=155)
    contact_me = models.BooleanField()
    date_of_signature = models.DateTimeField(auto_now=True)
    pronouns = models.CharField(max_length=150, blank=False, null=False)



class CareGiver(models.Model):
    care_giver_name = models.CharField(max_length=155, blank=False, null=False)
    relationship_to_client = models.CharField(max_length=150, blank=False, null=False)
    consent = models.ForeignKey(Consent, related_name='caregivers', on_delete=models.CASCADE)

    
    
class CareGiverType(models.Model):
    institution_name = models.CharField(max_length=155, blank=False, null=False)
    relationship_to_client = models.CharField(max_length=155,blank=False, null=False)
    consent = models.ForeignKey(Consent, related_name='caregiver_types', on_delete=models.CASCADE)

class CareGiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGiver
        fields = ['care_giver_name', 'relationship_to_client']

class CareGiverTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGiverType
        fields = ['institution_name', 'relationship_to_client']
        
        
class ConsentSerializer(serializers.ModelSerializer):
    caregivers = CareGiverSerializer(many=True, required=False)
    caregiver_types = CareGiverTypeSerializer(many=True, required=False)

    class Meta:
        model = Consent
        fields = ['client_name', 'name_on_health_card', 'health_card_number', 'date_of_birth', 'permission_to_communicate',
                  'email_to_communicate_with', 'contact_me', 'date_of_signature', 'pronouns', 'caregivers', 'caregiver_types']

    def create(self, validated_data):
        caregivers_data = validated_data.pop('caregivers', [])
        caregiver_types_data = validated_data.pop('caregiver_types', [])

        consent = Consent.objects.create(**validated_data)

        for caregiver_data in caregivers_data:
            CareGiver.objects.create(consent=consent, **caregiver_data)

        for caregiver_type_data in caregiver_types_data:
            CareGiverType.objects.create(consent=consent, **caregiver_type_data)

        return consent



 # RELATIONSHIPS = [
    #     ('father', 'Father'),
    #     ('mother', 'Mother'),
    #     ('sister', 'Sister'),
    #     ('brother', 'Brother'),
    #     ('half-brother', 'Half-Brother'),
    #     ('half-sister', 'Half-Sister'),
    #     ('cousin', 'Cousin'),
    #     ('foster-father', 'Foster-Father'),
    #     ('foster-mother', 'Foster-Mother'),
    #     ('grandfather', 'GrandFather'),
    #     ('grandmother', 'GrandMother'),
    #     ('aunty', 'Aunty'),
    #     ('uncle', 'Uncle'),
    #     ('friend', 'Friend'),
    #     ('legal-guardian', 'Legal Guardian'),
    #     # Add more relationships as needed
    # ]
    
    
    # INSTITUTION = [
    #     ('individual', 'Individual'),
    #     ('agency', 'Agency'),
    #     ('professional', 'Profession'),
    #     # Add more relationships as needed
    # ]
    
    
    
    
#     {
#   "client_name": "Client Name",
#   "name_on_health_card": "Name on Health Card",
#   "health_card_number": "Health Card Number",
#   "date_of_birth": "2022-03-29",
#   "permission_to_communicate": true,
#   "email_to_communicate_with": "email@example.com",
#   "contact_me": true,
#   "date_of_signature": "2022-03-29T12:00:00",
#   "pronouns": "pronouns",
#   "caregivers": [
#     {
#       "care_giver_name": "Care Giver Name 1",
#       "relationship_to_client": "Relationship 1"
#     },
#     {
#       "care_giver_name": "Care Giver Name 2",
#       "relationship_to_client": "Relationship 2"
#     }
#   ],
#   "caregiver_types": [
#     {
#       "institution_name": "Institution Name 1",
#       "relationship_to_client": "Relationship 1"
#     },
#     {
#       "institution_name": "Institution Name 2",
#       "relationship_to_client": "Relationship 2"
#     }
#   ]
# }
