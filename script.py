import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import re
import requests
import json
import os

MAPBOX_TOKEN = os.environ.get('ITALIAANDREALORENZON_MAPBOX_TOKEN')
YOUTUBE_TOKEN = os.environ.get('ITALIAANDREALORENZON_YOUTUBE_TOKEN')

#https://python.tutorialink.com/extract-individual-links-from-a-single-youtube-playlist-link-using-python/
urls = ['https://www.youtube.com/watch?v=QP1nnmEdEAY&list=PLokTFft4f9SdCFrHp0A-Pu-gnWUdaYUHm&pp=iAQB', # le città
        'https://www.youtube.com/watch?v=hUOCOnynjWM&list=PLokTFft4f9SdmA43ku7l3fZf0JsIP_Il5', # borghi più fescion
        'https://www.youtube.com/watch?v=XXDZxA7YVlg&list=PLokTFft4f9SdeRp88zb9fh0YMTV79bDNY', # guide per chi non ha tempo da perdere
        'https://www.youtube.com/watch?v=e7N6Jhfq8uU&list=PLokTFft4f9Scm-z4BRkk7bW4pUo-tpPB_&pp=iAQB', # puglia
        'https://www.youtube.com/watch?v=33nnoaBki_8&list=PLokTFft4f9SfPyx_ReqcAHjp02jxw12kc&pp=iAQB', # trentino alto adige
        'https://www.youtube.com/watch?v=MscZgGxSErM&list=PLokTFft4f9SdlJ8K87td26tY1F1IjnAdF&pp=iAQB', # umbria
        'https://www.youtube.com/watch?v=hKHt54JBHXw&list=PLokTFft4f9SdoA2j1O7ytKgF2GvZ-2mvm&pp=iAQB', # toscana
        'https://www.youtube.com/watch?v=uQspCBa__c0&list=PLokTFft4f9ScnUIuKhl5sTpfDeX1xNvXm&pp=iAQB', # veneto
        'https://www.youtube.com/watch?v=QP1nnmEdEAY&list=PLokTFft4f9Sdnz532tDMQITG6FqiWWEvZ&pp=iAQB', # emilia romagna
        'https://www.youtube.com/watch?v=cYSkKnAIZiQ&list=PLokTFft4f9SfAvfTR_4_NssXFPknqPYnZ&pp=iAQB', # borghi più mai sentiti
        ]

results = {}

for url in urls:
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

    print(f"items in playlist {url}: {len(playlist_items)}")
    for t in playlist_items:
        if(t["snippet"]["title"] != "Private video"):
            #https://stackoverflow.com/a/60738277/6884062
            titles_in_link = re.findall(r'\b[A-Z]+(?:\s+[A-Z]+)*\b', t["snippet"]["title"])
            for title in titles_in_link:
                if title not in results:
                    results[title] = []
                results[title].append('https://www.youtube.com/embed/' + t["snippet"]["resourceId"]["videoId"])

features = []
for (title, links) in results.items():
    feat = {}
    feat["type"] = "Feature"
    feat["properties"] = {}
    feat["properties"]["nome"] = title
    feat["properties"]["url"] = links
    print(title, links)
    
    response = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/"+title+".json?access_token="+MAPBOX_TOKEN+"&country=it&limit=1").json()
    if ("features" not in response) or len(response["features"]) == 0:
        print("No results found.")
        continue
    feat["geometry"] = response["features"][0]["geometry"]
    features.append(feat)
    

geojson = {}
geojson["type"]= "FeatureCollection"
geojson["features"] = features

#print(geojson)

# write geojson to file data.geojson
with open('data.geojson', 'w') as outfile:
    json.dump(geojson, outfile)


print("Wrote to file.")
