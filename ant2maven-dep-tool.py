#! /usr/bin/env python3
#
# Resolve a list of local JAR files against Maven Central.
# The script calculates the SHA-1 checksum of each JAR and
# matches them using Maven Central's REST web service. For
# files known to the service, it prints an POM dependency
# snippet, unknown files are printed for reference.
#
# Usage:
#   $ python3 ant2maven-dep-tool.py PATH
#   ex. python3 ant2maven-dep-tool.py ~/AntProject/lib
#


import requests
import sys
import hashlib
import glob

URL_FMT = 'http://search.maven.org/solrsearch/select?q=1:"{}"&rows=20&wt=json'
DEP_FMT = """\
    <dependency>
      <groupId>{}</groupId>
      <artifactId>{}</artifactId>
      <version>{}</version>
    </dependency>"""


def mkhash(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return hashlib.sha1(data).hexdigest()

def lookup(checksum):
    url = URL_FMT.format(checksum)
    result = requests.get(url)
    docs = result.json()['response']['docs']
    return docs[0] if len(docs) > 0 else None

if __name__ == '__main__':
    dep_set = set()

    for path in sys.argv[1:]:
        file_set = set()

        for filename in glob.iglob(path + '/**/*.jar', recursive=True):
            #print(filename)
            file_set.add(filename)
            print(filename)
            checksum = mkhash(filename)
            artifact = lookup(checksum)
            if artifact:
                # print(DEP_FMT.format(artifact['g'], artifact['a'], artifact['v']))
                dep_set.add(DEP_FMT.format(artifact['g'], artifact['a'], artifact['v']))
            else:
                # print('<!--UNKNOWN JAR SHA1 - {} -->'.format(filename))
                dep_set.add('<!--UNKNOWN JAR SHA1 - {} -->'.format(filename))

    # print(file_set)
    # print(dep_set)

    dep_list = sorted(dep_set)

    for dep in dep_list:
        print(dep)

# EOF