#!/usr/bin/env python
#
# Copyright 2009 Etienne Posthumus <etienne@pos.thum.us>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import wsgiref.handlers
from google.appengine.ext import webapp

from worldcat.request.search import SRURequest
from worldcat.util.extract import extract_elements, pymarc_extract
from django.utils import simplejson

class MainHandler(webapp.RequestHandler):

  def get(self):
    query = self.request.get('query', 'srw.ti = "IISG"')
    jsonp_callback = self.request.get('jsonp_callback')
    maximumRecords = self.request.get('maximumRecords', 30)
    wskey='You Need to stick your WS_KEY from OCLC in here'
    s = SRURequest(wskey=wskey, query=query, maximumRecords=maximumRecords)
    o = s.get_response()
    
    self.response.headers['Content-Type'] = 'application/json'
    buf = []
    for r in pymarc_extract(o.data):
        rr = {}
        for f in r.get_fields():
            rr[f.tag] = f.format_field()
        buf.append(rr)
    if jsonp_callback: self.response.out.write('%s(' % jsonp_callback)
    self.response.out.write(simplejson.dumps(buf))
    if jsonp_callback: self.response.out.write(')')

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
