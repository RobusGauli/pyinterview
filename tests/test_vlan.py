from nose.tools import (
    assert_equal,
    raises,
)

from main import VLanNode

class TestVlanNode:
    """Test for vlannode"""
    def __init__(self):
        self.vlan_node = None
    
    def setup(self):
        self.vlan_node = VLanNode(10)

    def teardown(self):
        self.vlan_node = None
  
    @raises(ValueError)
    def test_vlan_node(self):
        return VLanNode(None)
    
    @raises(ValueError)
    def test_get_device_list_with_None(self):
        return self.vlan_node.get_device_list(None)
    
    def test_get_device_list_with_bool(self):
        assert_equal(self.vlan_node.get_device_list(False), set())
    
