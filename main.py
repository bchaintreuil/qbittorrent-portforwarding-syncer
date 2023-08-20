#!/usr/bin/python3
import qbittorrentapi
import requests
import os

def main():
    # Initialization
    try:
        gluetun_hostname = os.environ['GLUETUN_HOSTNAME']
        gluetun_port = os.environ['GLUETUN_PORT']
        # Since qBittorrent is directly connected through the Gluetun container, we generally use the same hostname.
        qbittorrent_hostname = os.getenv("QBITTORRENT_HOSTNAME", gluetun_hostname)
        qbittorrent_port = os.environ['QBITTORRENT_PORT']
        qbittorrent_user = os.getenv('QBITTORRENT_USER', "admin") # qBittorrent default values
        qbittorrent_pwd = os.getenv('QBITTORRENT_PWD', "adminadmin") # qBittorrent default values
    except KeyError:
        print("One or more mandatory environment variables doesn't exist")
        exit(1)
    
    # First we retrieve the assigned forwarding port from Gluetun using the control server
    try:
        gluetun_fwport = requests.get(url="http://{}:{}/v1/openvpn/portforwarded".format(gluetun_hostname, gluetun_port)).json()["port"]
        print("Gluetun assigned forwarding port: " + str(gluetun_fwport))
    except requests.exceptions.RequestException as e:
        print("Gluetun connection error!")
        exit(1)

    # We retrieve the qBittorrent set up one
    with qbittorrentapi.Client(host=qbittorrent_hostname, port=qbittorrent_port, username=qbittorrent_user, password=qbittorrent_pwd) as qbt_client:
        # display qBittorrent info
        print(f"qBittorrent: {qbt_client.app.version}")
        print(f"qBittorrent Web API: {qbt_client.app.web_api_version}")

        qbittorrent_fwport = qbt_client.app_preferences()["listen_port"]
        print("qBittorrent assigned forwarding port: " + str(qbittorrent_fwport))

        if qbittorrent_fwport != gluetun_fwport:
            print("Gluetun & qBittorrent ports are differents, setting up new port accordingly")
            qbt_client.app_set_preferences(dict(listen_port=gluetun_fwport))
        else:
            print("Gluetun & qBittorrent ports are the same, nothing to do...")

if __name__ == '__main__':
    main()