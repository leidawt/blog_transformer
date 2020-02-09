import re
from urllib.request import urlretrieve
import argparse
import os
import codecs


class BlogTransformer:
    def __init__(self, mode='hexo-academic'):
        self.MD_FILE = ''
        self.SAVE_PATH = ''
        self.REPLACE_MODE = ''
        if mode == 'hexo-academic':
            # https://sourcethemes.com/academic/docs/writing-markdown-latex/#images
            # {{<figure src = "{0}" title = "" lightbox = "true">}}
            self.REPLACE_MODE = '{{{{<figure src = "{0}" title = "" lightbox = "true">}}}}'

    def _pic_download(self, url, path, file_name):
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

    def run(self, md_file, save_path='', save=True):
        self.MD_FILE = md_file
        if save_path == '':
            # use the same dir as md_file
            self.SAVE_PATH = os.path.dirname(os.path.abspath(self.MD_FILE))
        else:
            self.SAVE_PATH = save_path
        # read markdown file into str
        try:
            with open(self.MD_FILE, 'r') as f:
                md = f.read()
        except:
            # for "utf-8 with dom" format
            with open(self.MD_FILE, 'r', encoding='utf-8-sig') as f:
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
                save_name, file_type = self._pic_download(
                    url, self.SAVE_PATH, id)
            except(ValueError):
                pass
            print('Done')
            replace_str = self.REPLACE_MODE.format(id+file_type)
            print('Replacing {} to {}'.format(each, replace_str))
            md = md.replace(each, replace_str)

        # save the new markdown file
        print('#'*80)
        print('Saving modifieded markdown file into {}'.format(
            os.path.join(self.SAVE_PATH, '_'+self.MD_FILE)))
        if save:
            with codecs.open(os.path.join(self.SAVE_PATH, '_'+self.MD_FILE), "w", "utf-8") as f:
                f.write(md)
        print('Done!')
        return md


if __name__ == "__main__":

    parser = argparse.ArgumentParser()  # init
    parser.add_argument('-f', help="input markdown file")
    parser.add_argument('-d', help="path to save pictures", default='')
    parser.add_argument('-m', help="replace mode", default='hexo-academic')
    args = vars(parser.parse_args())

    print('MD_FILE = {}'.format(args['f']))
    print('SAVE_PATH = {}'.format(args['d']))
    print('REPLACE_MODE = {}'.format(args['m']))
    print('#'*80)

    bt = BlogTransformer(args['m'])
    bt.run(args['f'], args['d'])
