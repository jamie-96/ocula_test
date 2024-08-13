Weather Api
====================

Fetch and return weather data.

Local setup
------------------

- Python version 3.10



Task thoughts/TODO
------------------

- Thought about downloading the city id json to use the api, loaded into db on startup. Since it was quite large, I added it to the README, but 
- To make things quicker and more simple I've thrown all the db stuff into one file
- Ensure you have a Onecall3.0 api subscription with openweather (free for the first 1000 calls)
- returning the "openweather api error" was more for my debugging than anything. In a real API we probably wouldn't want the user to know if our subscription has run out or something so we'd log it as an error and investigate.
- probably most sensible to keep it in kelvin, but can have the frontend convert to other measures
- what happens if you post twice
- Could have used basic fastapi dependancy overrides for testdb, maybe should have, since now I'm patching every test which uses the db
- Decided not to do a proper database to save some time, instead just using local sqlite. I've named the test db differently to stop it interacting, but ideally this would be a completely separate instance.
- Decided not to make city and date update if added again, though it does add a second db call.
