from openvpn_status import parse_status

with open('/home/felipedev/openvpn-status.log') as logfile:
    status = parse_status(logfile.read())

print(status.updated_at)  # datetime.datetime(2015, 6, 18, 8, 12, 15)

foo_client = status.client_list['190.157.200.240:1194']
print("Name")
print(foo_client.common_name)  # foo@example.com
print("Bytes Recibidos")
print(foo_client.bytes_received)  # 334.9 kB
print("Bytes Enviados")
print(foo_client.bytes_sent)  # 2.0 MB
