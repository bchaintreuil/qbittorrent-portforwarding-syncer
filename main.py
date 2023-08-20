#!/usr/bin/python3
import qbittorrentapi
import requests

def main():
    # First we retrieve the forwarded port from gluetun using the control server
    r : requests.Response = requests.get(url="http://localhost:9011/v1/openvpn/portforwarded")

    print(r.json)

if __name__ == '__main__':
    main()