#!/usr/bin/python3
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Counts the number of occurrences of each word in the given subreddit and prints the results in descending order.

    :param subreddit: the name of the subreddit to search in (e.g. "python")
    :param word_list: a list of words to count the occurrences of
    :param after: the "after" parameter for pagination (optional, used for recursive calls)
    :param counts: a dictionary containing the counts for each word (optional, used for recursive calls)
    :return: None
    """
    if counts is None:
        counts = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}  # Reddit API requires a User-Agent header

    # Set the "after" parameter if it's provided
    params = {}
    if after:
        params["after"] = after

    # Send the request and handle the response
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return  # Invalid subreddit, do nothing
    data = response.json()

    # Count the occurrences of each word in the titles
    for post in data["data"]["children"]:
        title = post["data"]["title"].lower()
        for word in word_list:
            if word.lower() in title and not title.endswith(word.lower() + ".") and not title.endswith(word.lower() + "!") and not title.endswith(word.lower() + "_"):
                counts[word] = counts.get(word, 0) + title.count(word.lower())

    # Check if there are more pages to fetch
    if data["data"]["after"] is not None:
        # Recursively call the function with the "after" parameter
        count_words(subreddit, word_list, after=data["data"]["after"], counts=counts)
    else:
        # Print the counts in descending order
        for word, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            print(word.lower(), count)
count_words("python", ["python", "django", "flask", "sqlalchemy", "requests"])

