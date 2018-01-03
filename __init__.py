import csv
import heapq

class Device:
    '''It holds the '''

    def __init__(self, device_id):
        self.device_id = device_id
        self.available_vlan_id_primary = []
        self.available_vlan_id_secondary = []
        self.reserved_vlans = set()
    
    def __repr__(self):
        return 'Device({0})'.format(self.device_id)


class Network:

    def __init__(self, data):
        self.devices = {} #mapp of id and device for later access
        self.data = data
    
    def initialize_heapify(self):

        for vlan_data in self.data:
            #get the device_id
            print(vlan_data['vlan_id'])
            _id = int(vlan_data['device_id'])
            if _id in self.devices:
                #get the device
                device = self.devices[_id]
            else:
                device = Device(_id)
                self.devices[_id] = device

            _port_type = vlan_data['primary_port']
            if _port_type == '0':
                # means it s a primary port
                device.available_vlan_id_primary.append(int(vlan_data['vlan_id']))
                print(device.available_vlan_id_primary)
            else:
                device.available_vlan_id_secondary.append(int(vlan_data['vlan_id']))
        # finally heapify the list
        

    def __getitem__(self, key):
        return self.devices[key]
    
    def __iter__(self):
        for device in self.devices.values():
            yield device
            


def main():
    data = list(csv.DictReader(open('test_vlans.csv')))
    n = Network(data)
    n.initialize()
    print(n.devices[0].__dict__)
    return n            

if __name__ == '__main__':
    main()