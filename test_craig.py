#!/usr/bin/python
import craig
import urllib2
from BeautifulSoup import BeautifulSoup

# test all utilities on a given link
def test_one_link(link):
    req = urllib2.Request(link)#, headers={'User-Agent' : "Magic-Browser"})
    con = urllib2.urlopen(req)
    soup = BeautifulSoup(con.read())
    print link
    print craig.get_title(soup)
    print craig.get_bb(soup)
    print craig.get_cat(soup)
    print craig.get_sf(soup)
    print craig.get_available_date(soup)
    return

def main():
    # cat allowed
    test_one_link("https://sfbay.craigslist.org/sby/apa/5722070624.html")
    # no cat
    test_one_link("https://sfbay.craigslist.org/pen/apa/5727736486.html")

if __name__ == "__main__":
    main()
