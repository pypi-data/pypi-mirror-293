import pandas as pd
import math
from collections import Counter
from pprint import pprint

def entropy(probs):
    """Calculate the entropy of a list of probabilities."""
    return sum([-prob * math.log(prob, 2) for prob in probs])

def entropy_of_list(ls, value):
    """Calculate the entropy of a list with respect to a given value."""
    total_instances = len(ls)
    cnt = Counter(x for x in ls)
    probs = [x / total_instances for x in cnt.values()]
    return entropy(probs)

def information_gain(df, split_attribute, target_attribute, battr):
    """Calculate the information gain of a dataset split by a given attribute."""
    df_split = df.groupby(split_attribute)
    glist = [gname for gname, _ in df_split]
    glist.reverse()
    nobs = len(df.index) * 1.0
    df_agg1 = df_split.agg({target_attribute: lambda x: entropy_of_list(x, glist.pop())})
    df_agg2 = df_split.agg({target_attribute: lambda x: len(x) / nobs})
    df_agg1.columns = ['Entropy']
    df_agg2.columns = ['Proportion']
    new_entropy = sum(df_agg1['Entropy'] * df_agg2['Proportion'])
    old_entropy = entropy_of_list(df[target_attribute], battr)
    return old_entropy - new_entropy

def id3(df, target_attribute, attribute_names, default_class=None, default_attr='S'):
    """Implement the ID3 algorithm for building a decision tree."""
    cnt = Counter(x for x in df[target_attribute])
    if len(cnt) == 1:
        return next(iter(cnt))
    elif df.empty or (not attribute_names):
        return default_class
    else:
        default_class = max(cnt.keys())
        gainz = [information_gain(df, attr, target_attribute, default_attr) for attr in attribute_names]
        index_of_max = gainz.index(max(gainz))
        best_attr = attribute_names[index_of_max]
        tree = {best_attr: {}}
        remaining_attribute_names = [i for i in attribute_names if i != best_attr]
        for attr_val, data_subset in df.groupby(best_attr):
            subtree = id3(data_subset, target_attribute, remaining_attribute_names, default_class, best_attr)
            tree[best_attr][attr_val] = subtree
        return tree

def entropy_dataset(a_list):
    """Calculate the entropy of a dataset."""
    cnt = Counter(x for x in a_list)
    num_instances = len(a_list) * 1.0
    probs = [x / num_instances for x in cnt.values()]
    return entropy(probs)

def classify(instance, tree, default=None):
    """Classify a new instance using the decision tree."""
    attribute = next(iter(tree))
    if instance[attribute] in tree[attribute].keys():
        result = tree[attribute][instance[attribute]]
        if isinstance(result, dict):
            return classify(instance, result)
        else:
            return result
    else:
        return default
