# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs
import maya
from time import time
from time import sleep
from requests import get

from getProjectId import get_project_id
from createHostedClusterInProject import create_hosted_cluster
from checkHostedClusterIsHealthy import get_cluster_health_status


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

    my_parser = MyParser(description='Create a named cluster in Couchbase Capella within a specified Project')
    my_parser.ExampleCmdline = "With debug on -d \nWith debug off "

    # Add the arguments
    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    my_parser.add_argument('-pn', '--projectName',
                           dest="project_name",
                           action='store',
                           metavar="",
                           required=True,
                           type=str,
                           help='Name of the Project to create the cluster in (must be created in Capella Tenant)')

    my_parser.add_argument('-cn', '--clusterName',
                           dest="cluster_name",
                           action='store',
                           metavar="",
                           type=str,
                           required=True,
                           help='Name for the Cluster')

    args = my_parser.parse_args()

    # use these variables if you'd rather statically define names
    #project_name = "sam-demo"
    #cluster_name = "otto-cluster"

    # get the project ID from the Capella API from the args
    project_id = get_project_id(args, args.project_name)
    if not project_id:
        print(f"Project Name: {args.project_name} not found. Please create it in the Capella GUI.")
        quit()

    # create the capella cluster using the name from the args, return a UUID.
    cluster_uuid = create_hosted_cluster(args.cluster_name, project_id)
    if not cluster_uuid:
        quit()

    # get the hosted cluster status
    cluster_healthy = False
    stop_time = int(time()) + 300
    while not cluster_healthy:
        # check if it's ready
        cluster_healthy = get_cluster_health_status(cluster_uuid)
        if time() > stop_time:
            print("Timed out checking cluster health")
            break

    print(f"Check the Capella API, now created cluster {args.cluster_name}")