#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import frontmatter
from distutils.dir_util import copy_tree
import toml
import datetime
import re
import os

def get_arguments():
    parser = argparse.ArgumentParser(description='Convert hexo(next theme) posts to Zola(DogFood theme) posts.')
    parser.add_argument('-s', '--src', required=True, help='source posts directory')
    parser.add_argument('-d', '--dest', required=True, help='destination posts directory')
    return parser.parse_args()

def convert_frontmatter(txt: str, updated: datetime.datetime) -> str:
    post = frontmatter.loads(txt)
    obj = post.metadata
    obj['updated'] = updated.isoformat()
    obj['description'] = obj['desc']
    obj['in_search_index'] = True
    obj['taxonomies'] = {}
    obj['taxonomies']['tags'] = obj['tags']
    obj['taxonomies']['categories'] = obj['categories'] if isinstance(obj['categories'], list) else [obj['categories']]
    obj['taxonomies']['archives'] = ['archive']
    obj['date'] = obj['date'].isoformat()
    obj.pop('abbrlink', None)
    obj.pop('comment', None)
    obj.pop('connments', None)
    obj.pop('desc', None)
    obj.pop('summary', None)
    obj.pop('tags', None)
    obj.pop('categories', None)
    return "+++\n{:s}+++\n{:s}".format(toml.dumps(obj), post.content)

def change_img(txt: str) -> str:
    txt = re.sub(r'{% asset_img (.+?) (.+) %}', r'![\2](\1)', txt)
    txt = re.sub(r'date = "(.*)"', r'date = \1+00:00', txt)
    txt = re.sub(r'updated = "(.*)"', r'updated = \1+00:00', txt)
    return txt

def main():
    args = get_arguments()
    for root, _, files in os.walk(args.src):
        for name in files:
            if not name.endswith('.md'):
                continue
            src_path = os.path.join(root, name[:-3])
            post_path = os.path.join(root, name)
            dst_path = os.path.join(args.dest, name[:-3])
            updated = datetime.datetime.fromtimestamp(os.path.getmtime(post_path))
            copy_tree(src_path, dst_path)
            output = open(os.path.join(dst_path, 'index.md'), 'w')
            post = open(post_path).read()
            post = convert_frontmatter(post, updated)
            post = change_img(post)
            output.write(post)

if __name__ == "__main__":
    main()