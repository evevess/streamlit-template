terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}


### VARIABLES ###

variable "resource_group_location" {
  type        = string
  default     = "westeurope"
  description = "Location of the resource group."
}

variable "resource_group_name" {
  type        = string
  default     = "adc-app-dev" # <---- IMPORTANT: PROD == "adc-app" & TEST == "adc-app-dev"
  description = "Name of ressource group to deploy to"
}

variable "AZURE_STORAGE_CONNECTION_STRING" {
  type        = string
  description = "Secret must be set with prefix and env vars: export TF_VAR_AZURE_STORAGE_CONNECTION_STRING="
}

variable "MICROSOFT_PROVIDER_AUTHENTICATION_SECRET" {
  type        = string
  description = "Secret must be set with prefix and env vars: export TF_VAR_MICROSOFT_PROVIDER_AUTHENTICATION_SECRET="
}


### RESOURCES ###

# Generate a random integer to create a globally unique name
resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azurerm_key_vault" "adc-app-key-vault-dev" {
  name                        = "adc-app-key-vault-dev"
  location                    = var.resource_group_location
  resource_group_name         = var.resource_group_name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  purge_protection_enabled    = false

  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get",
    ]

    secret_permissions = [
      "Get",
    ]

    storage_permissions = [
      "Get",
    ]
  }
}

resource "azurerm_storage_account" "adcappstoraccdev" {
  name                     = "adcappstoraccdev"
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  account_kind             = "BlobStorage"
}

resource "azurerm_container_registry" "adcxappdev" {
  name                = "containerRegistry1dev"
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  sku                 = "Standard"
  admin_enabled       = true
}

resource "azurerm_service_plan" "adc-app-service" {
  name                = "ASP-adcapp-${random_integer.ri.result}"
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  os_type             = "Linux"
  sku_name            = "B1"
}

# resource "azurerm_linux_web_app" "adc-app-dev" {
#   name                = "adc-app-dev"
#   resource_group_name = var.resource_group_name
#   location            = var.resource_group_location
#   service_plan_id     = azurerm_service_plan.adc-app-service.id
#   https_only          = true

#   app_settings = {d
#     "AZURE_STORAGE_CONNECTION_STRING"          = var.AZURE_STORAGE_CONNECTION_STRING
#     "MICROSOFT_PROVIDER_AUTHENTICATION_SECRET" = var.MICROSOFT_PROVIDER_AUTHENTICATION_SECRET
#     "WEBSITES_ENABLE_APP_SERVICE_STORAGE"      = false
#   }

#   auth_settings_v2 {
#     auth_enabled           = true
#     require_authentication = true
#     unauthenticated_action = "RedirectToLoginPage"

#     microsoft_v2 {
#       client_id                  = "71e5ffef-d511-4071-b66f-4773cef6a5d1"
#       client_secret_setting_name = "MICROSOFT_PROVIDER_AUTHENTICATION_SECRET"
#     }
#     login {
#     }
#   }

#   site_config {
#     minimum_tls_version = "1.2"
#     # application_stack {
#     #   docker_image_name        = "adcapp:latest"
#     #   docker_registry_url      = "https://${azurerm_container_registry.adcxappdev.login_server}"
#     #   docker_registry_username = azurerm_container_registry.adcxappdev.admin_username
#     #   docker_registry_password = azurerm_container_registry.adcxappdev.admin_password
#     # }
#   }
# }
