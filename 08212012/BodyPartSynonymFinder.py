import urllib2
import re

f_in = open('body_parts.txt', 'r')
f_out = open('body_parts_extended.txt', 'w')

for line in f_in:
    body_part = line.strip()
    print body_part
    response = urllib2.urlopen("http://www.thesaurus.com/browse/%s" % body_part)
    html = response.read()
    if "No results found" in html:
        f_out.write("%s:\n" % body_part)
    else:
        synonyms = html.split('<td valign="top">Synonyms:</td>')[1].split('</span>')[0]
        parsed_synonyms = re.sub('<.*?>', '', synonyms.replace('\n', ''))
        f_out.write("%s: %s\n" % (body_part, parsed_synonyms))

f_in.close()
f_out.close()