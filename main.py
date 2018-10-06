import data_loader
import data_preprocess
import voc



if __name__ == "__main__":
    # Load/Assemble voc and pairs
    corpus_name = "metetext"
    datafile = "./data/datafile"
    voc, pairs = data_preprocess.loadPrepareData(corpus_name, datafile)
    # Print some pairs to validate
    pairs = data_preprocess.trimRareWords(voc, pairs, 3)
    print("\npairs:")
    for pair in pairs[:10]:
        print(pair)
