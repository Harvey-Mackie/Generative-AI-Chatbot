
import tensorflow as tf
import tensorlayer as tl
import numpy as np
from tensorlayer.cost import cross_entropy_seq, cross_entropy_seq_with_mask
from tqdm import tqdm
from sklearn.utils import shuffle
from data.twitter import data
from tensorlayer.models.seq2seq import Seq2seq
from tensorlayer.models.seq2seq_with_attention import Seq2seqLuongAttention
import os
from config import packageDir

#Source - https://github.com/tensorlayer/seq2seq-chatbot

#The Chatbot consists of a model ready for testing and an operation to enable further testing.
class Chatbot:
    
    #Extracting the core data points from the dataset and seperating each element in a seperate variable - Data PreProcessing
    def initial_setup(data_corpus):
        metadata, idx_q, idx_a = data.load_data(PATH=''+packageDir+'/data/{}/'.format(data_corpus))
        (trainX, trainY), (testX, testY), (validX, validY) = data.split_dataset(idx_q, idx_a)
        trainX = tl.prepro.remove_pad_sequences(trainX.tolist())
        trainY = tl.prepro.remove_pad_sequences(trainY.tolist())
        testX = tl.prepro.remove_pad_sequences(testX.tolist())
        testY = tl.prepro.remove_pad_sequences(testY.tolist())
        validX = tl.prepro.remove_pad_sequences(validX.tolist())
        validY = tl.prepro.remove_pad_sequences(validY.tolist())
        return metadata, trainX, trainY, testX, testY, validX, validY
    
    data_corpus = "twitter"
    metadata, trainX, trainY, testX, testY, validX, validY = initial_setup(data_corpus)

    # Model Parameters 
    src_len = len(trainX)
    tgt_len = len(trainY)
    batch_size = 32
    n_step = src_len // batch_size
    src_vocab_size = len(metadata['idx2w']) # 8002 (0~8001)
    emb_dim = 1024
    word2idx = metadata['w2idx']   # dict  word 2 index
    idx2word = metadata['idx2w']   # list index 2 word
    unk_id = word2idx['unk']   # 1
    pad_id = word2idx['_']     # 0
    start_id = src_vocab_size  # 8002
    end_id = src_vocab_size + 1  # 8003
    word2idx.update({'start_id': start_id})
    word2idx.update({'end_id': end_id})
    idx2word = idx2word + ['start_id', 'end_id']
    src_vocab_size = tgt_vocab_size = src_vocab_size + 2
    num_epochs = 25 # Number of epochs
    vocabulary_size = src_vocab_size 

    # Sequence to sequence model
    decoder_seq_length = 20
    model_ = Seq2seq(
        decoder_seq_length = decoder_seq_length,
        cell_enc=tf.keras.layers.GRUCell,
        cell_dec=tf.keras.layers.GRUCell,
        n_layer=3,
        n_units=256,
        embedding_layer=tl.layers.Embedding(vocabulary_size=vocabulary_size, embedding_size=emb_dim),
        )
    
    load_weights = tl.files.load_npz(name=''+packageDir+'/model/model-15-epochs-twitter.npz')
    tl.files.assign_weights(load_weights, model_)
    
    # Decode a responce from the trained model - Returns a list of strings, each word in the responce is a list element
    def inference(self, seed, top_n):
        self.model_.eval()
        seed_id = [self.word2idx.get(w, self.unk_id) for w in seed.split(" ")]
        sentence_id = self.model_(inputs=[[seed_id]], seq_length=20, start_token=self.start_id, top_n = top_n)
        sentence = []
        for w_id in sentence_id[0]:
            w = self.idx2word[w_id]
            if w == 'end_id':
                break
            sentence = sentence + [w]
        return sentence
    
    # Generate a responce by calling the inference script and passing in the users message
    # Generate 3 Messages from the model
    # Convert the responce into a String.
    def test(self,userMessage, top_n):
        print("Query >", userMessage)
        for i in range(top_n):
            sentence = self.inference(userMessage, top_n)
            print(" >", ' '.join(sentence))
        print(self.listToString(sentence))
        return self.listToString(sentence)

    # Train the model on the dataset  (cornell corpuss) using the varibales defined in the intial set-up
    # Each epoch's progress can be viewed visually by testing the model against 'x' seeds every iteration.
    # The model is saved to a .npz file type once trained.
    def train(self):
        optimizer = tf.optimizers.Adam(learning_rate=0.001)
        self.model_.train()

        seeds = ["happy birthday have a nice day","donald trump won last nights presidential debate according to snap online polls"]
        for epoch in range(self.num_epochs):
            self.model_.train()
            self.trainX, self.trainY = shuffle(self.trainX, self.trainY, random_state=0)
            total_loss, n_iter = 0, 0
            for X, Y in tqdm(tl.iterate.minibatches(inputs=self.trainX, targets=self.trainY, batch_size=self.batch_size, shuffle=False), 
                            total=self.n_step, desc='Epoch[{}/{}]'.format(epoch + 1, self.num_epochs), leave=False):

                X = tl.prepro.pad_sequences(X)
                _target_seqs = tl.prepro.sequences_add_end_id(Y, end_id=self.end_id)
                _target_seqs = tl.prepro.pad_sequences(_target_seqs, maxlen=self.decoder_seq_length)
                _decode_seqs = tl.prepro.sequences_add_start_id(Y, start_id=self.start_id, remove_last=False)
                _decode_seqs = tl.prepro.pad_sequences(_decode_seqs, maxlen=self.decoder_seq_length)
                _target_mask = tl.prepro.sequences_get_mask(_target_seqs)

                with tf.GradientTape() as tape:
                    ## compute outputs
                    output = self.model_(inputs = [X, _decode_seqs])
                    
                    output = tf.reshape(output, [-1, self.vocabulary_size])
                    ## compute loss and update model
                    loss = cross_entropy_seq_with_mask(logits=output, target_seqs=_target_seqs, input_mask=_target_mask)

                    grad = tape.gradient(loss, self.model_.all_weights)
                    optimizer.apply_gradients(zip(grad, self.model_.all_weights))
                
                total_loss += loss
                n_iter += 1

            # printing average loss after every epoch
            print('Epoch [{}/{}]: loss {:.4f}'.format(epoch + 1, self.num_epochs, total_loss / n_iter))

            # Test model at the end of each epoch  
            for seed in seeds:
                print("Query >", seed)
                top_n = 3
                for i in range(top_n):
                    sentence = self.inference(seed, top_n)
                    print(" >", ' '.join(sentence))

            tl.files.save_npz(self.model_.all_weights, name=''+packageDir+'/model/model-new.npz')
    
    # Convert a list of string/characters to a singular string variable
    def listToString(self, messageList):  
        # initialize an empty string 
        string = " " 
        # return string   
        return (string.join(messageList))
