import os
import argparse
import csv
import yaml

from main import (
    NetworkGraph,
    perform_mapping,
)


valid_csv_file = lambda path: os.path.exists(path) and \
                        os.path.isfile(path) and \
                        os.path.splitext(path)[1] == '.csv'

HEADER = ['request_id', 'device_id', 'primary_port', 'vlan_id']

def _main(reqs, vls, out_filepath):
    # create a graph instance
    graph = NetworkGraph(vls)
    graph.populate_graph()
    
    # get the vlan ids in sorted order from lowest to highest
    vlan_ids = list(sorted(graph.id_vlan_node_map.keys()))
    # perform the compuation and get the result
    result = perform_mapping(graph, reqs, vlan_ids)
    # flush the result to csv
    with open(out_filepath, mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(HEADER)
        writer.writerows(result)
    print('success..')
    
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Vlan-ID Mapper'
    )
    parser.add_argument(
        '-v', '--vlans',
        required=True,
        action='store',
        help='Vlans csv file'
    )
    parser.add_argument(
        '-r', '--requests',
        required=True,
        action='store',
        help='Requests csv file'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        action='store',
        help='Output file.'
    )
    args = parser.parse_args()
    
    #open a vlans file
    if not valid_csv_file(args.vlans):
        raise ValueError('Please provide the valid vlans csv file.')

    if not valid_csv_file(args.requests):
        raise ValueError('Please provide the valid requests csv file.')

    with open(args.vlans, mode='r', encoding='utf8') as file:
        vlans = list(csv.DictReader(file))
    
    with open(args.requests, mode='r', encoding='utf8') as file:
        requests = list(csv.DictReader(file))
    
    # MAIN
    _main(requests, vlans, args.output)