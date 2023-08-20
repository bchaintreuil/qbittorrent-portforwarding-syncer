FROM python:3-alpine

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

COPY crontabs /etc/crontabs/root
RUN chown root:root /etc/crontabs/root && chmod 600 /etc/crontabs/root

ENV GLUETUN_HOSTNAME=gluetun
ENV GLUETUN_PORT=8000
ENV QBITTORRENT_HOSTNAME=gluetun
ENV QBITTORRENT_PORT=8080
# qBittorrent default values
ENV QBITTORRENT_USER=admin
ENV QBITTORRENT_PWD=adminadmin

ENTRYPOINT ["/usr/sbin/crond"]
CMD ["-f", "-l", "6", "-L", "/dev/stdout"]