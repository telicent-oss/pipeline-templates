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
    tool = ies.IESTool(mode="rdflib", default_data_namespace=telicent_ns)

    csv = StringIO(item)
    df = pl.read_csv(csv)

    # Iterate through each row
    for row in df.to_dicts():
        first_name = row.get("first_name")
        surname = row.get("surname")
        dob = row.get("date_of_birth")
        passport_number = row.get("passport_number")
        person_id = row.get("unique_id")

        # 1 create a person, with given name, surname and date of birth
        person = ies.Person(tool=tool,
                            given_name=first_name,
                            date_of_birth = dob,
                            surname = surname,
                            uri=telicent_ns+person_id+"_person"
                            )
        
        # 2 add identifier
        person.add_identifier(passport_number)

        # 3 optional add nice display label with .add_telicent_primary_name()
        person.add_telicent_primary_name(f"Steve {surname}")

    return tool.graph.serialize(format="turtle")



