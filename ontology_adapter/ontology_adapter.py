from telicent_lib.sinks import KafkaSink
from telicent_lib import AutomaticAdapter, Record, RecordUtils
from telicent_lib.config import Configurator
from dotenv import load_dotenv
import json

# Mapper Configuration
load_dotenv()
config = Configurator()
BROKER = config.get("BOOTSTRAP_SERVERS", required = True)
TARGET_TOPIC = config.get(
    "TARGET_TOPIC",
    required=True,
    description="Specifies the Kafka topic the adaptor pushes its output to",
)
ADAPTER_NAME = config.get(
    "ADAPTER_NAME", required=True, description="Specifies the name of the adapter"
)
SOURCE_NAME = config.get(
    "SOURCE_NAME",
    required=True,
    description="Specifies the source that the data has originated from",
)
ONTOLOGY_FILE_PATH = config.get(
    "ONTOLOGY_FILE_PATH",
    required=True,
    description="Specifies path for the ontology rdf file",
)
ONTOLOGY_STYLES_FILE_PATH = config.get(
    "ONTOLOGY_STYLES_FILE_PATH",
    required=True,
    description="Specifies path for the ontology styles json file",
)



def create_record(data):
    return Record(
        RecordUtils.to_headers(
            {
                "Content-Type": "text/turtle", # modify if you decide to use a different RDF serialisation for your ontology file
                "Data-Source": ONTOLOGY_FILE_PATH,
                "Data-Producer": ADAPTER_NAME,
                "Security-Label": "*" 
            }
        ),
        None,
        data,
    )

def convert_into_core_style_structure(style_record):
    core_style = {
        "defaultStyles": {
            "dark": {
                "backgroundColor": style_record["dark"],
                "color": style_record["light"]
            },
            "light": {
                "backgroundColor": style_record["dark"],
                "color": style_record["light"]
            },
            "shape": style_record["shape"],
            "borderRadius": "5px",
            "borderWidth": "2px",
            "selectedBorderWidth": "3px"
            },
            "defaultIcons": {
                "riIcon": "ri-meteor-line",
                "faIcon": style_record["faIcon"],
                "faUnicode": f"{style_record['faUnicode']}",
                "faClass": style_record["faClass"]
            }
        }
    return json.dumps(core_style).replace('"', '\\"')

def generate_ontology_and_styles_records():
        # first we push the ontology schema to CORE
        with open(ONTOLOGY_FILE_PATH, "r", encoding="utf-8") as file:
            file_content = file.read()
            yield create_record(file_content)
        # then we push each ontology style as a triple. A record per triple.
        style_file_path = ONTOLOGY_STYLES_FILE_PATH
        with open(style_file_path) as f:
            styles = json.load(f)
        for uri in styles:
            style_string = convert_into_core_style_structure(styles[uri])
            yield create_record(
                data= f'<{uri}> <http://telicent.io/ontology/style> "{style_string}" .'
            )

if __name__ == "__main__":

    # Create a sink and  adapter
    sink = KafkaSink(topic = TARGET_TOPIC)
    adapter = AutomaticAdapter(
        target=sink, 
        adapter_function=generate_ontology_and_styles_records, 
        name=ADAPTER_NAME, 
    )

    # Call run() to run the action
    adapter.run()

    