# Import the necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URLs
wired_url = 'https://www.wired.com/category/artificial-intelligence/'
venture_beat_url = 'https://venturebeat.com/category/ai/'

# Create a list of URLs
urls = [wired_url, venture_beat_url]

# Create a list to hold the article data
data = []

# Loop through the list of URLs
for url in urls:
    print("Processing:", url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            if "wired.com" in url:
                page_titles = soup.find_all('h3', class_='SummaryItemHedBase-hiFYpQ cJGBzK summary-item__hed')
                page_links = soup.find_all('a', class_='SummaryItemHedLink-civMjp ejgyuy summary-item-tracking__hed-link summary-item__hed-link')

            elif "venturebeat.com" in url:
                page_titles = soup.find_all('a', class_='ArticleListing__title-link')
                page_links = soup.find_all('a', class_='ArticleListing__title-link', href=True)

            if not page_titles or not page_links:
                print("No articles found on", url)
            else:
                for title, link in zip(page_titles, page_links):
                    title_text = title.get_text().strip()
                    link_url = link['href']
                    data.append({'title': title_text, 'link': link_url})
        else:
            print(f"Error {response.status_code} while getting the page: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to get page: {url} due to {e}")

# Print the data list
df = pd.DataFrame(data)
df.to_csv('articles.csv', index=False)
# print(df)  # Print only first 10 rows

nextweb_url = 'https://thenextweb.com/artificial-intelligence'


# code to add to the df dataframe, example here is nextweb, just edit to your taste

# thenextweb
def add_nextweb_articles(df, nextweb_url):
    response = requests.get(nextweb_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the elements containing titles and links
    articles = soup.find_all('h4', class_='c-listArticle__heading')

    # Construct full URLs by prepending the domain to the relative URLs
    links = ['https://thenextweb.com' + article.find('a')['href'] for article in articles]
    titles = [article.text.strip() for article in articles]

    # Build a new dataframe from the scraped data
    nextweb_df = pd.DataFrame({
        'title': titles,
        'link': links
    })

    # Append the new dataframe to the given dataframe
    df = df._append(nextweb_df, ignore_index=True)

    return df


# Now you can use it like this:
df = add_nextweb_articles(df, nextweb_url)
# print(df)

aidaily_url = 'https://aidaily.co.uk/'

print(df)


