"""
KenLM is a highly efficient language model library that is primarily used to build n‑gram models. 
Its key features include:

Efficient Data Structures:
KenLM uses optimized data structures (like tries or arrays) to store n‑gram counts compactly. 
This enables fast querying and low memory overhead.

Probability Estimation:
It computes the probability of a sentence by breaking it into n‑grams. To handle data sparsity, 
it employs smoothing techniques—most notably, various forms of Kneser–Ney smoothing.

Kneser–Ney Smoothing:
In Kneser–Ney smoothing, the probability of a word given its history is computed by discounting the observed counts 
and redistributing the discounted probability mass to lower-order models (i.e., using a “backoff” strategy). 
The core idea is to use not only raw counts but also the diversity of contexts in which words appear.

Log Probabilities:
To avoid numerical underflow when multiplying many probabilities, probabilities are usually stored and computed 
in the logarithmic domain.


"""

from collections import defaultdict

def tokenize(text):
    return text.strip().split()

def count_ngrams(corpus, n):
    ngram_counts = defaultdict(int)
    context_counts = defaultdict(int)
    
    for sentence in corpus:
        tokens = ['<s>'] * (n-1) + tokenize(sentence) + ['</s>']
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            context = tuple(tokens[i:i+n-1])
            ngram_counts[ngram] += 1
            context_counts[context] += 1
    return ngram_counts, context_counts

# Example usage:
corpus = [
    "this is a sample sentence",
    "this is another example sentence"
]
ngram_counts, context_counts = count_ngrams(corpus, 3)
print(f"ngram_counts: {ngram_counts}; context_counts: {context_counts}")

class BigramLM:
    def __init__(self, discount=0.75):
        self.unigram_counts = defaultdict(int)
        self.bigram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)  # count for each history (first word)
        self.discount = discount
        self.total_contexts = 0
        self.continuation_counts = defaultdict(int)  # for P_continuation

    def train(self, corpus):
        for sentence in corpus:
            tokens = ['<s>'] + tokenize(sentence) + ['</s>']
            for i in range(len(tokens)):
                self.unigram_counts[tokens[i]] += 1
            for i in range(len(tokens) - 1):
                bigram = (tokens[i], tokens[i+1])
                self.bigram_counts[bigram] += 1
                self.context_counts[tokens[i]] += 1
                # For continuation: count how many unique histories lead to token
                self.continuation_counts[tokens[i+1]] += 1
        self.total_contexts = len(self.context_counts)
    
    def continuation_prob(self, word):
        # P_continuation(w) = (# of unique histories where w occurs) / (total unique bigrams)
        # Here we approximate total unique bigrams by the sum of unique continuations.
        return self.continuation_counts[word] / self.total_contexts

    def bigram_prob(self, history, word):
        bigram = (history, word)
        count_bigram = self.bigram_counts[bigram]
        count_history = self.context_counts[history]
        if count_history == 0:
            return self.continuation_prob(word)
        
        # Calculate the discounted probability part:
        prob = max(count_bigram - self.discount, 0) / count_history
        # Calculate backoff weight lambda(history):
        # lambda = (discount * (# of words that follow history)) / count_history
        num_continuations = sum(1 for (h, w) in self.bigram_counts if h == history)
        lambda_weight = (self.discount * num_continuations) / count_history
        
        prob += lambda_weight * self.continuation_prob(word)
        return prob

# Example usage:
lm = BigramLM(discount=0.75)
lm.train(corpus)
print("Probability of 'is' given 'this':", lm.bigram_prob("this", "a"))
print("context_counts:", lm.context_counts)
print("unigram_counts", lm.unigram_counts)
print("bigram_counts:", lm.bigram_counts)