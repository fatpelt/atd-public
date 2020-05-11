#!/usr/bin/python3

# TODO: Update file structure in production to match the topo_build.yaml topology type and move these files to 'all'

import os
from ruamel.yaml import YAML
import jinja2
import tornado.web

class FrontEnd(tornado.web.RequestHandler):
    def _get_menus(self):
      menu_list = [x for x in os.listdir('../menus')]
      menus_dict = {}
      for menu_item in os.listdir('../menus'):
        if menu_item != 'default.yaml':
          menus_dict[menu_item.replace('.yaml', '')] = []
          menu_file = open('../menus/{0}'.format(menu_item))
          menu_items = YAML().load(menu_file)
          for lab_item in menu_items['lab_list']:
            menus_dict[menu_item.replace('.yaml', '')].append(lab_item)

      return menus_dict

    def _render_template(self,menu_data):
      with open('./templates/labs_socket_tornado.html', 'r') as file:
          template = file.read()
          env = jinja2.Environment(
              loader=jinja2.BaseLoader(),
              trim_blocks=True,
              lstrip_blocks=True,
              extensions=['jinja2.ext.do'])
          templategen = env.from_string(template)
          if templategen:
              web_data = templategen.render({'data': menu_data})
              return(web_data)
          return('<html>Error rendering template</html>')


    def get(self):
      menu_dict = self._get_menus()
      self.write(self._render_template(menu_dict))