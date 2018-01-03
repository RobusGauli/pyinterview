import bisect

class VLanNode:

    def __init__(self, value):
        self.value = value
        self.device_primary = {} #mappin device_id -> device
        self.device_secondary = {} #mapping device_id -> device
        self.device_common = {}

        self.devices_primary = set()
        self.devices_secondary = set()
        self.devices_common = set()
    
    def get_device_list(self, is_primary):
        return self.devices_primary if is_primary else self.devices_secondary

    def get_device(self, device_id, is_primary):
        return self.device_primary[device_id] if is_primary else self.device_secondary[device_id]

    def get_device_mapping_dict(self, is_primary):
        return self.device_primary if is_primary else self.device_secondary
    
    def exists_primary_secondary(self, device_id):
        # return device id if there is a common in both the primary and secondary
        # else return the empty set
        return set(self.device_primary.keys()).\
            intersection(set(self.device_secondary.keys())).\
            intersection(set([device_id]))
    
    def common_device_with_lower_value(self, vlan_id):
        for device in sorted(self.device_common.values(), key=lambda dev: dev.device_id):
            if vlan_id not in device.reserved_vlan_ids:
                return device
    
    def primary_device_with_lower_value(self, vlan_id):
        for device in sorted(self.device_secondary.values(), key=lambda dev: dev.device_id):
            if vlan_id not in device.reserved_vlan_ids:
                return device
        
    
    def __repr__(self):
        return 'VLanNode({0})'.format(self.value)


class Device:
    def __init__(self, device_id):
        self.device_id = device_id
        self.reserved_vlan_ids = set()


class Graph:
    
    def __init__(self, data):
        self.data = data
        self.id_vlan_node_map = {}
    
    def start(self):
        #tehere is som
        for vlan_item in self.data:
            #get the id
            _id = int(vlan_item['vlan_id'])
            if _id in self.id_vlan_node_map:
                #then we have the vlan ndoe
                vlan_node = self.id_vlan_node_map[_id]
            else:
                vlan_node = VLanNode(_id)
                self.id_vlan_node_map[_id] = vlan_node
            #now we have vlan node
            #lets figure out which way to go by looking if its primary or secondary 
            is_primary_port = vlan_item['primary_port'] == '0'
            device_dict = vlan_node.get_device_mapping_dict(is_primary_port)
            device_list = vlan_node.get_device_list(is_primary_port)
            #get the deviceid
            device_id = int(vlan_item['device_id'])
            if device_id in device_dict:
                #the get the device node
                device_node = device_dict[device_id]
            else:
                #create one
                device_node = Device(device_id)
                device_dict[device_id] = device_node
            #bisect.insort_left(device_list, device_id)
            device_list.add(device_id)
            #check to see if this device node mapps to both the primary and secondary
            #then put this ina device_common dict
            if vlan_node.exists_primary_secondary(device_id):
                vlan_node.device_common[device_id] = device_node
                vlan_node.devices_common.add(device_id) 
    
    


def get_graph():
    import csv
    data = list(csv.DictReader(open('vlans.csv')))
    g = Graph(data)
    g.start()
    print(g.id_vlan_node_map)
    return g


# def perform_computation(graph, vlans_ids, requests, current_request_index=0):
#     #get the vlan_node from the lowest of the vlans_id
#     if current_request_index === len(requests) - 1:
#         return
#     request = requests[current_request_index]
#     if request['redundant'] == '1':
#         #we need to check for the common nodes
#         vlan_node = graph.id_vlan_node_map[vlans_ids[0]]
#         #get the device that has the lowest id and the vland_ids is not reserved
#         device = vlan_node.common_device_with_lower_value(vlans_ids[0])
#         print(device.device_id, '----', requests[current_request_index], '...', 0, '----', vlans_ids[0])
#         print(device.device_id, '----', requests[current_request_index], '...', 1, '----', vlans_ids[0])
#     else:
#         vlan_node = graph.id_vlan_node_map[vlans_ids[0]]



def perform(graph, requests, vlans_ids):
    for request in requests:
        request_id = request['request_id']
        if request['redundant'] == '0':
            current_index = 0
             
            
            while True:
                current_vlan_id = vlans_ids[current_index]
                vlan_node = graph.id_vlan_node_map[current_vlan_id]
                try:
                    device_id = min(vlan_node.devices_secondary)
                    vlan_node.devices_secondary.remove(device_id)
                    if device_id in vlan_node.devices_common:
                        vlan_node.devices_common.remove(device_id)
                    print(request_id, device_id, 1, current_vlan_id)
                    
                    break
                except ValueError:
                    current_index += 1
        elif request['redundant'] == '1':
            current_index = 0
            while True:
                current_vlan_id = vlans_ids[current_index]
                vlan_node = graph.id_vlan_node_map[current_vlan_id]
                try:
                    device_id = min(vlan_node.devices_common)
                    vlan_node.devices_common.remove(device_id)
                    if device_id in vlan_node.devices_secondary:
                        vlan_node.devices_secondary.remove(device_id)
                    if device_id in vlan_node.devices_primary:
                        vlan_node.devices_primary.remove(device_id)
                    print(request_id, device_id, 0, current_vlan_id)
                    print(request_id, device_id, 1, current_vlan_id)
                    break
                except ValueError:
                    current_index += 1
        

                


def perform_computation(graph, requests, vlans_ids):
    for request in requests:
        #request id
        request_id = request['request_id']
        if request['redundant'] == '0':
            #that means we need to look for the device with which has the reserved the vlans_id
            def find_device(graph, vlans_ids):
                if not len(vlans_ids):
                    return
                vlan_node = graph.id_vlan_node_map[vlans_ids[0]]
                device = vlan_node.primary_device_with_lower_value(vlans_ids[0])
                if device:
                    device.reserved_vlan_ids.add(vlans_ids[0])
                    return device
                else:
                    return find_device(graph, vlans_ids[1:])
            device = find_device(graph, vlans_ids)
            # print(request_id, device.device_id)
        elif request['redundant'] == '1':
            def find_device_(graph, vlans_ids):
                if not len(vlans_ids):
                    return
                vlan_node = graph.id_vlan_node_map[vlans_ids[0]]
                device = vlan_node.common_device_with_lower_value(vlans_ids[0])
                if device:
                    device.reserved_vlan_ids.add(vlans_ids[0])
                    return device
                else:
                    return find_device_(graph, vlans_ids[1:])
            device = find_device_(graph, vlans_ids)
            print(request_id)


def main():
    import csv
    data = list(csv.DictReader(open('vlans.csv')))
    g = Graph(data)
    g.start()
    
    vlan_ids = sorted(list(g.id_vlan_node_map.keys()), key= lambda k: int(k))
    #print(vlan_ids)
    requests = list(csv.DictReader(open('requests.csv')))
    perform(g, requests, vlan_ids)
    return g

if __name__ == '__main__':
    main()        


