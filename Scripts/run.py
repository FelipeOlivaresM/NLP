import csv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import array

myData = list()

with open('./data/Dataentrenamientolinks.csv') as csvfile:
    with open('./data/2.csv', 'w') as csvfile1:
        fieldnames = ['row ID', 'Short', 'LINK']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        i=0
        for row in reader:
            
            if row['LINK']:
                url = row['LINK']
                
                try:
                    session = requests.Session()  # so connections are recycled
                    retry = Retry(connect=3, backoff_factor=0.5)
                    adapter = HTTPAdapter(max_retries=retry)
                    session.mount('http://', adapter)
                    session.mount('https://', adapter)

                    resp = session.head(url, allow_redirects=True)
                    print({'row ID':row['row ID'], 'Short':row['LINK'], 'Full':resp.url})
                    myData.append({'row ID':row['row ID'], 'Short':row['LINK'], 'LINK':resp.url})
                    writer.writerows(myData)
                    myData.pop()                                       
                except requests.exceptions.ConnectionError:
                    print("Connection refused")
   
print("Writing complete")




myData = list()
        with open('datavpn.csv') as csvfile:
            fieldnames = ['name', 'vpnip', 'remoteip','full_location','bytes_recv','conected','total_time','VPNID']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for sis in session:
                print("Test#2")
                print(name,vpnip,remoteip,full_location,bytes_recv,conected,total_time)
                myData.append({'name':name, 'vpnip':vpnip,'remoteip':remoteip,'full_location':full_location,'bytes_recv':bytes_recv,'conected':conected,'total_time':total_time, 'VPNID':vpn_id})
                writer.writerows(myData)
                myData.pop()
                print("VPIID")
                print(vpn_id)










                print("\n Test \n ")
        URL = "http://ip-api.com/json/"
        myData = list()
        with open('datavpn.csv') as csvfile:
            print("Lectura Archivo")
            fieldnames = ['name', 'vpnip','VPNID']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for sis in session:
                print("Test#2")
                #print(name,vpnip,remoteip,full_location,bytes_recv,conected,total_time)
                myData.append({'name':name, 'vpnip':vpnip,'VPNID':vpn_id})
                print(myData)
        #row = [name,vpnip,remoteip,conected,total_time,bytes_recv,full_location]
        #variablescont=2
        #sheet.insert_row(row,variablescont)


 Sesiones

{'10.206.31.87': {'remote_ip': IPv4Address('200.29.110.48'), 'port': 1194, 'location': 'CO', 'region': 'VAC', \
     'city': 'Santiago de Cali', 'country': 'Colombia', 'longitude': -76.5232, 'latitude': 3.4384, $

 Fin Sesiones







 myData = list()
        with open('datavpn.csv', 'w') as csvfile:
             #print("Creacion Archivo")
             fieldnames = ['name', 'vpnip', 'remoteip','full_location','bytes_recv','conected','total_time','VPNID']
             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
             for sis in session:
                 #print("Test#2")
                 #print(name,vpnip,remoteip,full_location,bytes_recv,conected,total_time)
                 myData.append({'name':name, 'vpnip':vpnip,'remoteip':remoteip,'full_location':full_location,'bytes_recv':bytes_recv,'conected':conected,'total_time':total_time, 'VPNID':vpn_id})
                 
                 myData.append({'Username/Hostname':"Test", 'VPN IP':"Test", 'Remote IP':"Test",'Location':"Test",'Bytes In':"Test",'Conected Since':"Test",'Time Online':"Test",'Server:"Test"'})
                 writer.writerows(myData)
                 myData.pop()
{'host': '190.131.225.42', 'name': 'AvayaInbound', 'port': '5555', 'show_disconnect': False, 'socket_connected': True, 'release': 'OpenVPN 2.4.8 amd64-portbld-freebsd11.3 [SSL (OpenSSL)] [LZO] [LZ4] [MH/R





