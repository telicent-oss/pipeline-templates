from telicent_lib.sinks import KafkaSink
from telicent_lib import AutomaticAdapter, Record, RecordUtils
from telicent_lib.config import Configurator
from dotenv import load_dotenv
from typing import Iterable
import csv
import json
# uncomment below line if you want to use your own labels - see labels.py
# from adapter.labels import create_security_label_using_idh, create_security_label_using_TelicentSCV2

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

security_label = "*" 
file_path = "data/sanctioned_individuals.csv"

# Create a Telicent CORE record
def create_core_record(data, security_label):
    headers = RecordUtils.to_headers(
        {
            "Content-Type": "text/csv", 
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

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Send each row as JSON
            data = json.dumps(row).encode('utf-8')
    

            yield create_core_record(
                data = data,        
                security_label=security_label
                                    
            )


# Create a sink and adapter
target = KafkaSink(topic = TARGET_TOPIC)
adapter = AutomaticAdapter(
    name=ADAPTER_NAME,
    target=target, 
    adapter_function=generate_records_from_source, 
)

# Call run() to run the adapter
adapter.run()