# Step by Step to get and run Llama locally using docker
1. Install Docker Desktop - It supports WSL2

2. Create a docker-compose - llama3.1:8b model - Already created in the project

3. Run docker using the docker-compose config file. `-d` to run in detached mode.
```bash
$ docker compose up -d
```
And then to see logs (necessary to see if llama3 is downloaded):
```bash
$ docker logs -f ollama
```

4. And to test if it's using the GPU (after docker compose up):
```bash
$ docker exec -it ollama nvidia-smi
```

5. To stop
```bash
$ docker compose down
```

6. If any error occurs (not a must on each error):
Stop and remove all containers in this project
```bash
$ docker compose down -v
```

Remove the volume where models are stored
```bash
$ docker volume rm ollama_ollama-data
```

