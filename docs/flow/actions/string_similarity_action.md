# String similarity

This plugin checks similarity between two strings according to similarity algorithms.

# Configuration

Example:

```json
{
   "first_string": "event@properties.some_value1",
   "second_string": "event@properties.some_value2",
   "algorithm": "Levenshtein"
}
```

# Input

This plugin takes payload as input

# Output

Returns the result of similarity check.

Example:

```json
{
  "similarity": "1"
}
```

## String similarity algorithms <sup>from strsimpy documentation</sup>

The main characteristics of each implemented algorithm are presented below. The "cost" column gives an estimation of the computational cost to compute the similarity between two strings of length m and n respectively.

|  									|  						| Normalized? 	| Metric?	| Type    | Cost | Typical usage |
| --------					|-------			|-------------	|-------- | ------  | ---- | ---   |
| [Levenshtein](#levenshtein)		|distance 				| No 			| Yes 		|         | O(m*n) <sup>1</sup> |  |
| [Normalized Levenshtein](#normalized-levenshtein)	|distance<br>similarity	| Yes 			| No 		| 	      | O(m*n)  |  |
| [Weighted Levenshtein](#weighted-levenshtein)		|distance 				| No 			| No 		| 	      | O(m*n)  | OCR |
| [Damerau-Levenshtein](#damerau-levenshtein)  	|distance 				| No 			| Yes 		| 	      | O(m*n) <sup>1</sup> |  |
| [Optimal String Alignment](#optimal-string-alignment)  |distance | No 			| No 		| 	      | O(m*n) <sup>1</sup> |  |
| [Jaro-Winkler](#jaro-winkler) 		|similarity<br>distance	| Yes  			| No 		| 	      | O(m*n) | typo correction |
| [Longest Common Subsequence](#longest-common-subsequence) 		|distance 				| No 			| No 		| 	      | O(m*n)| diff utility, GIT reconciliation |

## Levenshtein
The Levenshtein distance between two words is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other.
It is a metric string distance. 

## Normalized Levenshtein
This distance is computed as levenshtein distance divided by the length of the longest string. The resulting value is always in the interval [0.0 1.0] but it is not a metric anymore!

The similarity is computed as 1 - normalized distance.


## Weighted Levenshtein
An implementation of Levenshtein that allows to define different weights for different character substitutions.

This algorithm is usually used for optical character recognition (OCR) applications. For OCR, the cost of substituting P and R is lower then the cost of substituting P and M for example because because from and OCR point of view P is similar to R.

It can also be used for keyboard typing auto-correction. Here the cost of substituting E and R is lower for example because these are located next to each other on an AZERTY or QWERTY keyboard. Hence the probability that the user mistyped the characters is higher.


## Damerau-Levenshtein
Similar to Levenshtein, Damerau-Levenshtein distance with transposition (also sometimes calls unrestricted Damerau-Levenshtein distance) is the minimum number of operations needed to transform one string into the other, where an operation is defined as an insertion, deletion, or substitution of a single character, or a **transposition of two adjacent characters**.

It does respect triangle inequality, and is thus a metric distance.

This is not to be confused with the optimal string alignment distance, which is an extension where no substring can be edited more than once.


## Optimal String Alignment
The Optimal String Alignment variant of Damerau–Levenshtein (sometimes called the restricted edit distance) computes the number of edit operations needed to make the strings equal under the condition that **no substring is edited more than once**, whereas the true Damerau–Levenshtein presents no such restriction.
The difference from the algorithm for Levenshtein distance is the addition of one recurrence for the transposition operations.

Note that for the optimal string alignment distance, the triangle inequality does not hold and so it is not a true metric.

## Jaro-Winkler
Jaro-Winkler is a string edit distance that was developed in the area of record linkage (duplicate detection) (Winkler, 1990). The Jaro–Winkler distance metric is designed and best suited for short strings such as person names, and to detect transposition typos.

Jaro-Winkler computes the similarity between 2 strings, and the returned value lies in the interval [0.0, 1.0].
It is (roughly) a variation of Damerau-Levenshtein, where the transposition of 2 close characters is considered less important than the transposition of 2 characters that are far from each other. Jaro-Winkler penalizes additions or substitutions that cannot be expressed as transpositions.

The distance is computed as 1 - Jaro-Winkler similarity.

## Longest Common Subsequence

The longest common subsequence (LCS) problem consists in finding the longest subsequence common to two (or more) sequences. It differs from problems of finding common substrings: unlike substrings, subsequences are not required to occupy consecutive positions within the original sequences.

It is used by the diff utility, by Git for reconciling multiple changes, etc.

The LCS distance between strings X (of length n) and Y (of length m) is n + m - 2 |LCS(X, Y)|
min = 0
max = n + m

LCS distance is equivalent to Levenshtein distance when only insertion and deletion is allowed (no substitution), or when the cost of the substitution is the double of the cost of an insertion or deletion.

This class implements the dynamic programming approach, which has a space requirement O(m.n), and computation cost O(m.n).

In "Length of Maximal Common Subsequences", K.S. Larsen proposed an algorithm that computes the length of LCS in time O(log(m).log(n)). But the algorithm has a memory requirement O(m.n²) and was thus not implemented here.
