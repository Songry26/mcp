"""
Function to retrieve compatible Kafka versions for an MSK cluster.
Maps to AWS CLI command: aws kafka get-compatible-kafka-versions
"""


def get_compatible_kafka_versions(cluster_arn=None, client=None):
    """
    Gets the Apache Kafka versions to which you can update a cluster.

    Args:
        cluster_arn (str): The ARN of the cluster to check (optional)
        client (boto3.client): Boto3 client for Kafka. Must be provided by get_cluster_info.

    Returns:
        dict: List of compatible Kafka versions
    """
    if client is None:
        raise ValueError(
            "Client must be provided. This function should only be called from get_cluster_info."
        )

    # Example implementation
    params = {}
    if cluster_arn:
        params["ClusterArn"] = cluster_arn

    response = client.get_compatible_kafka_versions(**params)

    return response
