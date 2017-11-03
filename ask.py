
import requests
#import pyquery
#from scapy.all import *
import webbrowser
import time
import os, sys, getopt
from random import randint

def request(links,wait=10):
    for link in links:
        s = requests.Session()
        r = s.get(link)
        time.sleep(wait)
        print('Response', r.text)

def browser(links, wait=20):
    controller = webbrowser.get()
    for link in links:
        controller.open(link)
        time.sleep(wait)
        os.system("wmctrl -a firefox")
        os.system("xdotool key Ctrl+w")

def mix_browser(po, wait=20):
    controller = webbrowser.get()
    for i in range(0,19):
        time.sleep(wait)
        weblist = (ebay, facebook, youtube, alexa)
        web_select = weblist[randint(0,3)]
        link = web_select[randint(0,19)]
        controller.open(link)
        if i == randint(0,19):
            print(i)
            os.system("wmctrl -a firefox")
            os.system("xdotool key Ctrl+w")

ebay = (
    'https://www.ebay.de/',
    'https://www.ebay.de/rpp/elektronik-technik',
    'https://www.ebay.de/rpp/zubehoer',
    'https://www.ebay.de/rpp/sammeln-antiquitaeten',
    'https://www.ebay.de/b/Fotokunst/28667/bn_1845121',
    'https://www.ebay.de/b/Kunstlerische-Malerei/551/bn_2394862',
    'http://www.ebay.de/itm/MARKUS-LUePERTZ-GROSSE-ORIGINAL-KOHLE-ZEICHNUNG-1989-POUSSIN-BACHUS-VP-5500/302452661441?hash=item466b955cc1%3Ag%3A2GwAAOSw0h9Zup2V',
    'https://www.ebay.de/rpp/smart-home/google-home',
    'http://www.ebay.de/itm/Google-Wifi-Zweierpack-/302383393880?_trkparms=%26rpp_cid%3D5979a341e4b0baabc210d26e%26rpp_icid%3D59774f31e4b0c9e090c974a8',
    'http://www.ebay.de/itm/ASUS-MAP-AC2200-Lyra-Tri-Band-WLAN-ac-Mesh-System/401354854683?_trkparms=aid%3D888007%26algo%3DDISC.MBE%26ao%3D1%26asc%3D46153%26meid%3D8660460734fe4b6f9d3348483438a590%26pid%3D100009%26rk%3D1%26rkt%3D1%26sd%3D302383393880&_trksid=p2047675.c100009.m1982',
    'https://www.ebay.de/rpp/sammeln-und-seltenes',
    'https://www.ebay.de/rpp/sammeln-und-seltenes/Gebrauchte-total-verruckte-Sammlerobjekte',
    'https://www.ebay.de/deals',
    'https://www.ebay.de/p/Seagate-STEB4000201-4TB-Externe-Festplatte-Schwarz/1379583754?iid=252478674965&_trkparms=5373%3A0%7C5374%3AFeatured%7C5079%3A6000001951',
    'http://www.ebay.de/usr/mediamarkt?_trksid=p2349526.m2547.l7859',
    'https://www.ebay.de/b/Samsung-Zubehor-fur-Handys/9394/bn_468397',
    'https://www.ebay.de/b/Tablet-eBook-Zubehor/176970/bn_796420',
    'http://www.ebay.de/itm/Luxury-Leder-Schutzhuelle-fuer-Apple-iPad-Air-1-Tablet-Tasche-Cover-Case-braun/222154115836',
    'http://www.ebay.de/itm/Tablet-Schutzhuelle-Tasche-USB-Tastatur-9-6-Samsung-Galaxy-Tab-E-SM-T560-T561/162114447303?hash=item25bec627c7%3Ag%3ACW8AAOSwe9dZnAxf',
    'http://www.ebay.de/itm/USB-LADEKABEL-Fuer-Tablet-Pc-SAMSUNG-Galaxy-Tab-2-8-9-10-1-GT-P5100-P5110-P5113/161304376180?hash=item258e7d7374%3Ag%3AUs4AAOxyCTtTcV-',
)

facebook=(
    'https://www.facebook.com/groups/supplyanddemandinuae/',
    'https://www.facebook.com/groups/intbahmonairaqi/',
    'https://www.facebook.com/justgirlyth/videos/1490030817712538/',
    'https://www.facebook.com/AmericanKennelClub/videos/10155147462364121/',
    'https://www.facebook.com/photo.php?fbid=10213598619140125&set=p.10213598619140125&type=3',
    'https://www.facebook.com/rosalie.hormann?ref=br_rs',
    'https://www.facebook.com/photo.php?fbid=10213703459488552&set=p.10213703459488552&type=3',
    'https://www.facebook.com/judith.tebarth',
    'https://www.facebook.com/search/top/?q=edeka%20burkowski',
    'https://www.facebook.com/frischecenterburkowski/',
    'https://www.facebook.com/tatiana.e.perepelkina',
    'https://www.facebook.com/ktronikgmbh/',
    'https://www.facebook.com/aly.simpara.9',
    'https://www.facebook.com/ronja.muhr',
    'https://www.facebook.com/glow.xhkijo',
    'https://www.facebook.com/photo.php?fbid=805802272817727&set=a.111689722228989.15067.100001638859326&type=3',
    'https://www.facebook.com/photo.php?fbid=4360111298458&set=a.1191801252687.25142.1758087900&type=3',
    'https://www.facebook.com/events/birthdays/',
    'https://www.facebook.com/majid.bayern',
    'https://www.facebook.com/Corinka90',
)

amazon = (
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
)

youtube = (
    'https://www.youtube.com',
    'https://www.youtube.com/watch?v=rQ7tMWOCQlM',
    'https://www.youtube.com/watch?v=FZ_paWpT9Mo',
    'https://www.youtube.com/watch?v=gQvHtXWlXDE',
    'https://www.youtube.com/watch?v=iOe6dI2JhgU',
    'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
    'https://www.youtube.com/watch?v=JGwWNGJdvx8',
    'https://www.youtube.com/watch?v=k2qgadSvNyU',
    'https://www.youtube.com/watch?v=tt2k8PGm-TI',
    'https://www.youtube.com/watch?v=ClU3fctbGls',
    'https://www.youtube.com/watch?v=yTCDVfMz15M',
    'https://www.youtube.com/watch?v=PVjiKRfKpPI',
    'https://www.youtube.com/watch?v=TJAfLE39ZZ8',
    'https://www.youtube.com/watch?v=DksSPZTZES0',
    'https://www.youtube.com/watch?v=QK-Z1K67uaA',
    'https://www.youtube.com/watch?v=6JnGBs88sL0',
    'https://www.youtube.com/watch?v=y7ZEVA5dy-Y',
    'https://www.youtube.com/watch?v=rYEDA3JcQqw',
    'https://www.youtube.com/watch?v=fRh_vgS2dFE',
)

alexa=(
    'https://www.google.com',
    'https://www.amazon.de',
    'https://www.vk.com',
    'https://www.Ebay-kleinanzeigen.de',
    'https://www.web.de',
    'https://www.gmx.net',
    'https://www.reddit.com',
    'https://www.twitter.com',
    'https://www.instagram.com',
    'https://www.paypal.com',
    'https://www.spiegel.de',
    'https://www.chip.de',
    'https://www.bing.com',
    'https://www.bild.de',
    'https://www.live.com',
    'https://www.netflix.com',
    'https://www.otto.de',
    'https://www.welt.de',
    'https://www.bahn.de',
    'https://www.wordpress.com'
)


db = {'ebay': ebay, 'facebook':facebook, 'youtube': youtube, 'amazon':amazon}
delay = {'ebay': 20, 'facebook': 20, 'youtube': 40, 'amazon': 20, 'mix':20, 'alexa':20}

if __name__ == "__main__":
    os.system("firefox &")
    #browser(db[sys.argv[1]], delay[sys.argv[1]])
    mix_browser(sys.argv[1], delay[sys.argv[1]])