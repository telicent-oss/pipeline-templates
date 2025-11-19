import ies_tool.ies_tool as ies
from io import StringIO
import polars as pl


def map_func(item):
    """
    TODO: replace with logic associated to some sort of 
    transformation you want to make to the source data
    e.g. cleansing, enrichment, resolving and/or mapping
    For mapping to knowledge, this is where your code
    to create RDF goes.
    """
    telicent_ns = "http://telicent.io/data#"
    csv = StringIO(item)
    df = pl.read_csv(csv)
    tool = ies.IESTool(mode="rdflib", default_data_namespace=telicent_ns)

    # Iterate through each row
    for row in df.to_dicts():
        # 1 create a person, with given name, surname and date of birth
        person_id = row.get("unique_id")
        first_name = row.get("first_name")
        person = ies.Person(
            tool=tool,
            uri=telicent_ns+person_id,
            given_name=first_name
        )

        # 2 add identifier
        #person.add_identifier 

        # 3 optional add nice display label with .add_telicent_primary_name()


    return tool.graph.serialize(format="turtle")






