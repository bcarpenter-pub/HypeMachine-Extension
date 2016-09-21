import argparse
import json
import os
import urllib
import glob
import re
import datetime
import requests
parser = argparse.ArgumentParser()
parser.add_argument('--audio_meta', required=True, help="folder containing meta data with extension '.hypemeta'")
parser.add_argument('--output', required=True, help="folder to save output mp3s")

def clean(s):
    return re.sub('($ +| +^)','',re.sub('[^a-zA-Z0-9]', ' ', s))

def main(args):
    meta_files = glob.glob(args.audio_meta + '/*.hypemeta')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    output = args.output
    if not os.path.exists(output):
        os.makedirs(output)

    for m in meta_files:
        try:
            print m
            with open(m) as f:
                meta = json.loads(f.read())
                artist = meta['artist']
                title = meta['title']
                url = meta['url']
                timestamp = meta['timestamp']
                date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y%m%d')
                response =  requests.get(url, headers=headers)
                if response.ok:
                    music_data = response.content
                    out_filename = args.output + '/' + date + "-" +clean(artist) + ' - ' + clean(title) + '.mp3'
                    with open(out_filename, 'w') as of:
                        of.write(music_data)
        except:
            print "Couldnt download or read file : " + m 




if __name__ == '__main__':
    args = parser.parse_args()
    main(args)