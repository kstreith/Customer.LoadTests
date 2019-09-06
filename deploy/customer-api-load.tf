terraform {
    required_version = ">= 0.12"
    backend "azurerm" {
        storage_account_name = "customerapiloadst"
        container_name = "terraform"
        key = "terraform.tfstate"
    }
}

provider "azurerm" {
    version = "=1.33.0"
}

resource "azurerm_resource_group" "main" {
    name = "customer-api-load-rg"
    location = "East US2"
}

resource "azurerm_container_registry" "main" {
    name = "customerapiloadacr"
    location = "${azurerm_resource_group.main.location}"
    resource_group_name = "${azurerm_resource_group.main.name}"
    sku = "Basic"
}

output "acr_username" {
	value = "${azurerm_container_registry.main.admin_username}"
}

output "acr_url" {
	value = "${azurerm_container_registry.main.login_server}"
}

output "acr_password" {
	value = "${azurerm_container_registry.main.admin_password}"
}