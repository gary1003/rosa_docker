# run and keep it running
docker run -d --name gary_container gary /bin/bash -c "python /app/main.py && tail -f /dev/null"
# wait for 5 seconds
sleep 5
# copy log file and name it with current time
docker cp gary_container:/app.log /home/garywu/rosa_docker/app/app.log
# remove container
docker rm gary_container -f