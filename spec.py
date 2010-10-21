import glob
import lessipy


for lessfile in glob.glob("specs/less/*.less"):
    result = lessipy.compile(lessfile)
    cssfile = lessfile[:-4] + "css"
    with open(cssfile) as f:
        expected = f.read()
    if expected != result:
        print "ERROR: " + lessfile
        print lessfile
        print "-" * 80
        print result
        print "=" * 80
        print cssfile
        print "-" * 80
        print expected
        print "=" * 80


