# -*- coding: utf-8 -*-

import json
from argparse import ArgumentParser

class Postman:
  def __init__(self, file_path):
    with open(file_path, 'r') as f:
      self.collection = json.loads(f.read())
      self.case_layer_level = 6

  def convert(self):
    ret = []
    ret.append('# {}'.format(self.collection.get('info').get('name')))
    ret.append('')

    ret.extend(
      self.make_table_markdown(
        self.make_table_list(
          self.items(self.collection.get('item')))))

    return ret

  def items(self, items):
    ret = {}
    for item in items:
      if ('request' in item):
        ret[item.get('name')] = item.get('request').get('url').get('raw')

      else:
        ret[item.get('name')] = self.items(item.get('item', []))

    return ret

  def make_table_list(self, d, columns = []):
    ret = []
    for k, v in d.items():
      if type(v) is dict:
        ret.extend(self.make_table_list(v, columns + [k]))
      else:
        tmp_col = columns + [k]
        [tmp_col.extend(['']) for i in range(self.case_layer_level - len(tmp_col))]
        tmp_col.extend([v])
        ret.append(tmp_col)
    return ret

  def make_table_markdown(self, table_list):
    ret = []
    if table_list:
      ret.append('|Case{}Url|'.format('|' * self.case_layer_level))
      ret.append('|{}--|'.format('--|' * self.case_layer_level))
      for table in table_list:
        ret.append('|{}|'.format('|'.join(table)))
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