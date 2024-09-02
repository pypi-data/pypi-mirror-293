# Web scraper looking for data on the web for a certain paper


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import pandas as pd
from bs4 import BeautifulSoup
from EcoOpen.utils.keywords import keywords
import os
import requests
from pathlib import Path
from itertools import chain
import urllib3


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from EcoOpen.utils.keywords import field_specific_repo, repositories


repos = field_specific_repo+repositories

def get_webdriver():
    try:
        # Try Chrome
        chrome_service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=chrome_service)
    except Exception as e:
        print(f"Chrome WebDriver not found or failed to start: {e}")

    try:
        # Try Firefox
        firefox_service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=firefox_service)
    except Exception as e:
        print(f"Firefox WebDriver not found or failed to start: {e}")

    try:
        # Try Edge
        edge_service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=edge_service)
    except Exception as e:
        print(f"Edge WebDriver not found or failed to start: {e}")

    return None

# Usage example
# driver = get_webdriver()
# if driver:
#     driver.get("https://www.example.com")
#     # Perform actions with the driver
#     driver.quit()
# else:
#     print("No available WebDriver found.")


urls = [
    'https://link.springer.com/article/10.1007/s10886-017-0919-8',
    "https://link.springer.com/article/10.1007/s10886-018-0942-4",
    "https://doi.org/10.1073/pnas.1211733109",
    "http://dx.doi.org/10.3955/046.091.0105",
    "https://doi.org/10.1016/j.scitotenv.2013.10.121",
    "https://doi.org/10.1111/nph.14333"
    ]

filetypes = [
    "csv", "xlsx", "xls", "txt", "pdf", "zip",
    "tar.gz", "tar", "gz", "json", "docx",
    "doc", "ods", "odt", "pptx", "ppt", "png", "jpg", "md"]

repositories = keywords["repositories"]

exclude = []
for i in filetypes:
    exclude.append(i.lower()+".")


def find_data_web(doi):
    url = "https://doi.org/" + doi
    driver = get_webdriver()
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    real_url = driver.current_url
    print(real_url)
    domain = real_url.split('/')[2]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # driver.quit()
    supplementary_files = []
    closed_article_snippets = [
        "buy article",
        "access the full article",
        "purchase pdf",
    ]
    # check if the article is closed

    supplementary_snippets = [
        "supplementary",
        "supplemental",
        "additional",
        "appendix",
        "appendices",
        "suppl_file",
        "download"
    ]

    if any(snippet in str(soup).lower() for snippet in closed_article_snippets):
        print("Article is not publicly available!")
    # specific for PNAS
    if any(snippet in str(soup).lower() for snippet in supplementary_snippets):
        print("SEARCHING FOR SUPPLEMENTARY MATERIAL")
        # find the link to the supplementary file
        links = soup.find_all('a')
        for link in links:
            try:
                # finding mentions of supplementary material
                try:
                    if any(snippet in link.get('href').lower() for snippet in supplementary_snippets):
                        print(link.get('href'))
                        supplementary_files.append(link.get('href'))
                        
                    if any(repo in link.get('href').lower() for repo in repos):
                        print(link.get('href'))
                        supplementary_files.append(link.get('href'))
                except AttributeError:
                    pass
            except TypeError:
                pass

    driver.close()
    
    links = []
    for i in supplementary_files:
        i_ = i.split("?")[0]
        
        if i_ not in links:
            links.append(i)
            
    
            
            
    return links


def download_file(url, output_dir):
    response = requests.get(url)
    filename = url.split('/')[-1]
    if len(filename) > 100:
        filename = filename.split("?")[0]
    with open(os.path.join(output_dir, filename), 'wb') as f:
        f.write(response.content)


def download_osf_file(url, output_dir, file_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # print(url)
    # print(output_dir)
    # print(file_name)
    try:
        # Send a GET request to the URL
        response = requests.get(url,  headers=headers, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Define the file path
            file_path = os.path.join(output_dir, file_name)
            
            # Save the content of the response as a file
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            # print(f"File downloaded successfully and saved as {file_path}")
            return file_path
        else:
            # print(f"Failed to download file. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # print(f"An error occurred: {e}")
        return None
    except WebDriverException as e:
        return None


def get_data_from_link(link, output_dir="examples/data"):
    print(link, "!!")
    if "osf.io" in link:
        print(link.split("/")[-2])
        zip_ = "https://files.osf.io/v1/resources/"+ link.split("/")[-2] +"/providers/osfstorage/?zip="
        fp = download_osf_file(zip_, output_dir, f'{link.split("/")[-2]}.zip')
        return [fp]
    else:
        try:
            output_dir = Path(os.path.expanduser(output_dir))
            output_dir = output_dir.absolute()
            driver = get_webdriver()
            driver.maximize_window()
            print(link)
            
            files = []
            wait = WebDriverWait(driver, 5)
            # check repositories
            
            if any([i in link for i in repositories]):
                try:
                    driver.get(link)
                    real_url = driver.current_url
                    # print(real_url)
                    domain = real_url.split('/')[2]
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    # driver.quit()
                    for i in filetypes:
                        filename = ""
                        links = soup.find_all('a')
                        for link in links:
                            try:
                                if "."+i in link.get('href') or "."+i in link.get('title'):
                                    # print("There is a file")
                                    l = link.get('href')
                                    if "http" not in l:
                                        l = "https://"+domain + l
                                    files.append(l)
                                    # print(link.get('href'))
                            except TypeError:
                                pass
                    # close the browser
                    driver.close()
                except:
                    pass
            else:
                pass
            # download the files
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # for f in files:
            #     print(f)
            downloaded_files = []
            print(files)
            for i in files:
                print("downloading", i)
                # example https://www.cell.com/cms/attachment/45d6fbc5-6dd3-47d1-9f2a-26c35d10c983/gr3_lrg.jpg
                filename = i.split("/")[-1]
                
                if len(filename) > 100:
                    filename = filename.split("?")[0]
                if filename != "":
                    # check i any of the filetypes are in the filename
                    if any([i in filename.lower() for i in filetypes]):
                        if filename not in downloaded_files:
                            download_file(i, output_dir)
                            downloaded_files.append(filename)
                else:
                    print("Invalid filename", i)

            # download_file(i, output_dir)
            # try:
            #     response = requests.get(i, timeout=2)
            # except requests.exceptions.InvalidSchema:
            #     l = i.split("http")[-1]
            #     response = requests.get("http"+l, timeout=2)
                
            # except requests.exceptions.ConnectionError:
            #     continue

            # try:
            #     response.raise_for_status()
            #     filename = i.split('/')[-1]
            #     if "?" in filename:
            #         filename = filename.split("?")[0]
            #     if filename != "":
            #         with open(os.path.join(output_dir, filename), 'wb') as f:
            #             f.write(response.content)
                
            #     if filename != "":
            #         if filename not in downloaded_files:
            #             downloaded_files.append(filename)
            # except requests.exceptions.HTTPError:
            #     pass
            # except requests.exceptions.InvalidSchema:
            #     pass

            return downloaded_files
        except WebDriverException as e:
            return []


def DownloadData(data_report, output_dir):
    print("")
    print("Attempting to download open data from the web.")
    print("Be advised that due to the nature of different websites, automatic download may not be possible.")
    print("Manual download may be required.")
    print("Please check the output directory for downloaded files.")
    print("")

    data_dirs = []
    number_of_files = []

    for idx, row in data_report.iterrows():
        data_amount = 0
        data_dir = ""
        # print(row)
        links = []
        for i in ["data_links_keywords", "data_links_web"]:
            try:
                links = links+row[i]
            except KeyError:
                pass
            except TypeError:
                pass
        # print(links)

        title = row["title"]
        # replace all special characters with underscores
        title = "".join([i if i.isalnum() else "_" for i in title])
        data_dir = Path(os.path.expanduser(str(output_dir)+"/"+title))

        data_dirs.append(str(data_dir))
        os.makedirs(data_dir, exist_ok=True)

        if len(links) > 0:
            for i in links:
                get_data_from_link(i, data_dir)
        # count downloaded files
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                data_amount += 1

        number_of_files.append(data_amount)

    data_report["data_dir"] = data_dirs
    data_report["number_of_files"] = number_of_files

    print("Download attempt complete.")

    return data_report


if __name__ == '__main__':
    doi = "10.1016/j.tpb.2012.08.002"
    doi = "10.3390/microorganisms10091765"

