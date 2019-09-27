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

class ApiTasks(TaskSet):
    @task(4)
    def getCustomer(self):
        self.client.get("/api/customer/%s" % (random.choice(consumer_ids)) , name="Get /api/consumer")

    @task(1)
    def createCustomer(self):
        self.client.post("/api/customer/", json=get_fake_customer(), name="Post /api/consumer")

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