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
{
    "count": 846,
    "data": [
        {
            "edit_at": "https://github.com/2020PB/police-brutality/blob/master/reports/Arkansas.md",
            "date": "2020-06-01",
            "date_text": "June 1st",
            "name": "Law enforcement gas a crowd chanting “we want peace” right after exiting the building.",
            "state": "Arkansas",
            "city": "Bentonville",
            "links": [
                "https://twitter.com/courtenay_roche/status/1267653137969623040",
                "https://twitter.com/yagirlbrookie09/status/1267647898365427714",
                "https://www.4029tv.com/article/bentonville-police-deploy-tear-gas-on-protesters/32736629#"
            ]
        },
        ...
    ]
}
```

## TODOs
- add better filtering
- geo coding
- cron tasks for update

## Development
1. `docker-compose up`
2. visit `localhost/api/videos` in browser
3. to generate data, hop into the `backend` shell and run `GitHubAPI()`
    ```
    > docker-compose exec backend bash
    > python
    > from app.utils.github import GitHubAPI
    > GitHubAPI().main()
    ```
## Acknowledgements
- Everyone on the intrawebs submitting there time and videos to the [repo](https://github.com/2020PB/police-brutality)/reddit
