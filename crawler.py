from wikipedia import Wikipedia
import sys

wiki = Wikipedia("en", False)
wiki.crawl(int(argv[1]), int(sys.argv[2]), int(sys.argv[3]))
