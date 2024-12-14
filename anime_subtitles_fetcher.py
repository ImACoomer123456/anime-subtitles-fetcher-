import os
import requests
from bs4 import BeautifulSoup

def get_episode_links(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    episode_links = []
    
    table = soup.find('table', {'id': 'search_results'})
    if table:
        for row in table.find_all('tr'):
            link_tag = row.find('a', href=True)
            if link_tag:
                link = link_tag['href']
                if 'imdbid-' in link or 'pimdbid-' in link:
                    episode_links.append(link)
    
    print("Episode Links:")
    for link in episode_links:
        print(link)
    
    return episode_links

def get_subtitle_links_from_episode(episode_url, target_uploader_name):
    response = requests.get(episode_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    subtitles = []
    
    table = soup.find('table', {'id': 'search_results'})
    if table:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 2:
                # Skip rows that do not have enough columns
                continue

            # Check if the subtitle is in English
            language_cell = cells[1]
            language_tag = language_cell.find('a', title="English")
            if not language_tag:
                continue  # Skip if the language is not English

            # Find the uploader name in the last column
            uploader_tag = cells[-1].find('a', href=True, string=target_uploader_name)
            if uploader_tag:
                print(f"Found English subtitle by {target_uploader_name}")
                
                # Locate the download link in the same row
                download_tag = cells[0].find('a', {'class': 'bnone'})
                if download_tag:
                    download_page_link = download_tag['href']
                    if not download_page_link.startswith('http'):
                        download_page_link = f'https://www.opensubtitles.org{download_page_link}'
                    
                    subtitles.append(download_page_link)
                    print(f"Download Page Link: {download_page_link}")
                else:
                    print("No download button found in the first column for this subtitle.")
    print("Finished checking for subtitles in this episode.")
    return subtitles

def download_subtitles(download_page_url, download_path):
    try:
        response = requests.get(download_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the actual subtitle file download link (updated button structure)
        actual_download_tag = soup.find('a', {'id': 'bt-dwl-bt'})
        if actual_download_tag:
            actual_download_link = actual_download_tag['href']
            if not actual_download_link.startswith('http'):
                actual_download_link = f'https://www.opensubtitles.org{actual_download_link}'
            
            print(f"Actual Download Link: {actual_download_link}")
            
            # Download the subtitle file
            subtitle_response = requests.get(actual_download_link, allow_redirects=True)
            subtitle_response.raise_for_status()  # Check for HTTP errors
            
            # Determine the file name
            if 'data-product-file-name' in actual_download_tag.attrs:
                file_name = actual_download_tag['data-product-file-name']
            else:
                file_name = actual_download_link.split('/')[-1]
            
            full_path = os.path.join(download_path, file_name)
            with open(full_path, 'wb') as f:
                f.write(subtitle_response.content)
            print(f"Subtitle downloaded to: {full_path}")
        else:
            print("Actual download link not found on the download page.")
    except requests.RequestException as e:
        print(f"Failed to download subtitle: {e}")

# The search_url can be obtained from the first webpage of any specific show (usually shows a list of episodes / seasons)
search_url = 'https://www.opensubtitles.org/en/ssearch/sublanguageid-all/idmovie-1463158'
target_uploader_name = 'tedi' 
download_path = r'D:\Projects\anime subtitles fetcher\subtitles'  # Updated path as a raw string

os.makedirs(download_path, exist_ok=True)

# Get episode links
episode_links = get_episode_links(search_url)

# Check each episode for subtitles
for episode_link in episode_links:
    full_episode_url = f'https://www.opensubtitles.org{episode_link}'
    download_page_urls = get_subtitle_links_from_episode(full_episode_url, target_uploader_name)
    
    for download_page_url in download_page_urls:
        download_subtitles(download_page_url, download_path)
