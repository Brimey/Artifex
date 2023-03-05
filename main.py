import scrapetube as scraper
import requests
from bs4 import BeautifulSoup


def visit_url(channel: str) -> str:
    return 'https://www.youtube.com/{}/videos'.replace('{}', f'@{channel}')


def get_id(channel_url: str) -> str:
    content = BeautifulSoup(visit_url(requests.get(channel_url).content), 'lxml').find_all(
        'meta')

    for tag in content:
        if tag.get('itemprop') == 'channelId':
            return tag.get('content')


def scrape_videos(channel_id: str) -> dict:
    scraped_videos = scraper.get_channel(channel_id)
    video_data = {data['title']['runs'][0]['text']: {'url': f'https://www.youtube.com/watch?v={data["videoId"]}',
                                                     'duration': data['lengthText']['simpleText']} for data in
                  scraped_videos}

    for title, scraped_data in video_data.items():
        minutes, seconds = scraped_data['duration'].split(':')
        video_data[title]['duration'] = (60 * int(minutes)) + int(seconds)

    return video_data


def find_longest_vid(videos: dict) -> str:
    return max(videos, key=lambda vid: videos.get(vid)['duration'])


def main():
    target_channels = input('Enter a channel name(s): ').split()
    print('Retrieving video(s)...')
    channel_data = {name: scrape_videos(get_id(visit_url(name))) for name in target_channels}

    for channel, vid_stats in channel_data.items():
        longest_vid = find_longest_vid(vid_stats)
        print(f'The longest video for "{channel}" is "{longest_vid}": {vid_stats[longest_vid]["url"]}')


main()
input()
