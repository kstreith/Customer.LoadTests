from os import getenv
from locust import HttpLocust, TaskSet, task
from faker import Faker
from uuid import uuid4
import requests
import random

users = ["estore","mobileapp","retailstore"]

def get_headers():
    headers = {"x-fake-user": random.choice(users)}
    return headers

def get_fake_customer():
    fake = Faker('en_US')
    hasAnyBirthFields = random.randint(1, 2)
    customer = {
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "EmailAddress": "test%s@loadtest.itsnull.com" % (uuid4())
    }
    if hasAnyBirthFields == 1:
        birthDate = fake.date_object()
        whichBirthFields = random.randint(1, 3)
        if whichBirthFields == 1:
            customer["BirthDay"] = birthDate.day
        elif whichBirthFields == 2:
            customer["BirthMonth"] = birthDate.month
        else:
            customer["BirthDay"] = birthDate.day
            customer["BirthMonth"] = birthDate.month
    return customer

def get_invalid_fake_customer():
    fake_invalid_customer = get_fake_customer()
    value = random.randint(1, 3)
    if value == 1:
        fake_invalid_customer["FirstName"] = None
    elif value == 2:
        fake_invalid_customer["LastName"] = None
    else:
        fake_invalid_customer["EmailAddress"] = None
    return fake_invalid_customer

class ApiTasks(TaskSet):
    @task(16)
    def getCustomer(self):
        self.client.get("/api/customer/%s" % (random.choice(consumer_ids)), headers=get_headers(), name="Get /api/consumer")

    @task(1)
    def getCustomerNotFound(self):
        with self.client.get("/api/customer/%s" % (uuid4()), headers=get_headers(), name="Get NotFound /api/consumer", catch_response=True) as response:
            if response.status_code == 404:
                response.success()

    @task(4)
    def createCustomer(self):
        self.client.post("/api/customer/", headers=get_headers(), json=get_fake_customer(), name="Post /api/consumer")

    @task(1)
    def createCustomerInvalid(self):
        with self.client.post("/api/customer/", headers=get_headers(), json=get_invalid_fake_customer(), name="Post Invalid /api/customer", catch_response=True) as response:
            if response.status_code == 400:
                response.success()

    @task(8)
    def updateConsumer(self):
        self.client.put("/api/customer/%s" % (random.choice(consumer_ids)), headers=get_headers(), json=get_fake_customer(), name="Put /api/consumer")

    @task(1)
    def updateCustomerInvalid(self):
        with self.client.put("/api/customer/%s" % (random.choice(consumer_ids)), headers=get_headers(), json=get_invalid_fake_customer(), name="Put Invalid /api/customer", catch_response=True) as response:
            if response.status_code == 400:
                response.success()

    @task(1)
    def updateCustomerNotFound(self):
        with self.client.put("/api/customer/%s" % (uuid4()), headers=get_headers(), json=get_fake_customer(), name="Put NotFound /api/customer", catch_response=True) as response:
            if response.status_code == 404:
                response.success()

def get_testconsumerids(host):
    response = requests.get(host + "/api/loadtest/randomcustomer")
    responseObj = response.json()
    print("responseObj", dir(responseObj))
    print("values", responseObj["values"])
    return responseObj["values"]

host = getenv("api_host")
consumer_ids = get_testconsumerids(host)

class ApiUser(HttpLocust):
    host = host
    task_set = ApiTasks
    min_wait = max_wait = 1000