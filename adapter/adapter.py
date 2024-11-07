from telicent_lib.sinks import KafkaSink
from telicent_lib import AutomaticAdapter, Record, RecordUtils
from telicent_lib.config import Configurator
import json
from dotenv import load_dotenv
from typing import Iterable
# from telicent_lib.logging import CoreLoggerFactory
# from logging import StreamHandler


# Mapper Configuration
load_dotenv()
config = Configurator()
broker = config.get("BOOTSTRAP_SERVERS", required = True)
target_topic = config.get(
    "TARGET_TOPIC",
    required=True,
    description="Specifies the Kafka topic the adaptor pushes its output to",
)
name = config.get(
    "PRODUCER_NAME", required=True, description="Specifies the name of the producer"
)
source_name = config.get(
    "SOURCE_NAME",
    required=True,
    description="Specifies the source that the data has originated from",
)

# logger = CoreLoggerFactory.get_logger(__name__)
# logger.logger.addHandler(StreamHandler())

# Create and process records
def create_record(data, security_labels):
    return Record(
        RecordUtils.to_headers(
            {
                "Content-Type": {{add_content_type}},
                "Data-Source": source_name,
                "Data-Producer": name,
                "Security-Label": security_labels,
            }
        ),
        None,
        data,
    )

def generate_records() -> Iterable[Record]:
    # add logic associated to the data you are ingested
    # this could be getting data from a file
    # or getting data from an external system or API
    yield create_record({{some_data}}, {{a_security_label}})


# Create a sink and adapter
sink = KafkaSink(topic = target_topic)
adapter = AutomaticAdapter(
    target=sink, 
    adapter_function=generate_records, 
    name=name, 
)

# Call run() to run the action
adapter.run()