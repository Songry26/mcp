# AWS Labs MSK MCP Server

A Model Context Protocol (MCP) Server for AWS MSK (Managed Streaming for Apache Kafka).

## Overview

This MCP server provides tools to interact with Amazon MSK clusters through a standardized interface. It allows you to list clusters, retrieve detailed cluster information, and get broker details.

## Prerequisites

1. AWS credentials configured with access to Amazon MSK
2. Python 3.10 or later
3. Required Python packages (installed via uv):
   - loguru>=0.7.0
   - mcp[cli]>=1.6.0
   - pydantic>=2.10.6
   - boto3>=1.34.0

## Installation

```bash
# Using uv (recommended)
uv pip install -e .
```

## Available Tools

### ListClusters

Lists all MSK clusters in the current AWS region.

Example usage:
```python
<use_mcp_tool>
<server_name>awslabs.msk-mcp-server</server_name>
<tool_name>ListClusters</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>
```

Returns information about each cluster including:
- ClusterName
- ClusterArn
- Status
- CreationTime

### GetClusterInfo

Gets detailed information about a specific MSK cluster.

Example usage:
```python
<use_mcp_tool>
<server_name>awslabs.msk-mcp-server</server_name>
<tool_name>GetClusterInfo</tool_name>
<arguments>
{
  "cluster_arn": "your-cluster-arn"
}
</arguments>
</use_mcp_tool>
```

Returns detailed cluster information including:
- ClusterName
- Status
- BrokerCount
- ZookeeperConnectString
- BootstrapBrokerString
- EncryptionInfo
- EnhancedMonitoring
- Tags
- CreationTime

### GetBrokerInfo

Gets information about all brokers in a specific MSK cluster.

Example usage:
```python
<use_mcp_tool>
<server_name>awslabs.msk-mcp-server</server_name>
<tool_name>GetBrokerInfo</tool_name>
<arguments>
{
  "cluster_arn": "your-cluster-arn"
}
</arguments>
</use_mcp_tool>
```

Returns information about each broker including:
- BrokerId
- BrokerType
- InstanceType
- ClientSubnet
- SecurityGroups
- Status

## Installation Placeholder

The instructions section is under development
