# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""awslabs AWS MSK MCP Server implementation."""

import argparse
import boto3
import os
import sys
from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field
from typing import Any, Dict, List


# Set up logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

mcp = FastMCP(
    'awslabs.msk-mcp-server',
    instructions="""
    # AWS MSK MCP Server

    This server provides tools to interact with Amazon Managed Streaming for Apache Kafka (MSK) clusters.

    ## Prerequisites

    1. AWS credentials configured with access to Amazon MSK
    2. Configure AWS credentials using ada (environment variables not set up)
    3. Ensure your IAM role/user has permissions to use Amazon MSK

    ## Best Practices

    - Use ListClusters to get an overview of all MSK clusters in your region
    - Use GetClusterInfo to get detailed information about a specific cluster
    - Use GetBrokerInfo to understand the broker configuration and status
    - Always check cluster and broker status before performing operations
    - Monitor broker health through the status information

    ## Tool Selection Guide

    - Use ListClusters when: You need to see all available MSK clusters
    - Use GetClusterInfo when: You need detailed information about a specific cluster
    - Use GetBrokerInfo when: You need to check broker health or configuration

    ## Configuration

    The server uses the AWS profile specified in AWS_PROFILE environment variable.
    If not provided, it defaults to the "default" profile.
    """,
    dependencies=[
        'pydantic',
        'loguru',
        'boto3',
    ],
)


@mcp.tool()
async def list_clusters(
    ctx: Context,
) -> List[Dict[str, Any]]:
    """List all MSK clusters in the current AWS region.

    ## Usage

    This tool retrieves a list of all MSK clusters in your AWS region.
    Use it to get an overview of your MSK infrastructure.

    ## Output Format

    Returns a list of dictionaries, each containing:
    - ClusterName: Name of the cluster
    - ClusterArn: ARN of the cluster
    - Status: Current status of the cluster (ACTIVE, CREATING, UPDATING, etc.)
    - CreationTime: When the cluster was created (ISO format)

    ## Example Response

    ```json
    [
        {
            "ClusterName": "my-kafka-cluster",
            "ClusterArn": "arn:aws:kafka:us-west-2:123456789012:cluster/my-kafka-cluster/abcd1234-...",
            "Status": "ACTIVE",
            "CreationTime": "2023-01-01T00:00:00Z"
        }
    ]
    ```

    Args:
        ctx: MCP context for logging and error handling

    Returns:
        List of dictionaries containing cluster information
    """
    logger.debug('Listing MSK clusters')
    try:
        kafka_client = boto3.client('kafka')
        response = kafka_client.list_clusters()
        clusters = response.get('ClusterInfoList', [])

        result = [
            {
                'ClusterName': cluster.get('ClusterName'),
                'ClusterArn': cluster.get('ClusterArn'),
                'Status': cluster.get('State'),
                'CreationTime': cluster.get('CreationTime').isoformat()
                if cluster.get('CreationTime')
                else None,
            }
            for cluster in clusters
        ]

        logger.debug(f'Found {len(result)} MSK clusters')
        return result
    except Exception as e:
        error_msg = f'Failed to list MSK clusters: {str(e)}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise ValueError(error_msg)


@mcp.tool()
async def get_cluster_info(
    ctx: Context,
    cluster_arn: str = Field(description='The ARN of the cluster to describe'),
) -> Dict[str, Any]:
    """Get detailed information about a specific MSK cluster.

    ## Usage

    This tool retrieves detailed information about a specific MSK cluster.
    Use it to understand the cluster's configuration and current state.

    ## Output Format

    Returns a dictionary containing:
    - ClusterName: Name of the cluster
    - Status: Current status of the cluster
    - BrokerCount: Number of broker nodes
    - ZookeeperConnectString: Zookeeper connection string
    - BootstrapBrokerString: Bootstrap broker connection string
    - EncryptionInfo: Encryption settings
    - EnhancedMonitoring: Monitoring level
    - Tags: Cluster tags
    - CreationTime: When the cluster was created

    ## Example Response

    ```json
    {
        "ClusterName": "my-kafka-cluster",
        "Status": "ACTIVE",
        "BrokerCount": 3,
        "ZookeeperConnectString": "z-1.my-kafka-cluster.123456.kafka.us-west-2.amazonaws.com:2181",
        "BootstrapBrokerString": "b-1.my-kafka-cluster.123456.kafka.us-west-2.amazonaws.com:9092",
        "EncryptionInfo": {
            "EncryptionAtRest": {"DataVolumeKMSKeyId": "arn:aws:kms:..."},
            "EncryptionInTransit": {"ClientBroker": "TLS"}
        },
        "EnhancedMonitoring": "DEFAULT",
        "Tags": {},
        "CreationTime": "2023-01-01T00:00:00Z"
    }
    ```

    Args:
        ctx: MCP context for logging and error handling
        cluster_arn: The ARN of the cluster to describe

    Returns:
        Dictionary containing detailed cluster information
    """
    logger.debug(f'Getting info for MSK cluster: {cluster_arn}')
    try:
        kafka_client = boto3.client('kafka')
        response = kafka_client.describe_cluster(ClusterArn=cluster_arn)
        cluster_info = response.get('ClusterInfo', {})

        # Get broker information
        broker_response = kafka_client.get_bootstrap_brokers(ClusterArn=cluster_arn)

        result = {
            'ClusterName': cluster_info.get('ClusterName'),
            'Status': cluster_info.get('State'),
            'BrokerCount': len(
                cluster_info.get('BrokerNodeInfo', {}).get('BrokerNodeInfoList', [])
            ),
            'ZookeeperConnectString': cluster_info.get('ZookeeperConnectString'),
            'BootstrapBrokerString': broker_response.get('BootstrapBrokerString'),
            'EncryptionInfo': cluster_info.get('EncryptionInfo'),
            'EnhancedMonitoring': cluster_info.get('EnhancedMonitoring'),
            'Tags': cluster_info.get('Tags', {}),
            'CreationTime': cluster_info.get('CreationTime').isoformat()
            if cluster_info.get('CreationTime')
            else None,
        }

        logger.debug(f'Successfully retrieved info for cluster {result["ClusterName"]}')
        return result
    except Exception as e:
        error_msg = f'Failed to get cluster info: {str(e)}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise ValueError(error_msg)


@mcp.tool()
async def get_broker_info(
    ctx: Context,
    cluster_arn: str = Field(description='The ARN of the cluster whose brokers to describe'),
) -> List[Dict[str, Any]]:
    """Get information about all brokers in a specific MSK cluster.

    ## Usage

    This tool retrieves information about all broker nodes in an MSK cluster.
    Use it to monitor broker health and understand the cluster's infrastructure.

    ## Output Format

    Returns a list of dictionaries, each containing:
    - BrokerId: ID of the broker
    - BrokerType: Type of broker instance (SYNC or ASYNC)
    - InstanceType: EC2 instance type (e.g., kafka.m5.large)
    - ClientSubnet: Subnet where the broker is located
    - SecurityGroups: List of security groups
    - Status: Current status of the broker

    ## Example Response

    ```json
    [
        {
            "BrokerId": 1,
            "BrokerType": "SYNC",
            "InstanceType": "kafka.m5.large",
            "ClientSubnet": "subnet-12345678",
            "SecurityGroups": ["sg-12345678"],
            "Status": "ACTIVE"
        }
    ]
    ```

    ## Status Codes

    Common broker status codes:
    - ACTIVE: Broker is running normally
    - CREATING: Broker is being created
    - UPDATING: Broker is being updated
    - MAINTENANCE: Broker is undergoing maintenance
    - REBOOTING: Broker is rebooting
    - INACTIVE: Broker is not active

    Args:
        ctx: MCP context for logging and error handling
        cluster_arn: The ARN of the cluster whose brokers to describe

    Returns:
        List of dictionaries containing broker information
    """
    logger.debug(f'Getting broker info for MSK cluster: {cluster_arn}')
    try:
        kafka_client = boto3.client('kafka')
        response = kafka_client.describe_cluster(ClusterArn=cluster_arn)
        cluster_info = response.get('ClusterInfo', {})
        broker_info = cluster_info.get('BrokerNodeInfo', {}).get('BrokerNodeInfoList', [])

        result = [
            {
                'BrokerId': broker.get('BrokerId'),
                'BrokerType': broker.get('BrokerType'),
                'InstanceType': broker.get('InstanceType'),
                'ClientSubnet': broker.get('ClientSubnet'),
                'SecurityGroups': broker.get('SecurityGroups', []),
                'Status': broker.get('BrokerState', {}).get('Code'),
            }
            for broker in broker_info
        ]

        logger.debug(f'Found {len(result)} brokers in cluster')
        return result
    except Exception as e:
        error_msg = f'Failed to get broker info: {str(e)}'
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise ValueError(error_msg)


def main():
    """Run the MCP server with CLI argument support."""
    parser = argparse.ArgumentParser(
        description='An AWS Labs Model Context Protocol (MCP) server for AWS MSK'
    )
    parser.add_argument('--sse', action='store_true', help='Use SSE transport')
    parser.add_argument('--port', type=int, default=8888, help='Port to run the server on')

    args = parser.parse_args()

    # Log startup information
    logger.info('Starting AWS MSK MCP Server')

    # Run server with appropriate transport
    if args.sse:
        logger.info(f'Using SSE transport on port {args.port}')
        mcp.settings.port = args.port
        mcp.run(transport='sse')
    else:
        logger.info('Using standard stdio transport')
        mcp.run()


if __name__ == '__main__':
    main()
