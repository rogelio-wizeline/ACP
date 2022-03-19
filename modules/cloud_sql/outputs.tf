output "instance_connection_name" {
  value = google_sql_database_instance.cloud_sql_instance.connection_name
}

output "instance_ip_address" {
  value = google_sql_database_instance.cloud_sql_instance.ip_address
}

output "database" {
  value = google_sql_database.database.id
}

output "database_connection" {
  value = google_sql_database.database.self_link
}