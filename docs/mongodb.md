# MongoDB Setup

## Make a Dockerfile for MongoDB

1. Make a Directory for MongoDB to store its data

```
mkdir mongoData
```

2. Run the MongoDB Container

```
docker run -d -p 27017:27017 -v ~/data:/data/db mongo
```

`-d`

Tells docker to run the container as a daemon

`-p 27017:27107`

Maps the port `27017` of the container to the port `27017` of the host.

The syntax is `-p HOST_PORT:CONTAINER_PORT`

`-v ~/data:/data/db`

Maps the `/data/db` directory of the container to the `~/data` directory on the host.

This is called a data volume, the principal mechanism to import and export data with your docker container.
