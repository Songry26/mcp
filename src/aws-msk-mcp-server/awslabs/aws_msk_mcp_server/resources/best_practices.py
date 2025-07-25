# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MSK Best Practices Resources.

This module provides resources for accessing AWS MSK best practices and recommendations.
"""

import json
from mcp.server.fastmcp import FastMCP


# Define all constants directly in this file
RECOMMENDED_CPU_UTILIZATION_PERCENT = 60  # Keep CPU (user+sys) under 60% for headroom
MAX_CPU_UTILIZATION_PERCENT = 70  # Avoid exceeding 70% (risk of instability during reassignments)
STORAGE_UTILIZATION_WARNING_PERCENT = 85  # Alert threshold for disk usage
STORAGE_UTILIZATION_CRITICAL_PERCENT = (
    90  # Critical threshold for disk usage (take immediate action)
)
RECOMMENDED_REPLICATION_FACTOR = 3  # Typical replication factor for production clusters
RECOMMENDED_MIN_INSYNC_REPLICAS = 2  # minISR for RF=3 to tolerate one broker failure
UNDER_REPLICATED_PARTITIONS_TOLERANCE = (
    0  # Under-replicated partitions should ideally be zero in steady state
)
LEADER_IMBALANCE_TOLERANCE_PERCENT = 10  # Leader imbalance threshold across brokers

# Resource specifications for supported broker instance types
INSTANCE_SPECS = {
    'kafka.t3.small': {
        'vCPU': 2,
        'Memory (GB)': 2,
        'Network Bandwidth (Gbps)': 5.0,
        'Ingress Recommended (MBps)': 4.8,
        'Ingress Max (MBps)': 7.2,
        'Egress Recommended (MBps)': 9.6,
        'Egress Max (MBps)': 18.0,
        'Partitions per Broker Recommended': 300,
        'Partitions per Broker Max': 300,
    },
    'kafka.m5.large': {
        'vCPU': 2,
        'Memory (GB)': 8,
        'Network Bandwidth (Gbps)': 10.0,
        'Ingress Recommended (MBps)': 4.8,
        'Ingress Max (MBps)': 7.2,
        'Egress Recommended (MBps)': 9.6,
        'Egress Max (MBps)': 18.0,
        'Partitions per Broker Recommended': 1000,
        'Partitions per Broker Max': 1500,
    },
    'kafka.m5.xlarge': {
        'vCPU': 4,
        'Memory (GB)': 16,
        'Network Bandwidth (Gbps)': 10.0,
        'Ingress Recommended (MBps)': 9.6,
        'Ingress Max (MBps)': 14.4,
        'Egress Recommended (MBps)': 19.2,
        'Egress Max (MBps)': 36.0,
        'Partitions per Broker Recommended': 1000,
        'Partitions per Broker Max': 1500,
    },
    'kafka.m5.2xlarge': {
        'vCPU': 8,
        'Memory (GB)': 32,
        'Network Bandwidth (Gbps)': 10.0,
        'Ingress Recommended (MBps)': 19.2,
        'Ingress Max (MBps)': 28.8,
        'Egress Recommended (MBps)': 38.4,
        'Egress Max (MBps)': 72.0,
        'Partitions per Broker Recommended': 2000,
        'Partitions per Broker Max': 3000,
    },
    'kafka.m5.4xlarge': {
        'vCPU': 16,
        'Memory (GB)': 64,
        'Network Bandwidth (Gbps)': 10.0,
        'Ingress Recommended (MBps)': 38.4,
        'Ingress Max (MBps)': 57.6,
        'Egress Recommended (MBps)': 76.8,
        'Egress Max (MBps)': 144.0,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m5.8xlarge': {
        'vCPU': 32,
        'Memory (GB)': 128,
        'Network Bandwidth (Gbps)': 10.0,
        'Ingress Recommended (MBps)': 76.9,
        'Ingress Max (MBps)': 115.4,
        'Egress Recommended (MBps)': 153.8,
        'Egress Max (MBps)': 288.5,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m5.12xlarge': {
        'vCPU': 48,
        'Memory (GB)': 192,
        'Network Bandwidth (Gbps)': 12.0,
        'Ingress Recommended (MBps)': 115.4,
        'Ingress Max (MBps)': 173.1,
        'Egress Recommended (MBps)': 230.8,
        'Egress Max (MBps)': 432.7,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m5.16xlarge': {
        'vCPU': 64,
        'Memory (GB)': 256,
        'Network Bandwidth (Gbps)': 20.0,
        'Ingress Recommended (MBps)': 153.8,
        'Ingress Max (MBps)': 230.7,
        'Egress Recommended (MBps)': 307.7,
        'Egress Max (MBps)': 576.9,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m5.24xlarge': {
        'vCPU': 96,
        'Memory (GB)': 384,
        'Network Bandwidth (Gbps)': 25.0,
        'Ingress Recommended (MBps)': 153.8,
        'Ingress Max (MBps)': 230.7,
        'Egress Recommended (MBps)': 307.7,
        'Egress Max (MBps)': 576.9,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m7g.large': {
        'vCPU': 2,
        'Memory (GB)': 8,
        'Network Bandwidth (Gbps)': 12.5,
        'Ingress Recommended (MBps)': 4.8,
        'Ingress Max (MBps)': 7.2,
        'Egress Recommended (MBps)': 9.6,
        'Egress Max (MBps)': 18.0,
        'Partitions per Broker Recommended': 1000,
        'Partitions per Broker Max': 1500,
    },
    'kafka.m7g.xlarge': {
        'vCPU': 4,
        'Memory (GB)': 16,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 9.6,
        'Ingress Max (MBps)': 14.4,
        'Egress Recommended (MBps)': 19.2,
        'Egress Max (MBps)': 36.0,
        'Partitions per Broker Recommended': 1000,
        'Partitions per Broker Max': 1500,
    },
    'kafka.m7g.2xlarge': {
        'vCPU': 8,
        'Memory (GB)': 32,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 19.2,
        'Ingress Max (MBps)': 28.8,
        'Egress Recommended (MBps)': 38.4,
        'Egress Max (MBps)': 72.0,
        'Partitions per Broker Recommended': 2000,
        'Partitions per Broker Max': 3000,
    },
    'kafka.m7g.4xlarge': {
        'vCPU': 16,
        'Memory (GB)': 64,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 38.4,
        'Ingress Max (MBps)': 57.6,
        'Egress Recommended (MBps)': 76.8,
        'Egress Max (MBps)': 144.0,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m7g.8xlarge': {
        'vCPU': 32,
        'Memory (GB)': 128,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 76.9,
        'Ingress Max (MBps)': 115.4,
        'Egress Recommended (MBps)': 153.8,
        'Egress Max (MBps)': 288.5,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m7g.12xlarge': {
        'vCPU': 48,
        'Memory (GB)': 192,
        'Network Bandwidth (Gbps)': 22.5,
        'Ingress Recommended (MBps)': 115.4,
        'Ingress Max (MBps)': 173.1,
        'Egress Recommended (MBps)': 230.8,
        'Egress Max (MBps)': 432.7,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'kafka.m7g.16xlarge': {
        'vCPU': 64,
        'Memory (GB)': 256,
        'Network Bandwidth (Gbps)': 30.0,
        'Ingress Recommended (MBps)': 153.8,
        'Ingress Max (MBps)': 230.7,
        'Egress Recommended (MBps)': 307.7,
        'Egress Max (MBps)': 576.9,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'express.m7g.large': {
        'vCPU': 2,
        'Memory (GB)': 8,
        'Network Bandwidth (Gbps)': 12.5,
        'Ingress Recommended (MBps)': 15.6,
        'Ingress Max (MBps)': 23.4,
        'Egress Recommended (MBps)': 31.2,
        'Egress Max (MBps)': 58.5,
        'Partitions per Broker Recommended': 1000,
        'Partitions per Broker Max': 1500,
    },
    'express.m7g.xlarge': {
        'vCPU': 4,
        'Memory (GB)': 16,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 31.2,
        'Ingress Max (MBps)': 46.8,
        'Egress Recommended (MBps)': 62.5,
        'Egress Max (MBps)': 117.0,
        'Partitions per Broker Recommended': 1000,
        'Partitions per Broker Max': 1500,
    },
    'express.m7g.2xlarge': {
        'vCPU': 8,
        'Memory (GB)': 32,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 62.5,
        'Ingress Max (MBps)': 93.7,
        'Egress Recommended (MBps)': 125.0,
        'Egress Max (MBps)': 234.2,
        'Partitions per Broker Recommended': 2000,
        'Partitions per Broker Max': 3000,
    },
    'express.m7g.4xlarge': {
        'vCPU': 16,
        'Memory (GB)': 64,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 124.9,
        'Ingress Max (MBps)': 187.5,
        'Egress Recommended (MBps)': 249.8,
        'Egress Max (MBps)': 468.7,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'express.m7g.8xlarge': {
        'vCPU': 32,
        'Memory (GB)': 128,
        'Network Bandwidth (Gbps)': 15.0,
        'Ingress Recommended (MBps)': 250.0,
        'Ingress Max (MBps)': 375.0,
        'Egress Recommended (MBps)': 500.0,
        'Egress Max (MBps)': 937.5,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'express.m7g.12xlarge': {
        'vCPU': 48,
        'Memory (GB)': 192,
        'Network Bandwidth (Gbps)': 22.5,
        'Ingress Recommended (MBps)': 375.0,
        'Ingress Max (MBps)': 562.5,
        'Egress Recommended (MBps)': 750.0,
        'Egress Max (MBps)': 1406.2,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
    'express.m7g.16xlarge': {
        'vCPU': 64,
        'Memory (GB)': 256,
        'Network Bandwidth (Gbps)': 30.0,
        'Ingress Recommended (MBps)': 500.0,
        'Ingress Max (MBps)': 750.0,
        'Egress Recommended (MBps)': 1000.0,
        'Egress Max (MBps)': 1875.0,
        'Partitions per Broker Recommended': 4000,
        'Partitions per Broker Max': 6000,
    },
}


def get_cluster_best_practices(instance_type: str, number_of_brokers: int) -> dict:
    """Provides detailed best practices and quotas for AWS MSK clusters.

    Args:
        instance_type (str): The AWS MSK broker instance type (e.g., kafka.m5.large).
        number_of_brokers (int): The total number of brokers in the MSK cluster.

    Returns:
        dict: Detailed best practice guidelines and recommended quotas.
    """
    if instance_type not in INSTANCE_SPECS:
        return {'Error': f"Instance type '{instance_type}' is not supported or recognized."}

    specs = INSTANCE_SPECS[instance_type]
    recommended_cluster_partitions = specs['Partitions per Broker Recommended'] * number_of_brokers
    max_cluster_partitions = specs['Partitions per Broker Max'] * number_of_brokers

    replication_factor = (
        RECOMMENDED_REPLICATION_FACTOR
        if number_of_brokers >= RECOMMENDED_REPLICATION_FACTOR
        else number_of_brokers
    )
    min_insync_replicas = (
        RECOMMENDED_MIN_INSYNC_REPLICAS
        if number_of_brokers >= RECOMMENDED_REPLICATION_FACTOR
        else number_of_brokers
    )

    # Determine if this is an express cluster type
    is_express_cluster = instance_type.startswith('express.')

    # For express clusters, always use replication factor of 3
    if is_express_cluster:
        replication_factor = 3

    return {
        'Instance Type': f'{instance_type} (provided as input)',
        'Number of Brokers': f'{number_of_brokers} (provided as input)',
        'vCPU per Broker': specs['vCPU'],
        'Memory (GB) per Broker': f'{specs["Memory (GB)"]} (available on the host)',
        'Network Bandwidth (Gbps) per Broker': f'{specs["Network Bandwidth (Gbps)"]} (available on the host)',
        'Ingress Throughput Recommended (MBps)': f'{specs["Ingress Recommended (MBps)"]} (Note: CloudWatch metrics may be in bytes; ensure proper conversion between bytes and megabytes)',
        'Ingress Throughput Max (MBps)': f'{specs["Ingress Max (MBps)"]} (Note: CloudWatch metrics may be in bytes; ensure proper conversion between bytes and megabytes)',
        'Egress Throughput Recommended (MBps)': f'{specs["Egress Recommended (MBps)"]} (Note: CloudWatch metrics may be in bytes; ensure proper conversion between bytes and megabytes)',
        'Egress Throughput Max (MBps)': f'{specs["Egress Max (MBps)"]} (Note: CloudWatch metrics may be in bytes; ensure proper conversion between bytes and megabytes)',
        'Recommended Partitions per Broker': specs['Partitions per Broker Recommended'],
        'Max Partitions per Broker': f'{specs["Partitions per Broker Max"]} (Note: Each partition should be 3-way replicated. For example, 1000 total partitions with three brokers will mean each broker has 1000 partitions.)',
        'Recommended Max Partitions per Cluster': recommended_cluster_partitions,
        'Max Partitions per Cluster': max_cluster_partitions,
        'CPU Utilization Guidelines': f'Keep below {RECOMMENDED_CPU_UTILIZATION_PERCENT}% regularly; never exceed {MAX_CPU_UTILIZATION_PERCENT}%.',
        'Disk Utilization Guidelines': f'Warning at {STORAGE_UTILIZATION_WARNING_PERCENT}%, critical at {STORAGE_UTILIZATION_CRITICAL_PERCENT}%.',
        'Replication Factor': f'{replication_factor}'
        + (
            ' (Note: For express clusters, replication factor should always be 3)'
            if is_express_cluster
            else ' (recommended)'
        ),
        'Minimum In-Sync Replicas': min_insync_replicas,
        'Under-Replicated Partitions Tolerance': UNDER_REPLICATED_PARTITIONS_TOLERANCE,
        'Leader Imbalance Tolerance (%)': LEADER_IMBALANCE_TOLERANCE_PERCENT,
    }


async def register_module(mcp: FastMCP) -> None:
    """Register MSK best practices resources with the MCP server."""

    @mcp.resource(
        uri='resource://msk-best-practices', name='MSKBestPractices', mime_type='application/json'
    )
    async def msk_best_practices() -> str:
        """Access comprehensive best practices for AWS MSK clusters.

        This resource provides a complete set of best practices, thresholds, and
        instance specifications for AWS MSK clusters in a single JSON document.

        When to use:
        - When designing or sizing a new MSK cluster
        - When evaluating the health and configuration of an existing cluster
        - When troubleshooting performance issues or planning capacity changes
        - When establishing monitoring thresholds and alerts

        Content overview:
        - Recommended thresholds for CPU, disk, replication, and other metrics
        - Detailed specifications for all supported instance types
        - Guidelines for partition counts, replication factors, and other configurations

        Returns:
            JSON string containing all best practice guidelines and specifications
        """
        # Create a comprehensive best practices object
        best_practices = {
            'thresholds': {
                'cpu_utilization': {
                    'recommended_max': RECOMMENDED_CPU_UTILIZATION_PERCENT,
                    'critical_max': MAX_CPU_UTILIZATION_PERCENT,
                    'description': f'Keep below {RECOMMENDED_CPU_UTILIZATION_PERCENT}% regularly; never exceed {MAX_CPU_UTILIZATION_PERCENT}%.',
                },
                'disk_utilization': {
                    'warning': STORAGE_UTILIZATION_WARNING_PERCENT,
                    'critical': STORAGE_UTILIZATION_CRITICAL_PERCENT,
                    'description': f'Warning at {STORAGE_UTILIZATION_WARNING_PERCENT}%, critical at {STORAGE_UTILIZATION_CRITICAL_PERCENT}%.',
                },
                'replication': {
                    'recommended_factor': RECOMMENDED_REPLICATION_FACTOR,
                    'min_insync_replicas': RECOMMENDED_MIN_INSYNC_REPLICAS,
                    'description': 'For optimal resilience, use replication factor 3 with minimum ISR of 2.',
                },
                'under_replicated_partitions': {
                    'tolerance': UNDER_REPLICATED_PARTITIONS_TOLERANCE,
                    'description': 'Any deviation from zero indicates potential replication health issues.',
                },
                'leader_imbalance': {
                    'tolerance_percent': LEADER_IMBALANCE_TOLERANCE_PERCENT,
                    'description': f'Maintain leader distribution within {LEADER_IMBALANCE_TOLERANCE_PERCENT}% balance to avoid performance bottlenecks.',
                },
            },
            'instance_specs': INSTANCE_SPECS,
            'instance_categories': {
                'standard': [key for key in INSTANCE_SPECS.keys() if key.startswith('kafka.')],
                'express': [key for key in INSTANCE_SPECS.keys() if key.startswith('express.')],
            },
        }

        return json.dumps(best_practices)

    @mcp.resource(
        uri='resource://msk-best-practices/cluster/{instance_type}/{number_of_brokers}',
        name='MSKClusterBestPractices',
        mime_type='application/json',
    )
    async def msk_cluster_best_practices(instance_type: str, number_of_brokers: int) -> str:
        """Access best practices for MSK clusters based on instance type and broker count.

        This resource provides detailed best practices and quotas for AWS MSK clusters to guide
        in evaluating cluster health and identifying deviations from recommended configurations.

        When to use:
        - When designing or sizing a new MSK cluster
        - When evaluating the health and configuration of an existing cluster
        - When troubleshooting performance issues or planning capacity changes
        - When establishing monitoring thresholds and alerts

        How to use:
        - Specify the instance type (e.g., 'kafka.m5.large') and number of brokers
        - Parse the returned JSON to access detailed recommendations
        - Compare actual cluster metrics against the recommended thresholds

        Content overview:
        - Instance specifications (vCPU, memory, network bandwidth)
        - Throughput recommendations (ingress and egress)
        - Partition guidelines (per broker and per cluster)
        - Resource utilization thresholds (CPU and disk)
        - Reliability configuration (replication factor, in-sync replicas)

        Args:
            instance_type: The AWS MSK broker instance type (e.g., kafka.m5.large)
            number_of_brokers: The total number of brokers in the MSK cluster

        Returns:
            JSON string containing best practice guidelines and recommended quotas
        """
        result = get_cluster_best_practices(instance_type, int(number_of_brokers))
        return json.dumps(result)
