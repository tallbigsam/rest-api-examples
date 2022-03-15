# -*- coding: utf-8 -*-
# Generic/Built-in

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


# creates a hosted cluster in a specified project, returning the cluster ID
def create_hosted_cluster(cluster_name, project_id, debug=False):

    cappella_api = CapellaAPI()

    if debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    cluster_configuration = {
        "environment": "hosted",
        "clusterName": cluster_name,
        "description": "Example hosted cluster create from Public API",
        "projectId": project_id,
        "place": {
            "singleAZ": True,
            "hosted": {
                "provider": "aws",
                "CIDR": "10.199.0.0/20",
                "region": "eu-west-2"
            }
        },
        "servers": [
            {
                "compute": "m5.large",
                "size": 3,
                "services": ["data", "index", "search", "query"],
                "storage": {
                    "size": 50,
                    "IOPS": 3000,
                    "type": "GP3"
                    },
            }
        ],
        "supportPackage": {
            "timezone": "GMT",
            "type": "Basic"
        },
        "version": "latest",
    }

    # Create the cluster, indicate that this is a hosted cluster by calling with True
    # and pass the configuration
    capella_api_response = cappella_api.create_cluster(True, cluster_configuration)

    # Check response code , 202 is success
    if capella_api_response.status_code == 202:
        #return "" + cappella_api.API_BASE_URL + \
        #      capella_api_response.headers['Location'] + '/status'

        # return the cluster id
        return capella_api_response.headers['Location'].split('/v3/clusters/')[1]
    else:
        return "" + capella_api_response.json()["message"]


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates a 3 node cluster using Couchbase managed cloud in Couchbase Capella\n '
                                     'with data, index, search, and query services and 50Gb of storage\n in aws '
                                     'us-east-2')
    my_parser.ExampleCmdline = "-cn aNewCluster -pid 1478c0f4-07b2-4818-a5e8-d15703ef79b0 "

    # Add the arguments

    my_parser.add_argument('-cn', '--clusterName',
                           action='store',
                           required=True,
                           type=str,
                           help='The name to use for the cluster')

    my_parser.add_argument('-pid', '--projectID',
                           action='store',
                           required=True,
                           type=check_if_valid_uuid,
                           help='ID of the project to use for the cluster')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
