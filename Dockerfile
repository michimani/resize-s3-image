FROM amazonlinux:latest

RUN yum install python3 -y
RUN mkdir /home/deploy
