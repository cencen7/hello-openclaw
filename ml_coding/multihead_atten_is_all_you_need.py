import torch
import torch.nn as nn
import math


class InputEmbeddings(nn.Module):
    def __init__(self, d_model: int, vocab_size: int):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        # (vocab_size, d_model)
        self.embedding = nn.Embedding(vocab_size, d_model)

    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)
    

class PositionEmbeddings(nn.Module):
    def __init__(self, d_model: int, seq_len: int, dropout: float):
        super().__init__()
        self.d_model = d_model
        self.seq_len = seq_len
        self.dropout = nn.Dropout(dropout)

        # creat a matrix of shape (seq_len, d_model)
        pe = torch.zeros(seq_len, d_model)
        # create a vecor of shape (seq_len, 1)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        # apply sin to even position
        pe[:, 0::2] = torch.sin(position * div_term)
        # apply cos to odd postion
        pe[:, 1::2] = torch.cos(position * div_term)
        # transform to (1, seq_len, d_model)
        pe = pe.unsqueeze(0)
        # when save, will save this positon embedding
        self.register_buffer('pe', pe)

    def forward(self, x):
        # add position embedding, postion emebdding does not need to be updated
        x = x + (self.pe[:, :x.size(1), :]).require_grad_(False)
        return x


class LayerNormalization(nn.Module):
    def __init__(self, eps: float = 1e-6) -> None:
        super().__init__()
        self.eps = eps
        self.alpha = nn.Parameter(torch.ones(1))
        self.bias = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.alpha * (x - mean) / (std + self.eps) + self.bias


class FeedFordward(nn.Module):
    def __init__(self, d_model: int, d_ff: int, dropout: float):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff) # w1 and b1
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(d_ff, d_model) # w2 and b2
          
    def forward(self):
        # (batch_size, seq_len, dmodel) --> (batch_size, seq_len, d_ff) --> (batch_size, seq_len, d_model)
        return self.linear2(self.dropout(torch.relu(self.linear1(x))))


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, h: int, dropout: float):
        super().__init__()
        self.d_model = d_model
        self.h = h
        assert d_model % h == 0, "d_model must be divisible by n_heads"
        self.d_k = d_model // h
        self.dropout = nn.Dropout(dropout)

        # Wq, Wk, Wv, Wo
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model)


    @staticmethod
    def attention(query, key, value, mask, dropout: nn.Dropout):
        d_k = query.shape[-1]
        attention_scores = (query @ key.transpose(-2, -1)) / math.sqrt(d_k)
        if mask is not None:
            attention_scores.masked_fill_(mask == 0, -1e9)
        attention_scores = attention_scores.softmax(dim=-1)
        if dropout is not None:
            attention_scores = dropout(attention_scores)
        return (attention_scores @ value), attention_scores

    def forward(self, q, k, v, mask=None):
        query = self.w_q(q) # (batch_size, seq_len, d_model)
        key = self.w_k(k) # (batch_size, seq_len, d_model)
        value = self.w_v(v) # (batch_size, seq_len, d_model)
        # (batch_size, seq_len, d_model) --> (batch_size, seq_len, h, d_k) --> (batch_size, h, seq_len, d_k)
        query = query.view(query.shape(0), query.shape(1), self.h, self.d_k).transpose(1, 2)
        key = key.view(key.shape(0), key.shape(1), self.h, self.d_k).transpose(1, 2)
        value = value.view(value.shape(0), value.shape(1), self.h, self.d_k).transpose(1, 2)

        x, attention = self.attention(query, key, value, mask, self.dropout)

        # (batch_size, h, seq_len, d_k) --> (batch_size, seq_len, h, d_k) --> (batch_size, seq_len, d_model)
        x = x.transpose(1, 2).contiguous().view(x.shape[0], -1, self.h * self.d_k)
        return self.w_o(x)
    

class RisualConnection(nn.Module):
        def __init__(self, dropout: float):
            super().__init__()
            self.dropout = nn.Dropout(dropout)
            self.norm = LayerNormalization()

        def forward(self, x, sublayer):
            return self.norm(x + self.dropout(sublayer(x)))


class EncoderBlock(nn.Module):

    def __init__(self,
                 self_attention_block: MultiHeadAttention,
                 feed_forward_block: FeedFordward,
                 dropout: float):
                 
        super().__init__()
        self.self_attention_block = self_attention_block
        self.feed_forward_block = feed_forward_block
        self.residual_connectio = nn.ModuleList([RisualConnection(dropout) for _ in range(2)])

    def forward(self, x, src_mask):
        x = self.residual_connectio[0](x, lambda x: self.self_attention_block(x, x, x, src_mask))
        x = self.residual_connectio[1](x, self.feed_forward_block)
        return x
    

class Encoder(nn.Module):
    def __init__(self, layers: nn.ModuleList) -> None:
        super().__init__()
        self.layers = layers
        self.norm = LayerNormalization()

    def forward(self, x, src_mask):
        for layer in self.layers:
            x = layer(x, src_mask)
        return self.norm(x)
    

class DecoderBlock(nn.Module):
    def __init__(self,
                 self_attention_block: MultiHeadAttention,
                 cross_attention_block: MultiHeadAttention,
                 feed_forward_block: FeedFordward,
                 dropout: float):
                 
        super().__init__()
        self.self_attention_block = self_attention_block
        self.cross_attention_block = cross_attention_block
        self.feed_forward_block = feed_forward_block
        self.residual_connectio = nn.ModuleList([RisualConnection(dropout) for _ in range(3)])

    def forward(self, x, encode_output, src_mask, tgt_mask):
        x = self.residual_connectio[0](x, lambda x: self.self_attention_block(x, x, x, tgt_mask))
        x = self.residual_connectio[1](x, lambda x: self.cross_attention_block(x, encode_output, encode_output, src_mask))
        x = self.residual_connectio[2](x, self.feed_forward_block)
        return x
    

class Decoder(nn.Module):
    def __init__(self, layers: nn.ModuleList) -> None:
        super().__init__()
        self.layers = layers
        self.norm = LayerNormalization()

    def forward(self, x, encode_output, src_mask, tgt_mask):
        for layer in self.layers:
            x = layer(x, encode_output, src_mask, tgt_mask)
        return self.norm(x)
    

class ProjectionLayer(nn.Module):
    def __init__(self, d_model: int, vocab_size: int) -> None:
        super().__init__()
        self.proj = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        # (batch_size, seq_len, d_model) --> (batch_size, seq_len, vocab_size)
        return torch.log_softmax(self.proj(x), dim=-1)
    
class Transformer(nn.Module):
    def __init__(self,
                 encoder: Encoder,
                 decoder: Decoder,
                 src_embed: InputEmbeddings,
                 src_pos: PositionEmbeddings,
                 tgt_embed: InputEmbeddings,
                 tgt_pos: PositionEmbeddings,
                 proj_layer: ProjectionLayer) -> None:
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = src_embed
        self.src_pos = src_pos
        self.tgt_embed = tgt_embed
        self.tgt_pos = tgt_pos 
        self.proj_layer = proj_layer

    def encode(self, src, src_mask):
        src = self.src_embed(src)
        src = self.src_pos(src)
        return self.encoder(src, src_mask)
    
    def decode(self, encode_output, src_mask, tgt_mask):
        tgt = self.tgt_embed(tgt)
        tgt = self.src_pos(tgt)
        return self.decoder(tgt, encode_output, src_mask, tgt_mask)
    
    def project(self, x):
        return self.proj_layer(x)
    
def build_transformer(src_vocab_size: int,
                      tgt_vocab_size: int,
                      src_seq_len: int,
                      tgt_seq_len: int,
                      d_model: int = 512,
                      N: int = 6,
                      h: int = 8,
                      dropout: float = 0.1,
                      d_ff: int = 2048):
    # create embedding layers
    src_embed = InputEmbeddings(d_model, src_vocab_size)
    tgt_embed = InputEmbeddings(d_model, tgt_vocab_size)

    # create the positional encoding layer
    src_pos = PositionEmbeddings(d_model, src_seq_len, dropout)
    tgt_pos = PositionEmbeddings(d_model, tgt_seq_len, dropout)

    # create the encoder blocks
    encoder_blocks = []
    for _ in range(N):
        encoder_self_attention_block = MultiHeadAttention(d_model, h, dropout)
        feed_forward_block = FeedFordward(d_model, d_ff, dropout)
        encoder_block = EncoderBlock(encoder_self_attention_block, feed_forward_block, dropout)
        encoder_blocks.append(encoder_block)


    # create the decoder blocks
    decoder_blocks = []
    for _ in range(N):
        decoder_self_attention_block = MultiHeadAttention(d_model, h, dropout)
        decoder_cross_attention_block = MultiHeadAttention(d_model, h, dropout)
        feed_forward_block = FeedFordward(d_model, d_ff, dropout)
        decoder_block = DecoderBlock(decoder_self_attention_block,
                                    decoder_cross_attention_block,
                                    feed_forward_block,
                                    dropout)
        decoder_blocks.append(decoder_block)

    # create the encoder and decoder
    encoder = Encoder(nn.ModuleList(encoder_blocks))
    decoder = Decoder(nn.ModuleList(decoder_blocks))

    # create the projection layer
    proj_layer = ProjectionLayer(d_model, tgt_vocab_size)

    # create the transformer
    transformer = Transformer(encoder, decoder, src_embed, src_pos, tgt_embed, tgt_pos, proj_layer)

    # intialize the paramters
    for p in transformer.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform_(p)
    return transformer


if __name__ == "__main__":
    # hyperparameters
    src_vocab_size = 10000
    tgt_vocab_size = 10000
    src_seq_len = 50
    tgt_seq_len = 50
    d_model = 512
    N = 6
    h = 8
    dropout = 0.1
    d_ff = 2048

    transformer = build_transformer(src_vocab_size, tgt_vocab_size, src_seq_len, tgt_seq_len, d_model, N, h, dropout, d_ff)

    print(transformer)