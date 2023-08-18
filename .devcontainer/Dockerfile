FROM ubuntu:latest

# install dotnet sdk, python, pip and git
RUN apt-get update && \
    apt-get install -y dotnet-sdk-7.0 python3.10 python3-pip git && \
    apt-get clean

# point python to python3.10
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# create user
ARG USERNAME=user
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash $USERNAME
USER $USERNAME
