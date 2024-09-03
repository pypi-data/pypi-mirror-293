import json
import re
from zipfile import ZipFile
from io import TextIOWrapper
from tqdm import tqdm
from spacy.lang.en import English
from saf import Token
from ..skb import KnowledgeBase, BASE_URL
from ..data_model import Statement, Entity

PATH = "ProofWiki/proofwiki.zip"
URL = BASE_URL + "proofwiki.zip"


class ProofWikiKB(KnowledgeBase):
    """
    Wrapper for the ProofWiki dataset (Ferreira et al., 2018): https://github.com/ai-systems/tg2022task_premise_retrieval
    """
    def __init__(self, path: str = PATH, url: str = URL):
        super().__init__(path, url)
        self.tokenizer = English().tokenizer
        self.id = PATH.split(".")[0]
        self.key_idx: dict[int, list[Statement]] = dict()
        if (not url):
            return

        with ZipFile(self.data_path) as dataset_file:
            self.data = list()

            with TextIOWrapper(dataset_file.open(f"ProofWiki/def_titles.txt"), encoding="utf-8") as ent_file:
                for line in ent_file:
                    ent = Entity(line.strip(), self.id)
                    self.entities.append(ent)

            with TextIOWrapper(dataset_file.open(f"ProofWiki/knowledge_base.json"), encoding="utf-8") as data_file:
                data = json.load(data_file)
                for key in tqdm(data, desc=f"Loading data [Knowledge Base]"):
                    sents = data[key].split("\n")
                    self.key_idx[int(key)] = list()
                    for sent in sents:
                        stt = Statement(sent)
                        stt.annotations["split"] = "KB"
                        stt.annotations["type"] = "fact"
                        stt.annotations["id"] = int(key)

                        for tok in self.tokenizer(stt.surface):
                            token = Token()
                            token.surface = tok.text
                            stt.tokens.append(token)

                        self.data.append(stt)
                        self.key_idx[int(key)].append(stt)

            for split in ["train", "dev", "test"]:
                with TextIOWrapper(dataset_file.open(f"ProofWiki/{split}_set.json"), encoding="utf-8") as data_file:
                    data = json.load(data_file)
                    for key in tqdm(data, desc=f"Loading data [{split}]"):
                        sents = data[key]["text"].split("\n")
                        prop_stts = list()
                        self.key_idx[int(key)] = list()
                        for sent in sents:
                            stt = Statement(sent)
                            stt.annotations["split"] = split
                            stt.annotations["type"] = "proposition"
                            stt.annotations["id"] = int(key)
                            if (len(prop_stts) == 0):
                                for prem_id in data[key]["premises"]:
                                    if (prem_id in self.key_idx):
                                        stt.premises.extend(self.key_idx[prem_id])
                            else:
                                stt.premises = prop_stts[0].premises

                            for tok in self.tokenizer(stt.surface):
                                token = Token()
                                token.surface = tok.text
                                stt.tokens.append(token)

                            self.data.append(stt)
                            self.key_idx[int(key)].append(stt)
                            prop_stts.append(stt)

        stt_text_l = [stt.surface.lower() for stt in self.data]
        for ent in tqdm(self.entities, desc="Searching entities"):
            ent_name = ent.surface.lower()
            stt_matches = [stt_idx for stt_idx, stt_txt in enumerate(stt_text_l)
                           if (self.entity_name_search(ent_name,stt_txt))]
            for stt_idx in stt_matches:
                self.data[stt_idx].entities.append(ent)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx: int | slice) -> Statement | list[Statement]:
        """Fetches the ith statement in the KB.

        Args:
            idx (int): index for the ith term in the KB.

        :return: A single term definition (Statement).
        """
        if (isinstance(idx, slice)):
            item = self.data[idx]
        else:
            item = self.data[idx] if (idx < len(self)) else self.key_idx[idx]

        return item

    def keys(self):
        return self.key_idx.keys()

    def entity_name_search(self, ent_name: str, text: str) -> bool:
        if (ent_name in text):
            match = f" {ent_name} " in text or f"'{ent_name}'" in text or f'"{ent_name}"' in text
        else:
            match = False

        return match


