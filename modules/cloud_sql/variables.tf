variable "instance_tier" {
    default = "db-f1-micro"
    description = "instance_tier"
}

variable "disk_space" {
    default = "1"
    description = "Disk size for the instance"
}

variable "zone" {
    description = "zone"
}

variable "database_name" {
  default     = "dbname"
  description = "Database name"
}

variable "database_version" {
  default     = "POSTGRES_11"
  description = "Database version"
}

variable "cloud_sql_username" {
  default     = ""
  description = "Postgres username"
}

variable "cloud_sql_password" {
  default     = ""
  description = "Postgres password"
}