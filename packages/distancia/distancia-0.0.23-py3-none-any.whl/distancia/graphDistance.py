class ShortestPath:
    def __init__(self, graph):
        """
        Initialise la classe avec un graphe représenté sous forme de dictionnaire.
        :param graph: Un dictionnaire représentant le graphe, où les clés sont les nœuds et les valeurs sont des dictionnaires
                      de voisins avec les poids des arêtes.
        """
        self.graph = graph

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

    def get_shortest_path(self, start_node, end_node):
        """
        Obtient la distance du plus court chemin entre deux nœuds dans le graphe.
        :param start_node: Le nœud de départ.
        :param end_node: Le nœud d'arrivée.
        :return: La distance du plus court chemin.
        """
        return self.dijkstra(start_node, end_node)


class GraphEditDistance:
    def __init__(self, graph1, graph2):
        """
        Initializes the GraphEditDistance class with two graphs.
        
        :param graph1: The first graph as a dictionary where keys are nodes and values are sets of connected nodes.
        :param graph2: The second graph as a dictionary where keys are nodes and values are sets of connected nodes.
        """
        self.graph1 = graph1
        self.graph2 = graph2

    def compute(self):
        """
        Computes the Graph Edit Distance (GED) between the two graphs.

        :return: The Graph Edit Distance between the two graphs.
        """
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

class SpectralDistance:
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

    def calculate(self, G1, G2):
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

class WeisfeilerLehmanSimilarity:
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

    def calculate(self, G1, G2):
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
