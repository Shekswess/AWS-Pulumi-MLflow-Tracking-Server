import logging

from pulumi_aws import rds

logger = logging.getLogger("rds")
logger.setLevel(logging.INFO)


def create_rds_subnet_group(name: str, subnet_ids: list[str]) -> rds.SubnetGroup:
    """
    Create an RDS subnet group
    :param name: The name of the subnet group
    :param subnet_ids: The subnet IDs
    :return: The subnet group
    """
    try:
        logger.info(f"Creating RDS subnet group: {name}")
        subnet_group = rds.SubnetGroup(name, subnet_ids=subnet_ids)
        return subnet_group
    except Exception as error:
        logger.error(f"Error creating RDS subnet group: {error}")
        raise error


def create_rds_instance(
    name: str,
    db_name: str,
    subnet_group_name: str,
    security_group_name: str,
    username: str,
    password: str,
) -> rds.Instance:
    """
    Create an RDS instance
    :param name: The name of the RDS instance
    :param db_name: The name of the database
    :param subnet_group_name: The name of the subnet group
    :param security_group_name: The name of the security group
    :param username: The username for the RDS instance
    :param password: The password for the RDS instance
    :return: The RDS instance
    """
    try:
        logger.info(f"Creating RDS instance: {name}")
        rds_instance = rds.Instance(
            name,
            allocated_storage=20,
            engine="postgres",
            engine_version="13.8",
            instance_class="db.t3.micro",
            db_name=db_name,
            username=username,
            password=password,
            skip_final_snapshot=False,
            db_subnet_group_name=subnet_group_name,
            vpc_security_group_ids=[security_group_name],
        )
        return rds_instance
    except Exception as error:
        logger.error(f"Error creating RDS instance: {error}")
        raise error
