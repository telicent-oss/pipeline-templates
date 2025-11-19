# Use this to test the output of your mapping function
from rdflib import Graph
from mapper.mapping_function import map_func


file_path = './adapter/sanctioned_individuals.csv'

with open(file_path) as file:
    test_source_data = file.read()
    
# OPTIONAL:
# Use the below for testing RDF intended for the knowledge topic
# your mapped data will be serialised to .ttl/turtle file in the local directory
graph = Graph()
mapped_data = map_func(test_source_data)
graph.parse(data=mapped_data, format="turtle")
graph.serialize(destination="mapper/test_mapped_data.ttl", format="turtle")
