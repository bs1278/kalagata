from django.urls import path
from .views import (
	check_or_issue_toll_pass,
	create_vehicle_toll_pass,
	TollTransactionListView,
	TollTransactionCreateView,
)

urlpatterns =  [
	path(
			'kalagata_tm/toll/check_or_issue_toll_pass',
			check_or_issue_toll_pass,
			name='check_or_issue_toll_pass'
		),
	path(
			'kalagata_tm/toll/transactions/create/',
			TollTransactionCreateView.as_view(),
			name='create_toll_transaction'
		),	
	path(	
			'kalagata_tm/toll/transactions/list/',
			TollTransactionListView.as_view(),
			name='toll_transaction_list'
		),	
	path(	
			'kalagata_tm/toll/create_vehicle_toll_pass', 
			create_vehicle_toll_pass, 
			name='create_vehicle_toll_pass'
		),
]