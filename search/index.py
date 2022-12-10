from flask import current_app

import data_pb2 as Data
import os



class Index():
    def __init__(self, dirname) -> None:
        self._properties = Data.Properties()
        self._keyindex = Data.KeyIndex()
        self._invindex = Data.InvIndex()

        self._load(dirname)

    def _load(self, dirname):
         with open(os.path.join(dirname, "properties.data"), mode="rb") as f:
            self._properties.ParseFromString(f.read())

         with open(os.path.join(dirname, "keyindex"), mode="rb") as f:
            self._keyindex.ParseFromString(f.read())

         with open(os.path.join(dirname, "invindex"), mode="rb") as f:
            self._invindex.ParseFromString(f.read())

    def search(self, text):
        # term_idxs = [self._keyindex.term_index[term] for term in terms if term in self._keyindex.term_index]

        if text not in self._keyindex.term_index:
            return 'None'

        term_idx = self._keyindex.term_index[text]

        doc_ids = [wp.doc_id for wp in  self._invindex.term_docs[term_idx].docs]

        return [p.url for p in [self._properties.properies[i] for i in doc_ids]]
