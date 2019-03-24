from bs4 import BeautifulSoup
import requests
import csv


import random
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


user_agent = random.choice(user_agent_list)
    #Set the headers 
headers = {'User-Agent': user_agent}


URL = "https://www.berlin.de/ba-charlottenburg-wilmersdorf/verwaltung/aemter/umwelt-und-naturschutzamt/naturschutz/pflanzen-artenschutz/artikel.112976.php"
r = requests.get(URL, headers)
soup = BeautifulSoup(r.text, 'html.parser')


# Pull all text from the BodyText div

header_links = soup.find_all(class_='html5-header header')
#header_links.decompose()
[header_link.decompose() for header_link in header_links]
birds_list = soup.find_all(class_='html5-section block modul-text_bild float')
with open('/home/gaiar/developer/smart-birds-feeder/birds_parser/berlin-birds.csv', 'w') as outfile:
    f = csv.writer(outfile)
    f.writerow(['Name', 'Latin name','Image URL'])


    for bird in birds_list:
        try:    
            link = "https://www.berlin.de"+bird.div.a['href']
            name = bird.find(class_="textile").p.a.get_text().replace(","," ")
            latin_name = bird.find(class_="html5-section body").div.div.p.contents[2].replace(","," ")
            f.writerow([name, latin_name, link])
        except Exception as e:
            print(e)


#print(birds_list[0])


"""
<div class="html5-section block modul-text_bild float">
    <div class="html5-figure image main-image imagealignleft type-teaser" style="">
        <a href="/ba-charlottenburg-wilmersdorf/verwaltung/aemter/umwelt-und-naturschutzamt/naturschutz/pflanzen-artenschutz/mdb-amsel_seehawer.jpg"
            title="Foto in Originalgröße"> <img alt="Link zu: Foto in Originalgröße"
                src="/converjon/?ts=1401188113&amp;width=166&amp;height=125&amp;url=https%3A%2F%2Fwww.berlin.de%2Fba-charlottenburg-wilmersdorf%2Fverwaltung%2Faemter%2Fumwelt-und-naturschutzamt%2Fnaturschutz%2Fpflanzen-artenschutz%2Fmdb-amsel_thumb.jpg"
                title="Foto in Originalgröße" />
        </a>
        <div class="caption">
            <div class="caption--text">
                <strong>Freibrüter - Amsel</strong>
            </div>
            <span class="copyright">Bild: Enrico Hübner</span>
        </div>
    </div>
    <div class="html5-section body">
        <div class="text textalignleft">
            <div class="textile">
                <p>
                    <a href="/ba-charlottenburg-wilmersdorf/verwaltung/aemter/umwelt-und-naturschutzamt/naturschutz/pflanzen-artenschutz/artikel.112939.php"
                        title="Amsel - Turdus merula"><strong>Amsel, Schwarzdrossel</strong></a> Turdus merula<br />
                    — <a
                        href="/ba-charlottenburg-wilmersdorf/verwaltung/aemter/umwelt-und-naturschutzamt/naturschutz/pflanzen-artenschutz/artikel.112964.php"><strong>Mein
                            Lebensraum</strong></a>
                </p>
            </div>
        </div>
    </div>
</div>"""
