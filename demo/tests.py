from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from .models import (
	Toll,
	TollBooth,
	Vehicle,
	TollPass,
	TollTransaction,
)
from .constants import (
	SINGLE_PASS_PRICE,
	RETURN_PASS_PRICE,
	SEVEN_DAY_PASS_PRICE,	
)


class TollPassAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.toll = Toll.objects.create(name='Kalagata Toll')
		self.booth = TollBooth.objects.create(toll=self.toll,name='KG Booth1')
		self.vehicle = Vehicle.objects.create(registration_num='AP1278')
		self.single_pass_price = SINGLE_PASS_PRICE
		self.return_pass_price = RETURN_PASS_PRICE
		self.seve_day_pass_price = SEVEN_DAY_PASS_PRICE

	def test_check_or_issue_toll_pass(self):
		vehicle_active_pass = TollPass.objects.create(
			pass_type=TollPass.SP,
			vehicle=self.vehicle,
			valid_from=timezone.now(),
			valid_untill=timezone.now()+timezone.timedelta(hours=1) 
		) 
		url = reverse('check_or_issue_toll_pass')
		data = {
			'registration_num': 'AP1278',
			'toll_id': self.toll.id
		}
		response = self.client.post(url,data,format='json')
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertIn('Vehicle has an active pass', response.data['message'])
		self.assertIn('vehicle_pass_data', response.data)
		self.assertEqual(
			response.data['vehicle_pass_data']['id'],
			vehicle_active_pass.id
		)

	def test_check_or_issue_toll_pass_without_active_pass(self):
		url = reverse('check_or_issue_toll_pass')
		data = {
			'registration_num': 'AP1278',
			'toll_id': self.toll.id,
		}
		response = self.client.post(url,data, format='json')
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertIn(
				'Vehicle does not have any active pass currently', 
				response.data['message']
			)
		self.assertIn('pass_prices', response.data)

	def test_create_toll_transaction(self):
		url = reverse('create_toll_transaction')
		data = {
			'toll_booth':self.booth.id,
			'vehicle':self.vehicle.id,
			'amt_collected':self.single_pass_price,
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code,status.HTTP_201_CREATED)
		self.assertEqual(TollTransaction.objects.count(), 1)
		self.assertEqual(
				TollTransaction.objects.first().amt_collected,
				self.single_pass_price
				)

	def test_toll_transaction_leaderboard(self):
		trans1 = TollTransaction.objects.create(
			toll_booth = self.booth,
			vehicle=self.vehicle,
			amt_collected=self.single_pass_price,
		)

		trans2 = TollTransaction.objects.create(
			toll_booth=self.booth,
			vehicle=self.vehicle,
			amt_collected=self.return_pass_price,			
		)

		trans3 = TollTransaction.objects.create(
			toll_booth=self.booth,
			vehicle=self.vehicle,
			amt_collected=self.seve_day_pass_price,
		)
		url = reverse('toll_transaction_list')
		response = self.client.get(url,format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data),3)
		self.assertEqual(response.data[0]['id'], trans3.id)
		self.assertEqual(response.data[1]['id'], trans2.id)
		self.assertEqual(response.data[2]['id'], trans1.id)


