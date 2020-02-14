#! py -3
#!/usr/bin/env python3

import os
import sys
import argparse
from blog_transformer import BlogTransformer
import codecs

if __name__ == "__main__":

    parser = argparse.ArgumentParser()  # init
    parser.add_argument('-f', help="input markdown file")
    parser.add_argument('-t', help="time in format YYYY-MM-DD")
    parser.add_argument('-d', help="path to save", default='')
    args = vars(parser.parse_args())

    # read markdown file into str
    try:
        with open(args['f'], 'r') as f:
            md = f.read()
    except:
        # for "utf-8 with dom" format
        with open(args['f'], 'r', encoding='utf-8-sig') as f:
            md = f.read()
    with open(sys.path[0]+'/templete.md', 'r') as f:
        # sys.path[0] is the path were this file(pipline.py) locate
        templete = f.read()
    file_name = os.path.basename(args['f']).split('.')[0]
    print('file_name = {}'.format(file_name))
    if args['d'] == '':
        new_dir = os.path.join(os.path.dirname(os.path.abspath(args['f'])), file_name)
    else:
        # args['d'] should be absolute path
        new_dir = os.path.join(args['d'], file_name)
    try:
        os.mkdir(new_dir)
    except(FileExistsError):
        print('dir already exist, pass')
        sys.exit(0)
    templete = templete.replace('TITLE_TO_BE_REPLACED', file_name)
    templete = templete.replace('TIME_TO_BE_REPLACED',
                                '{}T12:00:00+08:00'.format(args['t']))
    # print(templete)

    bt = BlogTransformer()
    md = bt.run(args['f'], save_path=new_dir, save=False)
    with codecs.open(os.path.join(new_dir, "index.md"), "w", "utf-8") as f:
        f.write(templete+'\n'+md)
