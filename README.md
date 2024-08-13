Weather Api
====================

Fetch and return weather data.

Local setup
------------------

Requirements:
- Docker (built using Docker version 27.0.3)


Steps:
- First, in `/app/config.py` add your API_KEY for openweather. This should have access to the Onecall3.0 api subscription.
- In the terminal, at the top level of this project, run `docker build -t ocula_test .`
- Run `docker run -p 8000:8000 ocula_test`
- You should be able to now make requests to `http://127.0.0.1:8000/weather`

Example requests:

- POST: `curl -X POST "http://127.0.0.1:8000/weather?city=paris&day=2023-01-01"`
- Once this has been run, trying GET: `curl -X GET "http://127.0.0.1:8000/weather?city=paris&day=2023-01-01"` should return the expected data.



Thoughts/TODO
------------------

- Using the city name isn't ideal, since we then have to use that to fetch coordinates for the city. If this was a requirement and a production service, we would probably store the ISO city names and codes, allowing users to select from a search box and saving an API call to openweather.
- To make things quicker and more simple I've thrown all the db stuff into one file, but ideally models would be separate from the database fetching logic.
- The db code in general isn't perfect, I went for a quick setup but I probably shouldn't be calling `create_all` on every db action.
- Will require a Onecall3.0 api subscription with openweather (free for the first 1000 calls)
- Returning the "openweather api error" was more for my debugging than anything. In a real API we probably wouldn't want the user to know if our subscription has run out or something so we'd log it as an error and investigate.
- Probably most sensible to keep the temperature it in kelvin, but can have the frontend convert to other measures
- I took a swing at what we want to happen if we call to ingest data twice (it updates with latest), but this could be expensive if people spam it. We'd probably have a separate PATCH/PUT for that if needed.
- Could have used basic fastapi dependancy overrides for testdb, maybe should have, since now I'm patching every test which uses the db
- Decided not to do a proper database to save some time, instead just using local sqlite. I've named the test db differently to stop it interacting, but ideally this would be a completely separate instance.
- Having the API_KEY in code/baked into the docker image isn't good, but I didn't end up having time to deploy this and use proper secret management in the cloud.
- I had looked at using Github actions to build the docker image, but since I can't deploy I thought it wouldn't be necessary, so just added linting and testing
- I've added docstrings to response models so that we can see explanations on autocreated openapi/wagger docs