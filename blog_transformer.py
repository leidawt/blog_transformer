import re
from urllib.request import urlretrieve
import argparse
import os
parser = argparse.ArgumentParser()  # init
parser.add_argument('-f', help="input markdown file")
parser.add_argument('-d', help="path to save pictures", default='')
parser.add_argument('-m', help="replace mode", default='hexo-academic')
args = vars(parser.parse_args())
if args['d'] == '':
    SAVE_PATH = os.path.dirname(os.path.abspath(args['f']))
if args['m'] == 'hexo-academic':
    # https://sourcethemes.com/academic/docs/writing-markdown-latex/#images
    # {{<figure src = "{0}" title = "" lightbox = "true">}}
    REPLACE_MODE = '{{{{<figure src = "{0}" title = "" lightbox = "true">}}}}'
MD_FILE = args['f']
print('MD_FILE = {}'.format(MD_FILE))
print('SAVE_PATH = {}'.format(SAVE_PATH))
print('REPLACE_MODE = {}'.format(REPLACE_MODE))
print('#'*80)


def pic_download(url, path, file_name):
    file_type = ''
    if '.png' in url:
        file_type = '.png'
    elif '.jpg' in url:
        file_type = '.jpg'
    elif '.gif' in url:
        file_type = '.gif'
    else:
        raise ValueError('Not supported pic type for url: {}'.format(url))
    save_name = os.path.join(path, file_name+file_type)
    print('saving to {}'.format(save_name))

    urlretrieve(url, save_name)
    return save_name, file_type


# read markdown file into str
try:
    with open(MD_FILE, 'r') as f:
        md = f.read()
except:
    # for "utf-8 with dom" format
    with open(MD_FILE, 'r', encoding='utf-8-sig') as f:
        md = f.read()
# findall all ![xxx](xxx) commands
url_commands = re.findall(r"!\[[\s\S]*?\]\(.+?\)", md)
# download each img and change the ![xxx](xxx) commands to new REPLACE_MODE format
for id, each in enumerate(url_commands):
    id = str(id)
    url = re.findall(r"!\[[\s\S]*?\]\((.+?)\)", each)
    if url is not []:
        url = url[0]
        print("Downloading: {}".format(url))

    else:
        raise ValueError('Err in matching url in {}'.format(each))
    try:
        save_name, file_type = pic_download(url, SAVE_PATH, id)
    except(ValueError):
        pass
    print('Done')
    replace_str = REPLACE_MODE.format(id+file_type)
    print('Replacing {} to {}'.format(each, replace_str))
    md = md.replace(each, replace_str)

# save the new markdown file
print('#'*80)
print('Saving modifieded markdown file into {}'.format(
    os.path.join(SAVE_PATH, '_'+MD_FILE)))
with open(os.path.join(SAVE_PATH, '_'+MD_FILE), "w") as f:
    f.write(md)
print('Done!')
