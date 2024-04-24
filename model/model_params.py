from dataclasses import dataclass


@dataclass
class ModelParams:
    n_layers: int = 8
    n_heads: int = 8
    dim: int = 256
    dim_ff_factor: int = 2
    max_seq_len: int = 200  # (in tokens)
    tokenizer_source_name: str = "custom"
    custom_tokenizer_ntokens: int = 20000
    layer_architecture: str = "torch-transformer"
    individual_head_params: bool = False
    pos_encoding: str = "learned"

# the base code only provides vanilla transformer models, this is how these
# parameters apply to them. You can reuse them also for other purposes - e.g.
# n_layers will also be useful if specifying an RNN.

# these parameters will not affect loading of a pretrained model, such
# as gpt2-small. However, the lm.py code refers to some of them in inference -
# for example, to max_seq_len while sampling - so these should be kept in order
# for pretrained models too.

# n_layers:
#   Number of layers in the transformer model.
# n_heads:
#   Number of heads per layer in the transformer model.
# dim:
#   Embedding width - input and model layer embedding dimension
# dim_ff_factor:
#   How much wider each transformer layer's feedforward hidden dimension is
#   than the input embedding dimension, e.g. with dim=256 and dim_ff_factor=2,
#   the feedforward layers will have hidden dimension 512.
# max_seq_len:
#   Maximum input length the transformer can take, in number of tokens.
# tokenizer_source_name:
#   Specifies how to prepare the tokenizer. in all cases, the optimizer is
#   adapted to some extent according to the dataset the model is created with.
#       "char":
#           Make a char-level tokenizer, using the characters in the
#           dataset.
#       "custom":
#           Make new BPE tokenizer based on the dataset, using the function
#           BpeTrainer from Huggingface. Can be slow if the dataset is large.
#           Tries to make custom_tokenizer_ntokens tokens, but may get
#           different amount.
#       "bert-base-uncased":
#           Will load the "bert-base-uncased" tokenizer from Huggingface, and
#           crop it to only the tokens which appear in the dataset (so the
#           token ids may be different)
#       "gpt2":
#           As with "bert-base-uncased", but with the gpt2 tokenizer.
# custom_tokenizer_ntokens:
#   Used when creating a custom tokenizer, as a guide for the desired tokenizer
#   vocabulary size. Does not force an exact size however.
# layer_architecture:
#   Implementation setting: how to build the transformer. Options:
#       "torch-transformer":
#           Use torch.nn.TransformerEncoderLayer for each layer of the
#           transformer. Enjoys pytorch optimised implementations and "fast
#           paths". Not customisable.
#       "custom-transformer":
#           Uses local, slightly cleaned, copy of
#           torch.nn.TransformerEncoderLayer for each layer of the transformer.
#           Optimisations gone in favour of keeping implementation in python -
#           hence customisable. The relevant files are in model/transformer/.
# individual_head_params:
#   Implementation setting: how to store the parameters of each head in each
#   transformer layer. Options:
#       False:
#           The parameters of all heads are stored together in one pair of big
#           weight and bias vectors. More efficient, less control. Default.
#       True:
#           The parameters of each head are stored separately. Slower (though
#           the implementation could be improved), but allows more control -
#           e.g. to freeze a specific head during training.
# pos_encoding:
#   How position is encoded for the transformer. Options:
#       "none":
#           No positional information is given (a transformer decoder can still
#           infer it however, thanks to the causal masking of the attention)
#       "learned":
#           An embedding (of size 'dim') of each input token position is added
#           to the token embeddings before they are passed to the transformer.
#           This embedding is learned alongside the other parameters of the
#           transformer.
#       "sin":
#           As with "learned", but here the embedding is predetermined.
#           Specifically, it is set to the sinusoidal positional encoding used
#           in the original transformer paper, "Attention is all you need".