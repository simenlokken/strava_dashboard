// Load libraries

using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using System.Linq;

// Actual program

// Create a class called StravaFetcher which encapsulates the methods related to fetching data and saving it to a .csv file
public class StravaFetcher
{
    // Method, receives access token from Strava API
    public static async Task<string> FetchAccessToken()
    {
        // URL endpoint
        string authUrl = "https://www.strava.com/oauth/token";
        // Environment variables
        string clientId = Environment.GetEnvironmentVariable("STRAVA_CLIENT_ID") ?? "";
        string clientSecret = Environment.GetEnvironmentVariable("STRAVA_CLIENT_SECRET") ?? "";
        string refreshToken = Environment.GetEnvironmentVariable("STRAVA_REFRESH_TOKEN") ?? "";

        // HttpClient is a class for sending HTTP requests
        using HttpClient client = new HttpClient();

        // Set a payload variable containing key-value pairs
        var payload = new FormUrlEncodedContent(new[]
        {
            new KeyValuePair<string, string>("client_id", clientId),
            new KeyValuePair<string, string>("client_secret", clientSecret),
            new KeyValuePair<string, string>("refresh_token", refreshToken),
            new KeyValuePair<string, string>("grant_type", "refresh_token"),
        });

        // Sends the request to the API with URL and payload, stored in variable called response
        HttpResponseMessage response = await client.PostAsync(authUrl, payload);

        // Error handling
        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Failed to fetch access token. Status Code: {response.StatusCode}");
        }

        // Fetches the content in the API response as a string called results
        string result = await response.Content.ReadAsStringAsync();
        JsonDocument json = JsonDocument.Parse(result);
        string accessToken = json.RootElement.GetProperty("access_token").GetString() ?? "";

        return accessToken;
    }

    public static async Task<List<Dictionary<string, object>>> GetStravaActivities(string accessToken)
    {
        var activities = new List<Dictionary<string, object>>();
        int page = 1;
        int perPage = 200;

        using HttpClient client = new HttpClient();

        while (true)
        {
            string url = $"https://www.strava.com/api/v3/athlete/activities?per_page={perPage}&page={page}";
            client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

            HttpResponseMessage response = await client.GetAsync(url);

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine($"Error fetching activities: {response.StatusCode}");
                break;
            }

            string result = await response.Content.ReadAsStringAsync();
            JsonDocument json = JsonDocument.Parse(result);

            if (json.RootElement.GetArrayLength() == 0) break;

            foreach (var activity in json.RootElement.EnumerateArray())
            {
                var activityDict = new Dictionary<string, object>();
                foreach (var property in activity.EnumerateObject())
                {
                    activityDict[property.Name] = property.Value.ToString();
                }
                activities.Add(activityDict);
            }

            page++;
        }

        return activities;
    }

    // New method to save activities to a CSV file
    public static void SaveActivitiesToCsv(List<Dictionary<string, object>> activities, string filePath)
    {
        if (activities.Count == 0)
        {
            Console.WriteLine("No activities to save.");
            return;
        }

        // Get headers from the first activity
        var headers = activities[0].Keys;

        using (var writer = new StreamWriter(filePath))
        {
            // Write headers
            writer.WriteLine(string.Join(",", headers));

            // Write each activity
            foreach (var activity in activities)
            {
                var row = headers.Select(header => activity.ContainsKey(header) ? activity[header].ToString() : "");
                writer.WriteLine(string.Join(",", row));
            }
        }

        Console.WriteLine($"Data saved to {filePath}");
    }
}

public class Program
{
    public static async Task Main(string[] args)
    {
        try
        {
            // Fetch access token
            string accessToken = await StravaFetcher.FetchAccessToken();

            // Fetch activities using access token
            var activities = await StravaFetcher.GetStravaActivities(accessToken);

            // Save activities to a CSV file
            string filePath = "strava_activities.csv";
            StravaFetcher.SaveActivitiesToCsv(activities, filePath);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }
}