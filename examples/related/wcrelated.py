"""find related things in worldcat by oclcnumber"""
from worldcat.request.search import BibRequest, CitationRequest, SRURequest
from worldcat.util.extract import extract_elements, pymarc_extract

import web

import os
import sys

urls = ('/', 'index', '/related/(.*)', 'related', '/related', 'related')
render = web.template.render('templates/')
WSKEY = sys.argv[1]

def get_eds(oclcnum):
    bib = BibRequest(wskey=WSKEY, rec_num=oclcnum).get_response()
    record = pymarc_extract(bib.data)
    subjects = []
    if len(record) == 0:
        return 'record %s not found' % oclcnum
    else:
        # if record[0].author() is not None:
        #         subjects.append(record[0].author())
        for s in record[0].subjects():
            if s.indicator2 == '0':
                subjects.append('"%s"' % s.format_field())
            elif s.indicator2 == '7' and s.tag == '655':
                subjects.append('"%s"' % s['a'])
        # if len(subjects) > 5:
        #     subjects = subjects[0:5]
        #     print 'more than 5 subjects - truncating'
        #print subjects
        # 'not srw.no = oclcnum'
        if len(subjects) > 0:
            sru = SRURequest(wskey=WSKEY)
            sru.args['query'] = '(srw.kw = %s) not srw.no = "%s"' % \
                                    (" or srw.kw = ".join(subjects), oclcnum)
            # sru.args['servicelevel'] = 'full'
            sru.args['sortKeys'] = 'LibraryCount,,0 relevance'
            #print sru.args['query']
            results = pymarc_extract(sru.get_response().data)
            results = [r['001'].format_field() for r in results]
            out = []
            for r in results:
                c = CitationRequest(wskey=WSKEY, rec_num=r)
                out.append(c.get_response().data)
            return "".join(out)
        else:
            return None

class index:
    def GET(self):
        print render.index()

class related:
    def GET(self, oclcnum):
        numcite = CitationRequest(wskey=WSKEY, rec_num=oclcnum).get_response().data
        print render.related(oclcnum=oclcnum, numcite=numcite,
                                response=get_eds(oclcnum))
    
    def POST(self):
        oclcnum = web.input().oclcnum
        numcite = CitationRequest(wskey=WSKEY, rec_num=oclcnum).get_response().data
        print render.related(oclcnum=oclcnum, numcite=numcite,
                                response=get_eds(oclcnum))

web.webapi.internalerror = web.debugerror
if __name__ == '__main__':
    web.run(urls, globals())