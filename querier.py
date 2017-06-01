from indexing import CustomAnalyzer
import lucene
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexSearcher, Version, QueryParser

if __name__ == "__main__":
    lucene.initVM()
    indexDir = "/home/leontin/lucene.dir"
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = CustomAnalyzer(Version.LUCENE_30)
    searcher = IndexSearcher(dir)
    query = QueryParser(Version.LUCENE_30, "content", analyzer).parse("camasa OR mama")
    MAX = 1000
    hits = searcher.search(query, MAX)
    print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
    for hit in hits.scoreDocs:
        print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        print doc.get("content").encode("utf-8")