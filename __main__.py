import logging

import pulumi

from services.ec2 import (
    create_ec2_instance,
    create_internet_gateway,
    create_ipv4_public_ip,
    create_route,
    create_security_group,
    create_security_group_egress,
    create_security_group_ingress,
    create_subnet,
    create_vpc,
    get_route_table,
)
from services.rds import create_rds_instance, create_rds_subnet_group
from services.s3 import create_s3_bucket

if __name__ == "__main__":
    logger = logging.getLogger("pulumi")
    logger.setLevel(logging.INFO)

    logging.info("Creating infrastructure for MLflow Tracking Server")

    name_vpc = "mlflow-vpc"
    cidr_block_vpc = "10.0.0.0/16"
    vpc = create_vpc(name_vpc, cidr_block_vpc)
    logging.info(f"VPC created: {vpc.id}")

    name_subnet_1 = "mlflow-subnet-1"
    cidr_block_subnet_1 = "10.0.1.0/24"
    availability_zone_1 = "eu-west-2a"

    subnet_1 = create_subnet(
        name_subnet_1, vpc.id, cidr_block_subnet_1, availability_zone_1
    )
    logging.info(f"Subnet created: {subnet_1.id}")

    name_subnet_2 = "mlflow-subnet-2"
    cidr_block_subnet_2 = "10.0.2.0/24"
    availability_zone_2 = "eu-west-2b"
    subnet_2 = create_subnet(
        name_subnet_2, vpc.id, cidr_block_subnet_2, availability_zone_2
    )

    name_ig = "mlflow-ig"
    ig = create_internet_gateway(name_ig, vpc.id)
    logging.info(f"Internet Gateway created: {ig.id}")

    ingress_1_from_to_ports = [22, 22]
    ingress_1_protocol = "tcp"
    ingress_1_cidr_blocks = ["0.0.0.0/0"]
    ingress_1 = create_security_group_ingress(
        ingress_1_from_to_ports,
        ingress_1_protocol,
        ingress_1_cidr_blocks,
    )
    logging.info(f"Security Group Ingress created: {ingress_1}")

    ingress_2_from_to_ports = [80, 80]
    ingress_2_protocol = "tcp"
    ingress_2_cidr_blocks = ["0.0.0.0/0"]
    ingress_2 = create_security_group_ingress(
        ingress_2_from_to_ports,
        ingress_2_protocol,
        ingress_2_cidr_blocks,
    )
    logging.info(f"Security Group Ingress created: {ingress_2}")

    ingress_3_from_to_ports = [5000, 5000]
    ingress_3_protocol = "tcp"
    ingress_3_cidr_blocks = ["0.0.0.0/0"]
    ingress_3 = create_security_group_ingress(
        ingress_3_from_to_ports,
        ingress_3_protocol,
        ingress_3_cidr_blocks,
    )
    logging.info(f"Security Group Ingress created: {ingress_3}")

    ingress_4_from_to_ports = [443, 443]
    ingress_4_protocol = "tcp"
    ingress_4_cidr_blocks = ["0.0.0.0/0"]
    ingress_4 = create_security_group_ingress(
        ingress_4_from_to_ports,
        ingress_4_protocol,
        ingress_4_cidr_blocks,
    )

    egress_1_from_to_ports = [0, 0]
    egress_1_protocol = "-1"
    egress_1_cidr_blocks = ["0.0.0.0/0"]
    egress_1 = create_security_group_egress(
        egress_1_from_to_ports,
        egress_1_protocol,
        egress_1_cidr_blocks,
    )
    logging.info(f"Security Group Egress created: {egress_1}")

    security_group_name = "mlflow-sg"
    security_group = create_security_group(
        security_group_name,
        vpc.id,
        [ingress_1, ingress_2, ingress_3, ingress_4],
        [egress_1],
    )
    logging.info(f"Security Group created: {security_group.id}")

    key_name = "mlflow-key"
    ec2_name = "mlflow-ec2"
    ami = "ami-0e5f882be1900e43b"
    instance_type = "t2.micro"
    server = create_ec2_instance(
        ec2_name,
        instance_type=instance_type,
        ami=ami,
        subnet_id=subnet_1.id,
        vpc_security_group_ids=[security_group.id],
        key_name=key_name,
    )
    logging.info(f"EC2 Instance created: {server.id}")

    public_ip = create_ipv4_public_ip("mlflow-public-ip", server.id)
    logging.info(f"Public IP created: {public_ip.id}")

    route_table_id = "(the id of the route table)"
    name_route = "mlflow-route"
    route_table = get_route_table(name_route, route_table_id)
    route_1 = create_route("route_1", route_table.id, "0.0.0.0/0", ig.id)
    logging.info(f"Route created: {route_1.id}")

    name_rds_subnet_group = "mlflow-rds-subnet-group"
    subnet_ids = [subnet_1.id, subnet_2.id]
    rds_subnet_group = create_rds_subnet_group(name_rds_subnet_group, subnet_ids)
    logging.info(f"RDS Subnet Group created: {rds_subnet_group.id}")

    ingress_3_from_to_ports = [5432, 5432]
    ingress_3_protocol = "tcp"
    ingress_3_cidr_blocks = ["0.0.0.0/0"]
    ingress_3 = create_security_group_ingress(
        ingress_3_from_to_ports,
        ingress_3_protocol,
        ingress_3_cidr_blocks,
    )
    logging.info(f"RDS Security Group Ingress created: {ingress_3}")

    security_group_name_rds = "mlflow-rds-sg"
    security_group_rds = create_security_group(
        security_group_name_rds, vpc.id, [ingress_3], [egress_1]
    )
    logging.info(f"RDS Security Group created: {security_group_rds.id}")

    rds_name = "metadata-rds-mlflow"
    db_name = "mlflow"
    username = "mlflowadmin"
    password = "Mlfl0wPassw0rd!"
    rds_instance = create_rds_instance(
        rds_name,
        db_name,
        rds_subnet_group.id,
        security_group_rds.id,
        username,
        password,
    )
    logging.info(f"RDS Instance created: {rds_instance.id}")

    name_s3_bucket = "mlflow-artifacts-s3"
    acl = "private"
    s3_bucket = create_s3_bucket(name_s3_bucket, acl)
    logging.info(f"S3 Bucket created: {s3_bucket.id}")

    pulumi.export("vpc_id", vpc.id)
    pulumi.export("subnet_1_id", subnet_1.id)
    pulumi.export("subnet_2_id", subnet_2.id)
    pulumi.export("security_group_id", security_group.id)
    pulumi.export("ec2_instance_id", server.id)
    pulumi.export("public_ip_id", public_ip.id)
    pulumi.export("rds_subnet_group_id", rds_subnet_group.id)
    pulumi.export("security_group_rds_id", security_group_rds.id)
    pulumi.export("rds_instance_id", rds_instance.id)
    pulumi.export("s3_bucket_id", s3_bucket.id)
