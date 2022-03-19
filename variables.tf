# General
variable "project_id" {
  description = "project id"
}

variable "region" {
  description = "region"
}

variable "zone" {
    description = "zone"
}

# Composer
# SQL
variable "instance_tier" {
    default = "db-f1-micro"
    description = "instance_tier"
}

variable "disk_space" {
    default = "1"
    description = "Disk size for the instance"
}

variable "cloud_sql_username" {
  default     = ""
  description = "Postgres username"
}

variable "cloud_sql_password" {
  default     = ""
  description = "Postgres password"
}

# GKE
variable "gke_username" {
  default     = ""
  description = "gke username"
}

variable "gke_password" {
  default     = ""
  description = "gke password"
}

variable "gke_num_nodes" {
  default     = 2
  description = "number of gke nodes"
}

# VPC