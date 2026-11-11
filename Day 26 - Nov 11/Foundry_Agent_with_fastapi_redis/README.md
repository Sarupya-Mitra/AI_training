# STEP 1:
Install the packages in requirements.txt

# STEP 2:
Create Foundry resource and copy the project endpoint(inside the foundry portal) and paste it in env file like:
FOUNDRY_PROJECT_ENDPOINT = <endpoint you copied>
Then create a Agent and paste the details in env file like:
FOUNDRY_AGENT_NAME = <agent name>

# Step 3:
Check whether you can connect with Agent using python, use az login and make the 
necessary changes to your main.py.

# Step 4:
Setup redis:
docker run -d --name employee-redis -p 127.0.0.1:6379:6379 -v employee_redis_data:/data redis:7-alpine redis-server --appendonly yes  

The above command creates and starts a Redis server inside a Docker container, makes it accessible 
on your local machine through port 6379, and stores its data persistently 
so that data isn't lost when the container is removed.

- 'docker run' : Creates and starts a new container
- "-d": stands for detached mode, meaning redis container runs 
in the background; if I had not written -d then docker
would attach the terminal to container's output.
- '--name employee-redis': Assigns a human readable name 
to container, we can use this name to start/stop or see logs
and execute the container.
- '-p 127.0.0.1:6379:6379': This port mapping. It connects 
port on my computer (1st 6379) to port inside Docker 
container (2nd 6379).
- '-v employee_redis_data:/data': It creates Docker volume 
to persist Redis data. -v tells docker to mount volume.
employee_redis_data is the name of the docker volume
/data is the directory inside Redis container where data
will be stored. With this docker store data separately from
container and so even if Redis container is deleted, Redis 
can recover it persisted data.
- 'redis:7-alpine': Specifies the docker image to use
- 'redis-server --appendonly yes': Docker executes this
inside the container after starting it. 
redis-server: starts the redis server process
--appendonly yes: Enables Redis Append Only File(AOF) persistance

The run:
docker exec employee-redis redis-cli ping 
Just to check if redis server is up and running or not. If it returns "PONG", you are good to start.
 
python -m uvicorn main:app --reload
 
http://127.0.0.1:8000/docs?utm_source=chatgpt.com#/default/chat_chat_post
 