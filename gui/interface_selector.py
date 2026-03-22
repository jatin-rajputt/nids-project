from scapy.all import IFACES

def get_interfaces():

    interfaces = {}

    for iface in IFACES.data.values():

        name = iface.name
        description = iface.description

        interfaces[description] = name

    return interfaces