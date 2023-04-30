This plugin classifies provided text. It requires a configuration object with the following properties: source.id,
language, model, title, and text. The source.id is an ID that points to a resource with an access token. The language is
the language of the text to classify. The model is the type of classification model to use. The title is an optional
title of the text, and the text is the text to classify. The resource configuration requires a token. The output of the
plugin is an object with an array of categories. Each category has a code, label, abs_relevance, and relevance. The code
is a unique identifier for the category. The label is a description of the category. The abs_relevance is a numerical
value that indicates the relevance of the category to the text. The relevance is a percentage value that indicates the
relevance of the category to the text. This plugin is useful for classifying text and determining the relevance of the
text to various categories.