"""
Cluster Information API Module

This module provides functions to retrieve information about MSK clusters.
"""

import boto3
from mcp.server.fastmcp import FastMCP

from .describe_cluster import describe_cluster
from .describe_cluster_operation import describe_cluster_operation
from .get_bootstrap_brokers import get_bootstrap_brokers
from .get_cluster_policy import get_cluster_policy
from .get_compatible_kafka_versions import get_compatible_kafka_versions
from .list_client_vpc_connections import list_client_vpc_connections
from .list_cluster_operations import list_cluster_operations
from .list_nodes import list_nodes
from .list_scram_secrets import list_scram_secrets


def register_module(mcp: FastMCP) -> None:
    @mcp.tool(name="describe_cluster_operation")
    def describe_cluster_operation_tool(region, cluster_operation_arn):
        """
        Returns information about a cluster operation.

        Args:
            cluster_operation_arn (str): The Amazon Resource Name (ARN) of the cluster operation
            region (str): AWS region

        Returns:
            dict: Information about the cluster operation
        """
        # Create a boto3 client
        client = boto3.client("kafka", region_name=region)
        return describe_cluster_operation(cluster_operation_arn, client)

    @mcp.tool(name="get_cluster_info")
    def get_cluster_info(region, cluster_arn=None, info_type="all", kwargs={}):
        """
        Unified API to retrieve various types of information about MSK clusters.

        Args:
            cluster_arn (str): The ARN of the cluster to get information for
            info_type (str): Type of information to retrieve (metadata, brokers, nodes, compatible_versions,
                            policy, operations, client_vpc_connections, scram_secrets, all)
            region (str): AWS region
            kwargs (dict, optional): Additional arguments specific to each info type:
                      - For "operations":
                          - max_results (int, optional): Maximum number of operations to return (default: 10)
                          - next_token (str, optional): Token for pagination
                      - For "client_vpc_connections":
                          - max_results (int, optional): Maximum number of connections to return (default: 10)
                          - next_token (str, optional): Token for pagination
                      - For "scram_secrets":
                          - max_results (int, optional): Maximum number of secrets to return
                          - next_token (str, optional): Token for pagination

        Returns:
            dict: Cluster information of the requested type, or a dictionary containing all types if info_type is "all"
        """

        # Create a single boto3 client to be shared across all function calls
        client = boto3.client("kafka", region_name=region)

        if info_type == "all":
            # Retrieve all types of information for the cluster
            result = {}

            # Use try-except blocks for each function call to handle potential errors
            try:
                result["metadata"] = describe_cluster(cluster_arn, client)
            except Exception as e:
                result["metadata"] = {"error": str(e)}

            try:
                result["brokers"] = get_bootstrap_brokers(cluster_arn, client)
            except Exception as e:
                result["brokers"] = {"error": str(e)}

            try:
                result["nodes"] = list_nodes(cluster_arn, client)
            except Exception as e:
                result["nodes"] = {"error": str(e)}

            try:
                result["compatible_versions"] = get_compatible_kafka_versions(cluster_arn, client)
            except Exception as e:
                result["compatible_versions"] = {"error": str(e)}

            try:
                result["policy"] = get_cluster_policy(cluster_arn, client)
            except Exception as e:
                result["policy"] = {"error": str(e)}

            try:
                result["operations"] = list_cluster_operations(cluster_arn, client)
            except Exception as e:
                result["operations"] = {"error": str(e)}

            try:
                result["client_vpc_connections"] = list_client_vpc_connections(cluster_arn, client)
            except Exception as e:
                result["client_vpc_connections"] = {"error": str(e)}

            try:
                result["scram_secrets"] = list_scram_secrets(cluster_arn, client)
            except Exception as e:
                result["scram_secrets"] = {"error": str(e)}

            return result
        elif info_type == "metadata":
            return describe_cluster(cluster_arn, client)
        elif info_type == "brokers":
            return get_bootstrap_brokers(cluster_arn, client)
        elif info_type == "nodes":
            return list_nodes(cluster_arn, client)
        elif info_type == "compatible_versions":
            return get_compatible_kafka_versions(cluster_arn, client)
        elif info_type == "policy":
            return get_cluster_policy(cluster_arn, client)
        elif info_type == "operations":
            # Extract only the parameters that list_cluster_operations accepts
            max_results = kwargs.get("max_results", 10)
            next_token = kwargs.get("next_token", None)
            return list_cluster_operations(cluster_arn, client, max_results, next_token)
        elif info_type == "client_vpc_connections":
            # Extract only the parameters that list_client_vpc_connections accepts
            max_results = kwargs.get("max_results", 10)
            next_token = kwargs.get("next_token", None)
            return list_client_vpc_connections(cluster_arn, client, max_results, next_token)
        elif info_type == "scram_secrets":
            # Extract only the parameters that list_scram_secrets accepts
            max_results = kwargs.get("max_results", None)
            next_token = kwargs.get("next_token", None)
            return list_scram_secrets(cluster_arn, client, max_results, next_token)
        else:
            raise ValueError(f"Unsupported info_type: {info_type}")
