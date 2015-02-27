import unittest
import canonicalize.centroid

class CanonicalizationTest(unittest.TestCase) :

	def test_get_centroid(self) :
		from affinegap import normalizedAffineGapDistance as comparator
		attributeList = ['mary crane center', 'mary crane center north', 'mary crane league - mary crane - west', 'mary crane league mary crane center (east)', 'mary crane league mary crane center (north)', 'mary crane league mary crane center (west)', 'mary crane league - mary crane - east', 'mary crane family and day care center', 'mary crane west', 'mary crane center east', 'mary crane league mary crane center (east)', 'mary crane league mary crane center (north)', 'mary crane league mary crane center (west)', 'mary crane league', 'mary crane', 'mary crane east 0-3', 'mary crane north', 'mary crane north 0-3', 'mary crane league - mary crane - west', 'mary crane league - mary crane - north', 'mary crane league - mary crane - east', 'mary crane league - mary crane - west', 'mary crane league - mary crane - north', 'mary crane league - mary crane - east']
		centroid = canonicalize.centroid.getCentroid (attributeList, comparator)
		assert centroid == 'mary crane'

	def test_get_canonical_rep(self) :
		record_list = [ {"name": "mary crane", "address": "123 main st", "zip":"12345"}, 
					 		 {"name": "mary crane east", "address": "123 main street", "zip":""}, 
							 {"name": "mary crane west", "address": "123 man st", "zip":""} ]
		rep = canonicalize.centroid.getCanonicalRep(record_list)
		assert rep == {'name': 'mary crane', 'address': '123 main street', 'zip':"12345"}

		rep = canonicalize.centroid.getCanonicalRep(record_list[0:2])
		assert rep == {"name": "mary crane", "address": "123 main st", "zip":"12345"}

		rep = canonicalize.centroid.getCanonicalRep(record_list[0:1])
		assert rep == {"name": "mary crane", "address": "123 main st", "zip":"12345"}

	def test_get_centroid_with_sort_arg(self) :
		from affinegap import normalizedAffineGapDistance as comparator
		attributeList = ['mary crane center', 'mary crane east 1', 'mary crane east 2', 'mary crane east 3']
		sort_values = [2.5, 0.002, 97., 102.5]

		centroid_with_args = canonicalize.centroid.getCentroid (attributeList, comparator, sort_values)
		assert centroid_with_args == 'mary crane east 3'
		
		centroid_without_args = canonicalize.centroid.getCentroid (attributeList, comparator)
		assert centroid_without_args == 'mary crane east 1'

	def test_get_canonical_rep_with_sort_arg(self):
		record_list = [ {"name": "mary crane", "address": "123 main st", "zip":"12345", "score":"2"}, 
					 		 {"name": "mary crane east", "address": "123 main street", "zip":"", "score":"3"}, 
							 {"name": "mary crane west", "address": "123 man st", "zip":"", "score":"1"} ]
		
		rep_with_args = canonicalize.centroid.getCanonicalRep(record_list[0:2], sort_arg='score')
		assert rep_with_args == {'name': 'mary crane east', 'address': '123 main street', 'zip':"12345"}

		rep_without_args = canonicalize.centroid.getCanonicalRep(record_list[0:2])
		assert rep_without_args == {"name": "mary crane", "address": "123 main st", "zip":"12345", "score":"2"}

		rep = canonicalize.centroid.getCanonicalRep(record_list[0:1],sort_arg='score')
		assert rep == {"name": "mary crane", "address": "123 main st", "zip":"12345"}

if __name__ == "__main__":
	unittest.main()
