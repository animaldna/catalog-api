# Cronenberg's Discogs API
This project is a "clone" of the public [Discogs API](https://api.discogs.com/) built using [FastAPI.](https://github.com/tiangolo/fastapi) Data is stored in [DynamoDB](https://aws.amazon.com/dynamodb/) using a single-table design. (Shout out to Alex DeBrie for putting together an excellent resource explaining [this tricky concept.](https://www.alexdebrie.com/posts/dynamodb-single-table/))

The API itself was actually a secondary focus; my main goals were to: 
1. Get hands-on experience with DynamoDB, specifically optimized table design
2. Have a "real world" project I could use to work with CircleCI, Terraform, and ECS. 
   
There's a very limited set of data. Data was generated with ______.

## Technologies
- Python 3.9
- fastAPI 0.70.1
- slowapi 0.1.5
- Uvicorn 0.16.0
- boto3 1.20.23
- DynamoDB

## Usage
As of this writing (Dec 2021), whatever version of this API that's working is hosted at [https://catalog-api.chloeboylan.work](https://catalog-api.chloeboylan.work). There are two sets of docs available at [/docs]() and [/redoc.]() I don't want to wake up to an absurd AWS bill, so it's rate-limited to _____ in case someone tries to blast it for whatever reason.

## TODOs
Right now I'm focused on building out a more production-ready CI/CD pipeline, so the TODOs below are back-burner. You can see what I'm working on in the [infrastructure repo]() for this project.

#### CircleCI
- [ ] Switch dev branch to EC2 runner
- [ ] Add Terraform job for dev env
- [ ] Add ecs-deploy for master branch
#### Routes
- [ ] /albums?genre="foo"&style="bar"
- [ ] /albums/latest
- [ ] /albums?artist=1234567 (alias for /artists/1234567/albums)
- [ ] /albums
- [ ] /artists
#### Misc.
- [ ] Logging
- [ ] Sorting
- [ ] Pagination

## Feedback
This is a personal project and a work in progress, but I'm always open to receiving any and all feedback about anything I'm working on. Feel free to email me or you can just open an issue and drop your thoughts.

## Author
Chloe Boylan

## License
Copyright © 2021 Chloe Boylan.
This project is MIT licensed.