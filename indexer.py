from indexing import CustomAnalyzer
import os
from path import path
import lucene
import sys
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, IndexWriter, Version, StandardTokenizer, \
    LowerCaseFilter, StopFilter, ASCIIFoldingFilter, StandardAnalyzer, Version

if __name__ == "__main__":
    lucene.initVM()
    documentsPath = '/home/leontin/work/luceene/tests'
    indexDir = "/home/leontin/lucene.dir"
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = CustomAnalyzer(Version.LUCENE_30)
    writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512))
    print "Currently there are %d documents in the index." % writer.numDocs()
    print "Reading files from ", documentsPath, "."
    for fileName in os.listdir(documentsPath):
        if fileName.endswith(".json") or fileName.endswith(".txt") or fileName.endswith(".doc"):
            print >> sys.stderr, "Started processing", fileName, "."
            documentContent = path(os.path.join(documentsPath, fileName)).bytes()
            doc = Document()
            doc.add(Field("title", fileName, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("content", documentContent, Field.Store.YES, Field.Index.ANALYZED))
            writer.addDocument(doc)
            print "Finished processing document", fileName, "."

    writer.optimize()
    writer.close()

