from __future__ import annotations
from telicent_lib.sinks import KafkaSink
from telicent_lib.sources import KafkaSource
from telicent_lib.config import Configurator
from telicent_lib import Mapper, Record, RecordUtils
from dotenv import load_dotenv
from mapping_function import map_func


load_dotenv()
# Mapper Configuration
config = Configurator()
BROKER = config.get("BOOTSTRAP_SERVERS", required = True)
SOURCE_TOPIC = config.get("SOURCE_TOPIC", required=True,
                    description="Specifies the Kafka topic the mapper ingests from.")
TARGET_TOPIC = config.get("TARGET_TOPIC", required=True,
                    description="Specifies the Kafka topic the mapper pushes its output to")

# Create a new set of headers based on the source headers
def get_headers(previous_headers):
    output = RecordUtils.to_headers(
        headers = {
            "Content-Type": "mime/type", #TODO: replace with MIME type of the data payload
                                         #TODO: is there are other headers you need to replace
                                         # e.g Security-Label, and then here. 
        },
        existing_headers = previous_headers 
    )
    return output

# Function each record on the source topic is passed to.
def mapping_function(record: Record) ->  Record | list[Record] | None:

    previous_headers = record.headers   # Header of source Record
    data = record.value                 # Value/Payload of source Record

    try:
        mapped_data = map_func(data) # this uses the function in mapping_function.py
        mapped_record = Record(
            get_headers(previous_headers),  # Header of the Record
            record.key,                     # Key of the Record
            mapped_data,                    # Value/Payload of the Record
        )
        return mapped_record
    except Exception as e :
        print("Error mapping object with exception {exp}".format(exp=e)) 

if __name__ == "__main__":

    source = KafkaSource(topic=SOURCE_TOPIC)
    target = KafkaSink(topic=TARGET_TOPIC)
    mapper = Mapper(
        source = source, 
        target = target, 
        map_function = mapping_function,
        name= f"{SOURCE_TOPIC} to {TARGET_TOPIC} Mapper"
    )
    mapper.run()