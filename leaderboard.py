import os
import requests
import json

# Load API key from GitHub Secrets
API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UC11c2OvSuXpK7c-T5jdSCzw"  # Replace with your actual YouTube channel ID

# YouTube API URL
YOUTUBE_API_URL = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=10"

def fetch_video_data():
    response = requests.get(YOUTUBE_API_URL)
    videos = response.json().get("items", [])

    video_stats = []
    for video in videos:
        if video["id"].get("videoId"):
            video_id = video["id"]["videoId"]
            title = video["snippet"]["title"]

            # Get video statistics
            stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
            stats_response = requests.get(stats_url).json()
            stats = stats_response.get("items", [])[0]["statistics"]

            video_stats.append({
                "title": title,
                "id": video_id,
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0))
            })

    return video_stats

def generate_markdown(video_stats):
    # Sort videos by views and likes
    top_views = sorted(video_stats, key=lambda x: x["views"], reverse=True)[:5]
    top_likes = sorted(video_stats, key=lambda x: x["likes"], reverse=True)[:5]

    # Find fastest-growing video
    fastest_growing = max(video_stats, key=lambda x: x["views"] / (x["likes"] + 1))  # Basic engagement ratio

    # Markdown Content
    markdown_content = "# 📊 YouTube Video Leaderboard\n\n"
    markdown_content += "## 🏆 Top 5 Most Viewed Videos\n"
    for vid in top_views:
        markdown_content += f"- [{vid['title']}](https://youtu.be/{vid['id']}) - {vid['views']} views\n"

    markdown_content += "\n## 🔥 Top 5 Most Liked Videos\n"
    for vid in top_likes:
        markdown_content += f"- [{vid['title']}](https://youtu.be/{vid['id']}) - {vid['likes']} likes\n"

    markdown_content += f"\n## 🚀 Fastest Growing Video\n"
    markdown_content += f"🔹 [{fastest_growing['title']}](https://youtu.be/{fastest_growing['id']}) - {fastest_growing['views']} views & {fastest_growing['likes']} likes\n"

    # Write to file
    with open("leaderboard.md", "w") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    video_data = fetch_video_data()
    generate_markdown(video_data)
