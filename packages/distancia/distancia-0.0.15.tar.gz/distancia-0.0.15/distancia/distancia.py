#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  distancia.py
#  
#  Copyright 2024 yves <yves.mercadier@...>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from tools import *


from abc import ABC   # permet de définir des classes de base

class Distance(ABC):
	obj1_exemple=[1, 2, 3]
	obj2_exemple=[4, 5, 6]
	type1=list
	type2=list
	
	def __call__(self,*args):
		if len(args)==2:
			return self.distance_function(args[0], args[1])
		if len(args)==3:
			return self.distance_function(args[0], args[1], args[2])
		if len(args)==4:
			return self.distance_function(args[0], args[1], args[2], args[3])
		
	def calculate(self,*args):
	#def distance(self, obj1, obj2):
		"""
		Calculate the distance between two objects.
		:param obj1: First object
		:param obj2: Second object
		....
		:return: Distance between obj1, obj2, ...
		"""
		if len(args)==2:
			return self.distance_function(args[0], args[1])
		if len(args)==3:
			return self.distance_function(args[0], args[1], args[2])
		if len(args)==4:
			return self.distance_function(args[0], args[1], args[2], args[3])

	def check_data(self, obj1, obj2):
		"""
		Verify the data of a distance measure: type, dimension.
		"""
		
		print(type(obj1))
		print(self.type1)
		properties = {
				f'collection1_type {self.type1}': type(obj1) is self.type1,
				f'collection2_type {self.type2}': type(obj2) is self.type2,
				f'data_type': True and True,
				f'association_rules': True and True,
		}
		print(f"Data verification: {properties}")
		
	def check_properties(self, obj1, obj2, obj3):
		"""
		Verify the properties of a distance measure: non-negativity, identity of indiscernibles, symmetry, and triangle inequality.
		:param obj1: First object
		:param obj2: Second object
		:param obj3: Third object
		:return: Dictionary indicating whether each property holds
		"""
		d12 = self.calculate(obj1, obj2)
		d13 = self.calculate(obj1, obj3)
		d23 = self.calculate(obj2, obj3)

		properties = {
				'non_negativity': d12 >= 0 and d13 >= 0 and d23 >= 0,
				'identity_of_indiscernibles': (d12 == 0) == (obj1 == obj2) and (d13 == 0) == (obj1 == obj3) and (d23 == 0) == (obj2 == obj3),
				'symmetry': d12 == self.calculate(obj2, obj1) and d13 == self.calculate(obj3, obj1) and d23 == self.calculate(obj3, obj2),
				'triangle_inequality': d12 <= d13 + d23 and d13 <= d12 + d23 and d23 <= d12 + d13,
		}
		print(f"Properties verification: {properties}")

	def exemple(self):
		# Example usage
		if not hasattr(self, 'obj3_exemple')and not hasattr(self, 'obj4_exemple'):
			print(f"{self.__class__.__name__} distance between {self.obj1_exemple} and {self.obj2_exemple} is {self.calculate(self.obj1_exemple, self.obj2_exemple):.2f}")
		elif not hasattr(self, 'obj4_exemple'):
			print(f"{self.__class__.__name__} distance {self.obj3_exemple} between {self.obj1_exemple} and {self.obj2_exemple} is {self.calculate(self.obj1_exemple, self.obj2_exemple, self.obj3_exemple):.2f}")
		else:
			print(f"{self.__class__.__name__} distance {self.obj3_exemple}, {self.obj4_exemple} between {self.obj1_exemple} and {self.obj2_exemple} is {self.calculate(self.obj1_exemple, self.obj2_exemple, self.obj3_exemple, self.obj4_exemple):.2f}")

###################################################
class Levenshtein(Distance):
	def __init__(self):
		super().__init__()
		self.type1=str
		self.type2=str
	def distance_function(self,s1, s2):
		dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

		for i in range(len(s1) + 1):
			dp[i][0] = i
		for j in range(len(s2) + 1):
			dp[0][j] = j

		for i in range(1, len(s1) + 1):
			for j in range(1, len(s2) + 1):
				if s1[i - 1] == s2[j - 1]:
					cost = 0
				else:
					cost = 1
				dp[i][j] = min(dp[i - 1][j] + 1,        # Suppression
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution

		return dp[len(s1)][len(s2)]
		
	def exemple(self):
		self.obj1_exemple = "kitten"
		self.obj2_exemple = "sitting"
		super().exemple()


class CosineSimilarity(Distance):
	def __init__(self):
		super().__init__()

	def dot_product(self,vec1, vec2):
		"""
		Calculate the dot product between two vectors.
    
		:param vec1: First vector
		:param vec2: Second vector
		:return: Dot product of vec1 and vec2
		"""
		return sum(x * y for x, y in zip(vec1, vec2))

	def norm(self,vec):
		"""
		Calculate the norm (magnitude) of a vector.
    
		:param vec: Input vector
		:return: Norm of the vector
		"""
		return (sum(x * x for x in vec))**0.5

	def distance_function(self,vec1, vec2):
		"""
		Calculate the cosine similarity between two vectors.
    
		:param vec1: First vector
		:param vec2: Second vector
		:return: Cosine similarity between vec1 and vec2
		"""
		dot_prod = self.dot_product(vec1, vec2)
		norm_vec1 = self.norm(vec1)
		norm_vec2 = self.norm(vec2)
		if norm_vec1 == 0 or norm_vec2 == 0:
			# Handling edge case if any vector has zero length to avoid division by zero
			return 0.0
		return dot_prod / (norm_vec1 * norm_vec2)
		

class CosineInverse(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,vec1, vec2):
		return 1-Cosine_Similarity().calculate(vec1,vec2)


class Euclidean(Distance):
	def __init__(self):
		super().__init__()
		
		
	def distance_function(self,point1, point2):
		"""
		Calculate the Euclidean distance between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:return: Euclidean distance between point1 and point2
		"""
		if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")

		distance = 0.0
		for p1, p2 in zip(point1, point2):
			distance += (p1 - p2) ** 2
		return distance**0.5
		
class L2(Euclidean):
	def __init__(self):
		super().__init__()

class Hamming(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,str1, str2):
		"""
		Calculate the Hamming distance between two strings.
    
		:param str1: First string
		:param str2: Second string
		:return: Hamming distance between str1 and str2
		:raises ValueError: If the strings are not of the same length
		"""
		if len(str1) != len(str2):
			raise ValueError("Strings must be of the same length")
    
		return sum(el1 != el2 for el1, el2 in zip(str1, str2))
	def exemple(self):
		self.obj1_exemple = "1011101"
		self.obj2_exemple = "1001001"
		super().exemple()

class Jaccard(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,set1, set2):
		"""
		Calculate the Jaccard distance between two sets.
    
		:param set1: First set
		:param set2: Second set
		:return: Jaccard distance between set1 and set2
		"""
		intersection = len(set1.intersection(set2))
		union = len(set1.union(set2))
		if union == 0:
			return 0.0  # Both sets are empty
		return 1 - (intersection / union)
	def exemple(self):
		self.obj1_exemple = {1, 2, 3, 4}
		self.obj2_exemple = {3, 4, 5, 6}
		super().exemple()

class GeneralizedJaccard(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,x, y):
		"""
		Calcule la distance de Jaccard généralisée entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:return: Distance de Jaccard généralisée entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		min_sum = sum(min(x_i, y_i) for x_i, y_i in zip(x, y))
		max_sum = sum(max(x_i, y_i) for x_i, y_i in zip(x, y))
    
		if max_sum == 0:
			return 0.0  # Pour éviter la division par zéro
        
		return 1 - (min_sum / max_sum)
	def exemple(self):
		self.obj1_exemple = {1, 2, 3, 4}
		self.obj2_exemple = {3, 4, 5, 6}
		super().exemple()

class Tanimoto(Jaccard):
	def __init__(self):
		super().__init__()

class InverseTanimoto:
    def __init__(self):
        pass

    def distance_function(self, set_a, set_b):
        """
        Calculate the Inverse Tanimoto coefficient between two sets.

        Parameters:
        - set_a: First set of elements.
        - set_b: Second set of elements.

        Returns:
        - Inverse Tanimoto coefficient: A float value representing the dissimilarity between the two sets.
        """
        if not isinstance(set_a, set) or not isinstance(set_b, set):
            raise ValueError("Inputs must be of type 'set'.")

        # Calculate the intersection and union of the two sets
        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)

        # Handle the edge case where the union is empty
        if not union:
            return 0.0

        # Calculate the Inverse Tanimoto coefficient
        inverse_tanimoto = (len(union) - len(intersection)) / len(union)

        return inverse_tanimoto


class Manhattan(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,point1, point2):
		"""
		Calculate the Manhattan distance, taxicab or L1 between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:return: Manhattan distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""
		if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")
    
		distance = sum(abs(p1 - p2) for p1, p2 in zip(point1, point2))
		return distance
		
class L1(Manhattan):
	def __init__(self):
		super().__init__()

class Minkowski(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,point1, point2, p):
		"""
		Calculate the Minkowski distance between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:param p: The order of the Minkowski distance
		:return: Minkowski distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""
		if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")
    
		distance = sum(abs(p1 - p2) ** p for p1, p2 in zip(point1, point2)) ** (1 / p)
		return distance
	def exemple(self,p):
		self.obj3_exemple = p
		super().exemple()


class Mahalanobis(Distance):
	def __init__(self):
		super().__init__()
	def mean(self,data):
		"""
		Calculate the mean of each dimension in the dataset.
    
		:param data: A dataset as a list of points (list of lists)
		:return: Mean of each dimension as a list
		"""
		n = len(data)
		d = len(data[0])
		mean = [0] * d
    
		for point in data:
			for i in range(d):
				mean[i] += point[i]
    
		mean = [x / n for x in mean]
		return mean

	def covariance_matrix(self,data, mean):
		"""
		Calculate the covariance matrix of the dataset.
    
		:param data: A dataset as a list of points (list of lists)
		:param mean: Mean of each dimension as a list
		:return: Covariance matrix as a list of lists
		"""
		n = len(data)
		d = len(data[0])
		cov_matrix = [[0] * d for _ in range(d)]
    
		for point in data:
			diff = [point[i] - mean[i] for i in range(d)]
			for i in range(d):
				for j in range(d):
					cov_matrix[i][j] += diff[i] * diff[j]
    
		cov_matrix = [[x / (n - 1) for x in row] for row in cov_matrix]
		return cov_matrix

	def matrix_inverse(self,matrix):
		"""
		Calculate the inverse of a matrix using Gauss-Jordan elimination.
    
		:param matrix: A square matrix as a list of lists
		:return: Inverse of the matrix as a list of lists
		"""
		n = len(matrix)
		identity = [[float(i == j) for i in range(n)] for j in range(n)]
		augmented = [row + identity_row for row, identity_row in zip(matrix, identity)]
		for i in range(n):
			pivot = augmented[i][i]
			for j in range(2 * n):
				augmented[i][j] /= pivot
			for k in range(n):
				if k != i:
					factor = augmented[k][i]
					for j in range(2 * n):
						augmented[k][j] -= factor * augmented[i][j]
    
		inverse = [row[n:] for row in augmented]
		return inverse

	def distance_function(self,point, data):
		"""
		Calculate the Mahalanobis distance between a point and a dataset.
    
		:param point: A point as a list of coordinates
		:param data: A dataset as a list of points (list of lists)
		:return: Mahalanobis distance between the point and the dataset
		:raises ValueError: If the point dimensions do not match the dataset dimensions
		! lever une execption si la matrice est singulière
		"""
		if len(data[0]) != len(point):
			raise ValueError("Point dimensions must match dataset dimensions")
    
		mean_data = self.mean(data)
		cov_matrix = self.covariance_matrix(data, mean_data)
		cov_matrix_inv = self.matrix_inverse(cov_matrix)
    
		diff = [point[i] - mean_data[i] for i in range(len(point))]
    
		# Matrix multiplication: diff^T * cov_matrix_inv * diff
		result = 0
		for i in range(len(diff)):
			for j in range(len(diff)):
				result += diff[i] * cov_matrix_inv[i][j] * diff[j]
    
		return result**0.5
	def exemple(self):
		self.obj2_exemple = [
    [2, 1, 0],
    [2, 3, 4],
    [3, 4, 5],
    [4, 5, 6],
]
		super().exemple()

class Chebyshev(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,point1, point2):

		"""
		Calculate the Chebyshev distance between two points.
    
		:param point1: A list of coordinates for the first point
		:param point2: A list of coordinates for the second point
		:return: Chebyshev distance between the two points
		:raises ValueError: If the points do not have the same dimensions
		"""
		if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")
    
		return max(abs(a - b) for a, b in zip(point1, point2))


class RatcliffObershelp(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,str1, str2):
		"""
		ou Similarité Gestalt.
		Calculate the Ratcliff/Obershelp distance between two strings.
    
		:param str1: The first string
		:param str2: The second string
		:return: Ratcliff/Obershelp distance between the two strings
		"""
		def find_longest_common_substring(s1, s2):
			"""
			Helper function to find the longest common substring between two strings.
        
			:param s1: The first string
			:param s2: The second string
			:return: The longest common substring
			"""
			matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
			longest_length = 0
			lcs_end = 0

			for i in range(1, len(s1) + 1):
				for j in range(1, len(s2) + 1):
					if s1[i - 1] == s2[j - 1]:
						matrix[i][j] = matrix[i - 1][j - 1] + 1
						if matrix[i][j] > longest_length:
							longest_length = matrix[i][j]
							lcs_end = i

			return s1[lcs_end - longest_length: lcs_end]

		def recursive_match(s1, s2):
			"""
			Helper function to recursively match substrings.
        
			:param s1: The first string
			:param s2: The second string
			:return: The total length of matched substrings
			"""
			lcs = find_longest_common_substring(s1, s2)
			if not lcs:
				return 0

			lcs_length = len(lcs)
			lcs_start1 = s1.find(lcs)
			lcs_start2 = s2.find(lcs)

			return (
				lcs_length +
				recursive_match(s1[:lcs_start1], s2[:lcs_start2]) +
				recursive_match(s1[lcs_start1 + lcs_length:], s2[lcs_start2 + lcs_length:])
			)

		total_length = len(str1) + len(str2)
		if total_length == 0:
			return 0.0

		matched_length = recursive_match(str1, str2)
		similarity = (2 * matched_length) / total_length

		return 1 - similarity
	def exemple(self):
		self.obj1_exemple = "kitten"
		self.obj2_exemple = "sitting"
		super().exemple()

'''
class RatcliffObershelp:
    def __init__(self):
        """
        Initialize the Ratcliff/Obershelp class with two strings.

        :param string1: First string for comparison.
        :param string2: Second string for comparison.
        """
        self.string1 = string1
        self.string2 = string2

    def distance_function(self, string1, string2):
        """
        Calculate the Ratcliff/Obershelp distance between the two strings.

        :return: The Ratcliff/Obershelp distance as a float.
        """
        def ratcliff_obershelp(s1, s2):
            if not s1 or not s2:
                return 0.0 if s1 != s2 else 1.0

            def lcs(s1, s2):
                m, n = len(s1), len(s2)
                dp = [[0] * (n + 1) for _ in range(m + 1)]

                for i in range(1, m + 1):
                    for j in range(1, n + 1):
                        if s1[i - 1] == s2[j - 1]:
                            dp[i][j] = dp[i - 1][j - 1] + 1
                        else:
                            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

                return dp[m][n]

            lcs_length = lcs(s1, s2)
            if lcs_length == 0:
                return 0.0

            prefix_length = 0
            while prefix_length < len(s1) and prefix_length < len(s2) and s1[prefix_length] == s2[prefix_length]:
                prefix_length += 1

            similarity = 2 * lcs_length / (len(s1) + len(s2))
            similarity += (2 * prefix_length) / (len(s1) + len(s2))
            return similarity

        similarity = ratcliff_obershelp(self.string1, self.string2)
        return 1 - similarity
'''
class Jaro(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,s1, s2):
		"""
		Calculate the Jaro similarity between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:return: Jaro similarity between the two strings
		"""
		if s1 == s2:
			return 1.0

		len_s1 = len(s1)
		len_s2 = len(s2)

		if len_s1 == 0 or len_s2 == 0:
			return 0.0

		match_distance = max(len_s1, len_s2) // 2 - 1

		s1_matches = [False] * len_s1
		s2_matches = [False] * len_s2

		matches = 0
		transpositions = 0

		for i in range(len_s1):
			start = max(0, i - match_distance)
			end = min(i + match_distance + 1, len_s2)

			for j in range(start, end):
				if s2_matches[j]:
					continue
				if s1[i] != s2[j]:
					continue
				s1_matches[i] = True
				s2_matches[j] = True
				matches += 1
				break

		if matches == 0:
			return 0.0

		k = 0
		for i in range(len_s1):
			if not s1_matches[i]:
				continue
			while not s2_matches[k]:
				k += 1
			if s1[i] != s2[k]:
				transpositions += 1
			k += 1

		return (matches / len_s1 + matches / len_s2 + (matches - transpositions // 2) / matches) / 3.0
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()

class JaroWinkler(Distance):
	def __init__(self):
		super().__init__()
	def Jaro(self,s1, s2):
		"""
		Calculate the Jaro similarity between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:return: Jaro similarity between the two strings
		"""
		if s1 == s2:
			return 1.0

		len_s1 = len(s1)
		len_s2 = len(s2)

		if len_s1 == 0 or len_s2 == 0:
			return 0.0

		match_distance = max(len_s1, len_s2) // 2 - 1

		s1_matches = [False] * len_s1
		s2_matches = [False] * len_s2

		matches = 0
		transpositions = 0

		for i in range(len_s1):
			start = max(0, i - match_distance)
			end = min(i + match_distance + 1, len_s2)

			for j in range(start, end):
				if s2_matches[j]:
					continue
				if s1[i] != s2[j]:
					continue
				s1_matches[i] = True
				s2_matches[j] = True
				matches += 1
				break

		if matches == 0:
			return 0.0

		k = 0
		for i in range(len_s1):
			if not s1_matches[i]:
				continue
			while not s2_matches[k]:
				k += 1
			if s1[i] != s2[k]:
				transpositions += 1
			k += 1

		return (matches / len_s1 + matches / len_s2 + (matches - transpositions // 2) / matches) / 3.0

	def distance_function(self,s1, s2, p=0.1):
		"""
		Calculate the Jaro-Winkler distance between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:param p: The scaling factor, usually 0.1
		:return: Jaro-Winkler distance between the two strings
		"""
		jaro_sim = self.Jaro(s1, s2)

		prefix_length = 0
		max_prefix_length = 4

		for i in range(min(len(s1), len(s2))):
			if s1[i] == s2[i]:
				prefix_length += 1
			else:
				break
			if prefix_length == max_prefix_length:
				break

		jaro_winkler_sim = jaro_sim + (prefix_length * p * (1 - jaro_sim))
		return jaro_winkler_sim
		
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()

class Hausdorff(Distance):
	def __init__(self):
		super().__init__()
		
	def euclidean_distance(self,point1, point2):
		"""utiliser la classe Euclidean!
		Calculate the Euclidean distance between two points.
    
		:param point1: The first point as a tuple (x, y)
		:param point2: The second point as a tuple (x, y)
		:return: Euclidean distance between the two points
		"""
		return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

	def distance_function(self,set1, set2):
		"""
		Calculate the Hausdorff distance between two sets of points.
    
		:param set1: The first set of points, each point represented as a tuple (x, y)
		:param set2: The second set of points, each point represented as a tuple (x, y)
		:return: Hausdorff distance between the two sets of points
		"""
		def max_min_distance(set_a, set_b):
			"""
			Helper function to find the maximum of the minimum distances from each point in set_a to the closest point in set_b.
        
			:param set_a: The first set of points
			:param set_b: The second set of points
			:return: Maximum of the minimum distances
			"""
			max_min_dist = 0
			for point_a in set_a:
				min_dist = float('inf')
				for point_b in set_b:
					dist = self.euclidean_distance(point_a, point_b)
					if dist < min_dist:
						min_dist = dist
				if min_dist > max_min_dist:
					max_min_dist = min_dist
			return max_min_dist

		return max(max_min_distance(set1, set2), max_min_distance(set2, set1))
	def exemple(self):
		self.obj1_exemple = [(0, 0), (0, 1), (1, 0), (1, 1)]
		self.obj2_exemple = [(2, 2), (2, 3), (3, 2), (3, 3)]
		super().exemple()

class KendallTau(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,permutation1, permutation2):
		"""
		Calculate the Kendall Tau distance between two permutations.
    
		:param permutation1: The first permutation (a list of integers)
		:param permutation2: The second permutation (a list of integers)
		:return: Kendall Tau distance between the two permutations
		"""
		assert len(permutation1) == len(permutation2), "Permutations must be of the same length"
    
		n = len(permutation1)
		pairs = [(permutation1[i], permutation2[i]) for i in range(n)]
    
		def count_inversions(pairs):
			"""
			Helper function to count inversions in a list of pairs.
        
			:param pairs: List of pairs
			:return: Number of inversions
			"""
			inversions = 0
			for i in range(len(pairs)):
				for j in range(i + 1, len(pairs)):
					if (pairs[i][0] > pairs[j][0] and pairs[i][1] < pairs[j][1]) or (pairs[i][0] < pairs[j][0] and pairs[i][1] > pairs[j][1]):
						inversions += 1
			return inversions

		return count_inversions(pairs)
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4]
		self.obj2_exemple = [4, 3, 2, 1]
		super().exemple()


        
class Haversine(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,p1,p2 ):
		"""
		Calculate the Haversine distance between two points on the Earth's surface.
    
		:param lat1: Latitude of the first point in decimal degrees
		:param lon1: Longitude of the first point in decimal degrees
		:param lat2: Latitude of the second point in decimal degrees
		:param lon2: Longitude of the second point in decimal degrees
		:return: Haversine distance between the two points in kilometers
		"""
		lat1, lon1=p1[0],p1[1]
		lat2, lon2=p2[0],p2[1]
		# Radius of the Earth in kilometers
		R = 6371.0
    
		# Convert latitude and longitude from degrees to radians
		lat1_rad = degrees_to_radians(lat1)
		lon1_rad = degrees_to_radians(lon1)
		lat2_rad = degrees_to_radians(lat2)
		lon2_rad = degrees_to_radians(lon2)
    
		# Differences in coordinates
		dlat = lat2_rad - lat1_rad
		dlon = lon2_rad - lon1_rad
    
		# Haversine formula
		a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
		c = 2 * atan2(a**0.5, (1 - a)**0.5)
    
		# Distance in kilometers
		distance = R * c
    
		return distance
	def exemple(self):
		self.obj1_exemple = (48.8566, 2.3522)# Paris coordinates
		self.obj2_exemple = (51.5074, -0.1278)# London coordinates
		super().exemple()

class Canberra(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,point1, point2):
		"""
		Calculate the Canberra distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Canberra distance between the two points
		"""
		assert len(point1) == len(point2), "Points must be of the same dimension"
    
		distance = 0
		for x1, x2 in zip(point1, point2):
			numerator = abs(x1 - x2)
			denominator = abs(x1) + abs(x2)
			if denominator != 0:
				distance += numerator / denominator
    
		return distance

class BrayCurtis(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,point1, point2):
		"""
		Calculate the Bray-Curtis distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Bray-Curtis distance between the two points
		"""
		assert len(point1) == len(point2), "Points must be of the same dimension"
    
		sum_diff = 0
		sum_sum = 0
    
		for x1, x2 in zip(point1, point2):
			sum_diff += abs(x1 - x2)
			sum_sum += abs(x1 + x2)
    
		if sum_sum == 0:
			return 0  # To handle the case when both points are zeros
    
		distance = sum_diff / sum_sum
		return distance


class Matching(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,seq1, seq2):
		"""
		Calculate the Matching (Hamming) distance between two sequences.
    
		:param seq1: The first sequence (a list or string of characters or binary values)
		:param seq2: The second sequence (a list or string of characters or binary values)
		:return: Matching distance between the two sequences
		"""
		assert len(seq1) == len(seq2), "Sequences must be of the same length"
    
		distance = sum(el1 != el2 for el1, el2 in zip(seq1, seq2))
    
		return distance
	def exemple(self):
		self.obj1_exemple = [1, 0, 1, 1, 0]
		self.obj2_exemple = [0, 1, 1, 0, 0]

		super().exemple()

class Dice(Distance):
	
	def __init__(self):
		super().__init__()

	def distance_function(self,set1, set2):
		"""
		Calculate the Dice distance between two sets.
    
		:param set1: The first set (a set of elements)
		:param set2: The second set (a set of elements)
		:return: Dice distance between the two sets
		"""
		intersection = len(set1.intersection(set2))
		total_elements = len(set1) + len(set2)
    
		if total_elements == 0:
			return 0.0
    
		dice_coefficient = (2 * intersection) / total_elements
    
		return 1 - dice_coefficient
		
	def exemple(self):
		self.obj1_exemple = {"a", "b", "c", "d"}
		self.obj2_exemple = {"b", "c", "e", "f"}

		super().exemple()

class Kulsinski(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,set1, set2):
		"""
		Calculate the Kulsinski distance between two sets or binary vectors.
    
		:param set1: The first set (a set of elements or a list of binary values)
		:param set2: The second set (a set of elements or a list of binary values)
		:return: Kulsinski distance between the two sets or binary vectors
		"""
		if isinstance(set1, set) and isinstance(set2, set):
			# Calculate for sets
			intersection = len(set1.intersection(set2))
			union = len(set1.union(set2))
			a = intersection
			b = len(set1) - intersection
			c = len(set2) - intersection
			d = union - a - b - c
		elif isinstance(set1, list) and isinstance(set2, list) and len(set1) == len(set2):
			# Calculate for binary vectors
			a = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 1)
			b = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 0)
			c = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 1)
			d = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 0)
		else:
			raise ValueError("Input must be two sets or two binary vectors of the same length")

		n = a + b + c + d
    
		return (b + c - a + n) / (b + c + n)
	def exemple(self):
		self.obj1_exemple = {"a", "b", "c", "d"}
		self.obj2_exemple = {"b", "c", "e", "f"}

		super().exemple()

class DamerauLevenshtein(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,s1, s2):
		d = {}
		lenstr1 = len(s1)
		lenstr2 = len(s2)

		for i in range(-1, lenstr1 + 1):
			d[(i, -1)] = i + 1
		for j in range(-1, lenstr2 + 1):
			d[(-1, j)] = j + 1

		for i in range(lenstr1):
			for j in range(lenstr2):
				cost = 0 if s1[i] == s2[j] else 1
				d[(i, j)] = min(
					d[(i - 1, j)] + 1,  # suppresion
					d[(i, j - 1)] + 1,  # insertion
					d[(i - 1, j - 1)] + cost,  # substitution
				)
				if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
					d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition

		return d[lenstr1 - 1, lenstr2 - 1]
	def exemple(self):
		self.obj1_exemple = "ca"
		self.obj2_exemple = "abc"

		super().exemple()

class SorensenDice(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,str1, str2):
		# Convert strings to sets of bigrams
		bigrams1 = {str1[i:i+2] for i in range(len(str1) - 1)}
		bigrams2 = {str2[i:i+2] for i in range(len(str2) - 1)}
    
		# Calculate the intersection and the sizes of the sets
		intersection = len(bigrams1 & bigrams2)
		size1 = len(bigrams1)
		size2 = len(bigrams2)
    
		# Calculate the Sørensen-Dice coefficient
		sorensen_dice_coeff = 2 * intersection / (size1 + size2)
    
		# The distance is 1 minus the coefficient
		distance = 1 - sorensen_dice_coeff
    
		return distance
	def exemple(self):
		self.obj1_exemple = "night"
		self.obj2_exemple = "nacht"

		super().exemple()

class Tversky(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,set1, set2, alpha=0.5, beta=0.5):
		"""
		Calcule la distance de Tversky entre deux ensembles.
    
		:param set1: Premier ensemble
		:param set2: Deuxième ensemble
		:param alpha: Paramètre de pondération pour |A - B|
		:param beta: Paramètre de pondération pour |B - A|
		:return: Distance de Tversky
		"""
		# Taille de l'intersection des ensembles
		intersection = len(set1 & set2)
    
		# Taille des éléments uniques à chaque ensemble
		unique_to_set1 = len(set1 - set2)
		unique_to_set2 = len(set2 - set1)
    
		# Calcul du coefficient de Tversky
		tversky_coeff = intersection / (intersection + alpha * unique_to_set1 + beta * unique_to_set2)
    
		# La distance est 1 moins le coefficient de Tversky
		distance = 1 - tversky_coeff
    
		return distance
	def exemple(self):
		self.obj1_exemple =  {'a', 'b', 'c', 'd'}
		self.obj2_exemple = {'c', 'd', 'e', 'f'}
		self.obj3_exemple = 0.5
		self.obj4_exemple = 0.5
		super().exemple()

class Yule(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,binary_vector1, binary_vector2):
		"""
		Calcule la distance de Yule entre deux vecteurs binaires.
    
		:param binary_vector1: Premier vecteur binaire (liste de 0 et 1)
		:param binary_vector2: Deuxième vecteur binaire (liste de 0 et 1)
		:return: Distance de Yule
		"""
		if len(binary_vector1) != len(binary_vector2):
			raise ValueError("Les vecteurs binaires doivent avoir la même longueur.")
    
		# Calcul des variables a, b, c, d
		a = b = c = d = 0
    
		for bit1, bit2 in zip(binary_vector1, binary_vector2):
			if bit1 == 1 and bit2 == 1:
				a += 1
			elif bit1 == 1 and bit2 == 0:
				b += 1
			elif bit1 == 0 and bit2 == 1:
				c += 1
			elif bit1 == 0 and bit2 == 0:
				d += 1
    
		# Calcul de l'indice de dissimilarité de Yule Q
		if (a * d + b * c) == 0:
			return 0.0  # Si le dénominateur est 0, la dissimilarité est 0 (vecteurs identiques)
    
		Q = 2 * b * c / (a * d + b * c)
        
		return Q / (Q + 2 * a * d)
	def exemple(self):
		self.obj1_exemple =  [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
		self.obj2_exemple = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
		super().exemple()



class Bhattacharyya(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self,P, Q):
		"""
		Calcule la distance de Bhattacharyya entre deux distributions de probabilité discrètes.
    
		:param P: Première distribution de probabilité (liste de probabilités)
		:param Q: Deuxième distribution de probabilité (liste de probabilités)
		:return: Distance de Bhattacharyya
		"""
		if len(P) != len(Q):
			raise ValueError("Les distributions doivent avoir la même longueur.")
    
		# Calcul du coefficient de Bhattacharyya
		bc = 0.0
		for p, q in zip(P, Q):
			bc += (p * q)**0.5
    
		# Calcul de la distance de Bhattacharyya
		distance = -log(bc)
    
		return distance
	def exemple(self):
		self.obj1_exemple =  [0.1, 0.2, 0.4, 0.3]
		self.obj2_exemple = [0.2, 0.3, 0.1, 0.4]
		super().exemple()


  
class Gower(Distance):
	def __init__(self):
		super().__init__()
	def distance_function(self, vec1, vec2, ranges):
		"""
		Calculate the Gower similarity between two vectors.

		Parameters:
		- vec1: List of values for the first entity (can include both numerical and categorical).
		- vec2: List of values for the second entity (can include both numerical and categorical).
		- ranges: List of ranges for numerical variables. Use `None` for categorical variables.

		Returns:
		- Similarity: Gower similarity between vec1 and vec2.
		"""
		if len(vec1) != len(vec2) or len(vec1) != len(ranges):
			raise ValueError("Vectors and ranges must have the same length.")

		total_similarity = 0
		num_variables = len(vec1)

		for i in range(num_variables):
			if ranges[i] is None:
				# Categorical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
				    similarity = 0
			else:
				# Numerical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
					range_value = ranges[i]
					if range_value == 0:
						similarity = 0
					else:
						similarity = 1 - abs(vec1[i] - vec2[i]) / range_value

			total_similarity += similarity

		# Normalize by the number of variables
		return total_similarity / num_variables
	def exemple(self):
		test_cases = [
			(["Red", 3.2, 5], ["Blue", 4.1, 3], [None, 5.0, 10]),
			([5.5, "M", 200], [6.1, "F", 180], [10, None, 50]),
			([0, "High", 10], [1, "Low", 10], [1, None, 10]),
			([100, "Yes", 3.5], [150, "No", 2.8], [50, None, 5]),
			([1.5, "Green", 2], [1.5, "Green", 2], [None, None, None])
		]

		# Compute and print the Gower similarity for each pair
		for vec1, vec2, ranges in test_cases:
			similarity = gower.calculate(vec1, vec2, ranges)
			print(f"Gower similarity between {vec1} and {vec2}: {similarity:.4f}")


class Pearson(Distance):
	def __init__(self):
		super().__init__()

	def distance_function(self,x, y):
		"""
		Calcule le coefficient de corrélation de Pearson entre deux listes de données.

		:param x: Liste des valeurs de la première variable.
		:param y: Liste des valeurs de la seconde variable.
		:return: Coefficient de corrélation de Pearson entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les listes x et y doivent avoir la même longueur.")
    
		n = len(x)
    
		# Calcul des moyennes
		mean_x = sum(x) / n
		mean_y = sum(y) / n
    
		# Calcul des covariances et des variances
		cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
		var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
		var_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
		# Calcul du coefficient de corrélation de Pearson
		if var_x == 0 or var_y == 0:
			raise ValueError("L'écart-type ne peut pas être nul.")
    
		pearson_corr = cov_xy / (var_x ** 0.5 * var_y ** 0.5)
    
		return 1 - pearson_corr
	def exemple(self):
		self.obj1_exemple = [1, 1, 3, 4, 5]
		self.obj2_exemple = [2, 3, 4, 5, 6]
		super().exemple()



class Spearman(Distance):
	def __init__(self):
		super().__init__()

	def distance_function(self,x, y):
		"""
		Calcule la distance de Spearman entre deux listes de données.
    
		:param x: Liste des valeurs de la première variable.
		:param y: Liste des valeurs de la seconde variable.
		:return: Distance de Spearman entre x et y.
		"""
		spearman_corr = spearman_correlation(x, y)
		# La distance de Spearman est 1 moins le coefficient de corrélation de Spearman
		distance = 1 - spearman_corr
    
		return distance
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4, 5]
		self.obj2_exemple = [5, 6, 7, 8, 7]
		super().exemple()

class Ochiai(Distance):
	def __init__(self):
		super().__init__()

	def distance_function(self,set1, set2):
		"""
		Calcule la distance d'Ochiai entre deux ensembles de données binaires.
    
		:param set1: Premier ensemble de données binaires (sous forme de liste de booléens).
		:param set2: Deuxième ensemble de données binaires (sous forme de liste de booléens).
		:return: Distance d'Ochiai entre set1 et set2.
		"""
		if len(set1) != len(set2):
			raise ValueError("Les ensembles doivent avoir la même longueur.")
    
		# Convertir les listes en ensembles de indices où la valeur est True
		indices1 = {i for i, v in enumerate(set1) if v}
		indices2 = {i for i, v in enumerate(set2) if v}
    
		# Calculer les éléments communs
		intersection = indices1 & indices2
		intersection_size = len(intersection)
    
		# Calculer les tailles des ensembles
		size1 = len(indices1)
		size2 = len(indices2)
    
		# Calculer la distance d'Ochiai
		if size1 == 0 or size2 == 0:
			# Eviter la division par zéro
			return 0
        
		return intersection_size / (size1 * size2) ** 0.5
	def exemple(self):
		self.obj1_exemple = [True, False, True, True, False]
		self.obj2_exemple = [True, True, False, False, True]
		super().exemple()

class Hellinger(Distance):
	def __init__(self):
		super().__init__()

	def distance_function(self,p, q):
		"""
		Calcule la distance de Hellinger entre deux distributions de probabilités.
    
		:param p: Première distribution de probabilités (sous forme de liste ou d'array).
		:param q: Deuxième distribution de probabilités (sous forme de liste ou d'array).
		:return: Distance de Hellinger entre p et q.
		"""
		if len(p) != len(q):
			raise ValueError("Les distributions doivent avoir la même longueur.")
    
		# Calculer la distance de Hellinger
		sum_of_squares = sum(((p_i)**0.5 - (q_i)**0.5 ) ** 2 for p_i, q_i in zip(p, q))
    
		return (1 / 2**0.5 ) * sum_of_squares**0.5
	def exemple(self):
		self.obj1_exemple = [0.1, 0.4, 0.5]
		self.obj2_exemple = [0.2, 0.3, 0.5]
		super().exemple()

class CzekanowskiDice(Distance):
	def __init__(self):
		super().__init__()

	def distance_function(self,x, y):
		"""
		Calcule la distance Czekanowski-Dice entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:return: Distance Czekanowski-Dice entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		min_sum = sum(min(x_i, y_i) for x_i, y_i in zip(x, y))
		sum_x = sum(x)
		sum_y = sum(y)
    
		if sum_x + sum_y == 0:
			return 0.0  # Pour éviter la division par zéro
    
		dice_similarity = (2 * min_sum) / (sum_x + sum_y)
    
		return 1 - dice_similarity
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4]
		self.obj2_exemple = [2, 2, 3, 5]
		super().exemple()

class MotzkinStraus(Distance):
	def __init__(self):
		super().__init__()

	def distance_function(self,x, y, p=2):
		"""
		Calcule une distance hypothétique Motzkin-Straus généralisée entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:param p: Paramètre pour la norme de Minkowski (par défaut 2 pour la distance Euclidienne).
		:return: Distance Motzkin-Straus entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		# Calcul de la norme de Minkowski (généralement Euclidienne pour p=2)
		minkowski_distance = sum(abs(x_i - y_i)**p for x_i, y_i in zip(x, y))**(1/p)
    
		# Ajout d'une composante structurelle simple (hypothétique)
		structure_distance = sum((x_i - y_i)**2 for x_i, y_i in zip(x, y)) / len(x)
    
		# Combinaison des deux distances
		motzkin_straus_distance = minkowski_distance + structure_distance
    
		return motzkin_straus_distance
		
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4]
		self.obj2_exemple = [2, 2, 3, 5]
		super().exemple()



class FagerMcGowan(Distance):
    def __init__(self):
        super().__init__()
    """
    FagerMcGowan similarity coefficient calculator.

    The FagerMcGowan similarity coefficient is used to measure the similarity 
    between two sets, particularly in ecological studies. It adjusts for the 
    expected overlap due to random chance, providing a more accurate reflection 
    of true similarity.

    Methods:
    --------
    calculate(set1, set2, N):
        Calculates the FagerMcGowan similarity coefficient between two sets.
    """

    def distance_function(self, set1, set2, N):
        """
        Calculate the Fager-McGowan similarity coefficient between two sets.

        Parameters:
        -----------
        set1 : set
            The first set of elements (e.g., species in a habitat).
        set2 : set
            The second set of elements.
        N : int
            The total number of unique elements in the universal set.

        Returns:
        --------
        float
            The Fager-McGowan similarity coefficient.
        """
        intersection_size = len(set1 & set2)  # Number of elements common to both sets
        set1_size = len(set1)  # Size of the first set
        set2_size = len(set2)  # Size of the second set

        # Calculate the Fager-McGowan similarity coefficient
        numerator = intersection_size - (set1_size * set2_size / N)
        denominator = min(set1_size, set2_size)

        if denominator == 0:
            return 0.0

        similarity = numerator / denominator
        return similarity


class EnhancedRogersTanimoto(Distance):
	def __init__(self):
		super().__init__()

	def distance_function(self,vector_a, vector_b, alpha=1):
		"""
		Calcule la distance Rogers-Tanimoto améliorée entre deux vecteurs binaires.
    
		:param vector_a: Premier vecteur (de type list).
		:param vector_b: Deuxième vecteur (de type list).
		:param alpha: Facteur de régularisation (par défaut: 1).
		:return: Distance Rogers-Tanimoto améliorée entre vector_a et vector_b.
		"""
		if len(vector_a) != len(vector_b):
			raise ValueError("Les deux vecteurs doivent avoir la même longueur")
    
		a = b = c = d = 0
    
		for i in range(len(vector_a)):
			if vector_a[i] == 1 and vector_b[i] == 1:
				a += 1
			elif vector_a[i] == 1 and vector_b[i] == 0:
				b += 1
			elif vector_a[i] == 0 and vector_b[i] == 1:
				c += 1
			elif vector_a[i] == 0 and vector_b[i] == 0:
				d += 1
    
		# Calcul de la distance Rogers-Tanimoto améliorée
		return (a + b + c) / (a + b + c + d + alpha)
	def exemple(self):
		self.obj1_exemple = [1, 1, 0, 0, 1]
		self.obj2_exemple = [1, 0, 1, 0, 1]
		self.obj3_exemple = 1# Facteur de régularisation
		super().exemple()

import numpy as np
from numpy import ones, pad, convolve,dot,linalg


class ContextualDynamicDistance(Distance):
    
	def __init__(self):
		super().__init__()
		"""
		Initialize the CDD with a context weight function.
        
		:param context_weight_func: A function that takes in the contexts of two points
                                    and returns the weight for each feature.
		"""

	def distance_function(self, x, y, context_x, context_y):
		"""
		Calculate the Contextual Dynamic Distance (CDD) between two points.
        
		:param x: List or vector representing the first data point.
		:param y: List or vector representing the second data point.
		:param context_x: List or vector representing the context of the first data point.
		:param context_y: List or vector representing the context of the second data point.
        
		:return: The CDD value as a float.
		"""
		if len(x) != len(y) or len(context_x) != len(context_y):
			raise ValueError("Data points and contexts must be of the same length.")
        
		distance = 0.0
		for i in range(len(x)):
			weight = self.convolution_context_weight_func(context_x, context_y, i)
			distance += weight * (x[i] - y[i]) ** 2
        
		return distance ** 0.5

	def convolution_context_weight_func(self,context_x, context_y, index, kernel_size=3):
		"""
		A context weight function based on convolution.
    
		:param context_x: Context vector for the first point.
		:param context_y: Context vector for the second point.
		:param index: Current index for which the weight is calculated.
		:param kernel_size: Size of the convolution kernel.
    
		:return: The weight for the feature at the given index as a float.
		"""
		half_kernel = kernel_size // 2

		# Define convolution kernel (e.g., a simple averaging kernel)
		kernel = np.ones(kernel_size) / kernel_size

		# Extract the relevant sub-contexts around the current index
		sub_context_x = context_x[max(0, index - half_kernel):min(len(context_x), index + half_kernel + 1)]
		sub_context_y = context_y[max(0, index - half_kernel):min(len(context_y), index + half_kernel + 1)]

		# If sub-contexts are shorter than the kernel, pad them
		if len(sub_context_x) < kernel_size:
			sub_context_x = np.pad(sub_context_x, (0, kernel_size - len(sub_context_x)), 'constant')
		if len(sub_context_y) < kernel_size:
			sub_context_y = np.pad(sub_context_y, (0, kernel_size - len(sub_context_y)), 'constant')

		# Convolve the contexts with the kernel
		conv_x = np.convolve(sub_context_x, kernel, mode='valid')
		conv_y = np.convolve(sub_context_y, kernel, mode='valid')

		# Calculate the weight as the similarity of the convolved signals
		similarity = np.dot(conv_x, conv_y) / (np.linalg.norm(conv_x) * np.linalg.norm(conv_y) + 1e-10)
		return similarity
	def exemple(self):
		# Feature vectors
		self.obj1_exemple = [1.0, 2.0, 3.0]
		self.obj2_exemple = [4.0, 5.0, 6.0]
		# Context vectors
		self.obj3_exemple = [0.2, 0.3, 0.5]
		self.obj4_exemple = [0.1, 0.4, 0.6]
		super().exemple()

#################################
#Loss function
#################################

class CrossEntropy(Distance):
	def __init__(self):
		super().__init__()    
	def __call__(self, y_true, y_pred):
		"""
		Calcul de la perte Cross Entropy.
        
		:param y_true: Les véritables étiquettes, de forme (batch_size, seq_len)
		:param y_pred: Les prédictions du modèle, de forme (batch_size, seq_len, vocab_size)
		:return: La valeur moyenne de la perte Cross Entropy
		"""
		batch_size = len(y_true)
		total_loss = 0.0
        
		for i in range(batch_size):
			for j in range(len(y_true[i])):
				true_label = y_true[i][j]
				pred_probs = self.softmax(y_pred[i][j])
                
				# Calculer la perte pour chaque échantillon
				total_loss += -log(pred_probs[true_label] + 1e-9)  # Ajout d'un epsilon pour éviter log(0)
        
		# Retourner la perte moyenne
		return total_loss / (batch_size * len(y_true[0]))
    
	def softmax(self, logits):
		"""
		Calculer la softmax pour transformer les logits en probabilités.
        
		:param logits: Logits de forme (vocab_size,)
		:return: Probabilités de forme (vocab_size,)
		"""
		max_logit = max(logits)  # Pour éviter des overflow dans l'exponentiation
		exp_logits = [math.exp(logit - max_logit) for logit in logits]
		sum_exp_logits = sum(exp_logits)
        
		# Retourner les probabilités
		return [exp_logit / sum_exp_logits for exp_logit in exp_logits]

class KullbackLeibler:
	def __init__(self):
		super().__init__()    
    
	def __call__(self, p, q):
		"""
		Calculate the Kullback-Leibler divergence between two probability distributions.
        
		:param p: The true probability distribution (list of probabilities).
		:param q: The predicted probability distribution (list of probabilities).
		:return: The KL divergence value.
		"""
		kl_divergence = 0.0
        
		for pi, qi in zip(p, q):
			if pi > 0 and qi > 0:  # To avoid log(0), we only calculate for positive values.
				kl_divergence += pi * math.log(pi / qi)
        
		return kl_divergence


class MeanAbsoluteError:
	def __init__(self):
		super().__init__()    
    
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Absolute Error between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MAE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			total_error += abs(y_true[i] - y_pred[i])
        
		mae = total_error / n
		return mae

class MAE(MeanAbsoluteError):
	def __init__(self):
		super().__init__()


class MeanAbsolutePercentageError:
	def __init__(self):
		super().__init__()    
    
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Absolute Percentage Error (MAPE) between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MAPE value as a percentage.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_percentage_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			if y_true[i] != 0:
				percentage_error = abs((y_true[i] - y_pred[i]) / y_true[i])
				total_percentage_error += percentage_error
			else:
				raise ValueError("y_true contains a zero value, which would cause a division by zero error in MAPE calculation.")
        
		mape = (total_percentage_error / n) * 100
		return mape

class MAPE(MeanAbsolutePercentageError):
	def __init__(self):
		super().__init__()
		
# distancia/loss_functions.py

class MeanSquaredError:
	def __init__(self):
		super().__init__()    
    
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Squared Error (MSE) between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MSE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_squared_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			squared_error = (y_true[i] - y_pred[i]) ** 2
			total_squared_error += squared_error
        
		mse = total_squared_error / n
		return mse

class MSE(MeanSquaredError):
	def __init__(self):
		super().__init__()
		

class SquaredLogarithmicError:
	def __init__(self):
		super().__init__()
    
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Squared Logarithmic Error (SLE) between two lists of values.
        
		:param y_true: List of true values. Must be positive.
		:param y_pred: List of predicted values. Must be positive.
		:return: The SLE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		if any(v <= 0 for v in y_true) or any(v <= 0 for v in y_pred):
			raise ValueError("All values in y_true and y_pred must be positive for SLE calculation.")
        
		total_squared_log_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			# Apply log transformation
			log_y_true = math.log(y_true[i] + 1)
			log_y_pred = math.log(y_pred[i] + 1)
			# Compute squared log error
			squared_log_error = (log_y_true - log_y_pred) ** 2
			total_squared_log_error += squared_log_error
        
		sle = total_squared_log_error / n
		return sle

class SLE(SquaredLogarithmicError):
	def __init__(self):
		super().__init__()


class GaloisWassersteinLoss:
    def __init__(self, alpha=1.0, beta=1.0, gamma=1.0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.trellis = self.build_galois_trellis()

    def build_galois_trellis(self):
        """
        Construct a Galois trellis representing the hierarchical relationships between classes.
        
        :return: A dictionary representing the trellis where the keys are pairs of classes,
                 and the values are the distances between those classes.
        """
        # Example structure for the trellis
        # Replace this with a more complex or domain-specific trellis if necessary
        trellis = {
            (0, 0): 0, (0, 1): 1, (0, 2): 2,
            (1, 0): 1, (1, 1): 0, (1, 2): 1,
            (2, 0): 2, (2, 1): 1, (2, 2): 0
        }
        return trellis
    
    def compute_cdf(self, probabilities):
        """
        Compute the cumulative distribution function (CDF) from a list of probabilities.
        
        :param probabilities: List of probabilities for each class.
        :return: CDF as a list.
        """
        cdf = []
        cumulative_sum = 0.0
        for p in probabilities:
            cumulative_sum += p
            cdf.append(cumulative_sum)
        return cdf
    
    def cross_entropy(self, y_true, y_pred):
        """
        Compute the Cross Entropy between true and predicted distributions.
        
        :param y_true: List of true class probabilities.
        :param y_pred: List of predicted class probabilities.
        :return: The cross-entropy value.
        """
        if len(y_true) != len(y_pred):
            raise ValueError("The length of y_true and y_pred must be the same.")
        
        entropy = 0.0
        for i in range(len(y_true)):
            if y_true[i] > 0:
                entropy -= y_true[i] * log(y_pred[i] + 1e-10)  # Adding a small epsilon to avoid log(0)
        return entropy
    
    def distance_function(self, y_true, y_pred):
        """
        Compute the Galois distance between true and predicted distributions using the internal Galois trellis.
        
        :param y_true: List of true class probabilities.
        :param y_pred: List of predicted class probabilities.
        :return: The Galois distance value.
        """
        distance = 0.0
        for i in range(len(y_true)):
            for j in range(len(y_pred)):
                if y_true[i] > 0 and y_pred[j] > 0:
                    distance += self.trellis.get((i, j), 1) * abs(y_true[i] - y_pred[j])
        return distance
    
    def __call__(self, y_true, y_pred):
        """
        Calculate the Galois-Wasserstein Loss between the true and predicted distributions.
        
        :param y_true: List of true class probabilities.
        :param y_pred: List of predicted class probabilities.
        :return: The Galois-Wasserstein Loss value.
        """
        if len(y_true) != len(y_pred):
            raise ValueError("The length of y_true and y_pred must be the same.")
        
        # Compute CDF for true and predicted distributions
        cdf_true = self.compute_cdf(y_true)
        cdf_pred = self.compute_cdf(y_pred)
        
        # Compute Wasserstein distance
        wasserstein_distance = sum(abs(cdf_true[i] - cdf_pred[i]) for i in range(len(cdf_true)))
        
        # Compute Cross Entropy
        cross_entropy = self.cross_entropy(y_true, y_pred)
        
        # Compute Galois distance
        galois_distance = self.galois_distance(y_true, y_pred)
        
        # Compute combined loss
        loss = self.alpha * wasserstein_distance + self.beta * cross_entropy + self.gamma * galois_distance
        return loss
	
class MahalanobisTaguchi:
    def __init__(self, reference_group):
        """
        Initialize the MahalanobisTaguchi class with a reference group.

        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        self.reference_group = reference_group
        self.mean_vector = self.calculate_mean_vector()
        self.covariance_matrix = self.calculate_covariance_matrix()
        self.inverse_covariance_matrix = self.invert_matrix(self.covariance_matrix)

    def calculate_mean_vector(self):
        """
        Calculate the mean vector of the reference group.

        :return: A list representing the mean vector.
        """
        num_points = len(self.reference_group)
        num_dimensions = len(self.reference_group[0])

        mean_vector = [0] * num_dimensions

        for point in self.reference_group:
            for i in range(num_dimensions):
                mean_vector[i] += point[i]

        mean_vector = [x / num_points for x in mean_vector]
        return mean_vector

    def calculate_covariance_matrix(self):
        """
        Calculate the covariance matrix of the reference group.

        :return: A 2D list representing the covariance matrix.
        """
        num_dimensions = len(self.reference_group[0])
        covariance_matrix = [[0] * num_dimensions for _ in range(num_dimensions)]

        for point in self.reference_group:
            diff_vector = [point[i] - self.mean_vector[i] for i in range(num_dimensions)]
            for i in range(num_dimensions):
                for j in range(num_dimensions):
                    covariance_matrix[i][j] += diff_vector[i] * diff_vector[j]

        num_points = len(self.reference_group)
        covariance_matrix = [[covariance_matrix[i][j] / (num_points - 1) for j in range(num_dimensions)] for i in range(num_dimensions)]
        return covariance_matrix

    def invert_matrix(self, matrix):
        """
        Invert a square matrix using Gaussian elimination.

        :param matrix: A 2D list representing the matrix to be inverted.
        :return: A 2D list representing the inverted matrix.
        """
        n = len(matrix)
        identity_matrix = [[float(i == j) for i in range(n)] for j in range(n)]

        # Forward elimination
        for i in range(n):
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
                identity_matrix[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
                        identity_matrix[k][j] -= factor * identity_matrix[i][j]

        return identity_matrix

    def distance_function(self, data_point):
        """
        Calculate the Mahalanobis-Taguchi distance for a given data point.

        :param data_point: A list representing the data point to be evaluated.
        :return: The Mahalanobis-Taguchi distance as a float.
        """
        diff_vector = [data_point[i] - self.mean_vector[i] for i in range(len(self.mean_vector))]
        
        # Matrix multiplication with the inverse covariance matrix
        temp_vector = [0] * len(diff_vector)
        for i in range(len(diff_vector)):
            for j in range(len(diff_vector)):
                temp_vector[i] += diff_vector[j] * self.inverse_covariance_matrix[j][i]

        # Final dot product to get the Mahalanobis-Taguchi distance
        distance_squared = sum(temp_vector[i] * diff_vector[i] for i in range(len(diff_vector)))
        return distance_squared ** 0.5

class Otsuka(Distance):
    def __init__(self):
        """
        Initialize the Otsuka class with two categorical vectors.

        :param vector1: First categorical vector (list of strings).
        :param vector2: Second categorical vector (list of strings).
        """
        pass
    def distance_function(self, vector1, vector2):
        """
        Calculate the Otsuka distance between the two categorical vectors.

        :return: The Otsuka distance as a float.
        """
        if len(self.vector1) != len(self.vector2):
            raise ValueError("Vectors must be of the same length.")

        a = b = c = d = 0

        for v1, v2 in zip(self.vector1, self.vector2):
            if v1 == v2:
                a += 1
            elif v1 != v2 and v1 != 'X' and v2 != 'X':
                b += 1
            elif v1 != v2 and v1 == 'X':
                c += 1
            elif v1 != v2 and v2 == 'X':
                d += 1

        total = a + b + c + d
        if total == 0:
            return 0.0

        return 0.5 * ( (a + d) / total + (b + c) / total )

class RogersTanimoto:
    def __init__(self):
        """
        Initialize the Rogers-Tanimoto class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        self.vector1 = vector1
        self.vector2 = vector2

    def distance_function(self, vector1, vector2):
        """
        Calculate the Rogers-Tanimoto distance between the two binary vectors.

        :return: The Rogers-Tanimoto distance as a float.
        """
        # Calculate the components of the formula
        a = sum(v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))  # Both are 1
        b = sum(v1 and not v2 for v1, v2 in zip(self.vector1, self.vector2))  # Present in vector1 but not in vector2
        c = sum(not v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))  # Present in vector2 but not in vector1
        d = sum(not v1 and not v2 for v1, v2 in zip(self.vector1, self.vector2))  # Both are 0

        # Calculate the Rogers-Tanimoto distance
        distance = (a + b + c) / (a + b + c + d)

        return distance

class RussellRao:
    def __init__(self, vector1, vector2):
        """
        Initialize the Russell-Rao class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        self.vector1 = vector1
        self.vector2 = vector2

    def distance_function(self):
        """
        Calculate the Russell-Rao distance between the two binary vectors.

        :return: The Russell-Rao distance as a float.
        """
        # Calculate the number of matching features (both present)
        a = sum(v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))

        # Calculate the total number of features
        n = len(self.vector1)

        # Calculate the Russell-Rao distance
        distance = a / n

        return distance

class SokalMichener:
    def __init__(self):
        """
        Initialize the SokalMichener class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        self.vector1 = vector1
        self.vector2 = vector2

    def distance_function(self, vector1, vector2):
        """
        Calculate the Sokal-Michener distance between the two binary vectors.

        :return: The Sokal-Michener distance as a float.
        """
        # Number of matches where both vectors have 1s (a)
        a = sum(v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))

        # Number of matches where both vectors have 0s (d)
        d = sum((not v1) and (not v2) for v1, v2 in zip(self.vector1, self.vector2))

        # Total number of features (n)
        n = len(self.vector1)

        # Calculate the Sokal-Michener distance
        similarity = (a + d) / n
        distance = 1 - similarity

        return distance

class SokalSneath:
    def __init__(self):
        """
        Initialize the SokalSneath class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        self.vector1 = vector1
        self.vector2 = vector2

    def distance_function(self, vector1, vector2):
        """
        Calculate the Sokal-Sneath distance between the two binary vectors.

        :return: The Sokal-Sneath distance as a float.
        """
        # Number of matches where both vectors have 1s (a)
        a = sum(v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))

        # Number of mismatches where vector1 has 1 and vector2 has 0 (b)
        b = sum(v1 and not v2 for v1, v2 in zip(self.vector1, self.vector2))

        # Number of mismatches where vector1 has 0 and vector2 has 1 (c)
        c = sum(not v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))

        # Calculate the Sokal-Sneath distance
        distance = (c + 2 * b) / (a + b + c)

        return distance

class Wasserstein(Distance):
    def __init__(self):
        """
        Initialize the Wasserstein class with two probability distributions.

        :param distribution1: First probability distribution (list of floats).
        :param distribution2: Second probability distribution (list of floats).
        """
        super().__init__()


    def distance_function(self, distribution1, distribution2):
        """
        Calculate the Wasserstein distance between the two distributions.

        :return: The Wasserstein distance as a float.
        """
        if len(distribution1) != len(distribution2):
            raise ValueError("Distributions must have the same length.")
        
    
        # Cumulative distribution functions (CDF) of both distributions
        cdf1 = self._cumulative_distribution(distribution1)
        cdf2 = self._cumulative_distribution(distribution2)

        # Wasserstein distance is the area between the CDFs
        distance = sum(abs(c1 - c2) for c1, c2 in zip(cdf1, cdf2))

        return distance

    def _cumulative_distribution(self, distribution):
        """
        Calculate the cumulative distribution for a given distribution.

        :param distribution: A probability distribution (list of floats).
        :return: The cumulative distribution (list of floats).
        """
        cdf = []
        cumulative_sum = 0.0
        for prob in distribution:
            cumulative_sum += prob
            cdf.append(cumulative_sum)
        return cdf

class DynamicTimeWarping(Distance):
    def __init__(self):
        """
        Compute the Dynamic Time Warping (DTW) distance between two time series.
    
        DTW is a measure of similarity between two temporal sequences that may vary in speed.
        This class allows the computation of the DTW distance and the optimal alignment path between the sequences.
    
        Attributes:
        series_a (list or array): First time series.
        series_b (list or array): Second time series.
        distance_matrix (2D list): The accumulated cost matrix used to compute the DTW distance.
        dtw_distance (float): The computed DTW distance between series_a and series_b.
        """
        super().__init__()


    def distance_function(self, series_a, series_b):
        """
        Compute the DTW distance between the two time series.
        
        Returns:
            float: The DTW distance.
        """
        self.series_a = series_a
        self.series_b = series_b
        self.distance_matrix = None
        self.dtw_distance = None
        
        n = len(self.series_a)
        m = len(self.series_b)
        self.distance_matrix = [[float('inf')] * m for _ in range(n)]
        self.distance_matrix[0][0] = 0
        
        for i in range(1, n):
            for j in range(1, m):
                cost = abs(self.series_a[i] - self.series_b[j])
                self.distance_matrix[i][j] = cost + min(self.distance_matrix[i-1][j],    # Insertion
                                                        self.distance_matrix[i][j-1],    # Deletion
                                                        self.distance_matrix[i-1][j-1])  # Match

        self.dtw_distance = self.distance_matrix[-1][-1]
        return self.dtw_distance

    def get_optimal_path(self):
        """
        Retrieve the optimal path that aligns the two time series with the minimum cost.
        
        Returns:
            list of tuples: The optimal path as a list of index pairs (i, j).
        """
        i, j = len(self.series_a) - 1, len(self.series_b) - 1
        path = [(i, j)]
        
        while i > 0 and j > 0:
            if i == 0:
                j -= 1
            elif j == 0:
                i -= 1
            else:
                step = min(self.distance_matrix[i-1][j], self.distance_matrix[i][j-1], self.distance_matrix[i-1][j-1])
                
                if step == self.distance_matrix[i-1][j-1]:
                    i -= 1
                    j -= 1
                elif step == self.distance_matrix[i-1][j]:
                    i -= 1
                else:
                    j -= 1
            
            path.append((i, j))
        
        path.reverse()
        return path

class LongestCommonSubsequence(Distance):
    def __init__(self):
        """
        Initialize the LongestCommonSubsequence class with two sequences.

        :param sequence_a: The first sequence (e.g., list, string, etc.)
        :param sequence_b: The second sequence
        """
        super().__init__()

    def distance_function(self, sequence_a, sequence_b):
        """
        Compute the LCSS distance between the two sequences.

        :return: The length of the Longest Common Subsequence
        """
        self.sequence_a = sequence_a
        self.sequence_b = sequence_b
        self.lcs_matrix = None
	
        len_a = len(self.sequence_a)
        len_b = len(self.sequence_b)
        self.lcs_matrix = [[0] * (len_b + 1) for _ in range(len_a + 1)]

        for i in range(1, len_a + 1):
            for j in range(1, len_b + 1):
                if self.sequence_a[i - 1] == self.sequence_b[j - 1]:
                    self.lcs_matrix[i][j] = self.lcs_matrix[i - 1][j - 1] + 1
                else:
                    self.lcs_matrix[i][j] = max(self.lcs_matrix[i - 1][j], self.lcs_matrix[i][j - 1])

        return self.lcs_matrix[len_a][len_b]

    def get_lcs(self):
        """
        Retrieve the Longest Common Subsequence.

        :return: A sequence representing the LCS
        """
        if self.lcs_matrix is None:
            self.compute()

        lcs = []
        i, j = len(self.sequence_a), len(self.sequence_b)

        while i > 0 and j > 0:
            if self.sequence_a[i - 1] == self.sequence_b[j - 1]:
                lcs.append(self.sequence_a[i - 1])
                i -= 1
                j -= 1
            elif self.lcs_matrix[i - 1][j] >= self.lcs_matrix[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return ''.join(reversed(lcs)) if isinstance(self.sequence_a, str) else list(reversed(lcs))

    def lcss_distance(self):
        """
        Compute the LCSS distance, which is the difference between the length of the sequences and the LCS length.

        :return: The LCSS distance
        """
        lcs_length = self.compute()
        return max(len(self.sequence_a), len(self.sequence_b)) - lcs_length

class Frechet(Distance):

    def __init__(self):
        """
        Initialize the FrechetDistance with two curves.

        :param curve_a: First curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
        :param curve_b: Second curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
        """
        super().__init__()

    def _c(self, i, j):
        """
        Internal method to compute the discrete Fréchet distance using dynamic programming.

        :param i: Index in curve_a
        :param j: Index in curve_b
        :return: Fréchet distance between curve_a[0..i] and curve_b[0..j]
        """
        if self.ca[i][j] > -1:
            return self.ca[i][j]
        elif i == 0 and j == 0:
            self.ca[i][j] = Euclidean().calculate(self.curve_a[0], self.curve_b[0])
        elif i > 0 and j == 0:
            self.ca[i][j] = max(self._c(i - 1, 0), Euclidean().calculate(self.curve_a[i], self.curve_b[0]))
        elif i == 0 and j > 0:
            self.ca[i][j] = max(self._c(0, j - 1), Euclidean().calculate(self.curve_a[0], self.curve_b[j]))
        elif i > 0 and j > 0:
            self.ca[i][j] = max(
                min(self._c(i - 1, j), self._c(i - 1, j - 1), self._c(i, j - 1)),
                Euclidean().calculate(self.curve_a[i], self.curve_b[j])
            )
        else:
            self.ca[i][j] = float('inf')
        return self.ca[i][j]

    def distance_function(self, curve_a, curve_b):
        """
        Compute the Fréchet distance between the two curves.

        :return: The Fréchet distance between curve_a and curve_b
        """
        self.curve_a = curve_a
        self.curve_b = curve_b
        self.ca = [[-1 for _ in range(len(curve_b))] for _ in range(len(curve_a))]
        
        return self._c(len(self.curve_a) - 1, len(self.curve_b) - 1)

#Graph
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






class CustomDistanceFunction(Distance):
    """
    A class to compute custom distance between two data points using a user-defined function.
    """
    def __init__(self):
        """
        Initialize the Wasserstein class with two probability distributions.

        :param distribution1: First probability distribution (list of floats).
        :param distribution2: Second probability distribution (list of floats).
        """
        super().__init__()


    def __init__(self, func):
        """
        Initialize the CustomDistanceFunction class with a user-defined function.

        Parameters:
        func (function): A function that takes two inputs (data points) and returns a distance metric.
        """
        if not callable(func):
            raise ValueError("The provided custom function must be callable.")
        self.func = func

    def calculate(self, data1, data2):
        """
        Compute the distance between two data points using the custom function.

        Parameters:
        data1: The first data point.
        data2: The second data point.

        Returns:
        The result of the custom function applied to data1 and data2.
        """
        return self.func(data1, data2)

import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

class IntegratedDistance:
    def __init__(self, func=Euclidean):
        """
        Initialize the IntegratedDistance class with a distance function.
        
        Parameters:
        func (callable): A function that takes two points and returns a distance. 
                         Default is Euclidean distance.
        """
        self.func = func

    def calculate(self, point1, point2):
        """
        Compute the distance between two points using the specified distance function.
        
        Parameters:
        point1, point2: The points between which to compute the distance. Can be tuples, lists, or numpy arrays.
        
        Returns:
        float: The computed distance.
        """
        return self.func(point1, point2)

    def apply_to_dataframe(self, df, col1, col2, result_col='distance'):
        """
        Apply the distance function to columns of a pandas DataFrame.
        
        Parameters:
        df (pandas.DataFrame): The DataFrame containing the points.
        col1 (str): The name of the first column containing the points.
        col2 (str): The name of the second column containing the points.
        result_col (str): The name of the column to store the computed distances.
        
        Returns:
        pandas.DataFrame: The DataFrame with an additional column containing the distances.
        """
        df[result_col] = df.apply(lambda row: self.calculate(row[col1], row[col2]), axis=1)
        return df
	
import pandas as pd
import numpy as np

class IntegratedDistance:
    def __init__(self, func=euclidean):
        """
        Initialize the IntegratedDistance class with a distance function.
        
        Parameters:
        func (callable): A function that takes two points and returns a distance. 
                         Default is Euclidean distance.
        """
        self.func = func

    def calculate(self, point1, point2):
        """
        Compute the distance between two points using the specified distance function.
        
        Parameters:
        point1, point2: The points between which to compute the distance. Can be tuples, lists, or numpy arrays.
        
        Returns:
        float: The computed distance.
        """
        return self.func(point1, point2)

    def apply_to_dataframe(self, df, col1, col2, result_col='distance'):
        """
        Apply the distance function to columns of a pandas DataFrame.
        
        Parameters:
        df (pandas.DataFrame): The DataFrame containing the points.
        col1 (str): The name of the first column containing the points.
        col2 (str): The name of the second column containing the points.
        result_col (str): The name of the column to store the computed distances.
        
        Returns:
        pandas.DataFrame: The DataFrame with an additional column containing the distances.
        """
        df[result_col] = df.apply(lambda row: self.calculate(row[col1], row[col2]), axis=1)
        return df

    def apply_to_sklearn(self, X, Y=None):
        """
        Apply the distance function within a scikit-learn pipeline.
        
        Parameters:
        X (numpy array or pandas DataFrame): The data for which to compute distances.
        Y (numpy array or pandas DataFrame, optional): Another data set to compare with.
        
        Returns:
        numpy.array: An array of computed distances.
        """
        if Y is None:
            Y = X
        
        distances = np.zeros((X.shape[0], Y.shape[0]))
        for i in range(X.shape[0]):
            for j in range(Y.shape[0]):
                distances[i, j] = self.calculate(X[i], Y[j])
                
        return distances

class DistanceMatrix:
    def __init__(self, data_points, metric=Euclidean()):
        """
        Initializes the DistanceMatrix class.

        Parameters:
        - data_points: List or array-like, a collection of data points where each point is an iterable of coordinates.
        - metric: str, the distance metric to be used (e.g., 'euclidean', 'cosine', 'manhattan'). The metric must be one of the predefined metrics in the `distancia` package.
        """
        self.data_points = data_points
        self.metric = metric
        self.distance_matrix = self._compute_distance_matrix()

    def _compute_distance_matrix(self):
        """
        Computes the distance matrix for the provided data points using the specified metric.

        Returns:
        - A 2D list representing the distance matrix where element (i, j) is the distance between data_points[i] and data_points[j].
        """
        num_points = len(self.data_points)
        matrix = [[0.0] * num_points for _ in range(num_points)]

        for i in range(num_points):
            for j in range(i + 1, num_points):
                distance = self.metric.calculate(self.data_points[i], self.data_points[j])
                matrix[i][j] = distance
                matrix[j][i] = distance

        return matrix

    def get_matrix(self):
        """
        Returns the computed distance matrix.
        """
        return self.distance_matrix

import concurrent.futures
from functools import partial
import multiprocessing

class ParallelandDistributedComputation:
    def __init__(self, data_points, metric):
        """
        Initializes the ParallelDistanceCalculator with a set of data points and a distance metric.

        :param data_points: A list or array of data points.
        :param metric: A callable that computes the distance between two data points.
        """
        self.data_points = data_points
        self.metric = metric

    def compute_distances_parallel(self, reference_point=None, max_workers=None, use_multiprocessing=False):
        """
        Computes distances in parallel between the reference point and all data points or pairwise among all data points.

        :param reference_point: A single data point to compare with all other data points. 
                                If None, computes pairwise distances among all data points.
        :param max_workers: The maximum number of workers to use for parallel computation.
                            If None, it will use the number of processors on the machine.
        :param use_multiprocessing: If True, uses multiprocessing for parallel computation.
                                    If False, uses multithreading.
        :return: A list of computed distances.
        """
        if reference_point is not None:
            compute_func = partial(self.metric.calculate, reference_point)
            data_iterable = self.data_points
        else:
            data_iterable = ((self.data_points[i], self.data_points[j]) for i in range(len(self.data_points)) for j in range(i + 1, len(self.data_points)))
            compute_func = lambda pair: self.metric.calculate(*pair)

        if use_multiprocessing:
            with multiprocessing.Pool(processes=max_workers) as pool:
                distances = pool.map(compute_func, data_iterable)
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                distances = list(executor.map(compute_func, data_iterable))

        return distances

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
import pandas as pd

from collections import defaultdict

class OutlierDetection:
    def __init__(self, data_points, metric=Euclidean(), threshold=2.0):
        """
        Initialize the OutlierDetection class.

        :param data_points: A list of data points, where each data point is a list or tuple of numeric values.
        :param metric: The distance metric to use for outlier detection. Supported metrics: 'euclidean', 'manhattan', 'mahalanobis'.
        :param threshold: The threshold value for determining outliers. Points with distances greater than this threshold times the standard deviation from the centroid are considered outliers.
        """
        self.data_points = data_points
        self.metric = metric
        self.threshold = threshold
        self.centroid = self._calculate_centroid()
        self.distances = self._calculate_distances()

    def _calculate_centroid(self):
        """
        Calculate the centroid of the data points.

        :return: The centroid as a list of numeric values.
        """
        n = len(self.data_points)
        centroid = [sum(dim)/n for dim in zip(*self.data_points)]
        return centroid

    def _calculate_distances(self):
        """
        Calculate the distances of all points from the centroid using the specified metric.

        :return: A list of distances as floats.
        """
        distances = []
        for point in self.data_points:
            distance = self.metric.calculate(point, self.centroid)
            distances.append(distance)
        return distances

    def detect_outliers(self):
        """
        Detect outliers based on the distance from the centroid.

        :return: A list of outliers, where each outlier is a tuple containing the point and its distance from the centroid.
        """
        mean_distance = sum(self.distances) / len(self.distances)
        std_distance = (sum((d - mean_distance) ** 2 for d in self.distances) / len(self.distances))**0.5

        outliers = []
        for i, distance in enumerate(self.distances):
            if distance > mean_distance + self.threshold * std_distance:
                outliers.append((self.data_points[i], distance))

        return outliers


    
class BatchDistance:
    def __init__(self, points_a, points_b, metric):
        """
        Initialize the BatchDistance class with two sets of points and a distance metric.

        :param points_a: A list of tuples representing the first set of points.
        :param points_b: A list of tuples representing the second set of points.
        :param metric: A string representing the distance metric to be used ('euclidean', 'manhattan', etc.).
        """
        self.points_a = points_a
        self.points_b = points_b
        self.metric = metric

    def compute_batch(self):
        """
        Compute the distances for all pairs in the two sets of points.

        :return: A list of distances for each pair of points.
        """
        if len(self.points_a) != len(self.points_b):
            raise ValueError("The two point sets must have the same length.")

        distances = []
        for point1, point2 in zip(self.points_a, self.points_b):
            distance = self.metric.calculate(point1, point2)
            distances.append(distance)

        return distances


import time

class ComprehensiveBenchmarking:
    def __init__(self, metrics, data, repeat=1):
        """
        Initialize the ComprehensiveBenchmarking class.

        :param metrics: List of metric functions to benchmark.
        :param data: The data points to use in the benchmarking.
        :param repeat: Number of times to repeat each metric calculation for averaging.
        """
        self.metrics = metrics
        self.data    = data
        self.repeat  = repeat
        self.results = {}

    def run_benchmark(self):
        """
        Run the benchmark for each metric on the provided data.

        :return: Dictionary with metrics as keys and their average computation time as values.
        """
        for metric in self.metrics:
            start_time = time.time()
            for _ in range(self.repeat):
                _ = [metric.calculate(x, y) for x, y in self.data]
            end_time = time.time()
            average_time = (end_time - start_time) / self.repeat
            self.results[metric.__class__.__name__] = average_time

        return self.results

    def print_results(self):
        """
        Print the benchmarking results in a readable format.
        """
        for metric, time_taken in self.results.items():
            print(f"Metric: {metric}, Average Time: {time_taken:.6f} seconds")


class DistanceMetricLearning:
    def __init__(self, data, labels, method='lmnn', **kwargs):
        """
        Initialize the DistanceMetricLearning class.

        Parameters:
        - data: array-like, shape (n_samples, n_features)
            The input data points.
        - labels: array-like, shape (n_samples,)
            The class labels or targets associated with the data points.
        - method: str, optional (default='lmnn')
            The distance metric learning method to use. Options are 'lmnn', 'itml', 'nca', etc.
        - kwargs: additional keyword arguments specific to the chosen method.
        """
        self.data = data
        self.labels = labels
        self.method = method.lower()
        self.kwargs = kwargs
        self.metric = None

    def fit(self):
        """
        Fit the distance metric to the data using the specified method.
        """
        if self.method == 'lmnn':
            self.metric = self._learn_lmnn()
        elif self.method == 'itml':
            self.metric = self._learn_itml()
        elif self.method == 'nca':
            self.metric = self._learn_nca()
        else:
            raise ValueError(f"Method {self.method} is not supported.")
    
    def transform(self, X):
        """
        Transform the data using the learned metric.

        Parameters:
        - X: array-like, shape (n_samples, n_features)
            The data to transform.

        Returns:
        - X_transformed: array-like, shape (n_samples, n_features)
            The data transformed using the learned metric.
        """
        if self.metric is None:
            raise ValueError("The model needs to be fitted before transformation.")
        return self.metric.transform(X)
    
    def _learn_lmnn(self):
        # Placeholder function for learning LMNN
        # In practice, you would use a library like metric-learn, or implement LMNN from scratch.
        from metric_learn import LMNN
        lmnn = LMNN(**self.kwargs)
        lmnn.fit(self.data, self.labels)
        return lmnn

    def _learn_itml(self):
        # Placeholder function for learning ITML
        from metric_learn import ITML
        itml = ITML(**self.kwargs)
        itml.fit(self.data, self.labels)
        return itml

    def _learn_nca(self):
        # Placeholder function for learning NCA
        from sklearn.neighbors import NeighborhoodComponentsAnalysis
        nca = NeighborhoodComponentsAnalysis(**self.kwargs)
        nca.fit(self.data, self.labels)
        return nca

    def get_metric(self):
        """
        Get the learned metric.
        
        Returns:
        - metric: the learned metric object
        """
        if self.metric is None:
            raise ValueError("The model needs to be fitted before accessing the metric.")
        return self.metric

class MetricFinder:
	def __init__(self):
		"""
		Initialize the MetricFinder class.
		"""
		self.list_metric=[]

	def find_metric(self, point1, point2):
		"""
		Determines the most appropriate metric for the given points based on their structure.

		Parameters:
		point1: The first point (can be a list, string, or other iterable).
		point2: The second point (can be a list, string, or other iterable).

		Returns:
		str: The name of the most appropriate metric.
		"""
		if isinstance(point1, str) and isinstance(point2, str):self.find_string_metric(point1, point2)
		elif isinstance(point1, (list)) and isinstance(point2, (list)):
			self.list_metric.append(LongestCommonSubsequence().__class__.__name__)

			if all(isinstance(x, (tuple)) for x in point1) and all(isinstance(x, (tuple)) for x in point2):
				self.list_metric.append(Frechet().__class__.__name__)

			if all(isinstance(x, (float,int)) for x in point1) and all(isinstance(x, (float,int)) for x in point2):
				if len(point1)==len(point2):
					self.list_metric.append(Euclidean().__class__.__name__)
					self.list_metric.append(Manhattan().__class__.__name__)
					self.list_metric.append(Minkowski().__class__.__name__)
					self.list_metric.append(L1().__class__.__name__)
					self.list_metric.append(L2().__class__.__name__)
					self.list_metric.append(Canberra().__class__.__name__)
					self.list_metric.append(BrayCurtis().__class__.__name__)
					self.list_metric.append(Gower().__class__.__name__)
					self.list_metric.append(Pearson().__class__.__name__)
					self.list_metric.append(Spearman().__class__.__name__)
					self.list_metric.append(CzekanowskiDice().__class__.__name__)
					self.list_metric.append(MotzkinStraus().__class__.__name__)
					self.list_metric.append(EnhancedRogersTanimoto().__class__.__name__)
					self.list_metric.append(DynamicTimeWarping().__class__.__name__)
					self.list_metric.append(CosineInverse().__class__.__name__)
					self.list_metric.append(CosineSimilarity().__class__.__name__)
					self.list_metric.append(GeneralizedJaccard().__class__.__name__)
					self.list_metric.append(Chebyshev().__class__.__name__)
					

			if all(isinstance(x, (int)) for x in point1) and all(isinstance(x, (int)) for x in point2):
					self.list_metric.append(KendallTau().__class__.__name__)
					
			if all(check_bin(x) for x in point1) and all(check_bin(x) for x in point2) and len(point1)==len(point2):
					self.list_metric.append(Kulsinski().__class__.__name__)
					self.list_metric.append(Yule().__class__.__name__)
					self.list_metric.append(RogersTanimoto().__class__.__name__)
					self.list_metric.append(SokalMichener().__class__.__name__)
					self.list_metric.append(SokalSneath().__class__.__name__)
			if all(check_probability(x) for x in point1) and all(check_probability(x) for x in point2) and len(point1)==len(point2):
					self.list_metric.append(CrossEntropy().__class__.__name__)
					self.list_metric.append(MeanAbsoluteError().__class__.__name__)
					self.list_metric.append(MAE().__class__.__name__)
					self.list_metric.append(MeanAbsolutePercentageError().__class__.__name__)
					self.list_metric.append(MAPE().__class__.__name__)
					self.list_metric.append(MeanSquaredError().__class__.__name__)
					self.list_metric.append(MSE().__class__.__name__)
					self.list_metric.append(SquaredLogarithmicError().__class__.__name__)
					self.list_metric.append(SLE().__class__.__name__)
					self.list_metric.append(KullbackLeibler().__class__.__name__)
					self.list_metric.append(Bhattacharyya().__class__.__name__)
					self.list_metric.append(Hellinger().__class__.__name__)
					self.list_metric.append(Wasserstein().__class__.__name__)
		elif isinstance(point1, (set)) and isinstance(point2, (set)):
				if all(isinstance(x, (float,int)) for x in point1) and all(isinstance(x, (float,int)) for x in point2):
					self.list_metric.append(InverseTanimoto().__class__.__name__)
					self.list_metric.append(Tanimoto().__class__.__name__)
					self.list_metric.append(Dice().__class__.__name__)
					self.list_metric.append(Kulsinski().__class__.__name__)
					self.list_metric.append(Tversky().__class__.__name__)
					self.list_metric.append(FagerMcGowan().__class__.__name__)
					self.list_metric.append(FagerMcGowan().__class__.__name__)
					self.list_metric.append(Hausdorff().__class__.__name__)
				if all(isinstance(x, (bool)) for x in point1) and all(isinstance(x, (bool)) for x in point2):
					self.list_metric.append(Ochiai().__class__.__name__)

		return self.list_metric

	def find_string_metric(self, str1, str2):
		"""
		Determines the appropriate string-based metric.

		Parameters:
		str1: The first string.
		str2: The second string.

		Returns:
		str: The name of the most appropriate string metric.
		"""
		if len(str1) == len(str2):
			if str1.isdigit() and str2.isdigit():
				self.list_metric.append(Hamming().__class__.__name__)
				self.list_metric.append(Matching().__class__.__name__)
				
		self.list_metric.append(Jaro().__class__.__name__)
		self.list_metric.append(JaroWinkler().__class__.__name__)
		self.list_metric.append(Levenshtein().__class__.__name__)
		self.list_metric.append(DamerauLevenshtein().__class__.__name__)
		self.list_metric.append(RatcliffObershelp().__class__.__name__)
		self.list_metric.append(SorensenDice().__class__.__name__)
		self.list_metric.append(Otsuka().__class__.__name__)
		



	def find_similarity_metric(self, point1, point2):
		"""
		Determines the most appropriate similarity metric for the given points.

		Parameters:
		point1: The first point (can be a list, string, or other iterable).
		point2: The second point (can be a list, string, or other iterable).

		Returns:
		str: The name of the most appropriate similarity metric.
		"""
		if isinstance(point1, str) and isinstance(point2, str):
			return "Jaccard Similarity"
		elif isinstance(point1, (list, tuple)) and isinstance(point2, (list, tuple)):
			if all(isinstance(x, (int, float)) for x in point1) and all(isinstance(x, (int, float)) for x in point2):
				return "Cosine Similarity"
		return "Unknown Similarity Metric"



import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class APICompatibility:
    def __init__(self, distance_metric):
        """
        Initialize with a specific distance metric.
        
        :param distance_metric: A function or class from the distancia package, e.g., EuclideanDistance
        """
        self.distance_metric = distance_metric
    
    def rest_endpoint(self, host="0.0.0.0", port=5000):
        """
        Set up a REST API endpoint using Flask.
        
        :param host: Host IP address for the REST service.
        :param port: Port number for the REST service.
        """
        @app.route('/calculate_distance', methods=['POST'])
        def calculate_distance():
            data = request.json
            point1 = data['point1']
            point2 = data['point2']
            distance = self.distance_metric(point1, point2)
            return jsonify({"distance": distance})

        app.run(host=host, port=port)




import numpy as np

class AutomatedDistanceMetricSelection:
    def __init__(self, metrics=None):
        """
        Initialize the selector with a list of potential distance metrics.
        
        :param metrics: List of distance metric classes or functions to choose from.
        """
        if metrics is None:
            self.metrics = [
                Euclidean(),
                CosineSimilarity(),
                Manhattan(),
                Jaccard(),
                Mahalanobis(),
                DynamicTimeWarping(),
                Frechet(),
                # Add other metrics as needed
            ]
        else:
            self.metrics = metrics
    
    def select_metric(self, data):
        """
        Automatically select the best distance metric based on data characteristics.
        
        :param data: The data to analyze (e.g., a numpy array or pandas DataFrame).
        :return: The selected distance metric class/function.
        """
        # Example heuristic based on data characteristics
        if self.is_high_dimensional(data):
            return CosineSimilarity()
        elif self.is_binary_data(data):
            return Jaccard()
        elif self.has_outliers(data):
            return Manhattan()
        elif self.is_time_series(data):
            return DynamicTimeWarping()
        else:
            # Default choice if no specific conditions are met
            return Euclidean()

    def is_high_dimensional(self, data):
        """Heuristic: Check if the data is high-dimensional."""
        return data.shape[1] > 50

    def is_binary_data(self, data):
        """Heuristic: Check if the data consists of binary values."""
        return np.array_equal(data, data.astype(bool))

    def has_outliers(self, data):
        """Heuristic: Check if the data has significant outliers."""
        q1, q3 = np.percentile(data, [25, 75], axis=0)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return np.any((data < lower_bound) | (data > upper_bound))

    def is_time_series(self, data):
        """Heuristic: Check if the data is time-series data."""
        # Simple heuristic: time series often have more rows than columns
        return data.shape[0] > data.shape[1]



