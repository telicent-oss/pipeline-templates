from __future__ import annotations
from telicent_lib.sinks import KafkaSink
from telicent_lib.sources import KafkaSource
from telicent_lib.config import Configurator
from telicent_lib import Mapper, Record, RecordUtils
from json import loads
from dotenv import load_dotenv
from mapper.mapping_function import map_func
# from telicent_lib.logging import CoreLoggerFactory
# from logging import StreamHandler

load_dotenv()
# Mapper Configuration
config = Configurator()
broker = config.get("BOOTSTRAP_SERVERS", required = True)
source_topic = config.get("SOURCE_TOPIC", required=True,
                    description="Specifies the Kafka topic the mapper ingests from.")
target_topic = config.get("TARGET_TOPIC", required=True,
                    description="Specifies the Kafka topic the mapper pushes its output to")


# logger = CoreLoggerFactory.get_logger(__name__)
# logger.logger.addHandler(StreamHandler())

def get_headers(previous_headers):
    output = RecordUtils.to_headers(
        headers = {
            {{add_any_header_additions_or_overides}}
        },
        existing_headers = previous_headers
    )
    return output

# Function each record on the source topic is passed to.
def mapping_function(record: Record) ->  Record | list[Record] | None:

    data = loads(record.value)
    previous_headers = record.headers

    try:
        mapped = map_func(data)
        mapped_record = Record(
            get_headers(previous_headers), 
            record.key, 
            mapped, 
            None
        )
        return mapped_record
    except Exception as e :
        print("Error mapping object with exception {exp}".format(exp=e)) 

source = KafkaSource(topic=source_topic)
target = KafkaSink(topic=target_topic)
mapper = Mapper(
    source = source, 
    target = target, 
    map_function = mapping_function,
    name= f"{source} to {target} Mapper"
)
mapper.run()