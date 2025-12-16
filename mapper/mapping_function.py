import ies_tool.ies_tool as ies

# add your mapping/enrichments/resolving in here
def map_func(item):
    """
    TODO: replace with logic associated to some sort of 
    transformation you want to make to the source data
    e.g. cleansing, enrichment, resolving and/or mapping
    For mapping to knowledge, this is where your code
    to create RDF goes.
    """
    # TODO add your logic here
    mapped_item = item # currently feed back the source item as the mapped item
    return mapped_item

# this section can be used to conduct local testing of the mapping_function by just running this file.
if __name__ == "__main__":

    test_data = ""
    mapped_data = map_func(test_data)
    print(mapped_data)
