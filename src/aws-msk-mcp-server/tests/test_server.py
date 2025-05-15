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
"""Tests for the msk MCP Server."""

import pytest
from awslabs.msk_mcp_server.server import get_broker_info, get_cluster_info, list_clusters
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch


# @pytest.mark.asyncio
# class TestMathTool:
#     """Test suite for the math_tool function."""

#     async def test_addition(self):
#         """Test addition operations with integers and floats."""
#         # Test integer addition
#         assert await math_tool('add', 2, 3) == 5
#         # Test float addition
#         assert await math_tool('add', 2.5, 3.5) == 6.0

#     async def test_subtraction(self):
#         """Test subtraction operations with integers and floats."""
#         # Test integer subtraction
#         assert await math_tool('subtract', 5, 3) == 2
#         # Test float subtraction
#         assert await math_tool('subtract', 5.5, 2.5) == 3.0

#     async def test_multiplication(self):
#         """Test multiplication operations with integers and floats."""
#         # Test integer multiplication
#         assert await math_tool('multiply', 4, 3) == 12
#         # Test float multiplication
#         assert await math_tool('multiply', 2.5, 2) == 5.0

#     async def test_division(self):
#         """Test division operations with integers and floats."""
#         # Test integer division
#         assert await math_tool('divide', 6, 2) == 3.0
#         # Test float division
#         assert await math_tool('divide', 5.0, 2.0) == 2.5

#     async def test_division_by_zero(self):
#         """Test that division by zero raises appropriate ValueError."""
#         # Test division by zero raises ValueError
#         with pytest.raises(ValueError) as exc_info:
#             await math_tool('divide', 5, 0)
#         assert str(exc_info.value) == 'The denominator 0 cannot be zero.'

#     async def test_invalid_operation(self):
#         """Test that invalid operations raise appropriate ValueError."""
#         # Test invalid operation raises ValueError
#         with pytest.raises(ValueError) as exc_info:
#             await math_tool('power', 2, 3)
#         assert 'Invalid operation: power' in str(exc_info.value)


@pytest.mark.asyncio
class TestMSKTools:
    """Test suite for MSK tools."""

    async def test_list_clusters(self):
        """Test listing MSK clusters."""
        mock_response = {
            'ClusterInfoList': [
                {
                    'ClusterName': 'test-cluster',
                    'ClusterArn': 'arn:aws:kafka:us-west-2:123456789012:cluster/test-cluster',
                    'State': 'ACTIVE',
                    'CreationTime': datetime(2023, 1, 1, tzinfo=timezone.utc),
                }
            ]
        }

        with patch('boto3.client') as mock_boto:
            mock_kafka = MagicMock()
            mock_kafka.list_clusters.return_value = mock_response
            mock_boto.return_value = mock_kafka

            result = await list_clusters()

            assert len(result) == 1
            assert result[0]['ClusterName'] == 'test-cluster'
            assert result[0]['Status'] == 'ACTIVE'
            assert result[0]['CreationTime'] == '2023-01-01T00:00:00+00:00'

    async def test_get_cluster_info(self):
        """Test getting detailed cluster information."""
        mock_cluster_response = {
            'ClusterInfo': {
                'ClusterName': 'test-cluster',
                'State': 'ACTIVE',
                'BrokerNodeInfo': {'BrokerNodeInfoList': [{'BrokerId': 1}, {'BrokerId': 2}]},
                'ZookeeperConnectString': 'zk1:2181,zk2:2181',
                'EncryptionInfo': {'EncryptionAtRest': {'DataVolumeKMSKeyId': 'key-1'}},
                'EnhancedMonitoring': 'DEFAULT',
                'Tags': {'Environment': 'test'},
                'CreationTime': datetime(2023, 1, 1, tzinfo=timezone.utc),
            }
        }

        mock_broker_response = {'BootstrapBrokerString': 'broker1:9092,broker2:9092'}

        with patch('boto3.client') as mock_boto:
            mock_kafka = MagicMock()
            mock_kafka.describe_cluster.return_value = mock_cluster_response
            mock_kafka.get_bootstrap_brokers.return_value = mock_broker_response
            mock_boto.return_value = mock_kafka

            result = await get_cluster_info('test-arn')

            assert result['ClusterName'] == 'test-cluster'
            assert result['Status'] == 'ACTIVE'
            assert result['BrokerCount'] == 2
            assert result['ZookeeperConnectString'] == 'zk1:2181,zk2:2181'
            assert result['BootstrapBrokerString'] == 'broker1:9092,broker2:9092'
            assert result['CreationTime'] == '2023-01-01T00:00:00+00:00'

    async def test_get_broker_info(self):
        """Test getting broker information."""
        mock_response = {
            'ClusterInfo': {
                'BrokerNodeInfo': {
                    'BrokerNodeInfoList': [
                        {
                            'BrokerId': 1,
                            'BrokerType': 'SYNC',
                            'InstanceType': 't3.small',
                            'ClientSubnet': 'subnet-1',
                            'SecurityGroups': ['sg-1'],
                            'BrokerState': {'Code': 'RUNNING'},
                        },
                        {
                            'BrokerId': 2,
                            'BrokerType': 'SYNC',
                            'InstanceType': 't3.small',
                            'ClientSubnet': 'subnet-2',
                            'SecurityGroups': ['sg-1'],
                            'BrokerState': {'Code': 'RUNNING'},
                        },
                    ]
                }
            }
        }

        with patch('boto3.client') as mock_boto:
            mock_kafka = MagicMock()
            mock_kafka.describe_cluster.return_value = mock_response
            mock_boto.return_value = mock_kafka

            result = await get_broker_info('test-arn')

            assert len(result) == 2
            assert result[0]['BrokerId'] == 1
            assert result[0]['BrokerType'] == 'SYNC'
            assert result[0]['InstanceType'] == 't3.small'
            assert result[0]['Status'] == 'RUNNING'
            assert result[1]['BrokerId'] == 2
            assert result[1]['SecurityGroups'] == ['sg-1']
