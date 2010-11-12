# Mapping WorldCat Holdings 

## Use Case 
*   Known item search
*   by standard identifier
*   for an unavailable item

## Web services 
*   Google Maps API
*   WorldCat Registry: [worldcat.org/affiliate/tools?atype=regdetail][1]
*   WorldCat Search: [worldcat.org/devnet/index.php/SearchAPIDetails][2]
*   Holding Libraries
*   Citation Formatter
*   xOCLCNUM: [xisbn.worldcat.org/xisbnadmin/xoclcnum/api.htm][3]
*   SIMILE Exhibit: [code.google.com/p/simile-widgets][4]

## Bringing It All Together: Python 
*   geopy: [exogen.case.edu/projects/geopy][5]
*   web.py: [webpy.org][6]
*   worldcat
*   Plus a bunch of standard library modules...
*   ElementTree
*   multiprocessing
*   simplejson

## Process Overview 
1.  User submits query containing terms for OCLC number and ZIP code
2.  geopy geocodes the ZIP code
3.  worldcat grabs citation information and variant works
4.  Renders locations view...but that's not all!
5.  Locations view communicates with Exhibit API to render page elements using AJAX
6.  JavaScript sends a call to a separate controller over HTTP, requesting JSON with holdings information (OCLC symbol, name, URL for catalog, latitude/longitude
7.  JSON controller sends requests to Holdings API and WorldCat Registry, and to Google Maps (as needed)
8.  Exhibit renders that data, and you've got the gravy

## Screenshot
![demo.png](https://github.com/anarchivist/worldcat/raw/master/examples/holdingsmap/demo.png)

[1]: http://www.worldcat.org/affiliate/tools?atype=regdetail
[2]: http://www.worldcat.org/devnet/index.php/SearchAPIDetails
[3]: http://xisbn.worldcat.org/xisbnadmin/xoclcnum/api.htm
[4]: http://code.google.com/p/simile-widgets/
[5]: http://exogen.case.edu/projects/geopy/
[6]: http://webpy.org/
