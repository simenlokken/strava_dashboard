library(purrr)
source("code/functions/fetch_strava_token.R")

# Save Strava token as an object
strava_token <- fetch_strava_token()

# Fetch the Strava activities as a list and save as an object
activities <- rStrava::get_activity_list(
  stoken = strava_token,
  after = as.Date("2023-01-01"),
  before = as.Date(Sys.time())
)

# Helper function to handle lists of unequal length when creating a dataframe
convert_list_to_tbl <- function(activities) {
  tryCatch({
    as.data.frame(t(unlist(activities)), stringsAsFactors = FALSE)
  }, error = function(e) {
    NA
  })
}

# Apply convert_list_to_tbl on the list and create a data frame of the activities
activities_raw <- purrr::map_df(
  activities,
  convert_list_to_tbl
)

# Save the raw data
readr::write_csv(
  activities_raw,
  file = "raw_data/raw_data.csv"
)

# Remove temporary variables
remove(strava_token)
remove(activities)
