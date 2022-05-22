# L'Italia di Andrea Lorenzon

Live on [alexperathoner.github.io/ItaliaAndreaLorenzon/](https://alexperathoner.github.io/ItaliaAndreaLorenzon/).

[Andrea Lorenzon](https://www.youtube.com/c/AndreaLorenzon) is an Italian youtuber who has been uploading videos showing small towns in an interesting way. These videos are available [here](https://www.youtube.com/playlist?list=PLokTFft4f9ScnHqKdGcIQFKlYGczbbUS9).

## How it works

A Github Action is run every couple of days, and runs a python script.
<br>The script does the following things:
1. Use the [Youtube API](https://console.cloud.google.com/apis/library/youtube.googleapis.com) to get info about the videos in the [playlist](https://www.youtube.com/playlist?list=PLokTFft4f9ScnHqKdGcIQFKlYGczbbUS9).
2. Parse the town's name of each video
3. Use the [Mapbox geocoding API](https://docs.mapbox.com/api/search/geocoding/) to get the coordinates of each town
4. Create a geojson object with a point for each video, and adding video url and town name to their `properties` 
5. Save the geojson file

---

The website is a simple mapbox map showing Italy and loading the generated geojson file as data source. When clicking on a marker a popup is generated, showing the respective embedded video.