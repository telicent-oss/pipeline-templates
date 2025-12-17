# Here you can build out either your IDH or EDH security labels
from telicent_labels import SecurityLabelBuilder, TelicentSecurityLabelsV2, IDHModel
import uuid
from datetime import UTC, datetime


# Information Data Header is a simpler model to specify security access
# BUT, currently does not support OR Groups. Use TelicentSecurityLabelsV2 for that
def create_security_label_using_TelicentSCV2():
    label = SecurityLabelBuilder()
    label.add(
        TelicentSecurityLabelsV2.CLASSIFICATION.value,
        "O",  # TODO: can either be "O", "OS", "S", "TS"
    )
    # .add() is used cases where there is only one allowed value this label dimension
    label.add(
        TelicentSecurityLabelsV2.PERMITTED_NATIONALITIES.value,
        "GBR", # TODO: list of allowed nationalities using ISO3166-1 alpha-3 country code strings (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)
    )
    # .add_multiple() is used to add more than one possible value for this label dimension
    label.add_multiple(
        TelicentSecurityLabelsV2.PERMITTED_ORGANISATIONS.value, 
        "replace-with-your-allowed-org", # TODO: strings representing orgs that can access the data
        "replace-with-another-allowed-org-if-required"
    )
    # TODO: list of strings representing custom AND access group. Remove if not required
    label.add( 
        TelicentSecurityLabelsV2.AND_GROUPS.value,
        "replace-with-allowed-and-group-if-required"
    )
    # TODO: list of strings representing custom OR access groups. Remove if not required
    label.add_multiple(
        TelicentSecurityLabelsV2.OR_GROUPS.value,
        "replace-with-allowed-or-group-if-required",      
        "replace-with-another-allowed-or-group-if-required",                        
    )
    return label.build()


# Information Data Header is a simpler modal to specify security access
# BUT, currently does not support OR Groups. Use TelicentSecurityLabelsV2 for that
def create_security_label_using_idh():
    idh = {
        "apiVersion": "v1alpha",
        "uuid": str(uuid.uuid4()),
        "createDate": datetime.now(UTC).isoformat(),
        "containsPii": False,
        "dataSource": "replace-with-your-data-source", # TODO: string to articulate source of data
        "access": {
            "classification": "O", # TODO: can either be "O", "OS", "S", "TS"
            "allowedOrgs": ["replace-with-your-allowed-org"], # TODO: list of strings representing orgs that can access the data
            "allowedNats": ["GBR"], # TODO: list of allowed nationalities using ISO3166-1 alpha-3 country code strings (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) 
            "groups": [], # TODO: list of strings representing custom AND access groups
        },
        "ownership": {"originatingOrg": "replace-with-your-data-owner"}, # TODO: string to articulate owner of data
    }
    security_label = IDHModel(**idh).build_security_labels()
    return security_label
