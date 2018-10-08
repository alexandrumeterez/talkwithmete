import data_loader
import data_preprocess
# import voc
import codecs
import csv
from config import *
import torch
from model import *
import voc
import pickle
import torch.optim as optim

    # # Load/Assemble voc and pairs
    # corpus_name = "metetext"
    # datafile = "./data/datafile"
    # voc, pairs = data_preprocess.loadPrepareData(corpus_name, datafile)
    # # Print some pairs to validate
    # pairs = data_preprocess.trimRareWords(voc, pairs, 3)
    #
    # keep_pairs = []
    # for pair in pairs:
    #     first = pair[0]
    #     second = pair[1]
    #     keep = True
    #     first_words = first.split(' ')
    #     second_words = second.split(' ')
    #     for word in first_words:
    #         if len(word) < 2:
    #             keep = False
    #             break
    #     for word in second_words:
    #         if len(word) < 2:
    #             keep = False
    #             break
    #     if keep:
    #         keep_pairs.append(pair)
    # pairs = keep_pairs
    #
    # delimiter = '\t'
    # # Unescape the delimiter
    # delimiter = str(codecs.decode(delimiter, "unicode_escape"))
    # with open("./data/processed_datafile", 'w', encoding='utf-8') as outputfile:
    #     writer = csv.writer(outputfile, delimiter=delimiter)
    #     for pair in pairs:
    #         writer.writerow(pair)
    # import pickle
    # pickle.dump(voc, open("./data/voc.pkl", 'wb'))
    # print("\npairs:")
    # for pair in pairs[:10]:
    #     print(pair)


# if __name__ == "__main__":
def run_chatbot(input_sentence=''):
    loadFilename = "./checkpoints/cb_model/metetext/2-2_500/5000_checkpoint.tar"
    checkpoint_iter = 4000
    voc = pickle.load(open("./data/voc.pkl", 'rb'))
    pairs = open("./data/processed_datafile", encoding='utf-8').read().strip().split('\n')
    pairs = [(pair.split('\t')[0], pair.split('\t')[1]) for pair in pairs]
    if loadFilename:
        # If loading on same machine the model was trained on
        # checkpoint = torch.load(loadFilename)
        # If loading a model trained on GPU to CPU
        checkpoint = torch.load(loadFilename, map_location=torch.device('cpu'))
        encoder_sd = checkpoint['en']
        decoder_sd = checkpoint['de']
        encoder_optimizer_sd = checkpoint['en_opt']
        decoder_optimizer_sd = checkpoint['de_opt']
        embedding_sd = checkpoint['embedding']
        voc.__dict__ = checkpoint['voc_dict']
    print('Building encoder and decoder ...')
    # Initialize word embeddings
    embedding = nn.Embedding(voc.num_words, hidden_size)
    if loadFilename:
        embedding.load_state_dict(embedding_sd)
    # Initialize encoder & decoder models
    encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
    decoder = DecoderRNN(embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
    if loadFilename:
        encoder.load_state_dict(encoder_sd)
        decoder.load_state_dict(decoder_sd)
    # Use appropriate device
    encoder = encoder.to(device)
    decoder = decoder.to(device)
    print('Models built and ready to go!')
    # Ensure dropout layers are in train mode
    encoder.train()
    decoder.train()

    # Initialize optimizers
    print('Building optimizers ...')
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
    if loadFilename:
        encoder_optimizer.load_state_dict(encoder_optimizer_sd)
        decoder_optimizer.load_state_dict(decoder_optimizer_sd)

    # Run training iterations
    # print("Starting Training!")
    # corpus_name = "metetext"
    # save_dir = "./checkpoints"
    # trainIters(model_name, voc, pairs, encoder, decoder, encoder_optimizer, decoder_optimizer,
    #            embedding, encoder_n_layers, decoder_n_layers, save_dir, n_iteration, batch_size,
    #            print_every, save_every, clip, corpus_name, loadFilename)

    # Set dropout layers to eval mode
    encoder.eval()
    decoder.eval()

    # Initialize search module
    searcher = GreedySearchDecoder(encoder, decoder)

    # Begin chatting (uncomment and run the following line to begin)
    return evaluateInput(encoder, decoder, searcher, voc, input_sentence)