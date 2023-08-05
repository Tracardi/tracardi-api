This plugin checks similarity between two strings according to similarity algorithms. It takes payload as input and
returns the result of similarity check. The plugin supports seven different algorithms: Levenshtein, Normalized
Levenshtein, Weighted Levenshtein, Damerau-Levenshtein, Optimal String Alignment, Jaro-Winkler, and Longest Common
Subsequence.

Levenshtein is a metric string distance that calculates the minimum number of single-character edits (insertions,
deletions or substitutions) required to change one word into the other. Normalized Levenshtein is computed as
levenshtein distance divided by the length of the longest string, and the resulting value is always in the
interval [0.0 1.0]. Weighted Levenshtein allows to define different weights for different character substitutions, and
is usually used for optical character recognition (OCR) applications. Damerau-Levenshtein is similar to Levenshtein, but
allows for transposition of two adjacent characters. Optimal String Alignment is an extension of Damerau-Levenshtein
where no substring can be edited more than once. Jaro-Winkler is a string edit distance that was developed in the area
of record linkage (duplicate detection) and is best suited for short strings such as person names, and to detect
transposition typos. Longest Common Subsequence is used by the diff utility, by Git for reconciling multiple changes,
etc.

The computational cost to compute the similarity between two strings of length m and n respectively varies depending on
the algorithm used. Levenshtein, Damerau-Levenshtein, and Optimal String Alignment have a cost of O(m*n), while
Jaro-Winkler and Longest Common Subsequence have a cost of O(m*n).