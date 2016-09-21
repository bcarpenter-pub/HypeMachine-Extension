import argparse
import json
import os
import urllib
import glob
import re
import datetime
parser = argparse.ArgumentParser()
parser.add_argument('--audio_meta', required=True, help="folder containing meta data with extension '.hypemeta'")
parser.add_argument('--output', required=True, help="folder to save output mp3s")

def main(args):
    meta_files = glob.glob(args.audio_meta + '/*.hypemeta')
    output = args.output
    if not os.path.exists(output):
        os.makedirs(output)

    for m in meta_files:
        try:
            with open(m) as f:
                meta = json.loads(f.read())
                artist = meta['artist']
                title = meta['title']
                url = meta['url']
                timestamp = meta['timestamp']
                date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%m%Y%d')
                music_data = urllib.urlopen(url).read()
                out_filename = args.output + '/' + date + "-" +re.sub('[^a-zA-Z0-9]', ' ', artist) + ' - ' + re.sub('[^a-zA-Z0-9]', ' ', title) + '.mp3'
                with open(out_filename, 'w') as of:
                    of.write(music_data)
        except:
            print "Couldnt download or read file : " + m 




if __name__ == '__main__':
    args = parser.parse_args()
    main(args)