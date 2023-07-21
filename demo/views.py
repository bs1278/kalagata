from django.shortcuts import render
from rest_framework import generics
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
	Toll,
	TollBooth,
	Vehicle,
	TollPass,
	TollTransaction,
)
from .serializers import (
	VehicleSerializer, 
	TollPassSerializer, 
	TollTransactionSerializer,
)

from .constants import (
	SINGLE_PASS_PRICE,
	RETURN_PASS_PRICE,
	SEVEN_DAY_PASS_PRICE,	
)


class TollTransactionCreateView(generics.CreateAPIView):
	"""
	API View Description
	This view handles the functionality of the Creating toll transaction
	Method: HTTP Method
	Allowed HTTP Methods: [POST]
	"""
	queryset =  TollTransaction.objects.all()
	serializer_class = TollTransactionSerializer


class TollTransactionListView(generics.ListAPIView):
	"""
	API View Description
	This view handles the functionality of the giving all the list of toll transactions 
	Method: HTTP Method
	Allowed HTTP Methods: [GET]
	"""	
	queryset = TollTransaction.objects.all()
	serializer_class = TollTransactionSerializer

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.order_by('-amt_collected')


@api_view(['POST'])
def check_or_issue_toll_pass(request):
	"""
	API View Description
	This view handles the functionality of the follows
	--> checking if vehicle has active pass or not
	--> if not displays/returns the availble pass prices,
	Method: HTTP Method
	Allowed HTTP Methods: [POST]
	Parameters:
		- registration number (string): vehicle  registration number.
		- toll id (string): toll from which vehicle passing
	"""
	registration_num = request.data.get('registration_num')
	toll_id = request.data.get('toll_id')

	try:
		vehicle = Vehicle.objects.get(registration_num=registration_num)
	except Vehicle.DoesNotExist:
		return Response({'error': 'Vehicle is not found'}, status=404)

	vehicle_active_pass = TollPass.objects.filter(
		vehicle=vehicle,
		valid_untill__gte=timezone.now()).first()

	if vehicle_active_pass:
		pass_serializer = TollPassSerializer(vehicle_active_pass)
		return Response(
			{
				'message': 'Vehicle has an active pass',
				'vehicle_pass_data':pass_serializer.data
			}
		)

	toll = Toll.objects.get(pk=toll_id)

	return Response({
		'message': 'Vehicle does not have any active pass currently,Choose the pass type',
		'pass_prices': {
			'single_pass': SINGLE_PASS_PRICE,
			'return_pass': RETURN_PASS_PRICE,
			'seven_day_pass': SEVEN_DAY_PASS_PRICE,
		}
	}, status=200)


@api_view(['POST'])
def create_vehicle_toll_pass(request):
	"""
	API View Description
	This view handles the functionality of the follows
	--> checking if vehicle has active pass or not
	--> Creating active pass for the incoming vehicle,
	Method: HTTP Method
	Allowed HTTP Methods: [POST]
	Parameters:
		- registration number (string): vehicle  registration number.
		- pass type : type of toll pass vehicle requested
	"""

	registration_num = request.data.get('registration_num')
	pass_type = request.data.get('pass_type')

	if pass_type not in [TollPass.SP, TollPass.RP, TollPass.SDP]:
		return Response({
				'error': 'Invalid pass type recieved',
			},status=status.HTTP_400_BAD_REQUEST)

	try:
		vehicle = Vehicle.objects.get(registration_num=registration_num)
	except:
		return Response({
			'error': 'Vehicle Not found in database',
		},status=status.HTTP_404_NOT_FOUND)

	check_pass = TollPass.objects.filter(
			vehicle=vehicle,
			pass_type=pass_type,
			valid_untill__gte=timezone.now()
			).first()

	# check if vehicle has pass already
	if check_pass:
		return Response(
			{'error': 'Vehicle Already has an active pass'},
			status=status.HTTP_400_CONFLICT
		)

	valid_from = timezone.now()
	if pass_type == TollPass.SP:
		# if one way toll pass
		valid_untill = valid_from + timezone.timedelta(hours=24)
	elif pass_type == TollPass.RP:
		# if return toll pass
		valid_untill = valid_from + timezone.timedelta(hours=24)
	elif pass_type == TollPass.SDP:
		# if seven day toll pass
		valid_untill = valid_from+timezone.timedelta(days=7)

	pass_data = {
		'pass_type':pass_type,
		'vehicle':vehicle.id,
		'valid_from':valid_from,
		'valid_untill':valid_untill
	}
	serializer = TollPassSerializer(data=pass_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)