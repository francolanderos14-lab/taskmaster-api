output "vpc_id" {
  description = "ID de la VPC creada"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs de las subredes públicas"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs de las subredes privadas"
  value       = aws_subnet.private[*].id
}

output "alb_url" {
  description = "URL publica de la API"
  value       = "http://${aws_lb.main.dns_name}"
}

output "github_actions_role_arn" {
  description = "ARN del rol IAM que GitHub Actions va a asumir"
  value       = aws_iam_role.github_actions.arn
}