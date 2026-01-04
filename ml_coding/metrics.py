import numpy as np
from itertools import combinations

"""
Ranking Metrics
"""
# precision @ K
def precision_at_k(ranked_list, relevant_itemts, K):
    top_k = ranked_list[:K]
    return len(set(top_k) & set(relevant_itemts)) / K

# recall @ K
def recall_at_k(ranked_list, relevant_items, K):
    top_k = ranked_list[:K]
    return len(set(top_k) & set(relevant_items)) / len(relevant_items)

# averege precison (AP)
def average_precison(ranked_list, relevant_items):
    ap_sum = 0
    num_relevant = 0
    # precision @ 1, precision @ 2, precision @ 3, ....
    for i, item in enumerate(ranked_list, start=1):
        if item in relevant_items:
            num_relevant += 1
            ap_sum += num_relevant / i
    return ap_sum / len(relevant_items)


# mean average precison (MAP)
def mean_average_precison(all_ranked_lists, all_relevant_items):
    return np.mean([average_precison(ranked, relevant) for ranked, relevant in zip(
        all_ranked_lists, all_relevant_items
    )])

# DCG @ K --> discouted as (2**rel - 1) / np.logs(i+1)
def dcg_at_k(ranked_list, relevant_items, K):
    dcg = 0
    for i, item in enumerate(ranked_list[:K], start=1):
        rel = 1 if item in relevant_items else 0
        dcg += (2*rel - 1) / np.log2(i + 1)

# NDCG @ K
def ndcg_at_k(ranked_list, relevant_items, K):
    dcg = dcg_at_k(ranked_list, relevant_items)
    ideal_ranking = sorted(relevant_items, key=lambda x: 1, reverse=True)
    idcg = dcg_at_k(ideal_ranking, relevant_items)
    return dcg / idcg if idcg > 0 else 0

# Mean reciprocal Rank (MRR) --> discounted as 1/ position
def mean_reciprocal_rank(all_ranked_lists, all_relevant_items):
    rr_sum = 0
    for ranked, relevant in zip(all_ranked_lists, all_relevant_items):
        for i, item in enumerate(ranked, start=1):
            if item in relevant:
                rr_sum += 1 / i
                break
    return rr_sum / len(all_ranked_lists)


"""
Diversity Metrics
"""

# Intra-list Diversity (ILD): diversity_sum / len(pairs)
def ild(ranked_list, item_similarity):
    # item_similarity: dict of tuple(item1, item2) -> similarity in [0,1]
    pairs = list(combinations(ranked_list, 2))
    if not pairs:
        return 0
    diversity_sum = 0
    for i, j in pairs:
        sim = item_similarity.get((i, j), item_similarity.get((j, i), 0))
        diversity_sum += 1 - sim
    
    ild_value = diversity_sum / len(pairs)
    return ild_value

# coverage 
def coverage(all_recommeneded_items, total_items):
    unique_items = set(item for rec_list in all_recommeneded_items for item in rec_list)
    return len(unique_items) / total_items

#novelty / serendipity
def novelty(ranked_list, item_populairty):
    # item_popularity: dict of item -> probability user knows it
    return -np.mean([np.log2(item_populairty.get(item, 1e-6) for item in ranked_list)])


"""
Bias Adjustment
"""
# inverse propensity scoring (IPS)
def compute_ips_weights(postions, max_weight=10.0, eps=1e-12):
    """
    Compute IPS weights based on ranking position.

    Args:
        positions (array-like): rank position (1 = top)
        max_weight (float): clip large weights to reduce variance
        eps (float): small value to avoid division by zero

    Returns:
        np.ndarray: IPS weights
    """
    postions = np.asarray(postions, dtype=np.float32)
    # simple explosue propensity: p(exposed) = 1 / position
    propensity = 1.0 / np.maximum(postions, 1.0)
    
    # ips weight = 1 / propensity
    weights = 1.0 / np.maximum(propensity, eps)

    # clip to prevent extreme values
    weights = np.minimum(weights, max_weight)

    return weights


def weighted_log_loss(logits, labels, weights=None, eps=1e-12):
    """
    Binary cross-entropy loss with optional IPS weights.
    """
    logits = np.asarray(logits)
    labels = np.asarray(labels)

    probs = 1.0 / (1.0 + np.exp(-logits))
    probs = np.clip(probs, eps, 1.0-eps)

    loss = -(labels * np.log(probs)) + (1 -labels) * np.log(1-probs)
    
    if weights is None:
        return loss.mean()
    
    return (weights * loss).sum() / (weights.sum() + eps)

positions = [1, 1, 2, 5, 10]
labels    = [1, 0, 1, 0, 1]
logits    = [2.0, -0.5, 1.2, -0.3, 0.7]

weights = compute_ips_weights(positions)

loss_plain = weighted_log_loss(logits, labels)
loss_ips   = weighted_log_loss(logits, labels, weights)

print("Plain loss:", loss_plain)
print("IPS loss:", loss_ips)

