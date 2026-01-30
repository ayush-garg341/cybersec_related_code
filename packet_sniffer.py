from scapy.all import sniff, Raw


chars = []


def packet_handler(pkt):
    """
    Sniff the network packet, load the byte and decode it.
    Append it into chars array to see the data.
    """

    # Data might not be there, so checking summary of the packet
    print(pkt.summary())
    if pkt.haslayer(Raw):
        flag_byte = pkt[Raw].load
        chars.append(flag_byte.decode("utf-8"))
        if len(chars) == 150:
            print(chars)
            return


sniff(filter="host 127.0.0.1 and tcp port 80", prn=packet_handler, store=False)
