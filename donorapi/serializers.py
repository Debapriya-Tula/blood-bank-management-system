from rest_framework import serializers
from .models import equationlog, userlog

class Userlogserializer(serializers.ModelSerializer):
#	userlogid = Equationlogserializer()
	class Meta:
		model = userlog
		fields = ('userlogid', 'fullname', 'email')

class Equationlogserializer(serializers.ModelSerializer):
	userlogid = Userlogserializer()
	class Meta:
		model = equationlog
		fields = ('mass', 'acceleration', 'force', 'userlogid')
		read_only_fields = ('force',)

	def create(self, validated_data):
		user_logid_data = validated_data.pop('userlogid')
		user_logid = userlog.objects.create(**user_logid_data)
		mass = validated_data['mass']
		acceleration = validated_data['acceleration']
		force = float(mass) * float(acceleration)
		eqlog = equationlog.objects.create(userlogid=user_logid, force=force, **validated_data)
		return eqlog

