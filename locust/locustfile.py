from os import getenv
from locust import HttpLocust, TaskSet, task
from faker import Faker
from uuid import uuid4
import requests
import random

def get_fake_customer():
    fake = Faker('en_US')
    return {
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "EmailAddress": "test%s@loadtest.itsnull.com" % (uuid4())
    }

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
    @task(4)
    def getCustomer(self):
        self.client.get("/api/customer/%s" % (random.choice(consumer_ids)) , name="Get /api/consumer")

    @task(1)
    def createCustomer(self):
        self.client.post("/api/customer/", json=get_fake_customer(), name="Post /api/consumer")

    @task(1)
    def createCustomerInvalid(self):
        with self.client.post("/api/customer/", json=get_invalid_fake_customer(), name="Post Invalid /api/customer", catch_response=True) as response:
            if response.status_code == 400:
                response.success()

    @task(2)
    def updateConsumer(self):
        self.client.put("/api/customer/%s" % (random.choice(consumer_ids)), json=get_fake_customer(), name="Put /api/consumer")

    @task(1)
    def updateCustomerInvalid(self):
        with self.client.put("/api/customer/%s" % (random.choice(consumer_ids)), json=get_invalid_fake_customer(), name="Put Invalid /api/customer", catch_response=True) as response:
            if response.status_code == 400:
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