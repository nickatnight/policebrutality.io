NOTE: this API is shutdown as of 11/01/2020

# :rotating_light: policebrutality.io

<p align="center">
<a href="https://github.com/nickatnight/policebrutality.io"><img alt="Build Status" src="https://github.com/nickatnight/policebrutality.io/workflows/build,%20test%20and%20deploy/badge.svg?branch=master"></a>
<a href="https://codecov.io/gh/nickatnight/policebrutality.io"><img alt="Actions Status" src="https://codecov.io/gh/nickatnight/policebrutality.io/branch/master/graph/badge.svg"></a>
<a href="https://github.com/nickatnight/policebrutality.io/releases"><img alt="Actions Status" src="https://img.shields.io/github/v/release/nickatnight/policebrutality.io"></a>
</p>

a REST api...that's all. All data generated from [here](https://github.com/2020PB/police-brutality)

## Stack
1. [Falcon](https://falcon.readthedocs.io/en/stable/) | backend api
2. [MongoDB](https://www.mongodb.com/) | data storage
3. [Nginx](https://www.nginx.com/) | web proxy
4. [Docker](https://www.docker.com/) | development
5. [Docker Swarm](https://docs.docker.com/engine/swarm/) | container orchestration

## Usage
```
> curl -XGET http://api.policebrutality.io/v2/videos
{
    "count": 846,
    "data": [
        {
            "id": "ar-bentonville-1",
            "edit_at": "https://github.com/2020PB/police-brutality/blob/master/reports/Arkansas.md",
            "date": "2020-06-01",
            "date_text": "June 1st",
            "name": "Law enforcement gas a crowd chanting “we want peace” right after exiting the building.",
            "state": "Arkansas",
            "city": "Bentonville",
            "description": "Some crazy description",
            "links": [
                {
                    "key": "1267653137969623040.mp4",
                    "link": "https://twitter.com/courtenay_roche/status/1267653137969623040",
                    "spaces_url": "https://prod-uploads-policebrutality.sfo2.digitaloceanspaces.com/1267653137969623040.mp4",
                    "text": "Unique New York"
                }, {
                    "key": "1267647898365427714.mp4",
                    "link": "https://twitter.com/yagirlbrookie09/status/1267647898365427714",
                    "spaces_url": "https://prod-uploads-policebrutality.sfo2.digitaloceanspaces.com/1267647898365427714.mp4",
                    "text": null
                },
            ],
        },
        ...
    ]
}
```

## Deployments (DigitalOcean)
- deployments are triggered via GitHub actions
- steps are: test/lint, build, deploy
- any merge to develop/master will deploy to staging/prod, respectively

## Development
1. create a `.env` file at the root dir: `mv .env_example .env`
2. `docker-compose up`
3. visit `localhost/v2/videos` in browser
4. to generate data, hop into the `backend` shell and run `GitHubAPI()`
    ```
    > docker-compose exec backend bash
    > python
    > from src.app import run
    > run()
    > from src.utils.github import GitHubAPI
    > GitHubAPI().main()
    ```

## TODOs
- add better filtering
- geo coding
- cron tasks for update
- add tests :white_check_mark:

## Acknowledgements
- Everyone on the intrawebs submitting there time and videos to the [repo](https://github.com/2020PB/police-brutality)/reddit
