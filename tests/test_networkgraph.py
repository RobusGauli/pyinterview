from nose.tools import (
  assert_equal,
  raises,
)
import csv
import os
from main import NetworkGraph

class TestNetworkGraph:

    def __init__(self):
        self.vlans = None
        self.requests = None

    def setup(self):
        """Setting up the vlans and requests from the csv"""
        self.vlans = list(csv.DictReader(open('./tests/test_vlans.csv')))
        self.requests = list(csv.DictReader(open('./tests/test_requests.csv')))
        print(self.vlans, self.requests)

    @raises(ValueError)
    def test_network_graph_instance(self):
        return NetworkGraph(None)
    
    def test_toge(self):
        pass
    
