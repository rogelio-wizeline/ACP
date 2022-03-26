# Cloud SQL resources
resource "google_sql_database_instance" "cloud_sql_instance" {
  name             = "main-instance"
  database_version = "POSTGRES_11"
  region           = "us-central1"

  settings {
    tier      = var.instance_tier
    disk_size = var.disk_space

    location_preference {
      zone = var.zone
    }

    ip_configuration {
      authorized_networks {
        value           = "0.0.0.0/0"
        name            = "sql-cluster"
      }
    }
  }

  # deletion_protection = "false"
}


resource "google_sql_database" "database" {
  name     = var.database_name
  instance = google_sql_database_instance.cloud_sql_instance.name
}

resource "google_sql_user" "users" {
  name     = var.cloud_sql_username
  instance = google_sql_database_instance.cloud_sql_instance.name
  host     = "*"
  password = var.cloud_sql_password
}