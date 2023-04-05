import os

import fusion
from fusion.rest import ApiException

from utils import wait_operation_succeeded


def teardown_protection_policies():
    print("Tearing down protection policies")
    # Setup Config
    config = fusion.Configuration()
    if os.getenv('HOST_ENDPOINT'):
        config.host = os.getenv('HOST_ENDPOINT')
    if os.getenv('TOKEN_ENDPOINT'):
        config.token_endpoint = os.getenv('TOKEN_ENDPOINT')
    config.issuer_id = os.getenv("API_CLIENT")
    config.private_key_file = os.getenv("PRIV_KEY_FILE")

    client = fusion.ApiClient(config)
    pp = fusion.ProtectionPoliciesApi(api_client=client)

    try:
        api_response = pp.list_protection_policies()
        # pprint(api_response)
    except ApiException as e:
        print("Exception when calling ProtectionPoliciesAPI->list_protection_policies: %s\n" % e)

    try:
        for protection_policy in api_response.items:
            print("Deleting protection policy", protection_policy.name)
            api_response = pp.delete_protection_policy(protection_policy.name)
            # pprint(api_response)
            wait_operation_succeeded(api_response.id, client)
    except ApiException as e:
        print("Exception when calling ProtectionPoliciesAPI->delete_protection_policy: %s\n" % e)
    print("Done tearing down protection policies!")


if __name__ == '__main__':
    teardown_protection_policies()
