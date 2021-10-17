import untangle


def get_net_ints(ovf_xml):
    ova_descriptor_obj = untangle.parse(ovf_xml)
    envelope = ova_descriptor_obj.Envelope
    network_section = envelope.NetworkSection
    interface = network_section.Network['ovf:name']
    return interface