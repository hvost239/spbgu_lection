import os
import sys
import json
import data_pb2 as Data

from collections import defaultdict

class Document:
    def __init__(self, **kwargs) -> None:
        self._doc_id = 0
        self._url = kwargs.get('url', '')
        self._title = kwargs.get('title', '')
        self._terms = kwargs.get('words', list())

    @property
    def doc_id(self):
        return self._doc_id

    @doc_id.setter
    def doc_id(self, value):
        self._doc_id = value

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return self._title

    def __str__(self) -> str:
        return 'url: {}, doc_id {}'.format(self._url, self._doc_id)


class Indexer:
    def __init__(self) -> None:
        self._documents = list()
        self._doc_count = 0

        self._terms = defaultdict(list)

    def add_document(self, doc):
        doc.doc_id = self._doc_count
        self._documents.append(doc)

        for s in doc.title.split():
            self._terms[s].append(doc.doc_id)

        self._doc_count += 1



    def save(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        self._save_property(dirname)
        self._save_keyinv(dirname)


    def _save_property(self, dirname):
        properties = Data.Properties()
        for d in self._documents:
            property = Data.Properties.Property()
            property.url = d.url
            property.title = 'tmp'
            properties.properies.append(property)

        with open(os.path.join(dirname, "properties.data"), mode="wb") as f:
            f.write(properties.SerializeToString())

    def _save_keyinv(self, dirname):
        keyindex = Data.KeyIndex()
        invindex = Data.InvIndex()

        cnt = 0
        for term, docs in self._terms.items():
            keyindex.term_index[term] = cnt
            td = Data.TermDocs()
            for d in docs:
                wp = Data.WordPos()
                wp.doc_id = d
                td.docs.append(wp)

            invindex.term_docs.append(td)
            cnt += 1

        with open(os.path.join(dirname, "keyindex"), mode="wb") as f:
            f.write(keyindex.SerializeToString())

        with open(os.path.join(dirname, "invindex"), mode="wb") as f:
            f.write(invindex.SerializeToString())

def main():
    idx = Indexer()

    for (dirpath,_dirnames, filenames) in os.walk(sys.argv[1]):
        for filename in filenames:
            if os.stat(os.path.join(dirpath, filename)).st_size == 0:
                continue

            with open(os.path.join(dirpath, filename)) as f:
                content = json.load(f)
                doc = Document(**content)
                idx.add_document(doc)

    idx.save(sys.argv[2])


if __name__ == "__main__":
    main()