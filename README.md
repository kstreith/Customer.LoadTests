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