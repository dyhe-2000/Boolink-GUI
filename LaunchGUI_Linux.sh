#!/bin/bash

xhost +

# stop the running containers on docker
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)

# create a volume on the host machine
sudo docker volume create data-store-loc

# store the location of the volume for future use
data_add=$(sudo docker volume inspect --format '{{ .Mountpoint }}' data-store-loc)

# run the container from the image. include the required options
#sudo docker run --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v data-store-loc:/usr/src/app aravindraok/boolink:pphys

#sudo docker run --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v data-store-loc:/usr/src/app aravindraok/boolink:pphys

sudo docker run --net=host -e DISPLAY=unix$DISPLAY --volume="/tmp/.X11-unix:/tmp/.X11-unix" -v data-store-loc:/usr/src/app aravindraok/boolink:pphys


# after the GUI is closed, retrieve the data from docker mount volume into a new directory
mkdir -p simulation_data
cd simulation_data
sudo cp -r ${data_add} ./
cd ../

# remove the volume created above
sudo docker volume rm data-store-loc
