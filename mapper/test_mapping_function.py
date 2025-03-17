# Use this to test the output of your mapping function
from rdflib import Graph
from mapping_function import map_func


test_source_data = "your-test-source-data" #TODO replace with representative source data e.g. json, csv etc.
test_mapped_data = map_func(test_source_data)
print(test_mapped_data)

# OPTIONAL:
# Use the below for testing RDF intended for the knowledge topic
# your mapped data will be serialised to .ttl/turtle file in the local directory
# graph = Graph()
# graph_string = map_func(test_item)
# graph.parse(data=graph_string, format="turtle")
# graph.serialize(destination="test_mapped_data.ttl", format="turtle")