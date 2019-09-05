import os
from locust import HttpLocust, TaskSet, task
from faker import Faker

class ApiTasks(TaskSet):
    @task(1)
    def getCustomer(self):
        self.client.get("/api/customer/88f37d26-6616-4598-8792-e3bb9b814c72")

class ApiUser(HttpLocust):
    host = os.getenv("api_host")
    task_set = ApiTasks
    min_wait = max_wait = 1000