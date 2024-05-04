# Create a function that accesses the Strava token needed for using the API

library(rStrava)
library(httr)

fetch_strava_token <- function() {
  strava_token <- httr::config(
    token = rStrava::strava_oauth(
      Sys.getenv("STRAVA_API_NAME"),
      Sys.getenv("STRAVA_API_CLIENT_ID"),
      Sys.getenv("STRAVA_API_SECRET_KEY"),
      app_scope = "activity:read_all",
      cache = TRUE)
  )
  return(strava_token)
}
