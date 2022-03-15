# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs


# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid
from capellaAPI.CapellaAPI import CapellaAPI

from time import sleep

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def get_cluster_health_status(cluster_id, wait_time=5, attempts=5):
    cappella_api = CapellaAPI()
    capella_api_response = None

    # Check Capella API status
    if cappella_api.api_status().status_code == 200:
        cluster_healthy = False
        attempt_no = 0

        while not cluster_healthy and attempt_no < attempts:
            capella_api_response = cappella_api.get_cluster_status(True, cluster_id)

            if capella_api_response.status_code == 200:
                # Cluster information was found
                if capella_api_response.json()['status'] == "healthy":
                    return True
                else:
                    # sleeping, the cluster might be coming up
                    sleep(wait_time)
                    attempt_no += 1
                    
            else:
                print("Failed to get status for cluster ID " + cluster_id)
                print("Capella API returned " + str(capella_api_response.status_code))
                print("Full error message")
                print(capella_api_response.json()["message"])

        print("Current Cluster Status: %s" % capella_api_response.json()['status'])

    else:
        print("Check Capella API is up.")