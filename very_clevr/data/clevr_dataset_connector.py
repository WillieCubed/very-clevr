# Thanks to https://github.com/mesnico/RelationNetworks-CLEVR/blob/master/clevr_dataset_connector.py
#
# MIT License
#
# Copyright (c) 2018 Nicola Messina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import pickle
import re
from PIL import Image

from collections import Counter
from torch.utils.data import Dataset
from tqdm import tqdm

import torch


# TODO: Create independent implementation because this is obviously nope
# https://github.com/mesnico/RelationNetworks-CLEVR/blob/b8e0e7af12408877c8a18d8f2802d88138605983/utils.py#L18


classes = {
    "number": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "material": ["rubber", "metal"],
    "color": ["cyan", "blue", "yellow", "purple", "red", "green", "gray", "brown"],
    "shape": ["sphere", "cube", "cylinder"],
    "size": ["large", "small"],
    "exist": ["yes", "no"],
}


def to_dictionary_indexes(dictionary, sentence):
    """
    Outputs indexes of the dictionary corresponding to the words in the sequence.
    Case insensitive.
    """
    split = tokenize(sentence)
    idxs = torch.LongTensor([dictionary[w] for w in split])
    return idxs


def tokenize(sentence):
    # punctuation should be separated from the words
    s = re.sub("([.,;:!?()])", r" \1 ", sentence)
    s = re.sub("\s{2,}", " ", s)

    # tokenize
    split = s.split()

    # normalize all words to lowercase
    lower = [w.lower() for w in split]
    return lower


def build_dictionaries(clevr_dir):
    def compute_class(answer):
        for name, values in classes.items():
            if answer in values:
                return name

        raise ValueError("Answer {} does not belong to a known class".format(answer))

    cached_dictionaries = os.path.join(
        clevr_dir, "questions", "CLEVR_built_dictionaries.pkl"
    )
    if os.path.exists(cached_dictionaries):
        print("==> using cached dictionaries: {}".format(cached_dictionaries))
        with open(cached_dictionaries, "rb") as f:
            return pickle.load(f)

    quest_to_ix = {}
    answ_to_ix = {}
    answ_ix_to_class = {}
    json_train_filename = os.path.join(
        clevr_dir, "questions", "CLEVR_train_questions.json"
    )
    # load all words from all training data
    with open(json_train_filename, "r") as f:
        questions = json.load(f)["questions"]
        for q in tqdm(questions):
            question = tokenize(q["question"])
            answer = q["answer"]
            # pdb.set_trace()
            for word in question:
                if word not in quest_to_ix:
                    quest_to_ix[word] = (
                        len(quest_to_ix) + 1
                    )  # one based indexing; zero is reserved for padding

            a = answer.lower()
            if a not in answ_to_ix:
                ix = len(answ_to_ix) + 1
                answ_to_ix[a] = ix
                answ_ix_to_class[ix] = compute_class(a)

    ret = (quest_to_ix, answ_to_ix, answ_ix_to_class)
    with open(cached_dictionaries, "wb") as f:
        pickle.dump(ret, f)

    return ret


class ClevrDataset(Dataset):
    def __init__(self, clevr_dir, train, dictionaries, transform=None):
        """
        Args:
            clevr_dir (string): Root directory of CLEVR dataset
                        train (bool): Tells if we are loading the train or the validation datasets
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        if train:
            quest_json_filename = os.path.join(
                clevr_dir, "questions", "CLEVR_train_questions.json"
            )
            self.img_dir = os.path.join(clevr_dir, "images", "train")
        else:
            quest_json_filename = os.path.join(
                clevr_dir, "questions", "CLEVR_val_questions.json"
            )
            self.img_dir = os.path.join(clevr_dir, "images", "val")

        cached_questions = quest_json_filename.replace(".json", ".pkl")
        if os.path.exists(cached_questions):
            print("==> using cached questions: {}".format(cached_questions))
            with open(cached_questions, "rb") as f:
                self.questions = pickle.load(f)
        else:
            with open(quest_json_filename, "r") as json_file:
                self.questions = json.load(json_file)["questions"]
            with open(cached_questions, "wb") as f:
                pickle.dump(self.questions, f)

        self.clevr_dir = clevr_dir
        self.transform = transform
        self.dictionaries = dictionaries

    def answer_weights(self):
        n = float(len(self.questions))
        answer_count = Counter(q["answer"].lower() for q in self.questions)
        weights = [n / answer_count[q["answer"].lower()] for q in self.questions]
        return weights

    def __len__(self):
        return len(self.questions)

    def __getitem__(self, idx):
        current_question = self.questions[idx]
        img_filename = os.path.join(self.img_dir, current_question["image_filename"])
        image = Image.open(img_filename).convert("RGB")

        question = to_dictionary_indexes(
            self.dictionaries[0], current_question["question"]
        )
        answer = to_dictionary_indexes(self.dictionaries[1], current_question["answer"])
        """if self.dictionaries[2][answer[0]]=='color':
            image = Image.open(img_filename).convert('L')
            image = numpy.array(image)
            image = numpy.stack((image,)*3)
            image = numpy.transpose(image, (1,2,0))
            image = Image.fromarray(image.astype('uint8'), 'RGB')"""

        sample = {"image": image, "question": question, "answer": answer}

        if self.transform:
            sample["image"] = self.transform(sample["image"])

        return sample


class ClevrDatasetStateDescription(Dataset):
    def __init__(self, clevr_dir, train, dictionaries):

        if train:
            quest_json_filename = os.path.join(
                clevr_dir, "questions", "CLEVR_train_questions.json"
            )
            scene_json_filename = os.path.join(
                clevr_dir, "scenes", "CLEVR_train_scenes.json"
            )
        else:
            quest_json_filename = os.path.join(
                clevr_dir, "questions", "CLEVR_val_questions.json"
            )
            scene_json_filename = os.path.join(
                clevr_dir, "scenes", "CLEVR_val_scenes.json"
            )

        cached_questions = quest_json_filename.replace(".json", ".pkl")
        cached_scenes = scene_json_filename.replace(".json", ".pkl")
        if os.path.exists(cached_questions):
            print("==> using cached questions: {}".format(cached_questions))
            with open(cached_questions, "rb") as f:
                self.questions = pickle.load(f)
        else:
            with open(quest_json_filename, "r") as json_file:
                self.questions = json.load(json_file)["questions"]
            with open(cached_questions, "wb") as f:
                pickle.dump(self.questions, f)

        if os.path.exists(cached_scenes):
            print("==> using cached scenes: {}".format(cached_scenes))
            with open(cached_scenes, "rb") as f:
                self.objects = pickle.load(f)
        else:
            all_scene_objs = []
            with open(scene_json_filename, "r") as json_file:
                scenes = json.load(json_file)["scenes"]
                print("caching all objects in all scenes...")
                for s in scenes:
                    objects = s["objects"]
                    objects_attr = []
                    for obj in objects:
                        attr_values = []
                        for attr in sorted(obj):
                            # convert object attributes in indexes
                            if attr in classes:
                                attr_values.append(
                                    classes[attr].index(obj[attr]) + 1
                                )  # zero is reserved for padding
                            else:
                                """if attr=='rotation':
                                attr_values.append(float(obj[attr]) / 360)"""
                                if attr == "3d_coords":
                                    attr_values.extend(obj[attr])
                        objects_attr.append(attr_values)
                    all_scene_objs.append(torch.FloatTensor(objects_attr))
                self.objects = all_scene_objs
            with open(cached_scenes, "wb") as f:
                pickle.dump(all_scene_objs, f)

        self.clevr_dir = clevr_dir
        self.dictionaries = dictionaries

    """def answer_weights(self):
        n = float(len(self.questions))
        answer_count = Counter(q['answer'].lower() for q in self.questions)
        weights = [n/answer_count[q['answer'].lower()] for q in self.questions]
        return weights"""

    def __len__(self):
        return len(self.questions)

    def __getitem__(self, idx):
        current_question = self.questions[idx]
        scene_idx = current_question["image_index"]
        obj = self.objects[scene_idx]

        question = to_dictionary_indexes(
            self.dictionaries[0], current_question["question"]
        )
        answer = to_dictionary_indexes(self.dictionaries[1], current_question["answer"])
        """if self.dictionaries[2][answer[0]]=='color':
            image = Image.open(img_filename).convert('L')
            image = numpy.array(image)
            image = numpy.stack((image,)*3)
            image = numpy.transpose(image, (1,2,0))
            image = Image.fromarray(image.astype('uint8'), 'RGB')"""

        sample = {"image": obj, "question": question, "answer": answer}

        return sample


class ClevrDatasetImages(Dataset):
    """
    Loads only images from the CLEVR dataset
    """

    def __init__(self, clevr_dir, train, transform=None):
        """
        :param clevr_dir: Root directory of CLEVR dataset
        :param mode: Specifies if we want to read in val, train or test folder
        :param transform: Optional transform to be applied on a sample.
        """
        self.mode = "train" if train else "val"
        self.img_dir = os.path.join(clevr_dir, "images", self.mode)
        self.transform = transform

    def __len__(self):
        return len(os.listdir(self.img_dir))

    def __getitem__(self, idx):
        padded_index = str(idx).rjust(6, "0")
        img_filename = os.path.join(
            self.img_dir, "CLEVR_{}_{}.png".format(self.mode, padded_index)
        )
        image = Image.open(img_filename).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image


class ClevrDatasetImagesStateDescription(ClevrDatasetStateDescription):
    def __init__(self, clevr_dir, train):
        super().__init__(clevr_dir, train, None)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, idx):
        return self.objects[idx]
