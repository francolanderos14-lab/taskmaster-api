resource "aws_iam_role" "k3s_instance_role" {
  name = "taskmaster-k3s-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "k3s_ssm_policy" {
  role       = aws_iam_role.k3s_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "k3s_ecr_policy" {
  role       = aws_iam_role.k3s_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "k3s_instance_profile" {
  name = "taskmaster-k3s-instance-profile"
  role = aws_iam_role.k3s_instance_role.name
}

resource "aws_security_group" "k3s_sg" {
  name        = "taskmaster-k3s-sg"
  description = "Security group for k3s EC2 instance"
  vpc_id      = aws_vpc.main.id

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Kubernetes API access from within the VPC"
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  ingress {
    description = "NodePort range for exposing services"
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "k3s_node" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.small"
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.k3s_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.k3s_instance_profile.name

  associate_public_ip_address = true
  monitoring = true

  root_block_device {
    encrypted = true
  }

  user_data = <<-EOF
    #!/bin/bash
    curl -sfL https://get.k3s.io | sh -
  EOF

  tags = {
    Name = "taskmaster-k3s-node"
  }
}