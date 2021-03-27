from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#Set up YouTube credentials
DEVELOPER_KEY = 'enter api key'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)


# -------------Build YouTube Search------------#
def youtubeSearch(query, max_results=1000, order="date"):
 NEXT_PAGE_TOKEN = None

 items = []

 while (True):

  search_response = youtube.search().list(
   q=query,
   type="video",
   pageToken=NEXT_PAGE_TOKEN,
   order=order,
   part="id,snippet",
   maxResults=max_results).execute()

  # Assign first page of results (items) to item variable

  NEXT_PAGE_TOKEN = search_response.get('nextPageToken')
  items += search_response['items']

  if (NEXT_PAGE_TOKEN is None) or (len(items) >= max_results):
   break

 return items


def storeResults(response):
 # create variables to store your values
 title = []
 channelId = []
 channelTitle = []
 categoryId = []
 videoId = []
 viewCount = []
 likeCount = []
 dislikeCount = []
 commentCount = []
 country = []
 category = []
 publishedDate = []
 videos = []
 publishedTime = []
 for search_result in response:
  if search_result["id"]["kind"] == "youtube#video":

   # append title and video for each item
   # title.append(search_result['snippet']['title'])
   videoId.append(search_result['id']['videoId'])

   # then collect stats on each video using videoId
   stats = youtube.videos().list(
    part='statistics, snippet',
    id=search_result['id']['videoId']).execute()
   DateTime = datetime.strptime(stats['items'][0]['snippet']['publishedAt'][:-1], \
                                "%Y-%m-%dT%H:%M:%S") + timedelta(hours=3, minutes=0)
   channelId.append(stats['items'][0]['snippet']['channelId'])
   channelTitle.append(stats['items'][0]['snippet']['channelTitle'])
   categoryId.append(stats['items'][0]['snippet']['categoryId'])
   category.append(categories_list[int(stats['items'][0]['snippet']['categoryId'])])
   # favoriteCount.append(stats['items'][0]['statistics']['favoriteCount'])

   publishedTime.append(DateTime.time())
   publishedDate.append(DateTime.date())
   # Not every video has likes/dislikes enabled so they won't appear in JSON response
   try:
    viewCount.append(stats['items'][0]['statistics']['viewCount'])
   except:
    # Good to be aware of Channels that turn off their Likes
    print("Video titled {0}, on Channel {1} Likes Count is not available".format(stats['items'][0]['snippet']['title'],
                                                                                 stats['items'][0]['snippet'][
                                                                                  'channelTitle']))
    print(stats['items'][0]['statistics'].keys())
    # Appends "Not Available" to keep dictionary values aligned
    viewCount.append(None)

   try:
    likeCount.append(stats['items'][0]['statistics']['likeCount'])
   except:
    # Good to be aware of Channels that turn off their Likes
    print("Video titled {0}, on Channel {1} Likes Count is not available".format(stats['items'][0]['snippet']['title'],
                                                                                 stats['items'][0]['snippet'][
                                                                                  'channelTitle']))
    print(stats['items'][0]['statistics'].keys())
    # Appends "Not Available" to keep dictionary values aligned
    likeCount.append(None)

   try:
    dislikeCount.append(stats['items'][0]['statistics']['dislikeCount'])
   except:
    # Good to be aware of Channels that turn off their Likes
    print(
     "Video titled {0}, on Channel {1} Dislikes Count is not available".format(stats['items'][0]['snippet']['title'],
                                                                               stats['items'][0]['snippet'][
                                                                                'channelTitle']))
    print(stats['items'][0]['statistics'].keys())
    dislikeCount.append(None)

   # Sometimes comments are disabled so if they exist append, if not append nothing...
   # It's not uncommon to disable comments, so no need to wrap in try and except
   if 'commentCount' in stats['items'][0]['statistics'].keys():
    commentCount.append(stats['items'][0]['statistics']['commentCount'])
   else:
    commentCount.append(0)

 # Break out of for-loop and if statement and store lists of values in dictionary
 youtube_dict = {'publishedDate': publishedDate, 'publishedTime': publishedTime, 'videoId': videoId,
                 'channelId': channelId, 'channelTitle': channelTitle,
                 'categoryId': categoryId, 'category': category,
                 'viewCount': viewCount, 'likeCount': likeCount, 'dislikeCount': dislikeCount,
                 'commentCount': commentCount}

 return youtube_dict

categories_list = {2: 'Autos & Vehicles',
1 :'Film & Animation',
10 : 'Music',
15 : 'Pets & Animals',
17 : 'Sports',
18 : 'Short Movies',
19 : 'Travel & Events',
20 : 'Gaming',
21 : 'Videoblogging',
22 : 'People & Blogs',
23 : 'Comedy',
24 : 'Entertainment',
25 : 'News & Politics',
26 : 'Howto & Style',
27 : 'Education',
28 : 'Science & Technology',
29 : 'Nonprofits & Activism',
30 : 'Movies',
31 : 'Anime/Animation',
32 : 'Action/Adventure',
33 : 'Classics',
34 : 'Comedy',
35 : 'Documentary',
36 : 'Drama',
37 : 'Family',
38 : 'Foreign',
39 : 'Horror',
40 : 'Sci-Fi/Fantasy',
41 : 'Thriller',
42 : 'Shorts',
43 : 'Shows',
44 : 'Trailers'
}

print("Please input your search query")
q=input()
#Run YouTube Search
response = youtubeSearch(q)
results = storeResults(response)

import pandas as pd
df_results = pd.DataFrame.from_dict(results)
df_results.shape
df_results.to_csv(q+'.csv')
