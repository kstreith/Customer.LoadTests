
az container create -g customer-api-load-rg --name nightly-load-test --image customerapiloadacr.azurecr.io/customer-api-load-test:${env:container_version} --registry-username $env:serviceprincipal_id --registry-password $env:serviceprincipal_password --environment-variables api_host=$env:loadtest_host show_ui=y user_count=$env:loadtest_usercount hatch_rate=$env:loadtest_hatchrate
