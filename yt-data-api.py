# Sample Python code for user authorization

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0" 

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  return build(API_SERVICE_NAME, API_VERSION,
      http=credentials.authorize(httplib2.Http()))

args = argparser.parse_args()
service = get_authenticated_service(args)
  

# Sample Python code for printing API response data

def print_results(results):
  for item in results['items']:
    if 'id' in item and isinstance(item['id'], dict):
      itemIdOrType = 'search result: '
    elif 'rating' in item:
      itemIdOrType = 'Rating: '
    else:
      itemIdOrType = item['id']

        
    title = ''
    snippet_properties = ['type', 'title', 'textDisplay', 'channelId', 'videoId', 'hl', 'gl', 'label']
    if 'snippet' in item:
      for i in range(0, len(snippet_properties)):
        if snippet_properties[i] in item['snippet']:
          title = item['snippet'][snippet_properties[i]]
          break
    else:       
      title = item['rating']
    print itemIdOrType.encode('utf-8') + ': ' + title.encode('utf-8')

    # This example retrieves the 25 most recent activities for the Google
# Developers channel. It retrieves the snippet and contentDetails parts for
# each activity resource.
def activities_list(service, part, channel_id, max_results):
  results = service.activities().list(
    channelId=channel_id,
    maxResults=max_results,
    part=part
  ).execute()

  print_results(results)

activities_list(service, 'snippet,contentDetails', 'UC_x5XG1OV2P6uZZ5FSM9Ttw', 25)

# This example retrieves the 25 most recent activities performed by the user
# authorizing the API request.
def activities_list_mine(service, part, max_results, mine):
  results = service.activities().list(
    maxResults=max_results,
    mine=mine,
    part=part
  ).execute()

  print_results(results)

activities_list_mine(service, 'snippet,contentDetails', 25, True)

# This example lists caption tracks available for the Volvo Trucks "Epic
# Split" commercial, featuring Jean-Claude Van Damme. (This video was selected
# because it has many available caption tracks and also because it is
# awesome.)
def captions_list(service, part, video_id):
  results = service.captions().list(
    part=part,
    videoId=video_id
  ).execute()

  print_results(results)

captions_list(service, 'snippet', 'M7FIvfx5J10')

# This example retrieves channel data for the GoogleDevelopers YouTube
# channel. It uses the id request parameter to identify the channel by its
# YouTube channel ID.
def channels_list_by_id(service, part, id):
  results = service.channels().list(
    id=id,
    part=part
  ).execute()

  print_results(results)

channels_list_by_id(service, 'snippet,contentDetails,statistics', 'UC_x5XG1OV2P6uZZ5FSM9Ttw')

# This example retrieves channel data for the GoogleDevelopers YouTube
# channel. It uses the forUsername request parameter to identify the channel
# by its YouTube username.
def channels_list_by_username(service, part, for_username):
  results = service.channels().list(
    forUsername=for_username,
    part=part
  ).execute()

  print_results(results)

channels_list_by_username(service, 'snippet,contentDetails,statistics', 'GoogleDevelopers')

# This example retrieves the channel data for the authorized user's YouTube
# channel. It uses the mine request parameter to indicate that the API should
# only return channels owned by the user authorizing the request.
def channels_list_mine(service, part, mine):
  results = service.channels().list(
    mine=mine,
    part=part
  ).execute()

  print_results(results)

channels_list_mine(service, 'snippet,contentDetails,statistics', True)

# This example retrieves the channel sections shown on the Google Developers
# channel, using the channelId request parameter to identify the channel.
def channel_sections_list_by_id(service, part, channel_id):
  results = service.channelSections().list(
    channelId=channel_id,
    part=part
  ).execute()

  print_results(results)

channel_sections_list_by_id(service, 'snippet,contentDetails', 'UC_x5XG1OV2P6uZZ5FSM9Ttw')

# This example retrieves the channel sections shown on the authorized user's
# channel. It uses the mine request parameter to indicate that the API should
# return channel sections on that channel.
def channel_sections_list_mine(service, part, mine):
  results = service.channelSections().list(
    mine=mine,
    part=part
  ).execute()

  print_results(results)

channel_sections_list_mine(service, 'snippet,contentDetails', True)

# This example retrieves comment replies for a specified comment, which is
# identified by the parentId request parameter. In this example, the parent
# comment is the first comment on a video about Apps Script. The video was
# chosen because this particular comment had multiple replies (in multiple
# languages) and also because Apps Script is really useful.
def comments_list(service, part, parent_id):
  results = service.comments().list(
    parentId=parent_id,
    part=part
  ).execute()

  print_results(results)

comments_list(service, 'snippet', 'z13icrq45mzjfvkpv04ce54gbnjgvroojf0')

# This example retrieves all comment threads associated with a particular
# channel. The response could include comments about the channel or about the
# channel's videos. The request's allThreadsRelatedToChannelId parameter
# identifies the channel.
def comment_threads_list_all_threads_by_channel_id(service, part, all_threads_related_to_channel_id):
  results = service.commentThreads().list(
    allThreadsRelatedToChannelId=all_threads_related_to_channel_id,
    part=part
  ).execute()

  print_results(results)

comment_threads_list_all_threads_by_channel_id(service, 'snippet,replies', 'UC_x5XG1OV2P6uZZ5FSM9Ttw')

# This example retrieves all comment threads about the specified channel. The
# request's channelId parameter identifies the channel. The response does not
# include comments left on videos that the channel uploaded.
def comment_threads_list_by_channel_id(service, part, channel_id):
  results = service.commentThreads().list(
    channelId=channel_id,
    part=part
  ).execute()

  print_results(results)

comment_threads_list_by_channel_id(service, 'snippet,replies', 'UCAuUUnT6oDeKwE6v1NGQxug')

# This example retrieves all comment threads associated with a particular
# video. The request's videoId parameter identifies the video.
def comment_threads_list_by_video_id(service, part, video_id):
  results = service.commentThreads().list(
    part=part,
    videoId=video_id
  ).execute()

  print_results(results)

comment_threads_list_by_video_id(service, 'snippet,replies', 'm4Jtj2lCMAA')

# This example retrieves a list of application languages that the YouTube
# website supports. The example sets the hlparameter value to es_MX,
# indicating that text values in the API response should be provided in that
# language. That parameter's default value is en_US.
def i18n_languages_list(service, part, hl):
  results = service.i18nLanguages().list(
    hl=hl,
    part=part
  ).execute()

  print_results(results)

i18n_languages_list(service, 'snippet', 'es_MX')

# This example retrieves a list of content regions that the YouTube website
# supports. The example sets the hlparameter value to es_MX, indicating that
# text values in the API response should be provided in that language. That
# parameter's default value is en_US.
def i18n_regions_list(service, part, hl):
  results = service.i18nRegions().list(
    hl=hl,
    part=part
  ).execute()

  print_results(results)

i18n_regions_list(service, 'snippet', 'es_MX')

# This example retrieves the list of videos in a specified playlist. The
# request's playlistId parameter identifies the playlist.

# Note that the API
# response does not include metadata about the playlist itself, such as the
# playlist's title and description. Additional metadata about the videos in
# the playlist can also be retrieved using the videos.listmethod.
def playlist_items_list_by_playlist_id(service, part, max_results, playlist_id):
  results = service.playlistItems().list(
    maxResults=max_results,
    part=part,
    playlistId=playlist_id
  ).execute()

  print_results(results)

playlist_items_list_by_playlist_id(service, 'snippet,contentDetails', 25, 'PLBCF2DAC6FFB574DE')

# This example retrieves playlists owned by the YouTube channel that the
# request's channelId parameter identifies.
def playlists_list_by_channel_id(service, part, channel_id, max_results):
  results = service.playlists().list(
    channelId=channel_id,
    maxResults=max_results,
    part=part
  ).execute()

  print_results(results)

playlists_list_by_channel_id(service, 'snippet,contentDetails', 'UC_x5XG1OV2P6uZZ5FSM9Ttw', 25)

# This example retrieves playlists created in the authorized user's YouTube
# channel. It uses the mine request parameter to indicate that the API should
# only return playlists owned by the user authorizing the request.
def playlists_list_mine(service, part, mine):
  results = service.playlists().list(
    mine=mine,
    part=part
  ).execute()

  print_results(results)

playlists_list_mine(service, 'snippet,contentDetails', True)

# This example retrieves the first 25 search results associated with the
# keyword surfing. Since the request doesn't specify a value for the type
# request parameter, the response can include videos, playlists, and channels.
def search_list_by_keyword(service, part, max_results, q, type):
  results = service.search().list(
    maxResults=max_results,
    part=part,
    q=q,
    type=type
  ).execute()

  print_results(results)

search_list_by_keyword(service, 'snippet', 25, 'surfing', 'video')

# This example retrieves search results associated with the keyword surfing
# that also specify in their metadata a geographic location within 10 miles of
# the point identified by the location parameter value. (The sample request
# specifies a point on the North Shore of Oahu, Hawaii . The request retrieves
# the top five results, which is the default number returned when the maxResults parameter is not
# specified.
def search_list_by_location(service, part, location, location_radius, q, type):
  results = service.search().list(
    location=location,
    locationRadius=location_radius,
    part=part,
    q=q,
    type=type
  ).execute()

  print_results(results)

search_list_by_location(service, 'snippet', '21.5922529,-158.1147114', '10mi', 'surfing', 'video')

# This example retrieves a list of acdtive live broadcasts (see the eventType
# parameter value) that are associated with the keyword news. Since the
# eventType parameter is set, the request must also set the type parameter
# value to video.
def search_list_live_events(service, part, event_type, max_results, q, type):
  results = service.search().list(
    eventType=event_type,
    maxResults=max_results,
    part=part,
    q=q,
    type=type
  ).execute()

  print_results(results)

search_list_live_events(service, 'snippet', 'live', 25, 'news', 'video')

# This example searches within the authorized user's videos for videos that
# match the keyword fun. The forMine parameter indicates that the response
# should only search within the authorized user's videos. Also, since this
# request uses the forMine parameter, it must also set the type parameter
# value to video.

# If you have not uploaded any videos associated with that
# term, you will not see any items in the API response list.
def search_list_mine(service, part, max_results, for_mine, q, type):
  results = service.search().list(
    maxResults=max_results,
    forMine=for_mine,
    part=part,
    q=q,
    type=type
  ).execute()

  print_results(results)

search_list_mine(service, 'snippet', 25, True, 'fun', 'video')

# This example sets the relatedToVideoId parameter to retrieve a list of
# videos related to that video. Since the relatedToVideoId parameter is set,
# the request must also set the type parameter value to video.
def search_list_related_videos(service, part, related_to_video_id, type):
  results = service.search().list(
    part=part,
    relatedToVideoId=related_to_video_id,
    type=type
  ).execute()

  print_results(results)

search_list_related_videos(service, 'snippet', 'Ks-_Mh1QhMc', 'video')

# This example retrieves a list of channels that the specified channel
# subscribes to. In this example, the API response lists channels to which the
# GoogleDevelopers channel subscribes.
def subscriptions_list_by_channel_id(service, part, channel_id):
  results = service.subscriptions().list(
    channelId=channel_id,
    part=part
  ).execute()

  print_results(results)

subscriptions_list_by_channel_id(service, 'snippet,contentDetails', 'UC_x5XG1OV2P6uZZ5FSM9Ttw')

# This example determines whether the user authorizing the API request
# subscribes to the channel that the forChannelId parameter identifies. To
# check whether another channel (instead of the authorizing user's channel)
# subscribes to the specified channel, remove the mine parameter from this
# request and add the channelId parameter instead.

# In this example, the API
# response contains one item if you subscribe to the GoogleDevelopers channel.
# Otherwise, the request does not return any items.
def subscriptions_list_for_channel_id(service, part, for_channel_id, mine):
  results = service.subscriptions().list(
    forChannelId=for_channel_id,
    mine=mine,
    part=part
  ).execute()

  print_results(results)

subscriptions_list_for_channel_id(service, 'snippet,contentDetails', 'UC_x5XG1OV2P6uZZ5FSM9Ttw', True)

# This example uses the mySubscribers parameter to retrieve the list of
# channels to which the authorized user subscribes.
def subscriptions_list_my_subscribers(service, part, my_subscribers):
  results = service.subscriptions().list(
    mySubscribers=my_subscribers,
    part=part
  ).execute()

  print_results(results)

subscriptions_list_my_subscribers(service, 'snippet,contentDetails,subscriberSnippet', True)

# This example uses the mine parameter to retrieve a list of channels that
# subscribe to the authenticated user's channel.
def subscriptions_list_my_subscriptions(service, part, mine):
  results = service.subscriptions().list(
    mine=mine,
    part=part
  ).execute()

  print_results(results)

subscriptions_list_my_subscriptions(service, 'snippet,contentDetails', True)

# This example shows how to retrieve a list of reasons that can be used to
# report abusive videos. You can retrieve the text labels in other languages
# by specifying a value for the hl request parameter.
def video_abuse_report_reasons_list(service, part):
  results = service.videoAbuseReportReasons().list(
    part=part
  ).execute()

  print_results(results)

video_abuse_report_reasons_list(service, 'snippet')

# This example retrieves a list of categories that can be associated with
# YouTube videos in the United States. The regionCode parameter specifies the
# country for which categories are being retrieved.
def video_categories_list(service, part, region_code):
  results = service.videoCategories().list(
    part=part,
    regionCode=region_code
  ).execute()

  print_results(results)

video_categories_list(service, 'snippet', 'US')

# This example uses the regionCode to retrieve a list of categories that can
# be associated with YouTube videos in Spain. It also uses the hl parameter to
# indicate that text labels in the response should be specified in Spanish.
def video_categories_list_for_region(service, part, hl, region_code):
  results = service.videoCategories().list(
    hl=hl,
    part=part,
    regionCode=region_code
  ).execute()

  print_results(results)

video_categories_list_for_region(service, 'snippet', 'es', 'ES')

# This example retrieves information about a specific video. It uses the id
# parameter to identify the video.
def videos_list_by_id(service, part, id):
  results = service.videos().list(
    id=id,
    part=part
  ).execute()

  print_results(results)

videos_list_by_id(service, 'snippet,contentDetails,statistics', 'Ks-_Mh1QhMc')

# This example retrieves a list of YouTube's most popular videos. The regionCode parameter
# identifies the country for which you are retrieving videos. The sample code
# is set to default to return the most popular videos in the United States.
# You could also use the videoCategoryId parameter to retrieve the most
# popular videos in a particular category.
def videos_list_most_popular(service, part, chart, region_code, video_category_id):
  results = service.videos().list(
    chart=chart,
    regionCode=region_code,
    part=part,
    videoCategoryId=video_category_id
  ).execute()

  print_results(results)

videos_list_most_popular(service, 'snippet,contentDetails,statistics', 'mostPopular', 'US', '')

# This example retrieves information about a group of videos. The id parameter
# value is a comma-separated list of YouTube video IDs. You might issue a
# request like this to retrieve additional information about the items in a
# playlist or the results of a search query.
def videos_list_multiple_ids(service, part, id):
  results = service.videos().list(
    id=id,
    part=part
  ).execute()

  print_results(results)

videos_list_multiple_ids(service, 'snippet,contentDetails,statistics', 'Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI')

# This example retrieves a list of videos liked by the user authorizing the
# API request. By setting the rating parameter value to dislike, you could
# also use this code to retrieve disliked videos.
def videos_list_my_rated_videos(service, part, my_rating):
  results = service.videos().list(
    myRating=my_rating,
    part=part
  ).execute()

  print_results(results)

videos_list_my_rated_videos(service, 'snippet,contentDetails,statistics', 'like')

# This example retrieves the rating that the user authorizing the request gave
# to a particular video. In this example, the video is of Amy Cuddy's TED talk
# about body language.
def videos_get_rating(service, id):
  results = service.videos().getRating(
    id=id
  ).execute()

  print_results(results)

videos_get_rating(service, 'Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI')
