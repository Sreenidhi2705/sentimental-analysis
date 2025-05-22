# Step 1: Install necessary packages
!pip install --upgrade google-api-python-client textblob

# Step 2: Import libraries
from googleapiclient.discovery import build
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

# Step 3: Use your YouTube API Key
api_key = "AIzaSyDSMO3SPxC6zSTeL6LoJuXHeVM-v4iQgcE"
youtube = build('youtube', 'v3', developerKey=api_key)

# Step 4: Function to fetch comments
def get_comments(video_id, max_comments=100):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()

    while request and len(comments) < max_comments:
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
            if len(comments) >= max_comments:
                break
        if "nextPageToken" in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response["nextPageToken"],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break
    return comments

# Step 5: Sentiment analysis function
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Step 6: Choose a YouTube video ID
video_id = "dQw4w9WgXcQ"  # You can replace this with any YouTube video ID

# Step 7: Run analysis
comments = get_comments(video_id, max_comments=100)
df = pd.DataFrame(comments, columns=["Comment"])
df["Sentiment"] = df["Comment"].apply(get_sentiment)

# Step 8: Display a sample
print(df.head())

# Step 9: Pie chart
sentiment_counts = df["Sentiment"].value_counts()
colors = ['lightgreen', 'salmon', 'lightgrey']
plt.figure(figsize=(6,6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors)
plt.title("YouTube Comment Sentiment Distribution (Pie Chart)")
plt.show()

# Step 10: Bar chart
plt.figure(figsize=(6,4))
sentiment_counts.plot(kind='bar', color=colors)
plt.title("YouTube Comment Sentiment (Bar Chart)")
plt.xlabel("Sentiment")
plt.ylabel("Number of Comments")
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()
