#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import frontmatter
import toml
import datetime
import re

def get_arguments():
    parser = argparse.ArgumentParser(description='Convert hexo(next theme) posts to Zola(DogFood theme) posts.')
    # parser.add_argument('-s', '--src', required=True, help='source posts directory')
    # parser.add_argument('-d', '--dest', required=True, help='destination posts directory')
    return parser.parse_args()

def convert_frontmatter(txt: str, updated: datetime.datetime) -> str:
    post = frontmatter.loads(txt)
    obj = post.metadata
    obj.pop('abbrlink', None)
    obj.pop('comment', None)
    obj.pop('connments', None)
    obj['updated'] = updated
    obj['description'] = obj['desc']
    obj.pop('desc', None)
    obj.pop('summary', None)
    obj['in_search_index'] = True
    obj['taxonomies'] = {}
    obj['taxonomies']['tags'] = obj['tags']
    obj['taxonomies']['categories'] = [obj['categories']]
    obj['taxonomies']['archive'] = ['archive']
    return "+++\n{:s}+++\n{:s}".format(toml.dumps(obj), post.content)

def change_img(txt: str) -> str:
    return re.sub(r'{% asset_img (.+) (.+) %}', r'![\2](\1)', txt)

def main():
    args = get_arguments()
    
    post = open('test.md', 'r').read()
    post = convert_frontmatter(post, datetime.datetime.utcnow())
    post = change_img(post)
    print(post)

if __name__ == "__main__":
    main()