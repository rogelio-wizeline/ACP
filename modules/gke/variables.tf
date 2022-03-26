variable "project_id" {}
variable "region" {}
variable "zone" {}

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

variable "vpc_id" {
  type = string
}

variable "subnet_id" {
  type = string
}