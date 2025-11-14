"""This project scapes The What's On Glasgow page for events 
and saves the event title, date, location, description, and link 
to a CSV file."""

import requests
from bs4 import BeautifulSoup
import csv

# Fetch website
url = "https://www.whatsonglasgow.co.uk/events/"
response = requests.get(url)
html_content = response.text

if response.status_code == 200:

    # Parse website html
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all event cards
    event_cards = soup.find_all("div", class_ = "card-body p-0")

    # to store the extracted event data
    events_data = []

    for card in event_cards:
        # Extract event title
        title_tag = card.find("h4")
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            title = "N/A" # If title doesn't exist

        # Extract event date
        date_tag = card.find("div", class_="border-bottom-light-grey border-top-light-grey font-weight-bold py-1 small")
        if date_tag:
            date = date_tag.get_text(strip=True)
        else:
            date = "N/A" # If date doesn't exist

        # Extract event location
        location_tag = card.find("div", class_="border-bottom-light-grey small py-1")
        if location_tag:
            location_link_tag = location_tag.find("a")
            if location_link_tag:
                location = location_link_tag.get_text(strip=True)
            else:
                # if there is no <a> tag
                location = location_tag.get_text(strip=True)
        else:
            location = "N/A" # If location doesn't exist

        # Extract event description
        description_tag = card.find("p", class_="card-text mt-3")
        if description_tag:
            description = description_tag.get_text(strip=True)
        else:
            description = "N/A" # If description doesn't exist

        # Extract the "Read More" link
        link_tag = card.find("a", string="READ MORE")
        if link_tag:
            link = link_tag["href"]
        else:
            link = "N/A"

        if link != "N/A" and link.startswith("/"):
            link = "https://www.whatsonglasgow.co.uk" + link

        # Store the event data in the events_data list
        events_data.append((title, date, location, description, link))

                   
    # Save data to a CSV file
    def save_to_csv(events, filename="glagow_events.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Date", "Location", "Description", "Link"])
            writer.writerows(events)
        print(f"Saved {len(events)} events to {filename}")

    save_to_csv(events_data)

else:
    print(f"Failed to retrieve the page, status code: {response.status_code}")