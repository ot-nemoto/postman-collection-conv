# -*- coding: utf-8 -*-

import json
from argparse import ArgumentParser

class Postman:
  def __init__(self, collection_path, environment_path = None):
    if environment_path:
      with open(environment_path, 'r') as f:
        self.environment = json.loads(f.read())

    with open(collection_path, 'r') as f:
      collection_str = f.read()
      if hasattr(self, 'environment'):
        for param in list(filter(lambda x: x.get('enabled'), self.environment.get('values'))):
          collection_str = collection_str.replace('{{{{{}}}}}'.format(param.get('key')), param.get('value'))
      self.collection = json.loads(collection_str)

  def convert(self):
    ret = []
    ret.append('{} {}'.format('#' * 1, self.collection.get('info').get('name')))
    ret.append('')

    ret.extend(self.items(self.collection.get('item'), 2))

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
        ret.extend(self.request_body(item.get('request').get('body')))
        ret.extend(self.test_script(item.get('event', [])))

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

  def request_body(self, request_body):
    ret = []
    if request_body and request_body.get('mode') == 'raw' and request_body.get('options').get('raw').get('language') == 'json':
      ret.append('**Request Body**')
      ret.append('')
      ret.append('```')
      ret.extend(json.dumps(json.loads(request_body.get('raw')), indent=2).split('\n'))
      ret.append('```')
      ret.append('')
    return ret

  def test_script(self, events):
    ret = []
    for event in list(filter(lambda x: x.get('script', {}) != {}, events)):
      if len(event.get('script').get('exec', [])) > 0:
        ret.append('**Test Script**')
        ret.append('')
        ret.append('```')
        ret.extend(event.get('script').get('exec', []))
        ret.append('```')
        ret.append('')
    return ret

def get_option():
  argparser = ArgumentParser()
  argparser.add_argument('-c', '--collection', required=True)
  argparser.add_argument('-e', '--environment')
  return argparser.parse_args()

def main():
  args = get_option()
  postman = Postman(args.collection, args.environment)
  print('\n'.join(postman.convert()))

if __name__ == "__main__":
  main()
