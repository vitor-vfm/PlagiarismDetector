import os
import sys
from graph import Graph

class Detector():
    """
    Main program class

    Reads a directory, organizes its contents
    into a graph and detects plagiarism
    """

    def __init__(self, directory, sequence_size = 5, num_sequences = 10):
        """
        >>> det = Detector("/test_essays", 6, 18)
        >>> det.directory
        '/test_essays'
        >>> det.sequence_size
        6
        >>> det.num_sequences
        18
        """

        # read attritbutes
        self._directory = directory
        # add a dot to beginnig of file path
        if directory[0] != ".":
            directory = "." + directory
            
        self._sequence_size = sequence_size
        self._num_sequences = num_sequences

        self.detector_function = self.same_sentences
        self._docs_dict = self.create_docs_dict(directory)

        #self.detector_function(self,self._docs_dict, sequence_size, num_sequences)




    @property
    def directory(self):
        return self._directory

    @property
    def sequence_size(self):
        return self._sequence_size

    @property
    def num_sequences(self):
        return self._num_sequences

    @property
    def docs_dict(self):
        return self._docs_dict


    def same_sentences(self, docs_dict, sequence_size, num_sequences):
        """
        Tries to find plagiarized documents by finding sentences
        in common

        Simplest algorithm
        """
        
        # split each document in the dict
        # into sentences (split by punctuation marks)
        docs_dict = self.split_docs_into_sentences(docs_dict)

        doc_graph = Graph()
        


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
            curr_file = open(path, "r")

            docs_dict[fh] = curr_file.read()

            curr_file.close()

        return docs_dict

    def split_docs_into_sentences(self, docs_dict):
        """
        Splits all the document files inside 
        the dictionary into sentences
        """

        filenames = docs_dict.keys()

        for fl in filenames:
            filestring = docs_dict[fl]
            split_file = self.break_into_sentences(filestring)
            docs_dict[fl] = split_file


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



# end of Detector definition

# TEST FUNCTIONS

def test_create_docs_dict(detector):
    for k in detector.docs_dict.keys():
        print("Name", k)
        print("first 50 chars", detector.docs_dict[k][:50])

def test_split_docs_into_sentences(detector):
    for k in detector.docs_dict.keys():
        print("Name", k)
        print("first 3 sentences: \n", detector.docs_dict[k][:3])

# END OF TEST FUNCTIONS


def run_program():

    # read arguments
    directory = sys.argv[1]
    sequence_size = int(sys.argv[2])
    num_sequences = int(sys.argv[3])

    # create detector
    detector = Detector(directory, sequence_size, num_sequences)





if __name__=="__main__":
    import doctest
    doctest.testmod()

    run_program()



