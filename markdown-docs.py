# -*- coding: utf-8 -*-

import json
from argparse import ArgumentParser

class Postman:
  def __init__(self, file_path):
    with open(file_path, 'r') as f:
      self.collection = json.loads(f.read())
      self.sub_heading_layer = 1

  def convert(self):
    ret = []
    ret.append('{} {}'.format('#' * 1, self.collection.get('info').get('name')))

    ret.extend(self.items(self.collection.get('item'), 1))

    return ret

  def items(self, items, heading_level):
    ret = []
    for item in items:
      if ('request' in item):
        ret.append('`{}` {}'.format(item.get('request').get('method'), item.get('name')))
        ret.append('')
        ret.append('```')
        ret.append('{}'.format(item.get('request').get('url').get('raw')))
        ret.append('```')
        ret.append('')

        ret.extend(self.request_headers(item.get('request').get('header', [])))
        ret.extend(self.query_params(item.get('request').get('url').get('query', [])))

      else:
        ret.append('{} {}'.format('#' * heading_level, item.get('name')))
        ret.append('')

        ret.extend(self.items(item.get('item', []), heading_level + 1))
    return ret

  def request_headers(self, request_headers):
    ret = []
    if request_headers and len(list(filter(lambda x: 'disabled' not in x, request_headers))) > 0:
      ret.append('**Request Headers**')
      ret.append('')
      ret.append('|KEY|VALUE|DESCRIPTION|')
      ret.append('|--|--|--|')
      for v in filter(lambda x: 'disabled' not in x, request_headers):
        ret.append('|{}|{}|{}|'.format(v.get('key', ''),v.get('value', ''),v.get('description', '')))
      ret.append('')
    return ret

  def query_params(self, query_params):
    ret = []
    if query_params and len(list(filter(lambda x: 'disabled' not in x, query_params))) > 0:
      ret.append('**Query Params**')
      ret.append('')
      ret.append('|KEY|VALUE|DESCRIPTION|')
      ret.append('|--|--|--|')
      for v in filter(lambda x: 'disabled' not in x, query_params):
        ret.append('|{}|{}|{}|'.format(v.get('key', ''),v.get('value', ''),v.get('description', '')))
      ret.append('')
    return ret

def get_option():
  argparser = ArgumentParser()
  argparser.add_argument('-f', '--file', required=True)
  return argparser.parse_args()

def main():
  args = get_option()
  postman = Postman(args.file)
  print('\n'.join(postman.convert()))

if __name__ == "__main__":
  main()