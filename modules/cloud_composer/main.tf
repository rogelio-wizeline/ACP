# Google Cloud Composer resources
# GCC
resource "google_composer_environment" "test" {
  name   = "example-composer-env"
  region = "us-central1"
}