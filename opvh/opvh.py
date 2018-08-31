import argparse
import os
import pickle

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup


DOCURL = {
    '2.2': 'https://www.opensips.org/Documentation/Script-CoreVar-2-2',
}
DATABASEPATH = '/tmp'

parser = argparse.ArgumentParser()
parser.add_argument("pv")
parser.add_argument("-V", "--doc-version",
                    help="Specify version")

parser.add_argument("-f", "--force-fetch",
                    action="store_true", help="Force documentation fetch.")

args = parser.parse_args()

def fetch_doc(version='2.2'):
    url = DOCURL[version]
    if not url:
        print("Could not find")
        return

    try:
        print("Fetching from %s" % url)
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError:
        print("Server down or incorrect domain")
    else:
        return BeautifulSoup(html.read(), features="html.parser")

def parse_doc(body, version='2.2'):
    doc = {
        'version': version,
    }
    tags = body.find_all('strong')
    for tag in tags:
        pv = tag.text
        if not pv.startswith('$'):
            continue
        doc[pv] = tag.parent.text

    return doc

def save_doc(doc, base_path=DATABASEPATH):
    filename = 'opvh_%s.p' % doc['version']
    path = os.path.join(base_path, filename)
    pickle.dump(doc, open(path, 'wb'))

def load_doc(version='2.2', base_path=DATABASEPATH):
    filename = 'opvh_%s.p' % version
    path = os.path.join(base_path, filename)
    if not os.path.isfile(path):
        return None

    return pickle.load(open(path, 'rb'))

def make_stdout(pv, description):
    description = description.replace(pv, '')
    return ('\n\033[1m%s\033[0m\n'
            '%s\n') % (pv, description)

def main():
    doc = (not args.force_fetch) and load_doc()
    if not doc:
        doc = parse_doc(fetch_doc())
        save_doc(doc)

    pv = "$%s" % args.pv
    print(make_stdout(pv, doc[pv]))


if __name__ ==  '__main__':
    main()

