FROM ubuntu:22.04

USER root

# Install necessary packages
RUN apt-get update && apt-get -y install \
  python3-pip \
  python3-dev \
  python3-lxml \
  build-essential \
  libssl-dev \
  libffi-dev \
  libxml2-dev \
  libxslt1-dev \
  openssl \
  wget \
  curl \
  unzip \
  gnupg \
  coreutils \
  apt-transport-https

# Create directory for the application
RUN mkdir -p /root/codes/
COPY . /root/codes/

# Set working directory
WORKDIR /root/codes/

COPY ./tor.list /etc/apt/sources.list.d/

RUN wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/deb.torproject.org-keyring.gpg >/dev/null

RUN apt-get update && apt-get -y install tor deb.torproject.org-keyring

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Start the startup script
ENTRYPOINT [""]
