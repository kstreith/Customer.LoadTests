$name = "customer-api-load-tf"
$rg = "$name-rg"
$storage = "customerapiloadst"

& az group create --location eastus2 --name "$rg"
& az storage account create --name "$storage" --resource "$rg" --location eastus2 --sku Standard_LRS
& az storage container create --name terraform --account-name "$storage"

$storageKey = & az storage account keys list -g "customer-api-load-tf-rg" -n "customerapiloadst" --query [0].value
& terraform.exe init --backend-config="access_key=$storageKey"
