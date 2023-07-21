"# kalagata" 

A Simple Toll Management App based on python,django and django rest framework
Instructions for running and checking an application

step1: clone the repository into  your local machine
step2: make sure you have already djano installation in your machine if not run the following script from your terminal 

```pip install django django```

Step3: from the root project directory run the following commong 

``` python manage.py runserver```
once your local server in run and up you can test it via two ways either running unit test cases or hitting api end points

API End points

```http://localhost:8000/api/v0.1/kalagata_tm/toll/check_or_issue_toll_pass```
```http://localhost:8000/api/v0.1/kalagata_tm/toll/create_vehicle_toll_pass```
```http://localhost:8000/api/v0.1/kalagata_tm/kalagata_tm/toll/transactions/create/```
```http://localhost:8000/api/v0.1/kalagata_tm/toll/transactions/list/```

For Testing unit test cases from the root project directory run the below commond from your terminal
``` python manage.py test demo ```
