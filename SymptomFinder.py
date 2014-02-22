import urllib2
import re
import time
import datetime

def open_website(url):
    try:
        response = urllib2.urlopen(url)
        return response.read()
    except urllib2.HTTPError, e:
        log_file.write("Time: %s\n URL: %s, Error: %s\n" % (str(datetime.datetime.now()), url, e.code))
        return urllib2.HTTPError

def write_to_file(list_of_symptoms):
    [f.write(symptom + '\n') for symptom in list_of_symptoms]

def find_symptoms():
    symptoms_website = 'http://www.rightdiagnosis.com/lists/symptoms.htm'
    html = open_website(symptoms_website)
    if html == urllib2.HTTPError:
        return
    symptoms_unparsed = re.findall('<a href=[\'\"]/sym/.*>.*</a>', html)
    symptoms_parsed = [re.sub('(<a.*?>)|(</a>)', '', symptom) for symptom in symptoms_unparsed]
    write_to_file(symptoms_parsed)

if __name__ == '__main__':
    f = open('symptom_list.txt', 'w')
    log_file = open('error_log.txt', 'a')
    find_symptoms()
    f.close()
    log_file.close()
