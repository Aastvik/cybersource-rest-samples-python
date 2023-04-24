from CyberSource import *
from pathlib import Path
import os
import json
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

process_payment_path = os.path.join(os.getcwd(), "samples", "Payments", "Payments", "service-fees-with-credit-card-transaction.py")
process_payment = SourceFileLoader("module.name", process_payment_path).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def service_fees_authorization_reversal():
    

    clientReferenceInformationCode = "TC50171_3"
    clientReferenceInformation = Ptsv2paymentsidreversalsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    reversalInformationAmountDetailsTotalAmount = "2325.00"
    reversalInformationAmountDetails = Ptsv2paymentsidreversalsReversalInformationAmountDetails(
        total_amount = reversalInformationAmountDetailsTotalAmount
    )

    reversalInformationReason = "34"
    reversalInformation = Ptsv2paymentsidreversalsReversalInformation(
        amount_details = reversalInformationAmountDetails.__dict__,
        reason = reversalInformationReason
    )

    requestObj = AuthReversalRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        reversal_information = reversalInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)


    try:
        api_payment_response = process_payment.service_fees_with_credit_card_transaction(False)
        id = api_payment_response.id
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = ReversalApi(client_config)
        return_data, status, body = api_instance.auth_reversal(id, requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling ReversalApi->auth_reversal: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    service_fees_authorization_reversal()
