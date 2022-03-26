output "subnet" {
  value = google_compute_subnetwork.subnet.id
}

output "vpc" {
  value = google_compute_network.vpc.id
}