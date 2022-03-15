# -*- coding: utf-8 -*-
# Generic/Built-in
import json

# Other Libs

# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid
from capellaAPI.CapellaAPI import CapellaAPI

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def get_hosted_cluster_info_from_uuid(cluster_id):
    cappella_api = CapellaAPI()

    # Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.get_cluster_info(True, cluster_id)
        if capella_api_response.status_code == 200:
            # Cluster information was found
            print("Got information for cluster ID " + cluster_id)
            print(json.dumps(capella_api_response.json(), indent=3))
            return capella_api_response.json()
        else:
            print("Failed to get information for cluster ID " + cluster_id)
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])
            return capella_api_response.json()

    else:
        print("Check Capella API is up.")
        return None


