# Strava Dashboard

## Information

Using the Strava v3 API, fetching activities from a Strava account to create a dashboard in Strava/Tableau/others.

For replication, see code. To set up a Strava application, see Strava v3 API documentation but also see Medium for several articles describing in detail how to perform the whole process.

## Code

**fetch_strava_data.py** fetches an access token using a refresh token from a Strava application, then fetching all activities from a Strava account.

**process_strava_data.py** processes the data and saves it locally.
