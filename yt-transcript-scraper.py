from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from decouple import config
import json

# YouTube API setup
api_key = config('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
# Replace with the channel's ID
channel_id = 'UCWsslCoN3b_wBaFVWK_ye_A'

# Function to get video IDs from a channel
def get_video_ids(channel_id):
    video_ids = []
    request = youtube.search().list(part='id', channelId=channel_id, maxResults=50, order='date', type='video')
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['id']['videoId'])
    return video_ids

# Function to get channel name
def get_channel_name(channel_id):
    request = youtube.channels().list(part='snippet', id=channel_id)
    response = request.execute()
    return response['items'][0]['snippet']['title']

# Function to get transcripts
def get_transcripts(video_ids):
    transcripts = {}
    transcript_status = {}
    for video_id in video_ids:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_generated_transcript(['en']).fetch()
            transcripts[video_id] = transcript
            transcript_status[video_id] = "Available"
        except Exception as e:
            print(f"Error in fetching transcript for video {video_id}: {e}")
            transcript_status[video_id] = "Not Available"
    return transcripts, transcript_status


# Extract video IDs, transcripts, and channel name
video_ids = get_video_ids(channel_id)
channel_name = get_channel_name(channel_id)
transcripts, transcript_status = get_transcripts(video_ids)

# Save transcripts to a JSON file
transcript_file_name = f'transcripts_{channel_name}.json'
with open(transcript_file_name, 'w') as file:
    json.dump(transcripts, file)

# Save transcript status to a separate file
status_file_name = f'transcript_status_{channel_name}.json'
with open(status_file_name, 'w') as file:
    json.dump(transcript_status, file)

print(f"Transcripts extracted and saved in {transcript_file_name}")
print(f"Transcript status saved in {status_file_name}")
