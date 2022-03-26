terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }

  required_version = ">= 0.14"
}

module "vpc" {
    source = "./modules/vpc"

    project_id = var.project_id
    region = var.region
    zone = var.zone
}

module "composer" {
    source = "./modules/cloud_composer"

    project_id = var.project_id
    vpc_id = module.vpc.vpc
    subnet_id = module.vpc.subnet
}

module "cloudsql" {
    source = "./modules/cloud_sql"

    instance_tier = var.instance_tier
    disk_space = var.disk_space
    zone = var.zone
    cloud_sql_username = var.cloud_sql_username
    cloud_sql_password = var.cloud_sql_password
}

module "gke" {
    source = "./modules/gke"

    project_id = var.project_id
    gke_username = var.gke_username
    region = var.region
    zone = var.zone
    gke_password = var.gke_password
    gke_num_nodes = var.gke_num_nodes
    vpc_id = module.vpc.vpc
    subnet_id = module.vpc.subnet
}
