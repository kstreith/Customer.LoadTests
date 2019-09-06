$servicePrincipalName = "acr-service-princial"
$registryId = az acr show --name customerapiloadacr --query id --output tsv
$sp_passwd = az ad sp create-for-rbac --name http://$servicePrincipalName --scopes $registryId --role acrpull --query password --output tsv
$sp_app_id = az ad sp show --id http://$servicePrincipalName --query appId --output tsv
write-host "Service Principal ID: $sp_app_id"
write-host "Service Principal password: $sp_passwd"
