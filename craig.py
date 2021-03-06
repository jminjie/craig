#!/usr/bin/python
import urllib2
from BeautifulSoup import BeautifulSoup
from progress.bar import Bar

# return a list of links from page_num of sfbay.craigslist.org
def get_links(page_num):
    links = []
    #url = "https://sfbay.craigslist.org/search/apa?s={}".format(page_num*100)
    url = "https://sfbay.craigslist.org/search/sfc/apa?s={}".format(page_num*100)
    req = urllib2.Request(url)#, headers={'User-Agent' : "Magic-Browser"})
    con = urllib2.urlopen(req)
    soup = BeautifulSoup(con.read())
    for thing in soup.findAll("a", { "class" : "result-image gallery"}):
        links.append(thing.get("href"))
    return links


# return price of listing from soup
def get_price(soup):
    price_span = soup.find("span", {"class" : "price"})
    if "$" in price_span.getText():
        return price_span.getText()
    return "price not found"

# return available date of listing from soup 
def get_available_date(soup):
    attr = soup.find("span", {"class" : "housing_movein_now property_date shared-line-bubble"})
    if attr is not None:
        return attr.get("data-date")
    else:
        return "no date listed"

# return title of listing from soup
def get_title(soup):
    return soup.find("title").getText().encode('ascii', 'ignore').decode('ascii')

# return bed/bathrooms from soup
def get_bb(soup):
    for thing in soup.findAll("p", {"class" : "attrgroup"}):
        if "BR" in thing.span.getText():
            return thing.span.getText()
    return "not found"

# return cat or not from soup
def get_cat(soup):
    for thing in soup.findAll("p", {"class" : "attrgroup"}):
        if "cats are OK" in thing.span.getText():
            return thing.span.getText()
    return "no cats"

# return square footage from soup
def get_sf(soup):
    for thing in soup.findAll("p", {"class" : "attrgroup"}):
        for span in thing:
            if "ft" in span:
                return span.b.getText()
    return "not found"

def main():
    # get three pages of 100 links each
    relative_links = get_links(0)
    relative_links.extend(get_links(1))
    relative_links.extend(get_links(2))
    links = ["https://sfbay.craigslist.org" + link for link in relative_links]
    # for each link, write out title and date
    fout = open("listing.txt", 'w')
    bar = Bar('Getting info for links:', max=300)
    for link in links:
        req = urllib2.Request(link)#, headers={'User-Agent' : "Magic-Browser"})
        con = urllib2.urlopen(req)
        soup = BeautifulSoup(con.read())
        fout.write(get_title(soup)+'\t'
                +link+'\t'
                +get_available_date(soup)+'\t'
                +get_price(soup)+'\t'
                +get_bb(soup)+'\t'
                +get_cat(soup)+'\t'
                +get_sf(soup)+'\t'
                +'\n')
        bar.next()
    bar.finish()
    fout.close()
    return

if __name__ == "__main__":
    main()
