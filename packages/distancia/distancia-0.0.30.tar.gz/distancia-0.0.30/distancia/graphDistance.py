from .mainClass import *
from .tools     import *

class ShortestPath(Distance):
    def __init__(self):
        """
        Initialise la classe avec un graphe représenté sous forme de dictionnaire.
        :param graph: Un dictionnaire représentant le graphe, où les clés sont les nœuds et les valeurs sont des dictionnaires
                      de voisins avec les poids des arêtes.
        """
        super().__init__()


    def dijkstra(self, start_node, end_node):
        """
        Implémente l'algorithme de Dijkstra pour trouver le plus court chemin entre deux nœuds.
        :param start_node: Le nœud de départ.
        :param end_node: Le nœud d'arrivée.
        :return: La distance du plus court chemin entre start_node et end_node.
        """
        import heapq

        # Initialisation des distances de tous les nœuds à l'infini, sauf le nœud de départ à 0
        distances = {node: float('inf') for node in self.graph}
        distances[start_node] = 0

        # File de priorité pour gérer les nœuds à explorer
        priority_queue = [(0, start_node)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Si nous avons atteint le nœud de destination, on peut arrêter
            if current_node == end_node:
                return current_distance

            # Si la distance actuelle est supérieure à la distance déjà trouvée, on saute
            if current_distance > distances[current_node]:
                continue

            # Explorer les voisins du nœud actuel
            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                # Si une distance plus courte est trouvée, mettre à jour et ajouter à la queue
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        # Si le nœud d'arrivée est injoignable, retourner l'infini
        return float('inf')

    def distance_function(self,graph, start_node, end_node):
        """
        Obtient la distance du plus court chemin entre deux nœuds dans le graphe.
        :param start_node: Le nœud de départ.
        :param end_node: Le nœud d'arrivée.
        :return: La distance du plus court chemin.
        """
        self.graph = graph

        return self.dijkstra(start_node, end_node)


class GraphEditDistance(Distance):
    def __init__(self):
        """
        Initializes the GraphEditDistance class with two graphs.
        
        :param graph1: The first graph as a dictionary where keys are nodes and values are sets of connected nodes.
        :param graph2: The second graph as a dictionary where keys are nodes and values are sets of connected nodes.
        """
        super().__init__()

        

    def distance_function(self, graph1, graph2):
        """
        Computes the Graph Edit Distance (GED) between the two graphs.

        :return: The Graph Edit Distance between the two graphs.
        """
        self.graph1 = graph1
        self.graph2 = graph2
        
        # Compute node differences
        node_diff = self._node_diff(self.graph1, self.graph2)

        # Compute edge differences
        edge_diff = self._edge_diff(self.graph1, self.graph2)

        # Total cost is the sum of node and edge differences
        return node_diff + edge_diff

    def _node_diff(self, g1, g2):
        """
        Computes the difference in nodes between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The node difference.
        """
        g1_nodes = set(g1.keys())
        g2_nodes = set(g2.keys())

        # Nodes to delete from g1 or add to g2
        node_deletions = g1_nodes - g2_nodes
        node_additions = g2_nodes - g1_nodes

        # Node difference is the sum of deletions and additions
        return len(node_deletions) + len(node_additions)

    def _edge_diff(self, g1, g2):
        """
        Computes the difference in edges between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The edge difference.
        """
        g1_edges = self._get_edges(g1)
        g2_edges = self._get_edges(g2)

        # Edges to delete from g1 or add to g2
        edge_deletions = g1_edges - g2_edges
        edge_additions = g2_edges - g1_edges

        # Edge difference is the sum of deletions and additions
        return len(edge_deletions) + len(edge_additions)

    def _get_edges(self, graph):
        """
        Returns a set of edges from a graph, ensuring each edge is only counted once in an undirected graph.
        
        :param graph: The graph as a dictionary.
        :return: A set of edges.
        """
        edges = set()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                if (node, neighbor) not in edges and (neighbor, node) not in edges:
                    edges.add((node, neighbor))
        return edges

#claude
import math
import networkx as nx

class SpectralDistance(Distance):
    """
    A class to compute the spectral distance between two graphs.

    The spectral distance is based on the difference between the eigenvalues
    of the Laplacian matrices of the graphs.

    Attributes:
        k (int): Number of eigenvalues to consider (default is None, which uses all eigenvalues)
        normalized (bool): Whether to use normalized Laplacian (default is False)
    """

    def __init__(self, k=None, normalized=False):
        """
        Initialize the SpectralDistance object.

        Args:
            k (int, optional): Number of eigenvalues to consider. If None, all eigenvalues are used.
            normalized (bool, optional): Whether to use the normalized Laplacian. Defaults to False.
        """
        super().__init__()

        self.k = k
        self.normalized = normalized

    def laplacian_matrix(self, G):
        """
        Compute the Laplacian matrix of the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list of list: Laplacian matrix
        """
        n = G.number_of_nodes()
        L = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    L[i][j] = G.degree(i)
                elif G.has_edge(i, j):
                    L[i][j] = -1
        
        if self.normalized:
            for i in range(n):
                for j in range(n):
                    if G.degree(i) > 0 and G.degree(j) > 0:
                        L[i][j] /= math.sqrt(G.degree(i) * G.degree(j))
        
        return L

    def eigenvalues(self, matrix):
        """
        Compute eigenvalues using the power iteration method.

        Args:
            matrix (list of list): Input matrix

        Returns:
            list: Approximate eigenvalues
        """
        n = len(matrix)
        eigenvalues = []
        for _ in range(n):
            # Initialize random vector
            v = [1/math.sqrt(n) for _ in range(n)]
            for _ in range(100):  # Number of iterations
                # Matrix-vector multiplication
                u = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
                # Normalize
                norm = math.sqrt(sum(x*x for x in u))
                if norm==0:norm=1
                v = [x/norm for x in u]
            # Compute Rayleigh quotient
            lambda_ = sum(v[i] * sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n))
            eigenvalues.append(lambda_)
            # Deflate the matrix
            for i in range(n):
                for j in range(n):
                    matrix[i][j] -= lambda_ * v[i] * v[j]
        return sorted(eigenvalues)

    def distance_function(self, G1, G2):
        """
        Calculate the spectral distance between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Spectral distance between G1 and G2

        Raises:
            ValueError: If the graphs have different numbers of nodes and k is None
        """
        L1 = self.laplacian_matrix(G1)
        L2 = self.laplacian_matrix(G2)
        
        eig1 = self.eigenvalues(L1)
        eig2 = self.eigenvalues(L2)

        if self.k is None:
            if len(eig1) != len(eig2):
                raise ValueError("Graphs must have the same number of nodes when k is None")
            k = len(eig1)
        else:
            k = min(self.k, len(eig1), len(eig2))

        # Pad or truncate eigenvalues to length k
        eig1 = eig1[:k] + [0] * max(0, k - len(eig1))
        eig2 = eig2[:k] + [0] * max(0, k - len(eig2))

        # Compute Euclidean distance between eigenvalues
        distance = math.sqrt(sum((e1 - e2)**2 for e1, e2 in zip(eig1, eig2)))

        return distance

#claude
import networkx as nx
from collections import Counter

class WeisfeilerLehmanSimilarity(Distance):
    """
    A class to compute the Weisfeiler-Lehman similarity between two graphs.

    The Weisfeiler-Lehman algorithm is used to create a multi-set of labels
    for each graph, which are then compared to compute a similarity score.

    Attributes:
        num_iterations (int): Number of iterations for the WL algorithm
        node_label_attr (str): Attribute name for initial node labels
    """

    def __init__(self, num_iterations=3, node_label_attr=None):
        """
        Initialize the WeisfeilerLehmanSimilarity object.

        Args:
            num_iterations (int): Number of iterations for the WL algorithm. Default is 3.
            node_label_attr (str, optional): Attribute name for initial node labels.
                If None, all nodes are initially labeled with the same value.
        """
        super().__init__()

        self.num_iterations = num_iterations
        self.node_label_attr = node_label_attr

    def wl_labeling(self, G):
        """
        Perform Weisfeiler-Lehman labeling on the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list: List of label multi-sets for each iteration
        """
        if self.node_label_attr:
            labels = nx.get_node_attributes(G, self.node_label_attr)
        else:
            labels = {node: '1' for node in G.nodes()}

        label_lists = [Counter(labels.values())]

        for _ in range(self.num_iterations):
            new_labels = {}
            for node in G.nodes():
                # Collect labels of neighbors
                neighbor_labels = sorted(labels[nbr] for nbr in G.neighbors(node))
                # Create a new label by combining current label and sorted neighbor labels
                new_labels[node] = f"{labels[node]}({''.join(neighbor_labels)})"
            
            # Update labels and add to label_lists
            labels = new_labels
            label_lists.append(Counter(labels.values()))

        return label_lists

    def distance_function(self, G1, G2):
        """
        Calculate the Weisfeiler-Lehman similarity between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Weisfeiler-Lehman similarity between G1 and G2
        """
        # Get label multi-sets for both graphs
        label_lists1 = self.wl_labeling(G1)
        label_lists2 = self.wl_labeling(G2)

        # Compute similarity for each iteration
        similarities = []
        for labels1, labels2 in zip(label_lists1, label_lists2):
            intersection = sum((labels1 & labels2).values())
            union = sum((labels1 | labels2).values())
            similarities.append(intersection / union if union > 0 else 0)

        # Return the average similarity across all iterations
        return sum(similarities) / len(similarities)

    def is_isomorphic(self, G1, G2, threshold=0.99):
        """
        Check if two graphs are potentially isomorphic using WL similarity.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph
            threshold (float): Similarity threshold for isomorphism. Default is 0.99.

        Returns:
            bool: True if the graphs are potentially isomorphic, False otherwise
        """
        if G1.number_of_nodes() != G2.number_of_nodes() or G1.number_of_edges() != G2.number_of_edges():
            return False
        
        similarity = self.calculate(G1, G2)
        return similarity > threshold

import numpy as np
import networkx as nx

class ComparingRandomWalkStationaryDistributions(Distance):
    """
    A class to compare stationary distributions of random walks on graphs.
    """

    def __init__(self, graph1, graph2):
        """
        Initialize the Distance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()

        self.graph1 = graph1
        self.graph2 = graph2

    def compute_stationary_distribution(self, graph):
        """
        Compute the stationary distribution of a random walk on the given graph.

        Parameters:
        graph (networkx.Graph): The graph to compute the stationary distribution for

        Returns:
        numpy.ndarray: The stationary distribution vector
        """
        # Get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(graph).toarray()

        # Compute the transition matrix
        degree = np.sum(adj_matrix, axis=1)
        transition_matrix = adj_matrix / degree[:, np.newaxis]

        # Compute the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)

        # Find the eigenvector corresponding to eigenvalue 1
        stationary_index = np.argmin(np.abs(eigenvalues - 1))
        stationary_distribution = np.real(eigenvectors[:, stationary_index])

        # Normalize the distribution
        return stationary_distribution / np.sum(stationary_distribution)

    def compare_distributions(self, metric='l1'):
        """
        Compare the stationary distributions of the two graphs.

        Parameters:
        metric (str): The distance metric to use. Options: 'l1', 'l2', 'kl'. Default is 'l1'.

        Returns:
        float: The distance between the two stationary distributions
        """
        dist1 = self.compute_stationary_distribution(self.graph1)
        dist2 = self.compute_stationary_distribution(self.graph2)

        if len(dist1) != len(dist2):
            raise ValueError("The graphs must have the same number of nodes")

        if metric == 'l1':
            return np.sum(np.abs(dist1 - dist2))
        elif metric == 'l2':
            return np.sqrt(np.sum((dist1 - dist2)**2))
        elif metric == 'kl':
            return np.sum(dist1 * np.log(dist1 / dist2))
        else:
            raise ValueError("Invalid metric. Choose 'l1', 'l2', or 'kl'.")

    def random_walk(self, graph, steps, start_node=None):
        """
        Perform a random walk on the given graph.

        Parameters:
        graph (networkx.Graph): The graph to walk on
        steps (int): The number of steps to take
        start_node (int): The starting node for the walk. If None, a random node is chosen.

        Returns:
        list: The sequence of nodes visited during the walk
        """
        if start_node is None:
            start_node = np.random.choice(list(graph.nodes()))

        walk = [start_node]
        current_node = start_node

        for _ in range(steps - 1):
            neighbors = list(graph.neighbors(current_node))
            if not neighbors:
                break
            current_node = np.random.choice(neighbors)
            walk.append(current_node)

        return walk

    def compare_random_walks(self, num_walks, walk_length):
        """
        Compare random walks on both graphs.

        Parameters:
        num_walks (int): The number of random walks to perform on each graph
        walk_length (int): The length of each random walk

        Returns:
        dict: A dictionary containing the average walk length and node visit frequencies for both graphs
        """
        results = {}

        for i, graph in enumerate([self.graph1, self.graph2]):
            total_length = 0
            node_visits = {node: 0 for node in graph.nodes()}

            for _ in range(num_walks):
                walk = self.random_walk(graph, walk_length)
                total_length += len(walk)
                for node in walk:
                    node_visits[node] += 1

            avg_length = total_length / num_walks
            visit_freq = {node: visits / (num_walks * walk_length) for node, visits in node_visits.items()}

            results[f'graph{i+1}'] = {
                'avg_walk_length': avg_length,
                'node_visit_frequencies': visit_freq
            }

        return results

