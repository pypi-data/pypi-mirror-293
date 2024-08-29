import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sparse_dot_topn import awesome_cossim_topn


def group_queryset(queryset, fields=[]) -> dict:
    # Instaniate our lookup hash table
    group_lookup = {}

    # Write a function for cleaning strings and returning an array of ngrams
    def ngrams_analyzer(string):
        string = re.sub(r"[,-./]", r"", string)
        ngrams = zip(*[string[i:] for i in range(5)])  # N-Gram length is 5
        return ["".join(ngram) for ngram in ngrams]

    def find_group(row, col):
        # If either the row or the col string have already been given
        # a group, return that group. Otherwise return none
        if row in group_lookup:
            return group_lookup[row]
        elif col in group_lookup:
            return group_lookup[col]
        else:
            return None

    def add_vals_to_lookup(group, row, col):
        # Once we know the group name, set it as the value
        # for both strings in the group_lookup
        group_lookup[row] = group
        group_lookup[col] = group

    def add_pair_to_lookup(row, col):
        # in this function we'll add both the row and the col to the lookup
        group = find_group(row, col)  # first, see if one has already been added
        if group is not None:
            # if we already know the group, make sure both row and col are in lookup
            add_vals_to_lookup(group, row, col)
        else:
            # if we get here, we need to add a new group.
            # The name is arbitrary, so just make it the row
            add_vals_to_lookup(row, row, col)

    # Construct your vectorizer for building the TF-IDF matrix
    vectorizer = TfidfVectorizer(analyzer=ngrams_analyzer)

    if fields:
        allfields = fields + ["pk"]
        values = queryset.values_list(*allfields)
        df = pd.DataFrame(list(values), columns=allfields)

        df["grouper"] = df[fields.pop(0)].astype(str).str.cat(df[fields].astype(str))

        # Grab the column you'd like to group, filter out duplicate values
        # and make sure the values are Unicode
        vals = df["grouper"].unique().astype("U")

        # Build the matrix!!!
        tfidf_matrix = vectorizer.fit_transform(vals)

        cosine_matrix = awesome_cossim_topn(
            tfidf_matrix, tfidf_matrix.transpose(), vals.size, 0.8
        )

        # Build a coordinate matrix
        coo_matrix = cosine_matrix.tocoo()

        # for each row and column in coo_matrix
        # if they're not the same string add them to the group lookup
        for row, col in zip(coo_matrix.row, coo_matrix.col):
            if row != col:
                add_pair_to_lookup(vals[row], vals[col])

        df["Group"] = df["grouper"].map(group_lookup).fillna(df["grouper"])

        d = df.groupby("Group")["pk"].apply(list).to_dict()
        ret = {key: value for key, value in d.items() if len(value) > 1}
        return dict(sorted(ret.items(), key=lambda item: len(item[1]), reverse=True))
    return {}
