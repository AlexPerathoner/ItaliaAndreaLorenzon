# L'Italia di Andrea Lorenzon

Live on [alexperathoner.github.io/ItaliaAndreaLorenzon/](https://alexperathoner.github.io/ItaliaAndreaLorenzon/).

[Andrea Lorenzon](https://www.youtube.com/c/AndreaLorenzon) is an Italian youtuber who has been uploading videos showing small towns in an interesting way. These videos are available [here](https://www.youtube.com/watch?v=QP1nnmEdEAY&list=PLokTFft4f9SdCFrHp0A-Pu-gnWUdaYUHm).

## How it works

A Github Action is run every couple of days, and runs a python script, which does the following things:
1. Use the [Youtube API](https://console.cloud.google.com/apis/library/youtube.googleapis.com) to get info about the videos in the [playlist](https://www.youtube.com/playlist?list=PLokTFft4f9ScnHqKdGcIQFKlYGczbbUS9).
2. Parse the town's name from the title of each video
3. Use the [Mapbox geocoding API](https://docs.mapbox.com/api/search/geocoding/) to get the coordinates of each town
4. Create a geojson object with a point for each video, and adding its corresponding video url and town name to their `properties` 
5. Save the geojson file

---

The website is a simple mapbox map showing Italy and using the generated geojson file as data source. When clicking on a marker a popup is generated, using the properties to show an embedded video.
