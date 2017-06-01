from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, Version, StandardTokenizer, \
    LowerCaseFilter, StopFilter, ASCIIFoldingFilter, PythonAnalyzer, HashSet

from lucene import PythonTokenFilter, TermAttribute, PositionIncrementAttribute

import snowballstemmer

class CustomAnalyzer(PythonAnalyzer):

    def __init__(self, Version):
        super(CustomAnalyzer, self).__init__(Version)
        data = self.file_get_contents('/home/leontin/work/luceene/stop.txt')
        self.stopwords = HashSet()
        for word in data:
            self.stopwords.add(word)

    def tokenStream(self, field, reader):
        res = StandardTokenizer(Version.LUCENE_30, reader)
        res = LowerCaseFilter(res)
        res = CustomSnowballFilter(res)
        res = ASCIIFoldingFilter(res)
        res = StopFilter(False, res, self.stopwords)
        return res

    def file_get_contents(self, fileName):
        with open(fileName, "r") as f:
            return f.read()

class CustomSnowballFilter(PythonTokenFilter):
    def __init__(self, input):
        PythonTokenFilter.__init__(self, input)
        self.input = input

    def incrementToken(self):
        if not self.input.incrementToken():
            return False
        self.stemmer = snowballstemmer.stemmer('romanian')
        term_attribute = self.addAttribute(
            TermAttribute.class_)
        position_attribute = self.addAttribute(
            PositionIncrementAttribute.class_)
        token = self.input.getAttribute(
            TermAttribute.class_).toString()

        new = self.stemmer.stemWord(token)

        term_attribute.setTermBuffer(new)
        position_attribute.setPositionIncrement(1)
        return True