import numpy
from affinegap import normalizedAffineGapDistance as comparator

def getCentroid(attribute_variants, comparator, sort_values=None):
    """ 
    Takes in a list of attribute values for a field,
    evaluates the centroid using the comparator,
    & returns the centroid (i.e. the 'best' value for the field)
    """
    
    n = len(attribute_variants)
    
    distance_matrix = numpy.zeros([n,n])
    
    # populate distance matrix by looping through elements of matrix triangle
    for i in range (0,n):
        for j in range (0, i):
            distance = comparator(attribute_variants[i], attribute_variants[j])
            distance_matrix[i,j] = distance_matrix[j,i] = distance
    
    average_distance = distance_matrix.mean(0)
    
    # there can be ties for minimum, average distance string
    min_dist_indices = numpy.where(average_distance==average_distance.min())[0]
    if len(min_dist_indices) > 1:
        centroid = breakCentroidTie(attribute_variants, min_dist_indices, sort_values=sort_values)
    else :
        centroid_index = min_dist_indices[0]
        centroid = attribute_variants[centroid_index]

    return centroid    

def breakCentroidTie(attribute_variants, min_dist_indices, sort_values=None):
    """
    Finds centroid when there are multiple values w/ min avg distance 
    (e.g. any dupe cluster of 2) right now this selects the first among a set of 
    ties, but can be modified to break ties in strings by selecting the longest string
    """
    if sort_values:
        sort_values = map(float,sort_values)
        idx = numpy.argsort(numpy.array(sort_values)[min_dist_indices])[-1]
    else:
        idx = 0
    return attribute_variants[min_dist_indices[idx]]

def getCanonicalRep(record_cluster, sort_arg=None):
    """
    Given a list of records within a duplicate cluster, constructs a canonical representation
    of the cluster by finding canonical values for each field
    Sort_arg is a key which contains values for breaking ties 
    """
    canonical_rep = {}
    for key in record_cluster[0].keys():
        key_values = []
        sort_values = None
        if sort_arg:
            if key == sort_arg: continue 
            else: sort_values = []
        for record in record_cluster :
            # assume non-empty values always better than empty value for canonical record
            if record[key]:
                key_values.append(record[key])
                if sort_arg: sort_values.append(record[sort_arg])
        if key_values:
            # make sure to sort by numerics, not strings 
            canonical_rep[key] = getCentroid(key_values, comparator, sort_values=sort_values)
        else:
            canonical_rep[key] = ''
    
    return canonical_rep
