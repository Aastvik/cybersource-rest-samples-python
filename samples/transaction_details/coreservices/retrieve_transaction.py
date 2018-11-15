from CyberSource import *
import os
from importlib.machinery import SourceFileLoader
config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()


def transaction_details():
    try:
        config_obj = configuration.Configuration()
        details_dict1 = config_obj.get_configuration()
        transction_details_obj = TransactionDetailsApi(details_dict1)
        id="5408386919326811103004"
        return_data, status, body =transction_details_obj.get_transaction(id)
        print(status)
        print(body)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    transaction_details()
