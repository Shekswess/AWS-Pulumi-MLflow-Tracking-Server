import logging

from pulumi_aws import ec2

logger = logging.getLogger("ec2")
logger.setLevel(logging.INFO)


def create_vpc(name: str, cidr_block: str) -> ec2.Vpc:
    """
    Create a VPC
    :param name: The name of the VPC
    :param cidr_block: The CIDR block of the VPC
    :return: The VPC
    """
    try:
        logger.info(f"Creating VPC: {name}")
        vpc = ec2.Vpc(
            name,
            cidr_block=cidr_block,
            enable_dns_support=True,
            enable_dns_hostnames=True,
        )
        logger.info(f"VPC created: {vpc.id}")
        return vpc
    except Exception as error:
        logger.error(f"Error creating VPC: {error}")
        raise error


def create_subnet(
    name: str, vpc_id: str, cidr_block: str, availability_zone: str
) -> ec2.Subnet:
    """
    Create a subnet
    :param name: The name of the subnet
    :param vpc_id: The ID of the VPC
    :param cidr_block: The CIDR block of the subnet
    :param availability_zone: The availability zone of the subnet
    :return: The subnet
    """
    try:
        logger.info(f"Creating subnet: {name}")
        subnet = ec2.Subnet(
            name,
            vpc_id=vpc_id,
            cidr_block=cidr_block,
            availability_zone=availability_zone,
        )
        return subnet
    except Exception as error:
        logger.error(f"Error creating subnet: {error}")
        raise error


def create_internet_gateway(name: str, vpc_id: str) -> ec2.InternetGateway:
    """
    Create an internet gateway
    :param name: The name of the internet gateway
    :param vpc_id: The ID of the VPC
    :return: The internet gateway
    """
    try:
        logger.info(f"Creating internet gateway: {name}")
        ig = ec2.InternetGateway(name, vpc_id=vpc_id)
        return ig
    except Exception as error:
        logger.error(f"Error creating internet gateway: {error}")
        raise error


def create_security_group_ingress(
    from_to_ports: list[int],
    protocol: str,
    cidr_blocks: list[str],
) -> ec2.SecurityGroupIngressArgs:
    """
    Create a security group ingress
    :param from_to_ports: The from and to ports
    :param protocol: The protocol
    :param cidr_blocks: The CIDR blocks
    :return: The security group ingress
    """
    try:
        logger.info(
            f"Creating security group ingress: {from_to_ports} {protocol} {cidr_blocks}"
        )
        ingress = ec2.SecurityGroupIngressArgs(
            from_port=from_to_ports[0],
            to_port=from_to_ports[1],
            protocol=protocol,
            cidr_blocks=cidr_blocks,
        )
        return ingress
    except Exception as error:
        logger.error(f"Error creating security group ingress: {error}")
        raise error


def create_security_group_egress(
    from_to_ports: list[int],
    protocol: str,
    cidr_blocks: list[str],
) -> ec2.SecurityGroupEgressArgs:
    """
    Create a security group egress
    :param from_to_ports: The from and to ports
    :param protocol: The protocol
    :param cidr_blocks: The CIDR blocks
    :return: The security group egress
    """
    try:
        logger.info(
            f"Creating security group egress: {from_to_ports} {protocol} {cidr_blocks}"
        )
        egress = ec2.SecurityGroupEgressArgs(
            from_port=from_to_ports[0],
            to_port=from_to_ports[1],
            protocol=protocol,
            cidr_blocks=cidr_blocks,
        )
        return egress
    except Exception as error:
        logger.error(f"Error creating security group egress: {error}")
        raise error


def create_security_group(
    name: str,
    vpc_id: str,
    security_ingress: list[ec2.SecurityGroupIngressArgs],
    security_egress: list[ec2.SecurityGroupEgressArgs],
) -> ec2.SecurityGroup:
    """
    Create a security group
    :param name: The name of the security group
    :param vpc_id: The ID of the VPC
    :param security_ingress: The security group ingress
    :param security_egress: The security group egress
    :return: The security group
    """
    try:
        logger.info(f"Creating security group: {name}")
        security_group = ec2.SecurityGroup(
            name,
            vpc_id=vpc_id,
            ingress=security_ingress,
            egress=security_egress,
        )
        return security_group
    except Exception as error:
        logger.error(f"Error creating security group: {error}")
        raise error


def create_ec2_instance(
    name: str,
    instance_type: str,
    ami: str,
    subnet_id: str,
    vpc_security_group_ids: list,
    key_name: str,
) -> ec2.Instance:
    """
    Create an EC2 instance
    :param name: The name of the EC2 instance
    :param instance_type: The instance type
    :param ami: The AMI
    :param subnet_id: The ID of the subnet
    :param vpc_security_group_ids: The IDs of the security groups
    :param key_name: The name of the key pair
    :return: The EC2 instance
    """
    try:
        logger.info(f"Creating EC2 instance: {name}")
        instance = ec2.Instance(
            name,
            instance_type=instance_type,
            ami=ami,
            subnet_id=subnet_id,
            vpc_security_group_ids=vpc_security_group_ids,
            key_name=key_name,
        )
        return instance
    except Exception as error:
        logger.error(f"Error creating EC2 instance: {error}")
        raise error


def create_ipv4_public_ip(name: str, server_id: str) -> ec2.Eip:
    """
    Create an IPv4 public IP
    :param name: The name of the IPv4 public IP
    :param server_id: The ID of the server
    :return: The IPv4 public IP
    """
    try:
        public_ip = ec2.Eip(name, instance=server_id)
        return public_ip
    except Exception as error:
        logger.error(f"Error creating IPv4 public IP: {error}")
        raise error


def get_route_table(name: str, route_table_id: str) -> ec2.RouteTable:
    """
    Get a route table
    :param name: The name of the route table
    :param route_table_id: The ID of the route table
    :return: The route table
    """
    try:
        route_table = ec2.RouteTable.get(name, route_table_id)
        return route_table
    except Exception as error:
        logger.error(f"Error getting route table: {error}")
        raise error


def create_route(
    name: str,
    route_table_id: str,
    destination_cidr_block: str,
    gateway_id: str,
) -> ec2.Route:
    """
    Create a route
    :param name: The name of the route
    :param route_table_id: The ID of the route table
    :param destination_cidr_block: The destination CIDR block
    :param gateway_id: The ID of the gateway
    :return: The route
    """
    try:
        route = ec2.Route(
            name,
            route_table_id=route_table_id,
            destination_cidr_block=destination_cidr_block,
            gateway_id=gateway_id,
        )
        return route
    except Exception as error:
        logger.error(f"Error creating route: {error}")
        raise error
