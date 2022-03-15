# -*- coding: utf-8 -*-
# Generic/Built-in

# Other Libs

# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import pretty_table
from capellaAPI.CapellaAPI import CapellaAPI

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def get_cluster_id_from_name(searched_cluster_name):
    cappella_api = CapellaAPI()

    capella_api_response = cappella_api.get_clusters()

    # Check response code , 200 is success
    if capella_api_response.status_code == 200:
        clusters_table_rows = []

        # There could not be any clusters, lets check if that's the case
        if capella_api_response.json()['data'] == {}:
            cluster_entries = None
            print("No clusters found")
        else:
            cluster_entries = capella_api_response.json()['data']['items']

            # Got a list of clusters, just double check that we do have entries

            for cluster_entry in cluster_entries:
                cluster_environment = cluster_entry['environment']
                cluster_id = cluster_entry['id']
                cluster_name = cluster_entry['name']

                # if the cluster is inVPC, then we will have a cloud ID
                if cluster_environment == 'inVpc':
                    clusterCloudID = cluster_entry['cloudId']
                else:
                    clusterCloudID = 'N/A'

                

                if cluster_name == searched_cluster_name:
                    return cluster_id


    else:
        print("Failed to get list of clusters ")
        print("Capella API returned " + str(capella_api_response.status_code))
        print("Full error message")
        print(capella_api_response.json()["message"])
        return None


if __name__ == '__main__':
    # Process command line args
    # Create the parser

    my_parser = MyParser(description='List clusters managed by Couchbase Capella')
    my_parser.ExampleCmdline = """With debug on -d \nWith debug off """

    # Add the arguments
    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()
    args.get_cluster_id = False

    main(args)
