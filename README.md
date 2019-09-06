Build container locally
-----------------------
docker build . -t "customer-api-load-test:local"

Run locust with Web UI
----------------------
docker run --rm -it -p 8089:8089 -e api_host=https://customer-api-itsnull.azurewebsites.net customer-api-load-test:local

-To mount host files, so that quick fixes can be made.
docker run --rm -it -p 8089:8089 -v ${PWD}/locust:/locust customer-api-load-test:local

-Run local container against Azure App Service, with host filesystem mounted
docker run --rm -it -p 8089:8089 -v ${PWD}/locust:/locust -e api_host=https://customer-api-itsnull.azurewebsites.net customer-api-load-test:local

-Run local container against VS debugger, with host filesystem mounted
docker run --rm -it -p 8089:8089 -v ${PWD}/locust:/locust -e api_host=http://host.docker.internal:33663 customer-api-load-test:local

Run locust without web ui
-------------------------

Run local container against Azure App Service, with host filesystem mounted, 10 users, hatch rate 1
docker run --rm -it -p 8089:8089 -v ${PWD}/locust:/locust -e api_host=https://customer-api-itsnull.azurewebsites.net -e show_ui=y -e user_count=10 -e hatch_rate=1 customer-api-load-test:local

Create Azure Container Registry
-------------------------------
cd deploy
.\create-terraform-storage.ps1
.\apply-terraform.ps1

Push to Azure Container Registry
---------------
az acr login --name customerapiloadacr
docker tag customer-api-load-test:local customerapiloadacr.azurecr.io/customer-api-load-test:latest
docker push customerapiloadacr.azurecr.io/customer-api-load-test:latest

Create Service Principal for Azure Container Registry
-----------------------------------------------------
cd deploy
.\create-acr-service-principal.ps1

Run Load Test using Azure Container Instances
----------------------------------------------

- Run against cloud service using Locust UI
az container create -g customer-api-load-rg --name nightly-load-test --image customerapiloadacr.azurecr.io/customer-api-load-test:latest --registry-username $sp_id --registry-password $sp_password --ports 8089 --environment-variables api_host=https://customer-api-itsnull.azurewebsites.net --dns-name-label customer-api-nightly-load-test
- Open http://customer-api-nightly-load-test.eastus2.azurecontainer.io:8089/ in browser


- Run against cloud service, no UI
az container create -g customer-api-load-rg --name nightly-load-test --image customerapiloadacr.azurecr.io/customer-api-load-test:latest --registry-username $sp_id --registry-password $sp_password --environment-variables api_host=https://customer-api-itsnull.azurewebsites.net show_ui=y user_count=100 hatch_rate=5

- Clean up Azure Container Instance
az container delete -g customer-api-load-rg --name nightly-load-test --yes