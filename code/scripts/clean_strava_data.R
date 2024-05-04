# Load the raw data
readr::read_csv("raw_data/raw_data.csv")

# Clean data
activities_cleaned <- activities_raw |> 
  as_tibble() |> # Create a tibble for readability
  select(
    name:sport_type, 
    average_speed:kilojoules, 
    has_heartrate, 
    average_heartrate, 
    max_heartrate, 
    start_date_local) |> 
  mutate(
    across(
      c(
        "distance", "moving_time", "elapsed_time", "total_elevation_gain",
        "average_speed", "max_speed", "kilojoules", "average_heartrate"
      ),
      ~ as.double(.x)
    ),
    has_heartrate = as_factor(has_heartrate),
    sport_type = as_factor(case_when(
      sport_type == "VirtualRide" ~ "Virtual Ride")
    )
  ) |>
  rename(
    session = name,
    avg_hr_bpm = average_heartrate,
    max_hr_bpm = max_heartrate,
    has_hr = has_heartrate,
    kcal_exp = kilojoules,
    elev_gain_m = total_elevation_gain,
  ) |> 
  mutate(
    distance_km = round(distance / 1000, 2),
    moving_time_min = round(moving_time / 60, 2),
    elapsed_time_min = round(elapsed_time / 60, 2),
    avg_speed_kmh = round(average_speed * 3.6, 2),
    max_speed_kmh = round(max_speed * 3.6, 2),
    elev_gain_m_per_min = round(elev_gain_m / moving_time_min, 2),
    start_date_local = gsub("Z$", "", start_date_local)
  ) |>
  separate(start_date_local, into = c("date", "time"), sep = "T") |> 
  mutate(
    date = as.Date(date),
    time = hms(time),
    weekday = wday(date, label = TRUE),
    month = month(date, label = TRUE),
    year = year(date)
  ) |> 
  select(
    -c(distance, moving_time, elapsed_time, average_speed, max_speed, type)
  )

# Save cleaned data
readr::write_csv(
  activities_cleaned,
  "data/cleaned_data.csv"
)

# Remove
remove(activities_cleaned)
remove(activities_raw)
remove(convert_list_to_tbl)
remove(fetch_strava_token)
