from CyberSource import *
from pathlib import Path
import os
import json
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def remove_from_history(id):
    riskInformationMarkingDetailsNotes = "Adding this transaction as suspect"
    riskInformationMarkingDetailsReason = "suspected"
    riskInformationMarkingDetailsAction = "hide"
    riskInformationMarkingDetails = Riskv1decisionsidmarkingRiskInformationMarkingDetails(
        notes = riskInformationMarkingDetailsNotes,
        reason = riskInformationMarkingDetailsReason,
        action = riskInformationMarkingDetailsAction
    )

    riskInformation = Riskv1decisionsidmarkingRiskInformation(
        marking_details = riskInformationMarkingDetails.__dict__
    )

    requestObj = FraudMarkingActionRequest(
        risk_information = riskInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)


    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = DecisionManagerApi(client_config)
        return_data, status, body = api_instance.fraud_update(id, requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling DecisionManagerApi->fraud_update: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    id = "5825489395116729903003"

    remove_from_history(id)
