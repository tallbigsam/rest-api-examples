# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs
import maya
from time import time
from time import sleep
from requests import get

from get_project_id import get_project_id
from createHostedClusterInProject import create_hosted_cluster
from checkHostedClusterIsHealthy import get_cluster_health_status
from getHostedClusterInfoFromUUID import get_hosted_cluster_info_from_uuid
from getClusterIdFromName import get_cluster_id_from_name
from createHostedClusterUser import request_user_creation

# Owned
from capellaAPI.CapellaAPICommon import MyParser


__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'



if __name__ == '__main__':
    # Process command line args
    # Create the parser

    my_parser = MyParser(description='List projects defined in Couchbase Capella')
    my_parser.ExampleCmdline = "With debug on -d \nWith debug off "

    # Add the arguments
    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    project_name = "sam-demo"
    cluster_name = "otto-cluster"
    project_id = get_project_id(args, project_name)

    cluster_uuid = create_hosted_cluster(cluster_name, project_id)

    # get the hosted cluster status
    cluster_healthy = False
    stop_time = int(time()) + 300
    while not cluster_healthy:
        # check if it's ready
        cluster_healthy = get_cluster_health_status(cluster_uuid)
        if time() > stop_time:
            print("Timed out checking cluster health")
            break

    # when it's ready, get the srv record to connect to
    #cluster_uuid = get_cluster_id_from_name(cluster_name)
    
    #cluster_uuid = get_cluster_uuid("travel-sample", project_id)
    #server_list = get_servers(cluster_uuid)

    # create the bucket on the cluster

    # create the cluster user
    cluster_info = get_hosted_cluster_info_from_uuid(cluster_uuid)
    print(cluster_info)

    cluster_user_struct = {
        "password": "Password123!",
        "username": "TheDude",
        "buckets": []
    }

    password = "Password123!"
    username = "TheDude"
    buckets_and_scope = "travel-sample:*:rw"
    
    # create a database user to allow the SDK to connect
    request_user_creation(cluster_uuid, username, password, buckets_and_scope)

    # create an IP whitelist for the cluster
    my_ip = get('https://api.ipify.org').content.decode('utf8')

    # when we have the servers, run the test! 
    # cluster is ready, get the srv