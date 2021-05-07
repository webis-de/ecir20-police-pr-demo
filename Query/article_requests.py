# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 13:46:44 2019

@author: Nina
"""
import urllib.request as urllib
from bs4 import BeautifulSoup
import re
import csv
import os
import ssl
from functools import lru_cache
ssl._create_default_https_context = ssl._create_unverified_context

class ParsedArticle:
    def __init__(self, parsed_article, url):
        self.__parsed_article = parsed_article
        self.url = url

    def title(self):
        return self.__parsed_article['title']

    def has_title(self):
        return article_has_field(self.__parsed_article, 'title')

    def body(self):
        return self.__parsed_article['body']

    def has_body(self):
        return article_has_field(self.__parsed_article, 'body')

    def date(self):
        return self.__parsed_article['date']
    
    def has_date(self):
        return article_has_field(self.__parsed_article, 'date')

    def date2(self):
        return self.__parsed_article['date2']
    
    def has_date2(self):
        return article_has_field(self.__parsed_article, 'date2')

    def place(self):
        return self.__parsed_article['place']

    def has_place(self):
        return article_has_field(self.__parsed_article, 'place')


def article_has_field(parsed_article, field):
    return parsed_article is not None and field is not None\
           and field in parsed_article and parsed_article[field] is not None\
           and parsed_article[field].strip() != ''


def extract_title(soup):
    try:    
        title = soup.title.text
    except Exception as e:
        try: 
            title = soup.select('p[class="id-Article-kicker"]')[0].text +': ' + soup.select('h2[itemprop="headline"]')[0].text
        except:
            title = None
    if(title==None):
        return title
    else:
        title = title.replace('\n', '')
        title = title.replace('\t', '')
        title = title.replace('| ', '')
        title = title.replace('"', '')
        title = title.replace('„', '')
        title = title.replace('“', '')
        title = title.replace(':', '')
        return title

def apply_first_working_extractor(extractors, soup):
    for extractor in extractors:
        try:
            return extractor(soup)
        except:
            pass
    return None

def extract_place(soup):
    EXTRACT_PLACE_FUNCTIONS = [
        lambda soup: soup.select('span[class="ortsmarke"]')[0].text,
        lambda soup: soup.select('h2[class="StoryShowLocation"]')[0].text,
        lambda soup: soup.select('div[class="dachzeile"]')[0].text,
        lambda soup: soup.select('span[class="article__location"]')[0].text,
        lambda soup: soup.select('em[class="park-article__dateline"]')[0].text,
        lambda soup: soup.select('span[itemprop="dateline"]')[0].text,
        lambda soup: soup.select('p[class="article-location"]')[0].text,
        lambda soup: soup.select('div[class="published clearfix"]')[0].h2.text,
        lambda soup: soup.select('span[class="news-bereich"]')[0].text,
    ]

    place = apply_first_working_extractor(EXTRACT_PLACE_FUNCTIONS, soup)
   
    if(place==None):
        return place
    else:
        place = place.replace('.','')
        place = place.replace('-', ' ')
        place = place.replace('\n','')
        place = re.sub('\d', '', place)
        place = place.replace('In ','')
        place = place.replace(':','')
        place = place.replace('Uhr','')
        place = place.replace(',','')
        place = place.replace('Juli','')
        return place

def concat_all_story_texts(soup):
    body = soup.select('div[class="story_text"]').text 
    for article in soup.find_all('div', class_="story_text"):
        body = body + article.text
    return body

def concat_all_park_article_contents(soup):
    body = ''
    for article in soup.find_all('div', class_="park-article-content"):
        body = body + article.text
    return body

def extract_body(soup):
    EXTRACT_BODY_FUNCTIONS = [
        lambda soup: soup.select('div[class="article__body"]')[0].p.text + soup.select('p[class="article__paragraph p_1 "]')[0].text + soup.select('p[class="article__paragraph p_2 "]')[0].text + soup.select('p[class="article__paragraph p_3 "]')[0].text + soup.select('p[class="article__paragraph p_4 "]')[0].text + soup.select('p[class="article__paragraph p_5 "]')[0].text + soup.select('p[class="article__paragraph p_6 "]')[0].text + soup.select('p[class="article__paragraph p_7 "]')[0].text,
        lambda soup: soup.select('p[class="article__paragraph p_1 "]')[0].text + soup.select('p[class="article__paragraph p_2 p"]')[0].text + + soup.select('p[class="article__paragraph p_3 p"]')[0].text,
        lambda soup: soup.select('p[class="First atc-TextParagraph"]')[0].text + soup.select('p[class="atc-TextParagraph"]')[0].text,
        lambda soup: concat_all_story_texts(soup),
        lambda soup: soup.select('div[class="story_text"]')[0].p.text,
        lambda soup: soup.select('div[itemprop="articleBody"]')[0].text,
        lambda soup: soup.select('div[class="article-intro"]')[0].text + soup.select('div[id="articlecontent"]')[0].text,
        lambda soup: soup.select('div[class="nfy-ticker-text nfy-article-body"]')[0].text,
        lambda soup: soup.select('p[class="intro"]')[0].text + soup.select('p[id="BaseTextFirstParagraph"]')[0].text + soup.select('div[id="BaseText"]')[0].text,
        lambda soup: soup.select('div[class="entry excerpt"]')[0].text + soup.select('div[class="entry-inner"]')[0].text,
        lambda soup: soup.select('p[class="article_teaser"]')[0].text + soup.select('div[class="article_body"]')[0].text,
        lambda soup: soup.select('div[class="container-text"]')[2].text + soup.select('div[class="container-text"]')[3].text,
        lambda soup: soup.select('p[class="p_2"]')[0].text + soup.select('p[class="p_3"]')[0].text + soup.select('p[class="p_4"]')[0].text + soup.select('p[class="p_5"]')[0].text,
        lambda soup: soup.select('div[class="story-text serif"]')[0].text,
        lambda soup: soup.select('p[class="box-lead"]')[0].text + soup.select('p')[1].text + soup.select('p')[2].text + soup.select('p')[3].text,
        lambda soup: soup.select('div[class="txt"]')[0].text,
        lambda soup: soup.select('div[class="leadIn"]')[0].text + soup.select('div[class="textBlock"]')[0].text,
        lambda soup: soup.select('p[class="park-article__intro park-article__content"]')[0].text,
        lambda soup: concat_all_park_article_contents(soup)
    ]
    body = apply_first_working_extractor(EXTRACT_BODY_FUNCTIONS, soup)

    if body == None:
        return body

    body = body.replace('\n', '')
    body = body.replace('\t', '')
    body = body.replace('\xa0', '')
    body = body.replace('"', '')
    body = body.replace('„', '')
    body = body.replace('“', '')
    body = body.replace('{', '')
    body = body.replace('}', '')
    return body

def extract_date(soup):
    EXTRACT_DATE_FUNCTIONS = [
        lambda soup: soup.select('time[datetime]')[0].text,
        lambda soup: soup.select('time[class="nfy-c-ticker-date"]')[0].text,
        lambda soup: soup.select('div[class="nfy-ar-date"]')[0].text,
        lambda soup: soup.select('time[class="author__time"]')[0].text,
                #added for www.volksstimme.de/lokal/madeburg
        lambda soup: soup.select('span[class="ph-ah-sub-info-date"]')[0].text,
        lambda soup: soup.select('div[class="displayDate"]')[0].text,
        lambda soup: soup.select('span[class="date"]')[0].text,
        lambda soup: soup.select('time[class="park-date"]')[0].text,
        lambda soup: soup.select('span[class="date updated"]')[0].text,
        lambda soup: soup.select('span[class="authors-date"]')[0].text,
        lambda soup: soup.select('div[class="container-autor"]')[0].text,
        lambda soup: soup.select('div[class="article-info"]')[0].text,
        lambda soup: soup.select('i[itemprop="datePublished"]')[0].text,
        lambda soup: soup.select('time[class="label"]')[0].text,
        lambda soup: soup.select('span[itemprop="dateline"]')[0].text,
        lambda soup: soup.select('span[itemprop="datePublished"]')[0].text,
        lambda soup: soup.select('p[class="lastUpdated"]')[0].text,
        lambda soup: soup.select('div[class="published clearfix"]')[0].p.span.text,
        lambda soup: soup.select('span[class="news-bereich"]')[0].text,
        lambda soup: soup.select('span[itemprop="datepublished"]')[0].text,
    ]
    date = apply_first_working_extractor(EXTRACT_DATE_FUNCTIONS, soup)

    if(date==None):
        return date
    else:
        date = date.replace('\t', '')
        date = date.replace('"', '')
        date = date.replace('„', '')
        date = date.replace('“', '')
        date = date.replace('\n', '')
        date = date.replace('Von neu, ', '')
        date = date.replace('am ', '')
        date = date.replace('um ', '')
        date = date.replace(' Rottweil.', '')
        date = date.replace('Akt: ', '')
        date = date.replace(' - Eintracht Braunschweig', '')
        return date

@lru_cache(maxsize=None)
def perfect_content_for_urls():
    topic_content_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Evaluierung', 'Topics-content.CSV')
    with open(topic_content_file, encoding='utf8') as topic_content:
        ret = {}
        csvReader = csv.DictReader(topic_content, ['_id', 'title', 'body', 'date', 'place', 'date2', 'url', 'difficulty'], delimiter=';')
        next(csvReader)
        for row in csvReader:
            ret[row['url']] = row
        return ret

@lru_cache(maxsize=None)
def parse_article_for_url(url):
    if url.replace('"', '') in perfect_content_for_urls():
        return ParsedArticle(perfect_content_for_urls()[url.replace('"', '')], url)

    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    return ParsedArticle({
            "title":
            extract_title(soup), 
            "body":
            extract_body(soup),
            "date": 
            extract_date(soup),
            "place": 
            extract_place(soup)
        }, url)


def to_csv(url_list):
    csv_file = open('results_web_scrape.csv','w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["id","headline", "body", "date", "place"])
    for k in range(15):
        csv_writer.writerow(["url7_"+str(k+1), request(url_list[k])])
    csv_file.close()
if __name__ == '__main__':
    url1 = "https://web.archive.org/web/20190825194635/https://www.fnp.de/lokales/blaulicht-sti879542/probefahrt-endet-festnahme-10929715.html"
    url = "https://web.archive.org/web/20170103185708/https://www.neuepresse.de/Hannover/Meine-Stadt/Polizei-greift-am-Hauptbahnhof-Hannover-durch"
    
    url7_1="https://web.archive.org/web/20190909124140/https://www.morgenweb.de/newsticker_ticker,-speyer-polizei-verhindert-massenschlaegerei-_tickerid,61704.html"
    url7_2="https://web.archive.org/web/20190909130902/https://www.rnz.de/nachrichten/heidelberg/polizeibericht-heidelberg_artikel,-heidelberg-betrunkene-studenten-randalieren-in-der-altstadt-_arid,338491.html"
    url7_3="https://web.archive.org/web/20190909134319/https://www.waz.de/sport/fussball/schiedsrichter-in-gelsenkirchen-von-zuschauern-attackiert-id214387019.html"
    url7_4="https://web.archive.org/web/20190909135333/https://www.volksstimme.de/lokal/magdeburg/fahndung-handy-raeuber-in-magdeburg-gefasst"
    url7_5="https://web.archive.org/web/20190909140720/https://www.ruhrnachrichten.de/dortmund/web-artikel-1285328.html"
    url7_6="https://web.archive.org/web/20190909141435/https://www.wz.de/nrw/duesseldorf/raubueberfall-in-oberkassel-mann-bedroht-15-jaehrigen-mit-messer_aid-25783327"
    url7_7="https://web.archive.org/web/20190909141755/https://www.duesseldorfer-anzeiger.de/duesseldorf/raub-mit-messer-in-oberkassel_aid-36017829"
    url7_8="https://web.archive.org/web/20190909143941/https://www.nordbuzz.de/niedersachsen/zwei-versuchte-ueberfaelle-beim-bahnhof-verden-jugendgang-geld-handys-abgesehen-9813901.html"
    url7_9="https://web.archive.org/web/20190909154410/https://rp-online.de/nrw/staedte/kevelaer/nach-schlag-ins-gesicht-das-portemonnaie-gestohlen_aid-22641963"
    url7_10="https://web.archive.org/web/20190909154654/https://www.wp.de/staedte/kleve-und-umland/23-jaehriger-in-kevelaer-verpruegelt-id214291839.html"
    url7_11="https://web.archive.org/web/20190909162230/https://www.wz.de/nrw/krefeld/erneuter-angriff-auf-busfahrer-in-krefeld_aid-25756075"
    url7_12="https://web.archive.org/web/20190909204047/https://www.wp.de/staedte/siegerland/polizei-siegen-drogenfahnder-nehmen-amphetamin-bande-fest-id213377103.html"
    url7_13="https://web.archive.org/web/20190909204342/https://weserreport.de/2018/03/polizei/raubueberfaelle-auf-spielotheken-bande-gefasst/"
    url7_14="https://web.archive.org/web/20190909204516/https://www.weser-kurier.de/bremen/bremen-stadt_artikel,-raubserie-auf-spielotheken-in-bremen-aufgeklaert-_arid,1713227.html"
    url7_15="https://web.archive.org/web/20190909210043/https://www.journal-frankfurt.de/journal_news/Panorama-2/In-Bornheim-und-Ostend-Polizei-zerschlaegt-Drogenhaendlerring-32062.html"
    
    url6_1="https://web.archive.org/web/20190908182604/https://www.wolfenbuetteler-zeitung.de/wolfenbuettel/article213230329/Motorradfahrerin-bei-Unfall-schwer-verletzt.html"
    url6_2="https://web.archive.org/web/20190908183148/https://www.wz.de/nrw/krefeld/auto-faehrt-radlerin-an-schwer-verletzt_aid-25924297"
    url6_3="https://web.archive.org/web/20190908184207/https://rp-online.de/nrw/staedte/willich/a44-bei-willich-17-jaehrige-motorradfahrerin-stirbt-nach-schwerem-unfall_aid-22392155"
    url6_4="https://web.archive.org/web/20190908190413/https://rp-online.de/nrw/staedte/geldern/kerken-schwerer-unfall-auf-der-rheinstrasse_aid-20648503"
    url6_5="https://web.archive.org/web/20190908192926/https://www.news38.de/wolfenbuettel/article213926659/Mit-voller-Wucht-gerammt-22-Jaehriger-entwurzelt-Baum.html"
    url6_6="https://web.archive.org/web/20190908193203/https://live.goslarsche.de/post/view/5ac5e2e09aa99f613b9a4f1e/Hornburg/Zwei-Verletzte-nach-Verkehrsunfall-"
    url6_7="https://web.archive.org/web/20190908193801/https://rp-online.de/nrw/staedte/moenchengladbach/a61-bei-moenchengladbach-vier-verletzte-bei-unfall-mit-zivilem-polizeiauto_aid-17794639"
    url6_8="https://web.archive.org/web/20190908194618/https://www.ruhrnachrichten.de/dortmund/web-artikel-1285087.html"
    url6_9="https://web.archive.org/web/20190908200104/https://www.stuttgarter-zeitung.de/inhalt.ludwigsburg-toter-welpe-jogger-erhaelt-strafbefehl.d768b799-3598-495c-8c0c-54b260b72f49.html"
    url6_10="https://web.archive.org/web/20190908200104/https://www.stuttgarter-zeitung.de/inhalt.ludwigsburg-toter-welpe-jogger-erhaelt-strafbefehl.d768b799-3598-495c-8c0c-54b260b72f49.html"
    url6_11="https://web.archive.org/web/20190908215744/https://www.wp.de/staedte/wittgenstein/auto-haelt-auf-gleisen-und-wird-in-erndtebrueck-vom-zug-erfasst-id209459737.html"
    url6_12="https://web.archive.org/web/20190908220547/http://www.general-anzeiger-bonn.de/region/sieg-und-rhein/mehr-sieg-und-rhein/26-j%C3%A4hriger-Eitorfer-unter-Zug-gefunden-article1513698.html"
    url6_13="https://web.archive.org/web/20190908221519/https://www.mt.de/lokales/regionales/20671017_Wetter-verursacht-Verkehrsprobleme-auf-Niedersachsens-Strassen.html?em_cnt=20671017"
    url6_14="https://web.archive.org/web/20190908222833/https://www.noz.de/deutschland-welt/bremen/artikel/1251590/von-zug-erfasst-37-jaehriger-in-bremen-gestorben"
    url6_15="https://web.archive.org/web/20190908225515/https://www.faz.net/aktuell/rhein-main/zwoelfjaehriger-stirbt-nach-autounfall-an-seinen-schweren-verletzungen-14071562.html"
      
    url5_1 ="https://web.archive.org/web/20190905195831/https://www.bild.de/news/inland/polizistenmord/linksradikale-verhoehnen-ermordeten-polizisten-43938300.bild.html"
    url5_2 ="https://web.archive.org/web/20190905200326/https://www.focus.de/regional/hessen/herborner-bahnhof-an-weihnachten-erstochen-linksradikale-verhoehnen-ermordeten-polizisten-im-netz_id_5177472.html"
    url5_3 ="https://web.archive.org/web/20190905202540/https://www.bild.de/regional/koeln/wmautokorso-in-bergheim-drei-autos-beschossen-36815144.bild.html"
    url5_4 ="https://web.archive.org/web/20190905203625/https://www.derwesten.de/staedte/duisburg/nettes-cafe-am-hafen-warum-wurde-ausgerechnet-im-vivo-eine-frau-getoetet-id210449711.html"
    url5_5 ="https://web.archive.org/web/20190905203934/https://www.derwesten.de/staedte/duisburg/cafe-vivo-in-duisburg-geschaeftsfuehrerin-46-wurde-erschossen-angestellte-fand-die-leiche-id210456067.html"
    url5_6 ="https://web.archive.org/web/20190905204030/https://www.derwesten.de/staedte/duisburg/getoetete-frau-im-cafe-taucher-suchen-nach-tatwaffe-im-duisburger-innenhafen-id210446115.html"
    url5_7 ="https://web.archive.org/web/20190905205008/https://www.mopo.de/hamburg/polizei/vergewaltigung-in-harburg-angeklagte-feiern-sich-im-gericht-24644788"
    url5_8 ="https://web.archive.org/web/20190905205515/https://www.mopo.de/hamburg/polizei/14-jaehrige-vergewaltigt-jetzt-hat-die-polizei-alle-mutmasslichen-sex-taeter-geschnappt--23726562"
    url5_9 ="https://web.archive.org/web/20190905210620/https://www.waz.de/panorama/dreifach-mord-angeklagter-erschoss-sohn-wohl-aus-rache-id213744925.html"
    url5_10 ="https://web.archive.org/web/20190905210527/http://www.general-anzeiger-bonn.de/news/panorama/Polizistin-weint-im-Prozess-um-Dreifach-Mord-article3808717.html"
    url5_11 ="https://web.archive.org/web/20190905213005/https://www.nrz.de/staedte/duesseldorf/mord-an-galina-a-noch-immer-keine-heisse-spur-id1424409.html"
    url5_12 ="https://web.archive.org/web/20190905213218/https://www.express.de/mordfall-galina-wird-ihr-tod-niemals-gesuehnt--22014128"
    url5_13 ="https://web.archive.org/web/20190905214559/https://www.schwarzwaelder-bote.de/inhalt.mord-in-magstadt-moerdersuche-beim-csd.3650f51f-3ae6-46cc-98eb-49905b012f1e.html"
    url5_14 ="https://web.archive.org/web/20190905215058/https://www.suedkurier.de/region/hochrhein/stuehlingen/Stuehlingen-Festnahme-nach-Mord-an-Waffenhaendler;art372620,8805832"
    url5_15 ="https://web.archive.org/web/20190906090609/https://www.fnweb.de/newsticker_ticker,-niedernhall-mann-tot-aufgefunden-_tickerid,76140.html"


    url4_1 ="https://web.archive.org/web/20190904185155/http://www.uisf.de/27-04-14-1400-ksv-hessen-kassel-kickers-offenbach-22/"
    url4_2 ="https://web.archive.org/web/20160301011007/http://fanzeit.de/polizei-verwechselt-dortmunder-mit-frankfurter-ultras/4567"
    url4_3 ="https://web.archive.org/web/20160324125325/http://www.oberhessen-live.de/2014/05/12/pruegelnde-fans-beschaeftigen-die-polizei/"
    url4_4 ="https://web.archive.org/web/20190904193313/https://www.focus.de/regional/hessen/kriminalitaet-17-jaehriger-nach-fussballspiel-durch-messerstich-verletzt_id_3853664.html"
    url4_5 ="https://web.archive.org/web/20140623005904/http://www.faz.net/aktuell/rhein-main/wiesbaden-messerattacke-nach-fussballspiel-12945585.html"
    url4_6 ="https://web.archive.org/web/20190904201815/http://www.lessentiel.lu/de/news/grossregion/story/streit-uber-gehalter-von-fu-ballprofis-eskaliert-26560896"
    url4_7 ="https://web.archive.org/web/20190904203532/https://www.mittelbayerische.de/sport/regional/neumarkt-nachrichten/stadionverbot-fuer-125-hooligans-21522-art1232914.html"
    url4_8 ="https://web.archive.org/web/20190904204003/https://www.faszination-fankurve.de/index.php?head=Braunschweiger-Ultras-landen-in-Gewahrsam&folder=sites&site=news_detail&news_id=9751"
    url4_9 ="https://web.archive.org/web/20190904204727/https://www.mittelkreis.de/alle-ligen/bdl-hessen/hes-mannschafft-herren/hes-her-klasse-kreisligen-a/hes-her-kreisliga-a-main-taunus/a-liga-mtk-spielabbruch-und-polizeieinsatz-im-testspiel-in-floersheim/"
    url4_10 ="https://web.archive.org/web/20190904204954/https://www.extratipp.com/hessen/fussball-freundschaftsspiel-floersheim-eskaliert-8513040.html"
    url4_11 ="https://web.archive.org/web/20190905123256/https://www.morgenweb.de/mannheimer-morgen_artikel,-ludwigshafen-aggressiver-30-jaehriger-_arid,1267714.html"
    url4_12 ="https://web.archive.org/web/20190905124326/https://www.stuttgarter-nachrichten.de/inhalt.vfb-stuttgart-schlaegerei-nach-23-niederlage-gegen-dortmund.af26064c-29e9-4d4f-922d-b00f1b2ab07b.html"
    url4_13 ="https://web.archive.org/web/20190905124521/https://www.focus.de/regional/stuttgart/kriminalitaet-schlaegereien-unter-fussball-fans_id_4496715.html"
    url4_14 ="https://web.archive.org/web/20190905125413/https://www.stuttgarter-nachrichten.de/inhalt.streit-in-schwetzingen-schlaegerei-mit-stoecken-und-aesten-auf-fussballplatz.da497c3c-ff04-470c-bfae-714e14980bcf.html"
    url4_15 ="https://web.archive.org/web/20190905125509/https://www.allgemeine-zeitung.de/streit-um-fussballplatz-in-schwetzingen-eskaliert_17892387"


    url3_1 ="https://web.archive.org/web/20150826224434/https://www.haz.de/Nachrichten/Der-Norden/Uebersicht/Rechte-attackieren-Asylbewerber-in-Hildesheim"
    url3_2 ="https://web.archive.org/web/20180915103432/https://www.noz.de/lokales/osnabrueck/artikel/716185/betrunkener-mann-beleidigt-zugreisende-in-osnabruck"
    url3_3 ="https://web.archive.org/web/20190807070911/https://www.nwzonline.de/oldenburg/blaulicht/nadorst-zeugen-gesucht-exhibitionist-zeigt-sich-in-oldenburger_a_50,5,2100258528.html"
    url3_4 ="https://web.archive.org/web/20160928144949/http://www.denken-macht-frei.info:80/stade-massenschlaegerei-zwischen-tuerken-und-libanesen/"
    url3_5 ="https://web.archive.org/web/20170103185708/https://www.neuepresse.de/Hannover/Meine-Stadt/Polizei-greift-am-Hauptbahnhof-Hannover-durch"
    url3_6 ="https://web.archive.org/web/20190827124654/https://www.goettinger-tageblatt.de/Nachrichten/Der-Norden/Streit-in-Peine-eskaliert-Polizei-Grossaufgebot-verhindert-Ausschreitungen"
    url3_7 ="https://web.archive.org/web/20190827124746/https://www.paz-online.de/Stadt-Peine/Massenschlaegerei-in-Suedstadt-Polizei-verhindert-Eskalation"
    url3_8 ="https://web.archive.org/web/20170515213855/https://www.bild.de/regional/aktuelles/baden-wuerttemberg/streit-um-fussballplatz-freizeitsportler-51741100.bild.html"
    url3_9 ="https://web.archive.org/web/20190905213452/https://www.n-tv.de/panorama/Auftragsmord-in-Duesseldorf-article246244.html"
    url3_10 ="https://web.archive.org/web/20190905213956/https://www.bild.de/regional/ruhrgebiet/auftragsmord/mord-auftraggeber-festgenommen-41030064.bild.html"
    url3_11 ="https://web.archive.org/web/20190909140056/https://www.goettinger-tageblatt.de/Die-Region/Goettingen/Drei-Polizisten-in-Goettingen-verletzt"
    url3_12 ="https://web.archive.org/web/20190909182401/https://www.wochenendspiegel.de/zahl-festgestellter-illegaler-migranten-weiter-steigend/"
    url3_13 ="https://web.archive.org/web/20190909203221/http://www.wzonline.de/nachrichten/lokal/artikel/maedchen-im-nautimo-bedraengt.html"
    url3_14 ="https://web.archive.org/web/20190909203500/https://www.nwzonline.de/blaulicht/maedchen-im-schwimmbad-von-mehreren-maennern-belaestigt_a_6,0,3472534831.html"
    url3_15 ="https://web.archive.org/web/20190909203511/https://harlinger.de/nachrichten/artikel/zwei-elfjaehrige-im-nautimo-in-wilhelmshaven-belaestigt"
    

    print(request(url7_6))
    #url7list = [url7_1, url7_2, url7_3, url7_4, url7_5, \
    #            url7_6, url7_7, url7_8, url7_9, url7_10, \
   #             url7_11, url7_12, url7_13, url7_14, url7_15]
    #to_csv(url7list)
