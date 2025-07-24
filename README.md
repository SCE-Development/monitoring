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

## Running Monitoring Locally in Dev Mode
- [ ] connect to the vpn
- [ ] run the below command in the monitoring folder
```
docker-compose -f docker-compose.dev.yml up --build
```
- [ ] visit http://localhost:3000 to see grafana
- [ ] visit http://localhost:9100 to see the status page
