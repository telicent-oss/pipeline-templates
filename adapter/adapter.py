from telicent_lib.sinks import KafkaSink
from telicent_lib import AutomaticAdapter, Record, RecordUtils
from telicent_lib.config import Configurator
from dotenv import load_dotenv
from typing import Iterable


# Adapter Configuration
load_dotenv()
config = Configurator()
TARGET_TOPIC = config.get(
    "TARGET_TOPIC", required=True,
    description="Specifies the Kafka topic the adaptor pushes its output to",
)
ADAPTER_NAME = config.get(
    "ADAPTER_NAME", required=True, 
    description="Specifies the name of the adapter"
)

# Create a Telicent CORE record
def create_core_record(data, security_label):
    headers = RecordUtils.to_headers(
        {
            "Content-Type": "mine/type", #TODO: replace with MIME type of the data payload
            "Security-Label": security_label,
        }
    )
    return Record(
        headers,# Header of the Record
        None,   # Key of the Record
        data,   # Value/Payload of the Record
    )


# get data from some where and create CORE records. This is fed into the Adapter initialiser 
def generate_records_from_source() -> Iterable[Record]:
    """
    TODO: replace with logic associated to sourcing and preparing
    your data for ingest. This could be getting data from a file
    or getting data from an external system or API
    """
    
    # TODO add your logic here

    yield create_core_record(
        data = None,        # TODO: replace with the results of the above data sourcing
        security_label="*"  # TODO: * allows anyone access to this data, replace with better label
                            # see labels.py on how to create better label
    )


# Create a sink and adapter
target = KafkaSink(topic = TARGET_TOPIC)
adapter = AutomaticAdapter(
    name=ADAPTER_NAME,
    target=target, 
    adapter_function=generate_records_from_source, 
    distribution_id="my-data-distribution-id" # TODO: replace with your own. This is used for the data catalog
)

# Call run() to run the adapter
adapter.run()