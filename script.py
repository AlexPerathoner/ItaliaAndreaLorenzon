import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import re
import requests
import json
import os

MAPBOX_TOKEN = os.environ.get('ITALIAANDREALORENZON_MAPBOX_TOKEN')
YOUTUBE_TOKEN = os.environ.get('ITALIAANDREALORENZON_YOUTUBE_TOKEN')

#https://python.tutorialink.com/extract-individual-links-from-a-single-youtube-playlist-link-using-python/
url = 'https://www.youtube.com/playlist?list=PLokTFft4f9ScnHqKdGcIQFKlYGczbbUS9'
query = parse_qs(urlparse(url).query, keep_blank_values=True)
playlist_id = query["list"][0]

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = YOUTUBE_TOKEN)

request = youtube.playlistItems().list(
    part = "snippet",
    playlistId = playlist_id,
    maxResults = 50
)
response = request.execute()

playlist_items = []
while request is not None:
    response = request.execute()
    playlist_items += response["items"]
    request = youtube.playlistItems().list_next(request, response)

titles = []
links = []

print(f"total: {len(playlist_items)}")
for t in playlist_items:
    if(t["snippet"]["title"] != "Private video"):
        #https://stackoverflow.com/a/60738277/6884062
        titles.append(re.findall(r'\b[A-Z]+(?:\s+[A-Z]+)*\b', t["snippet"]["title"])[0])
        links.append('https://www.youtube.com/embed/' + t["snippet"]["resourceId"]["videoId"])

print(titles)
print(links)

features = []
for i in range(len(titles)):
    title = titles[i]
    link = links[i]

    dict = {}
    dict["type"] = "Feature"
    dict["properties"] = {}
    dict["properties"]["nome"] = title
    dict["properties"]["url"] = link
    
    response = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/"+title+".json?access_token="+MAPBOX_TOKEN+"&country=it&limit=1").json()
    dict["geometry"] = response["features"][0]["geometry"]
    features.append(dict)
    

geojson = {}
geojson["type"]= "FeatureCollection"
geojson["features"] = features

#print(geojson)

# write geojson to file data.geojson
with open('data.geojson', 'w') as outfile:
    json.dump(geojson, outfile)


print("Wrote to file.")