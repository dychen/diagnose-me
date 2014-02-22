import urllib2
import re
import time
import sys
import datetime

def open_website(url):
    try:
        response = urllib2.urlopen(url)
        return response.read()
    except urllib2.HTTPError, e:
        log_file.write("Time: %s\n URL: %s, Error: %s\n" % (str(datetime.datetime.now()), url, e.code))
        return urllib2.HTTPError

def strip_website_letter_index(html):
    return html.split('<div id="b" class="tests">')[1].split('</div>')[0]

def strip_website_symptoms(html):
    return html.split('<div id="b">')[1].split('</div>')[0]

def strip_link(link):
    return link.split('=\"')[1].split('\">')[0]

def strip_symptom(symptom):
    return symptom.split('<li>')[1].split('</li>')[0]

def find_disease_links_from_html(html):
    return re.findall('<a *href=.*?>', html)

def find_disease_name(html):
    return html.split('<title>')[1].split(':')[0]

def find_symptoms(html):
    return re.findall('<li>.*?</li>', html)

def write_to_file(disease_name, list_of_symptoms):
    f.write(disease_name + "::")
    f.write(';;'.join(map(strip_symptom, list_of_symptoms)) + '\n')

def find_and_write_diseases(letter):
    index_url = 'http://www.mayoclinic.com/health/DiseasesIndex/DiseasesIndex/METHOD=displayAlphaList&LISTTYPE=mcDisease&LETTER=%s'
    base_url = 'http://www.mayoclinic.com%s'
    html = open_website(index_url % letter)
    if html == urllib2.HTTPError:
        return
    stripped_html = strip_website_letter_index(html)
    disease_links = find_disease_links_from_html(stripped_html)
    print "Number of diseases starting with letter %c found: %s" % (letter, len(disease_links))
    for link in disease_links:
        disease_url = strip_link(link)
        target_url = base_url % disease_url + '/DSECTION=symptoms'
        html = open_website(target_url)
        if html == urllib2.HTTPError:
            continue
        disease_name = find_disease_name(html)
        write_to_file(disease_name, find_symptoms(strip_website_symptoms(html)))
        # Print stuff out... and be nice...
        print disease_name
        for symptom in find_symptoms(strip_website_symptoms(html)):
            print symptom
        #time.sleep(0.5)

def find_diseases(letter = None):
    if letter == None:
        for letter in map(chr, range(97, 123)):
            find_and_write_diseases(letter)
    else:
        for letter in map(chr, range(ord(letter), 123)):
            find_and_write_diseases(letter)

if __name__ == '__main__':
    f = open('diseases_and_symptoms.txt', 'w')
    log_file = open('error_log.txt', 'a')
    if len(sys.argv) == 2 and sys.argv[1].lower() in map(chr, range(97, 123)):
        find_diseases(sys.argv[1])
    find_diseases()
    f.close()
    log_file.close()
