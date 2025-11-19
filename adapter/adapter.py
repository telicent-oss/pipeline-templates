from telicent_lib.sinks import KafkaSink
from telicent_lib import AutomaticAdapter, Record, RecordUtils, SimpleDataSet
from telicent_lib.config import Configurator
from dotenv import load_dotenv
from typing import Iterable
from adapter.labels import create_security_label_using_TelicentSCV2

# Adapter Configuration
load_dotenv()
config = Configurator()
BROKER = config.get("BOOTSTRAP_SERVERS", required = True)
TARGET_TOPIC = config.get(
    "TARGET_TOPIC", required=True,
    description="Specifies the Kafka topic the adaptor pushes its output to",
)
ADAPTER_NAME = config.get(
    "ADAPTER_NAME", required=True, 
    description="Specifies the name of the adapter"
)
security_label = create_security_label_using_TelicentSCV2()

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


# process data and 
def generate_records_from_source() -> Iterable[Record]:
    """
    TODO: replace with logic associated to sourcing and preparing
    your data for ingest. This could be getting data from a file
    or getting data from an external system or API
    """
    file_path = './adapter/sanctioned_individuals.csv'
    with open(file_path) as file:
        csv_content = file.read()
        yield create_core_record(
            data=csv_content,
            security_label=security_label
        )

# Create a sink and adapter
target = KafkaSink(topic = TARGET_TOPIC)
dataset = SimpleDataSet(
    dataset_id='sanctions',
    title='sanctioned_individuals.csv',
    source_mime_type='text/csv'
)

adapter = AutomaticAdapter(
    name=ADAPTER_NAME,
    target=target, 
    adapter_function=generate_records_from_source, 
    dataset=dataset
)

# Call run() to run the adapter
adapter.run()