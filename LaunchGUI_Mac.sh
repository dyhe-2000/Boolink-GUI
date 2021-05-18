#!/bin/bash

xhost + 127.0.0.1
#defaults write org.xquartz.X11.plist nolisten_tcp -bool false 

# create a volume on the host machine
docker volume create data-store-loc

# store the location of the volume for future use
data_add=$(docker volume inspect --format '{{ .Mountpoint }}' data-store-loc)

# run the container from the image. include the required options
docker run -e DISPLAY=host.docker.internal:0 -v data-store-loc:/usr/src/app aravindraok/boolink:pphys 


# after the GUI is closed, retrieve the data from docker mount volume into a new directory
mkdir -p simulation_data
cd simulation_data
cp -r ${data_add} ./

cd ../

#defaults write org.xquartz.X11.plist nolisten_tcp -bool true
