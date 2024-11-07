from rdflib import Graph

from mapper.mapping_function import map_func


test_item =  {{some_test_data}}

graph = Graph()
graph_string = map_func(test_item)
graph.parse(data=graph_string, format="turtle")
graph.serialize(destination={{some_output_path}}, format="turtle")