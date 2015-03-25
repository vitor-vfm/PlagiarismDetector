def test_create_docs_dict(detector):
    for k in detector.docs_dict.keys():
        print("Name", k)
        print("first 50 chars", detector.docs_dict[k][:50])

def test_split_docs_into_sentences(detector):
    for k in detector.docs_dict.keys():
        print("Name", k)
        print("first 3 sentences: \n", detector.docs_dict[k][:3])

