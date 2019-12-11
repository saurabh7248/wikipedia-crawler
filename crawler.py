from wikipedia import Wikipedia
import sys

wiki = Wikipedia(sys.argv[4] if len(sys.argv)==5 else "en", False)
wiki.crawl(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
