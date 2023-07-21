from rest_framework import serializers
from .models import (
	Toll,
	TollBooth,
	Vehicle,
	TollPass,
	TollTransaction,
)

class TollSerializer(serializers.ModelSerializer):
	class Meta:
		model = Toll
		fields = '__all__'


class TollBoothSerializer(serializers.ModelSerializer):
	class Meta:
		model = TollBooth
		fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vehicle
		fields =  '__all__'

class TollPassSerializer(serializers.ModelSerializer):
	class Meta:
		model = TollPass
		fields = '__all__'


class TollTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TollTransaction
		fields = '__all__'


















