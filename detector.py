import os
import sys
import math
from suffix_tree import SuffixTree
from collections import Counter
from graph import Graph

class Detector:
    """
    Main program class

    Reads a directory, organizes its contents
    into a graph and detects plagiarism
    """

    def __init__(self, directory = "/test_essays", threshold = 100, algorithm = 2, mFile = None):
        """
        >>> det = Detector("/test_essays", 6, 18)
        >>> det.directory
        '/test_essays'
        >>> det.threshold
        6
        >>> det.algorithm
        18
        """

        # read attritbutes
        self._directory = directory
        self._file = mFile
        # add a dot to beginnig of file path
        if directory[0] != ".":
            directory = "." + directory
            
        self._threshold = threshold
        self._algorithm = algorithm

        self._docs_dict = self.create_docs_dict(directory)


    def run_detection(self, flag = 0):
        """
        Runs the detection and returns a list of tuples
        of possible plagiarisms

        flag determines algorithm:
        1 = same_sentences
        """
        if flag < 1 or flag > 4:
            flag = self._algorithm

        if flag == 1:
            return self.same_sentences()
        elif flag == 2:
            return self.common_sequences()
        elif flag == 3:
            return self.suffix_tree()
        elif flag == 4:
            return self.tf_idf_similarity()




    @property
    def directory(self):
        return self._directory

    @property
    def threshold(self):
        return self._threshold

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def docs_dict(self):
        return self._docs_dict


    def create_docs_dict(self, directory):
        """
        reads the directory and returns a dict
        with filenames as keys and files (as strings)
        as values
        """
        filenames = os.listdir(directory)
        docs_dict = {}

        for fh in filenames:
            path = directory + "/" + fh
            curr_file = open(path, "rb")
            docs_dict[fh] = curr_file.read().decode("utf-8", "ignore")
            curr_file.close()

        if self._file is not None:
            curr_file = open("./" + self._file)
            self.mainFile = curr_file.read().decode("utf-8", "ignore")
            curr_file.close()

        return docs_dict
    
    # 1st algorithm

    def same_sentences(self):
        """
        Tries to find plagiarized documents by finding sentences
        in common

        Simplest algorithm
        """
        
        # split each document in the dict
        # into sentences (split by punctuation marks)
        docs_dict = self.split_docs_into_sentences()

        # create a graph for the docs and 
        # add all docnames as vertices
        doc_graph = Graph(set(docs_dict.keys()))

        # find number of sentences in common
        # and add the numbers as edges
        docnames_list = list(doc_graph.vertices())
        if self._file is None:
            for i, v1 in enumerate(docnames_list):
                for j in range(i+1,len(docnames_list)):
                    v2 = docnames_list[j]
                    # each vertex is compared only to 
                    # its subsequent vertices in the list,
                    # to avoid double-computing

                    sentences_in_common = 0
                    sentences_in_2 = set(docs_dict[v2])

                    for sentence_in_1 in docs_dict[v1]:
                        if sentence_in_1 in sentences_in_2:
                            sentences_in_common += 1

                    if sentences_in_common >= self._threshold:
                        doc_graph.add_edge((v1,v2), sentences_in_common)
        else:
            # Do the same thing, except only there is no inner loop
            doc_graph.add_vertex(self._file)
            v2 = self._file
            sentences_in_2 = set(self.break_into_sentences(self.mainFile))
            for i, v1 in enumerate(docnames_list):
                
                sentences_in_common = 0
                for sentence_in_1 in docs_dict[v1]:
                    if sentence_in_1 in sentences_in_2:
                        sentences_in_common += 1

                if sentences_in_common >= self._threshold:
                    doc_graph.add_edge((v1, v2), sentences_in_common)

        # return sorted list of edges, from most in common to least
        return sorted(doc_graph.edges(), key = doc_graph.edges().get, reverse = True)


    def split_docs_into_sentences(self):
        """
        Splits all the document files inside 
        the dictionary into sentences
        """

        filenames = self._docs_dict.keys()
        split_dict = {}

        for fl in filenames:
            filestring = self._docs_dict[fl]
            split_file = self.break_into_sentences(filestring)
            split_dict[fl] = split_file

        return split_dict

    def break_into_sentences(self, s):
        """
        Separte the file strings into sentences
        (strings delimitated by punctuation)
        e.g.:

        'Hello, world' -> ['Hello', ' world']

        >>> det = Detector("/test_essays", 6, 18)
        >>> det.break_into_sentences('Hello, world')
        ['Hello', ' world']
        >>> det.break_into_sentences('Str, to. test; breaking? function')
        ['Str', ' to', ' test', ' breaking', ' function']
        """
        punctuation = set([",", ".", ";", "!", "?", "\n", "\t"])

        #return list
        ret = []

        curr_sentence = ""

        for c in s:

            if c in punctuation:
                if curr_sentence != "":
                    # add sentence to return list
                    # and reset current sentence
                    ret.append(curr_sentence)
                    curr_sentence = ""
            else:
                # add character to sentence
                curr_sentence += c

        #after loop, add last sentence
        if curr_sentence != "":
            ret.append(curr_sentence)

        return ret


    # 2nd Algorithm

    def common_sequences(self):
        """
        Find the pairs of documents that have
        sequences in common of size n or
        greater (where n was determined by the user)

        Each pair of documents gets a score equal to the sum of the 
        lengths of the common sequences

        This is a variation of the Longest Common Substring problem
        using dynamic programming
        """

        docnames_list = list(self._docs_dict.keys())

        docs_dict = self._docs_dict
        doc_graph = Graph(set(docnames_list))

        if self._file is None:
            for i, v1 in enumerate(docnames_list):
                for j in range(i+1, len(docnames_list)):
                    v2 = docnames_list[j]
                    # each vertex is compared only to 
                    # its subsequent vertices in the list,
                    # to avoid double-computing
                    nbr = self.common_sequences_score(docs_dict[v1], docs_dict[v2], self._threshold)
                    if nbr > 0:
                        doc_graph.add_edge((v1, v2), nbr)
        else:
            v2 = self._file
            doc_graph.add_vertex(v2)
            for i, v1 in enumerate(docnames_list):
                nbr = self.common_sequences_score(docs_dict[v1], self.mainFile, self._threshold)
                if nbr > 0:
                    doc_graph.add_edge((v1, v2), nbr)


        # return sorted list of edges, from most in common to least
        return sorted(doc_graph.edges(), key = doc_graph.edges().get, reverse = True)

    def common_sequences_score(self,l1,l2,size=0):
        """
        Finds how many substrings 
        are common between 2 strings
        and gives a score equal to the sum of the lengths
        of these common substrings
        
        Only substrings greater or equal to 'size' are counted

        O( len(l1) * len(l2) )

        """

        # the memo dictionary will be used 
        # as a memoization matrix
        memo = {}
        nbr = 0

        # the longest common substring starting at l1[i] and l2[j] has length:
        # 1) 0, if l1[i] != l2[j]
        # 2) 1 + length of longest common substring starting at l1[i+1] and l2[j+1]
        # This property will be used to find lengths of all common substrings bigger or equal
        # to 'size'

        # go through all pairs i,j starting at the ends of the strings
        for i in range(len(l1)-1,-1,-1):
            for j in range(len(l2)-1,-1,-1):
                # only add non-zero elements to memo
                # to save memory
                if l1[i] == l2[j]:
                    if (i+1,j+1) in memo:
                        memo[(i,j)] = 1 + memo[(i+1,j+1)]
                    else:
                        memo[(i,j)] = 1

                # if l1[i-1] and l2[j-1] exist and are different,
                # then the common substring starting at (i,j)
                # is a substring of l1 and l2, but not part
                # of any other common substring

                # Add its length to score if it's above
                # the size threshold
                if i == 0 or j == 0 or l1[i-1] != l2[j-1]:
                    if (i,j) in memo and memo[(i,j)] >= size:
                        nbr += memo[(i,j)]

        return nbr

    # 3rd Algorithm
    def suffix_tree(self):
        '''
        Use a suffix-tree to quickly get the longest common subsequence.
        Rank according to the length

        O(len(l1) + len(l2))
        '''
        docnames_list = list(self._docs_dict.keys())
        doc_graph = Graph(set(docnames_list))
        docs_dict = self._docs_dict

        if self._file is None:
            for i, v1 in enumerate(docnames_list):
                for j in range(i+1, len(docnames_list)):
                    v2 = docnames_list[j]
                    # each vertex is compared only to
                    # its subsequent vertices in the list,
                    # to avoid double-computing
                    tree = SuffixTree(docs_dict[v1], docs_dict[v2])
                    tree.buildSuffixTree()
                    lcs = tree.getLCS()
                    nbr = len(lcs)
                    if nbr > self._threshold:
                        doc_graph.add_edge((v1, v2), nbr)
        else:
            v2 = self._file
            doc_graph.add_vertex(v2)
            for i, v1 in enumerate(docnames_list):
                tree = SuffixTree(docs_dict[v1], self.mainFile)
                tree.buildSuffixTree()
                lcs = tree.getLCS()
                nbr = len(lcs)
                if nbr > self._threshold:
                    doc_graph.add_edge((v1, v2), nbr)

        # return sorted list of edges, from most in common to least
        return sorted(doc_graph.edges(), key=doc_graph.edges().get, reverse=True)

    # 4th Algorithm
    
    def tf_idf_similarity(self):
        """
        Vector Space Model

        This algorithm is based on tf-idf information retrieval

        For every pair of documents, turn both into a vector of n-gram frequencies
        and measure their similarity by calculating the cosine of these vectors

        An n-gram is a series of n words

        For this algorithm, the 'threshold' parameter
        is used as the size n of the n-grams
        """
        docnames_list = list(self._docs_dict.keys())
        ngram_size = int(self._threshold)
        min_similarity = 0.2

        # create dictionaries with each document as
        # a list and a set of n-grams 
        docs_dict = {}
        docs_dict_set_ngrams = {}
        for doc in docnames_list:
            docs_dict[doc] = self.break_into_ngrams(self._docs_dict[doc], ngram_size)
            docs_dict_set_ngrams[doc] = set(docs_dict[doc])

        # create graph
        doc_graph = Graph(set(docnames_list))
        if self._file is None:
            for i, v1 in enumerate(docnames_list):
                # use ngrams in v1 as corpus for this query
                # eliminate duplicates
                wordspace = list(set(docs_dict[v1]))

                # make a dictionary that maps each n-gram in the corpus to its idf
                idf = self.inverse_document_frequency(wordspace, docs_dict_set_ngrams)

                doc1 = self.document_vector(docs_dict[v1], idf, wordspace)

                for j in range(i+1,len(docnames_list)):
                    v2 = docnames_list[j]
                    # each vertex is compared only to 
                    # its subsequent vertices in the list,
                    # to avoid double-computing
                    doc2 = self.document_vector(docs_dict[v2], idf, wordspace)
                    sim = self.cosine_similarity(doc1,doc2)
                    if sim >= min_similarity:
                        doc_graph.add_edge((v1,v2), sim)
        else:
            v2 = self._file
            doc_graph.add_vertex(v2)
            v2ngram = self.break_into_ngrams(self.mainFile, ngram_size)
            docs_dict_set_ngrams[v2] = set(v2ngram)
            for i, v1 in enumerate(docnames_list):
                # use ngrams in v1 as corpus for this query
                # eliminate duplicates
                wordspace = list(set(docs_dict[v1]))

                # make a dictionary that maps each n-gram in the corpus to its idf
                idf = self.inverse_document_frequency(wordspace, docs_dict_set_ngrams)

                doc1 = self.document_vector(docs_dict[v1], idf, wordspace)
                doc2 = self.document_vector(v2ngram, idf, wordspace)
                sim = self.cosine_similarity(doc1, doc2)
                if sim >= min_similarity:
                    doc_graph.add_edge((v1, v2), sim)

        # return sorted list of edges, from most in common to least
        return sorted(doc_graph.edges(), key = doc_graph.edges().get, reverse = True)

    def cosine_similarity(self, doc1, doc2):
        """
        Get the cosine of two document vectors

        cosine = dot product / product of magnitudes

        The higher the cosine, the closer the vectors are
        """

        mag1 = 0
        mag2 = 0
        dot_product = 0
        for i in range(len(doc1)):
            mag1 += doc1[i]**2
            mag2 += doc2[i]**2
            dot_product += doc1[i]*doc2[i]

        mag1 = math.sqrt(mag1)
        mag2 = math.sqrt(mag2)

        if dot_product == 0:
            return 0
        else:
            return dot_product/(mag1*mag2)

    def inverse_document_frequency(self,wordspace, words_sets):
        """
        A measure of how rare an n-gram is
        in the collection of documents

        idf = log( N / (count + 1) )
        where:
        N = size of document set
        count = number of documents that contain the n-gram

        (the +1 is to avoid problems when count is 0)
        """
        idf = {}

        for ngram in wordspace:
            count = 0
            for doc in words_sets:
                if ngram in doc:
                    count += 1
            try:
                idf[ngram] = math.log(len(wordspace)/(count + 1))
            except:
                idf[ngram] = 100000000  #  Some large number

        return idf

    def document_vector(self,doc,idf,wordspace):
        """
        Returns a vector corresponding to each document
        where each element x_i corresponds to the tf-idf
        (term frequency)*(inverse document frequency) of
        word i in the wordspace

        term frequency = how frequent a word is in the document
        inverse_document_frequency = a measure of how rare an n-gram is
        in the collection of documents
        """
        tf_idf = []
        for ngram in wordspace:
            # count the number of ocurrences of the ngram in the doc and
            # divide by length to get a percentage (float between 0 and 1)
            term_frequency = (doc.count(ngram)/float(len(doc)))

            tf_idf.append(term_frequency*idf[ngram])

        return tf_idf

    def break_into_ngrams(self, s, n):
        """
        Separate the file strings into n-grams
        (sequences of n words)
        e.g.:

        Similar to break_into_sentences
        """
        punctuation = set([",", ".", ";", "!", "?", "\n", "\t"])

        #return list
        ret = []

        curr_ngram = ""
        n_gram_count = 0
        for c in s:

            # ignore punctuation
            if c in punctuation:
                continue

            # spaces mark separation between words
            if c == " ":
                n_gram_count += 1

            # every n words, add n-gram to list
            if n_gram_count == n:
                # make it not case-sensitive
                curr_ngram = curr_ngram.lower()
                if curr_ngram != "":
                    ret.append(curr_ngram)
                # reset current n-gram
                curr_ngram = ""
                # reset counter
                n_gram_count = 0
            else:
                # if we haven't completed an n-gram,
                # simply add the character
                curr_ngram += c

        #after loop, add last ngram
        if curr_ngram != "":
            ret.append(curr_ngram)

        return ret


# end of Detector definition

if __name__=="__main__":
    import doctest
    doctest.testmod()
