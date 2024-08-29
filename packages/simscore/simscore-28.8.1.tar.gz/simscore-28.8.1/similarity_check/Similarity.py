

class Similarity:
    """
    The class provides various similarity and dissimilarity methods including jaccard_coefficient,overlap_coefficient and hamming_distance
    Attributes:
    ----------
        str1 :str
            The first attribute for comparison. This can be any string that will be converted into a set.
        str2 :str
            The second attribute for comparison. This can be any string that will be converted into a set.
     Methods
    -------
     jaccard_coefficient( str1, str2)
        Calculates the Jaccard similarity coefficient between two sets.

    overlap_coefficient(str1, str2)
        Calculates the Overlap coefficient between two  sets.

    hamming_distance(str1, str2)
        Calculates the Hamming distance between two strings.

    """

    def __init__(self):
        """
              Initializes the Similarity object.
        """
        return
    def jaccard_coefficient(self, str1, str2):
        """
                Computes the Jaccard similarity coefficient between two sets.

                The Jaccard coefficient is defined as the size of the intersection
                divided by the size of the union of the sets.

                Parameters
                ----------
                str1 : str
                    The first string, which will be converted to a set.
                str2 : str
                    The second string, which will be converted to a set.

                Returns
                -------
                float
                    The Jaccard similarity coefficient. Returns 0 if both sets are empty
       """
        set1=set(str1)
        set2=set(str2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0
    def overlap_coefficient(self, str1, str2):
        """
         Computes the Overlap coefficient between two sets.

        The Overlap coefficient is defined as the size of the intersection
        divided by the size of the smaller set.

        Parameters
        ----------
        str1 : str
            The first string, which will be converted to a set.
        str2 : str
            The second string, which will be converted to a set.

        Returns
        -------
        float
            The Overlap coefficient. Returns 0 if either set is empty.
        """

        set1=set(str1)
        set2=set(str2)
        intersection = len(set1.intersection(set2))
        smaller_set_size = min(len(set1), len(set2))
        return intersection / smaller_set_size if smaller_set_size > 0 else 0
    def hamming_distance(self,str1, str2):
        """
                Computes the Hamming distance between two strings.

                The Hamming distance is defined as the number of positions at which
                the corresponding symbols in two strings of equal length are different.

                Parameters
                ----------
                str1 : str
                    The first string for comparison.
                str2 : str
                   The second string for comparison.

                Returns
                -------
                int
                    The Hamming distance between the two strings.Returns -1 if the strings have different lengths.
        """
        if len(str1) != len(str2):
            return -1
        distance = sum(el1 != el2 for el1, el2 in zip(str1, str2))
        return distance
    help(hamming_distance)

