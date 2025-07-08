# Monitoring

The SCE Monitoring stack. A diagram of how we aggregate Prometheus metrics into grafana is below:

![Monitoring Architecture](https://github.com/SCE-Development/monitoring/assets/36345325/299afe97-285e-4fd4-9f6d-2d9010c5e576)


## How does this work?
This use of Grafana/Prometheus/Discord bot alerting is covered in
 this [YouTube series](https://www.youtube.com/watch?v=L17-EN4HcY0)

## Setting things up
- [ ] Create an ssh key that lives at the location `~/.ssh/id_ed25519`. This
 key should allow for automatic access to the clark machine. To allow for
 automatic access, run:
```sh
ssh-copy-id -i ~/.ssh/id_ed25519 sce@10.31.5.15
```
- [ ] Get a webhook url for your Discord server and create a `.env` file
 in this project's directory like below:
```sh
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/SERVER_ID/OTHER_STUFF
```
- [ ] Run the project with
```sh
docker-compose up -d
```
**Note:** if you are not planning to run grafana behind nginx,
 expose port 3000 in the yml file and remove the `GF_SERVER_ROOT_URL`
 entry in the environment section for the Grafana container.

## Running Monitoring Locally
- In the `docker-compose.yml` file, under the `grafana` service, comment out the environment and the first two volumes, then add ports.
 Your Grafana section should now look like this:
 ```
 grafana:
    # environment:
    #   - GF_SERVER_ROOT_URL=%(protocol)s://%(domain)s/grafana/
    build:
      context: ./grafana/
      dockerfile: ./Dockerfile
    restart: always
    volumes:
      # - /etc/localtime:/etc/localtime:ro
      # - /etc/timezone:/etc/timezone:ro
      - grafana-data:/var/lib/grafana
    ports:
      - 3000:3000
```

- In the `docker-compose.yml` file, under the `poweredge-2950-node-exporter` service, comment out the volumes.
 Your poweredge-2950-node-exporter section should now look like this:
 ```
 poweredge-2950-node-exporter:
    image: quay.io/prometheus/node-exporter:latest
    command:
      - '--path.rootfs=/host'
    pid: host
    restart: unless-stopped
    # volumes:
      # - '/:/host:ro,rslave'
```
- In the `docker-compose.yml` file, under the `portainer` service, comment out the entire service.
 Your portainer section should now look like this:
 ```
  # portainer:
  #   image: portainer/portainer-ce:lts
  #   container_name: portainer
  #   volumes:
  #     - "/var/run/docker.sock:/var/run/docker.sock"
  #     - portainer_data:/data
```
 
 - In the `docker-compose.yml` file, at the very end of the file are the `networks` comment this entire part out. 
 Your networks section should now look like this:
 ```
# networks: 
#   default:
#     external: 
#       name: poweredge
```

- Goto file `grafana/provisioning/datasources/all.yml`, change the url of "http://prometheus-federated:9090" to `"http://one.sce/prometheus"`.
 
- Finally, run the project with
```sh
docker-compose up -build
```