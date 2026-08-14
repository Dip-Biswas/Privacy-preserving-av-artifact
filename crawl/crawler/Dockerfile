FROM ubuntu:24.04

ENV DEBIAN_FRONTEND noninteractive

RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y curl sudo
RUN apt-get install -y xvfb
RUN apt-get install -y wget
RUN apt-get install -y gnupg
RUN wget --no-check-certificate -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN apt-get install -y ca-certificates
RUN apt-get install -y python3 pipx tmux

ENV PYTHONUNBUFFERED 1
ENV HOME /home/doe
ENV DISPLAY :99

WORKDIR /home/doe/crawler
COPY . .

RUN mkdir -p /home/doe/.cache/uv
RUN useradd doe
RUN chown -R doe:doe /home/doe

RUN pipx install uv
RUN pipx ensurepath
RUN chown -R doe:doe /home/doe

RUN echo "doe:doe" | chpasswd && adduser doe sudo
USER doe
