
from yt_dlp import YoutubeDL
import anthropic
import openai


# TODO: enter your openai API key, anthropic API key, and target channel
openai_client = openai.OpenAI(api_key="")
client = anthropic.Anthropic(api_key="")
channel = ""


def get_latest_video_transcript(channel):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': "/tmp/vid_audio.mp3",
        'playlistend': 1   # only download the first video in the playlist
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel, download=False)
        latest_video = info_dict['entries'][0]      # get the latest video
        ydl.download([latest_video['webpage_url']]) # download the audio of the latest video
    
    # go back to the start of the file
    f = open("/tmp/vid_audio.mp3", "rb")

    # get the transcript
    transcript = openai_client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        file=f,
    )
    return transcript.text


def summarize(transcript):
    anthropic_response = client.messages.create(
        # model=model,
        model = "claude-3-haiku-20240307",
        messages=[{"role":"user", "content": transcript}],
        max_tokens=2048,
        system="summarize the provided video transcript"
    )
    return anthropic_response.content[0].text


transcript = get_latest_video_transcript(channel)
summary = summarize(transcript)
print(summary)

