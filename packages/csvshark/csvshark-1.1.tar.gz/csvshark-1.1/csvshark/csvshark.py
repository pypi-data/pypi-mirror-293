import csv
from ipaddress import ip_address, IPv4Address, IPv6Address

def filter_from_csv(csv_file):
    """
    Generates a Wireshark display filter based on IP addresses and ports 
    extracted from a CSV file. The filter will exclude traffic based on 
    the provided IP addresses and ports.

    Args:
        csv_file (str): The path to the CSV file containing the data. 
                        The CSV is expected to have columns for 'Source', 
                        'Destination', 'Source Port', and 'Destination Port'.

    Returns:
        str: The Wireshark filter expression to exclude traffic involving the 
             specified IP addresses and ports.
    """
    ip_set = set()
    port_set = set()

    # Read CSV file and extract IP addresses and ports
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for field in ['Source', 'Destination']:
                if field in row and row[field]:
                    try:
                        ip = ip_address(row[field])
                        ip_set.add(str(ip))
                    except ValueError:
                        pass  # Ignore invalid IP addresses
            
            for field in ['Source Port', 'Destination Port']:
                if field in row and row[field]:
                    try:
                        port = int(row[field])
                        port_set.add(port)
                    except ValueError:
                        pass  # Ignore invalid ports

    # Generate Wireshark filter expressions for IP addresses
    ip_filters = []
    for ip in ip_set:
        if isinstance(ip_address(ip), IPv4Address):
            ip_filters.append(f'ip.addr == {ip}')
        else:
            ip_filters.append(f'ipv6.addr == {ip}')
    
    # Generate Wireshark filter expressions for ports
    port_filters = [f'tcp.port == {port} || udp.port == {port}' for port in port_set]

    # Combine filters to exclude all captured traffic
    ip_filter = ' || '.join(ip_filters)
    port_filter = ' || '.join(port_filters)

    final_filter = f'!({ip_filter}) && !({port_filter})' if ip_filter and port_filter else f'!({ip_filter or port_filter})'

    return final_filter