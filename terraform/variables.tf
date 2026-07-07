variable "aws_region" {
  description = "Región de AWS donde se despliega todo"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto, usado como prefijo en los recursos"
  type        = string
  default     = "taskmaster"
}

variable "alert_email" {
  description = "Correo donde se reciben las alertas de CloudWatch"
  type        = string
}