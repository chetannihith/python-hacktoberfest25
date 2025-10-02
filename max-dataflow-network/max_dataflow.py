#!/usr/bin/env python3
"""
Maximum Data Flow Network Optimization
HackerRank Problem Solution

Problem: As an engineer in Amazon's Data Infrastructure Team, optimize how 
information flows through a network of processing nodes by finding the maximum 
total dataFlow that can be achieved by optimally selecting unique pairs of 
connections for each data channel.

Author: [Your Name]
Date: October 2025
"""


def determineMaxDataFlow(bandwidth, streamCount):
    """
    Determine the maximum total dataFlow from the unique connections of node pairs.
    
    The dataFlow for each data channel is defined as the sum of the bandwidth 
    of its main and secondary nodes.
    
    Strategy:
    - To maximize total dataFlow, we want to select pairs with the highest 
      sum of bandwidths
    - Each node can be used in multiple pairs (as different connections)
    - We need to select streamCount unique pairs
    - Pairs (x, y) and (y, x) are considered different connections
    - A node can be paired with itself
    
    Args:
        bandwidth (list): Array of bandwidth capability provided by each processing node
        streamCount (int): Number of data channels that needs to be connected
        
    Returns:
        int: The maximum total dataFlow from the unique connections of node pairs
        
    Constraints:
        - 1 ≤ n ≤ 2 * 10^5
        - 1 ≤ bandwidth[i] ≤ 2 * 10^5
        - 1 ≤ streamCount ≤ min(n^2, n^2)
    """
    n = len(bandwidth)
    
    # Generate all possible dataFlow values (sum of pairs)
    # We can have:
    # - Same node pairs: (i, i) -> bandwidth[i] + bandwidth[i]
    # - Different node pairs: (i, j) where i != j -> bandwidth[i] + bandwidth[j]
    
    dataflows = []
    
    # For each node, it can pair with itself
    for i in range(n):
        dataflows.append(bandwidth[i] + bandwidth[i])
    
    # For each pair of different nodes (both directions count as different pairs)
    for i in range(n):
        for j in range(n):
            if i != j:
                dataflows.append(bandwidth[i] + bandwidth[j])
    
    # Sort in descending order to get the highest dataflows first
    dataflows.sort(reverse=True)
    
    # Select the top streamCount pairs and sum their dataflows
    max_dataflow = sum(dataflows[:streamCount])
    
    return max_dataflow


def main():
    """
    Main function to read input and call the solution function.
    Follows HackerRank input/output format.
    """
    # Read number of nodes
    n = int(input().strip())
    
    # Read bandwidth array
    bandwidth = []
    for _ in range(n):
        bandwidth.append(int(input().strip()))
    
    # Read stream count
    streamCount = int(input().strip())
    
    # Calculate and print result
    result = determineMaxDataFlow(bandwidth, streamCount)
    print(result)


if __name__ == '__main__':
    main()
