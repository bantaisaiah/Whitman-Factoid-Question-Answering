# Whitman-Factoid-Question-Answering


CS-357-A: Natural Language Processing

Professor Andy Exley

Isaiah Banta

December 21st

**Final Project**

**The Problem**

I decided to pursue the problem of Factoid Question Answering (as shown in the book section 23.2 on page 778). I recognize the difficulty with testing/training and measuring of both of those. In fact, a training/test set approach isn&#39;t as applicable with a Factoid Question Answering problem. However, I think I will be able to accurately show that I worked toward the problem, how I chose to build my corpora, and the ways that I can improve my implementation in the future.

**Method**

The problem itself follows the following steps (also laid out in the book):

1. **Question Processing**

Here we need to do two main things: find a suitable **query** to query to serve to our IR (information retrieval) system and an **answer type** , or what would be deemed as an appropriate answer. As an example:

        What department does Andy Exley teach in?

Here we would hope to get the following:

Query: [&#39;department&#39;, &#39;andy&#39;, &#39;exley&#39;, &#39;teach&#39;]
Answer Type: Location or Department

1. **Passage Retrieval**

In order to make our corpus, I made a collection of .txt files made up of the course catalog, Whitman&#39;s website, and Whitman&#39;s Wikipedia page. Then I followed the following steps:

  1. Gather/create a collection of .txt files from Whitman&#39;s website, the course catalog, and their Wikipedia page.
  2. Strip all non alphabetic, numeric, punctuation characters.
  3. Read all of these files sentence by sentence, classifying each sentence as we go and inserting it into a python dictionary that will act as our database which is categorized by answer types. (a sentence may be classified under multiple answer types)

Then passage retrieval becomes much easier, now our &#39;passages&#39; are split into individual sentences and under labels. Now that we have set up our database we can do retrieval. For retrieval we follow what the book says:

1. Rank the top _n_ sentences that score highest on the following criteria:
  1. Number of question keywords in the passage
  2. The proximity of the keywords from the original query to each other
2. Take the top sentence and pass it to our answer\_processor() function.


**Answer Processing**

Once passage retrieval and ranking happens, answer processing is actually quite simple. We just print out the word that has the corresponding tag of our answer type.

If no answer is found and our rankings list is empty, then our function will print out &quot;No answer found&quot;.



**Corpora**

I determined which type of questions I wanted my FQA to answer first (aka, person, place, time). I then picked representative sentences from the database (the course catalog and the website) that I knew could be parsed to give that data.

Because of this, my corpus is very small. But it was important to me to develop a way of turning a plain sentence into usable data for Information Retrieval, as that is a key part of being able to further extend this program.

Corpora from libraries:

- --Nltk stop words
- --SpaCy en\_core\_web\_sm



**Training, Development, and Testing Sets**

Because of the nature of this assignment, I did not have any sets that I developed.

**Roadblocks and Analysis**
_Big-Picture Project_

- When to stop reading new libraries, research, and new terms and definitions and just start coding was difficult. Partly because the stuff I was reading was really interesting and also because I gave myself a somewhat ambiguous project and it felt much easier to read about it rather than start doing it.
- The textbook isn&#39;t much of a help on this either. It is much more high-level and vague than many of the other sections which have pseudo code and examples.
- Determining the scope and what I would deem a success was very difficult
- Getting discouraged by [people doing something similar in a](https://towardsdatascience.com/building-a-question-answering-system-part-1-9388aadff507)[_way_](https://towardsdatascience.com/building-a-question-answering-system-part-1-9388aadff507)[cooler way than I am](https://towardsdatascience.com/building-a-question-answering-system-part-1-9388aadff507).

I generally got through these roadblocks by setting small goals for myself by splitting my project into smaller functions:

- --find\_key\_words()
- --question\_classification()
- --Etc…

Another mentality I found useful was to only focus on the variable types that my function needed as input and in what format it should output.

_Libraries and Code base_

- It was an added difficulty to learn the Stanford Core NLP library at first and to know when to use that versus NLTK. But it is so much faster and its Pipeline method is incredible (even if it does print out every time in an annoying way).

_Difficulty of the Problem_

This problem was a lot harder than I anticipated, especially when it comes to ranking sentences inside my corpus and wanting the correct sentence to win out, but seeing it fail to on a consistent basis. Whitman has had a lot of presidents.. And I&#39;m also using a corpus that is heavily populated by Wikipedia information, which means Kathy Murray may not be mentioned much there.

This was also difficult because it was entirely new territory for me. So most of my time was spent reading up on strategy and new concepts that I hadn&#39;t learned before like: Lemmatization, Entity Recognition, Question Classification, and Information Retrieval.

I also worked with new libraries like Scapy and the Stanford NLP libraries.

**Success Rate of Solution**
Success rate is very low as mentioned for many reasons. I suspect that web scraping the Whitman website and adding that to the database would do wonders for the accuracy of the answers. In addition, implementing N-gram overlap for passage ranking would probably do very well with a larger corpus, whereas with a small corpus, it might end up hurting the correct answer rate.

**Further Improvements**

_For query formulation_

- --Process for adding morphological variants of the content words in the question
- --Applying thesaurus-based expansion algorithms

_For question classification_

- --Supervised machine learning to determine answer types
- --Hypernyms and hyponyms to build better answer type taxonomies that are specific to Whitman
- --Would try and implement the code found [in this paper](https://www.aclweb.org/anthology/C16-1116/) which I skimmed.

_For passage retrieval_

- --This is where I would have benefited from having a larger corpus so that I could experiment more with different or multiple query strings and techniques.

_For answer processing_

- --I would want to build a pattern-learning algorithm that is built from a predefined set of answers and word relationships as discussed in the book on page 785 steps 1 - 5. Then use the winning high precision values to assign to various answer types in my dictionary, so that a given answer type knows the winning question-answer pattern (or even store it as a regex somehow)

_For evaluation of factoid answers_

- --. this would require me to apply my program to many other similar schools (perhaps the panel of 13) and then self label them for accuracy and build a small training set to run the MRR (page 787)



**Acknowledgements**

- [This great article](https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da) by Susan Li for helping with how to use nltk and SpaCy to do named entity recognition.
- Alvira Swalin for giving me inspiration [with her project](https://towardsdatascience.com/building-a-question-answering-system-part-1-9388aadff507) to build upon this project in the future.
- /timotito for an [elegant implementation of assigning answer types](https://github.com/timotito/NLP-Question-Answer-System) to questions which I was successfully doing but in a much more sloppy way.
