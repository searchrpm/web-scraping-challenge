from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    # Mars News

    #mars["news_title"] = soup.find('div', class_='content_title').find('a').text
    #mars["news_p"] = soup.find ('div', class_='article_teaser_body').text   


    # JPL Mars Space Image - Featured Image

    browser = init_browser()
    mars = {}

    base_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/'
    search_url = 'https://www.jpl.nasa.gov/spaceimages/index.php?category=Mars'

    response = requests.get(search_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attributes
    result = soup.find('article', class_='carousel_item').attrs

    carousel_container = str(result['style'])
    jpg_name = carousel_container.replace("background-image: url('/spaceimages/images/wallpaper/", "")

    image = jpg_name.replace("-1920x1200.jpg');", "_hires.jpg")

    mars["featured_image_url"] = base_url + image

    # Mars Weather

    twitter_url="https://twitter.com/marswxreport?lang=en"

    response = requests.get(twitter_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    result = soup.find('div', class_='js-tweet-text-container')

    mars["mars_weather"] = result.p.text

    # Mars Facts

    mars_facts="http://space-facts.com/mars/"
    table = pd.read_html(mars_facts)
    df = table[0]
    df.columns=['Parameters', 'Value']
    html_table=df.to_html()

    mars["html_table2"] = html_table.replace('\n','')

    # Mars Hemisphreres

    astrology_url = "http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "http://web.archive.org"

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', headless=False)
    browser.visit(astrology_url)

    soup = BeautifulSoup(browser.html, 'html.parser')

    result = soup.find_all('div', class_='item')

    hemispheres = []

    for link in result:
        itemLink = link.find('a')['href']
        hemispheres.append(itemLink)
    
    print("Printing hemisphere lists")
    print(hemispheres)
    print("")
    print("---------------------------------------------------------------------------------------------------------------------")
    print("Printing 'hemisphere_image_urls' Dictionary")
    print("")

    hemisphere_image_urls = []

    for hem in hemispheres:
        astrology_url = base_url + hem
        
        browser.visit(astrology_url)
    
        soup = BeautifulSoup(browser.html, 'html.parser')
    
        # image url
        # <img class="wide-image" src="/web/20181114182248im_/https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg">
        image_url = soup.find('img', class_="wide-image")
        image = base_url + image_url["src"]
    
        # page title and remove enhanced
        # <h2 class="title">Valles Marineris Hemisphere Enhanced</h2>
        # https://python-reference.readthedocs.io/en/latest/docs/str/rsplit.html
        page_title = soup.find('h2', class_='title')
        title = page_title.text
        title = title.rsplit(' ', 1)[0]
        
        m_hemisphere = {"Title": title, "img_url": image}
        hemisphere_image_urls.append(m_hemisphere)
        
        mars["hemisphere_image_urls"]

    return mars