from rest_framework import serializers
from accounts.models import Donor_details, Donor_reg

class Donor_regSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor_reg
        fields = ['email', 'first_name']

class Donor_detailsSerializer(serializers.ModelSerializer):
    userd = Donor_regSerializer()
    class Meta:
        model = Donor_details
        fields = ('weight','height','blood_group','city', 'ph_no', 'userd')

#    def create(self, validated_data):
 #       Donor_regid_data = validated_data.pop('Donor_reg')
  #      Donor_regid = Donor_reg.objects.create(**Donor_regid_data)
   #     mass = validated_data['mass']
    #    acceleration = validated_data['acceleration']
     #   force = float(mass) * float(acceleration)
      #  Donor_details = Donor_details.objects.create(Donor_regid=Donor_regid,force=force,**validated_data)
       # return Donor_details
