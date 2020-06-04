# :rotating_light: policebrutality.io

a REST api...that's all. All data generated from [here](https://github.com/2020PB/police-brutality)

## Stack
1. [Falcon](https://falcon.readthedocs.io/en/stable/) | backend api
2. [MongoDB](https://www.mongodb.com/) | data storage
3. [Nginx](https://www.nginx.com/) | web proxy
4. [Docker](https://www.docker.com/) | development
5. [Docker Swarm](https://docs.docker.com/engine/swarm/) | container orchestration

## Usage
```
> curl -XGET http://staging.policebrutality.io/api/videos
{"count": 0, "data": [{"city": "Huntsville", "link": "https://twitter.com/ETfonehome97/status/1267657232411435008", "state": "Alabama", "title": "Law enforcement shove woman and she is seemingly trampled | June 1st"},]}
```

## TODOs
- add better filtering
- geo coding
- cron tasks for update

## Development
1. `docker-compose up`
2. visit `localhost/api/videos` in browser

## Acknowledgements
- Everyone on the intrawebs submitting there time and videos to the repo/reddit
