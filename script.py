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
titles = []
links = []

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
    print(title, link)
    
    response = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/"+title+".json?access_token="+MAPBOX_TOKEN+"&country=it&limit=1").json()
    if len(response["features"]) == 0:
        print("No results found.")
        continue
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
