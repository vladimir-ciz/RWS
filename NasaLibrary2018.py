import requests
import random

base_url = 'https://images-api.nasa.gov'
limit = 100


def get_all_nasa_images():
    result = []

    # API endpoint construction for getting all photos
    endpoint = f"{base_url}/search?keywords=Mars%20MRO&description=Mars&center=JPL&media_type=image&year_start=2018&year_end=2018"

    # Initial API request
    response = requests.get(endpoint)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve test cases. Status code: {response.status_code}"
        )

    data = response.json()
    result.extend(data['collection']['items'])

    # Total number of pages
    total_pages = (data['collection']['metadata']['total_hits'] + limit - 1) // limit

    # Fetching subsequent pages
    for page in range(2, total_pages + 1):
        # Construct the API endpoint for the next page
        page_endpoint = f"{endpoint}&page={page}"

        # API request for the next page
        response = requests.get(page_endpoint)

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve test cases. Status code: {response.status_code}"
            )

        data = response.json()
        result.extend(data['collection']['items'])

    return result


def get_mars_videos_2018():
    result = []

    # API endpoint construction for getting all videos related to Mars taken in 2018
    endpoint = f"{base_url}/search?keywords=Mars&media_type=video&year_start=2018&year_end=2018"

    # API request
    response = requests.get(endpoint)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve videos. Status code: {response.status_code}"
        )

    data = response.json()
    result.extend(data['collection']['items'])

    return result


def print_video_links(videos):
    for i in range(min(5, len(videos))):
        video = videos[i]
        links = video.get('links', [])
        video_links = [link['href'] for link in links if link['rel'] == 'preview']
        date_created = video.get('data', [{}])[0].get('date_created', 'Date not available')
        if video_links:
            print(f"Video {i + 1} links:")
            for link in video_links:
                print(link)
        else:
            print(f"No video links found for Video {i + 1}")
        print(f"Date created: {date_created}")
        print()


if __name__ == "__main__":
    images = get_all_nasa_images()
    print(f"Total images fetched: {len(images)}")
    print()

    # Randomize the order of images
    random.shuffle(images)

    # Print details of 5 images of Mars
    print("Details of 5 images:")
    for i in range(5):
        image = images[i]
        description = image.get('data', [{}])[0].get('description', '')
        keywords = image.get('data', [{}])[0].get('keywords', [])
        location = image.get('data', [{}])[0].get('location', [])
        location_str = ', '.join(location) if location else 'Location not available'
        date_created = image.get('data', [{}])[0].get('date_created', 'Date not available')
        links = image.get('links', [])
        image_link = next((link['href'] for link in links if link['rel'] == 'preview'), 'Link not available')

        print(f"Image {i + 1}:")
        print(f"Description: {description}")
        print(f"Keywords: {', '.join(keywords)}")
        print(f"Location: {location_str}")
        print(f"Date created: {date_created}")
        print(f"Image link: {image_link}")
        print()

    # Print details of the first 5 videos taken in 2018 with keyword "Mars"
    print("Details of the first 5 videos:")
    mars_videos_2018 = get_mars_videos_2018()
    print_video_links(mars_videos_2018)
