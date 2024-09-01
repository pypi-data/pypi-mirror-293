import pandas as pd
import math
from pprint import pprint
from collections import Counter
import os

current_dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(current_dir, 'playgolf_data.csv'))

# Rest of your code...
print("\n Given Play Golf Dataset:\n\n", df)
t = df.keys()[-1]
print('Target Attribute is ➡ ', t)

# Get the attribute names from the input dataset
attribute_names = list(df.keys())

# Remove the target attribute from the attribute names list
attribute_names.remove(t)
print('Predicting Attributes ➡ ', attribute_names)

# Function to calculate entropy
def entropy(probs):
    return sum([-prob * math.log(prob, 2) for prob in probs])

# Function to calculate the entropy of the given dataset/list with respect to target attributes
def entropy_of_list(ls, value):
    total_instances = len(ls)  # Total instances associated with the respective attribute
    print("---------------------------------------------------------")
    print("\nTotal no of instances/records associated with '{0}' is ➡ {1}".format(value, total_instances))

    cnt = Counter(x for x in ls)  # Counter calculates the proportion of class
    print('\nTarget attribute class count (Yes/No) =', dict(cnt))

    # Probabilities for each class
    probs = [x / total_instances for x in cnt.values()]
    print("\nClasses➡", max(cnt), min(cnt))
    print("\nProbabilities of Class 'p'='{0}' ➡ {1}".format(max(cnt), max(probs)))
    print("Probabilities of Class 'n'='{0}' ➡ {1}".format(min(cnt), min(probs)))

    return entropy(probs)

# Function to calculate information gain
def information_gain(df, split_attribute, target_attribute, battr):
    print("\n\n----- Information Gain Calculation of", split_attribute, "----- ")

    df_split = df.groupby(split_attribute)
    glist = []

    for gname, group in df_split:
        print('Grouped Attribute Values \n', group)
        print("---------------------------------------------------------")
        glist.append(gname)

    glist.reverse()
    nobs = len(df.index) * 1.0

    df_agg1 = df_split.agg({target_attribute: lambda x: entropy_of_list(x, glist.pop())})
    df_agg2 = df_split.agg({target_attribute: lambda x: len(x) / nobs})

    df_agg1.columns = ['Entropy']
    df_agg2.columns = ['Proportion']

    new_entropy = sum(df_agg1['Entropy'] * df_agg2['Proportion'])

    if battr != 'S':
        old_entropy = entropy_of_list(df[target_attribute], 'S-' + df.iloc[0][df.columns.get_loc(battr)])
    else:
        old_entropy = entropy_of_list(df[target_attribute], battr)

    return old_entropy - new_entropy

# ID3 Algorithm to build decision tree
def id3(df, target_attribute, attribute_names, default_class=None, default_attr='S'):
    cnt = Counter(x for x in df[target_attribute])  # Class of YES/NO

    # First check: Is this split of the dataset homogeneous?
    if len(cnt) == 1:
        return next(iter(cnt))  # next input data set, or raises StopIteration when EOF is hit.

    # Second check: Is this split of the dataset empty? if yes, return a default value
    elif df.empty or (not attribute_names):
        return default_class  # Return None for Empty Data Set

    # Otherwise: This dataset is ready to be divided up!
    else:
        default_class = max(cnt.keys())  # Get Default Value for next recursive call
        gainz = []

        for attr in attribute_names:
            ig = information_gain(df, attr, target_attribute, default_attr)
            gainz.append(ig)
            print('\nInformation gain of', '“', attr, '”', 'is ➡', ig)

        print("========================================================= ")

        index_of_max = gainz.index(max(gainz))  # Index of Best Attribute
        best_attr = attribute_names[index_of_max]  # Choose Best Attribute to split on

        print("\nList of Gain for attributes:", attribute_names, "\nare:", gainz, "respectively.")
        print("\nAttribute with the maximum gain is ➡", best_attr)
        print("\nHence, the Root node will be ➡", best_attr)
        print("=========================================================")

        tree = {best_attr: {}}  # Create an empty tree, to be populated in a moment
        remaining_attribute_names = [i for i in attribute_names if i != best_attr]

        for attr_val, data_subset in df.groupby(best_attr):
            subtree = id3(data_subset, target_attribute, remaining_attribute_names, default_class, best_attr)
            tree[best_attr][attr_val] = subtree

        return tree

# Function to calculate entropy of the dataset
def entropy_dataset(a_list):
    cnt = Counter(x for x in a_list)
    num_instances = len(a_list) * 1.0  # Total number of instances

    print("\nNumber of Instances of the Current Sub-Class is {0}".format(num_instances))
    probs = [x / num_instances for x in cnt.values()]

    print("\nClasses➡", "'p'=", max(cnt), "'n'=", min(cnt))
    print("\nProbabilities of Class 'p'='{0}' ➡ {1}".format(max(cnt), max(probs)))
    print("Probabilities of Class 'n'='{0}' ➡ {1}".format(min(cnt), min(probs)))

    return entropy(probs)

# Initial entropy of the YES/NO attribute for our dataset
print("Entropy calculation for input dataset:\n")
print(df['PlayGolf'])
total_entropy = entropy_dataset(df['PlayGolf'])

print("\nTotal Entropy(S) of PlayGolf Dataset➡", total_entropy)
print("==============================================================")

# Build decision tree using ID3 algorithm
tree = id3(df, t, attribute_names)

print("\nThe Resultant Decision Tree is: ⤵\n")
pprint(tree)

attribute = next(iter(tree))
print("\nBest Attribute ➡", attribute)
print("Tree Keys ➡", tree[attribute].keys())
print("==============================================================")

# Function to classify new instances using the decision tree
def classify(instance, tree, default=None):
    attribute = next(iter(tree))  # Outlook/Humidity/Wind

    if instance[attribute] in tree[attribute].keys():  # Value of the attribute in set of Tree keys
        result = tree[attribute][instance[attribute]]
        if isinstance(result, dict):  # this is a tree, delve deeper
            return classify(instance, result)
        else:
            return result  # this is a label
    else:
        return default

# Classify new dataset
df_new = pd.read_csv(os.path.join(current_dir, 'playgolf_test.csv'))
df_new['Predicted'] = df_new.apply(classify, axis=1, args=(tree, '?'))
print(df_new)
