import itertools
import torch
from voc import PAD_token, EOS_token
import voc
import random


def indexesFromSentence(voc, sentence):
    print(sentence)
    return [voc.word2index[word] for word in sentence.split(' ')] + [EOS_token]


def zeroPadding(l, fillvalue=PAD_token):
    return list(itertools.zip_longest(*l, fillvalue=fillvalue))


def binaryMatrix(l, value=PAD_token):
    m = []
    for i, seq in enumerate(l):
        m.append([])
        for token in seq:
            if token == value:
                m[i].append(0)
            else:
                m[i].append(1)
    return m


def inputVar(l, voc):
    # Turn sentence to tensor
    print(l)
    indexes_batch = [indexesFromSentence(voc, sentence) for sentence in l]

    # Get lengths vector for each sentence
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    # Pad the batch with zeroes in order to get a tensor of size (batch_size, max_sentence_length)
    pad_list = zeroPadding(indexes_batch)
    pad_var = torch.LongTensor(pad_list)
    return pad_var, lengths


def outputVar(l, voc):
    # Turn sentence to tensor
    indexes_batch = [indexesFromSentence(voc, sentence) for sentence in l]
    # Get longest sentence in order to know how much to pad
    max_target_len = max([len(indexes) for indexes in indexes_batch])
    pad_list = zeroPadding(indexes_batch)
    # Get a tensor the size of the output tensor, with 1 in all elements different from PAD_token
    mask = binaryMatrix(pad_list)
    mask = torch.ByteTensor(mask)
    pad_var = torch.LongTensor(pad_list)
    return pad_var, mask, max_target_len


def batch2TrainData(voc, pair_batch):
    pair_batch.sort(key=lambda x: len(x[0].split(" ")), reverse=True)
    input_batch, output_batch = [], []
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])
    inp, lengths = inputVar(input_batch, voc)
    output, mask, max_target_len = outputVar(output_batch, voc)
    return inp, lengths, output, mask, max_target_len


