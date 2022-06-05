# WSM 2022 project

## Data Crawling and Pre-processing (spider/)

Based on scrapy framework, we crawl more than 35000 news items from Global Times, Fox news, Huxiu from 2019 to May 2022. 
Global Times and Fox news are crawled from sitemap, while Huxiu is crawled according to its url law. 
The file mainly includes five parts {source, title, time, url, content}, and due to memory limitation, we only crawl the text content and not other media information. 
In the news query, some news with length 0 will be discarded.

## Search System (searching/engine/)

### Build data structures

Read in the `.json` data file generated in the previous step, and first process the document data appropriately:

First, tokenize the document data. Here, the sources of our article data are several news websites, and some articles may be missing due to the relatively early release time. In addition, the language of the article may not only be Chinese or English, and the title and content of the article need to be properly segmented according to this feature. English word segmentation is relatively simple. Here, we use some existing tools (`jieba`) to perform Chinese word segmentation. In the process of word segmentation, keep the "sticky" feature as much as possible, so as to maintain a certain overlap between word segmentations, so as to improve the post-sequence search engine. the recall rate. When the word segmentation result comes out, the word segmentation will be filtered and corrected, and some stop words and punctuation marks will be taken out to improve the accuracy of word segmentation.

Second, we build an inverted index of each segmented term. Let's first build a sequence number to id mapping for all terms in all articles `(term) -> termOd`, which uses `dict` in python. Second, we scan the term sequences of all articles and build an inverted index `(termId) -> (docId, type, pos)` in order, indicating where the term corresponding to the id exists in the article.
In addition, we have also established some auxiliary indexes that are convenient for other queries, such as auxiliary indexes established with time as the primary key, which are convenient for subsequent complex queries that use time as filter conditions.

### Boolean Search 

According to some experience of the existing system, when the syntax of the query is complex, we can design and simplify it with reference to the `Sql` syntax, and correspondingly there are `Lex` and `yacc` libraries for lexical analysis and syntax analysis. Here our query is just a simple combination of the `AND, OR, NOT` operators with precedence, which can simplify this step and generate results while parsing.

The algorithm passes in a query string and a range of the current search range. The processing logic is as follows:

1. If the input is empty, return an empty result.
2. If it is a single term, return all occurrences of the document according to the inverted index.
3. If the leftmost and rightmost terms are left and right parentheses, return the result in the parentheses.
4. Find the first AND operator `&&` outside the parentheses, and or operator `||`, and non-operator `!!` or union processing. The latter processes the right part and then complements the result on the corpus of documents.

The result returns the corresponding document `docId` collection.

### Specific search 

For point queries, if the `source` of the recalled article is a certain value, we can simply create a hash index, just go to the corresponding hash table (`dict`) to retrieve the corresponding `docId` list.

For interval queries, we need some sort of ordered index structure, such as `B+ tree`, `LSM tree`, etc. Since we are an offline news resource here, we only need to create an auxiliary index in chronological order when reading news data. 

When the user specifies the query time interval, we can use the dichotomy method to calculate the `O(logn)` Find the corresponding subscript range within the time limit, and then filter if the user needs it.

### Ranked Search 

Here we use the `TF-IDF` algorithm to rank the result set, which is the usual practice for most of the simple search engines today.

In the previous pre-processing process, the $$DF(i)=|\{j|term_i \in doc_j\}|$$ and $$IDF(i)=log\frac{|Docs|}{1+DF(i)}$$ values of all terms can be processed in advance. For all documents and terms, we can also find the corresponding TF value, that is, how many words this document contains: $$TF(i,j)=\frac{count(term_i,doc_j)}{\sum_k{count(term_k,doc_j)}}$$。

Let $TF\mathit{-} IDF(i,j)=DF(i)TF(i,j)$, and $TF\mathit{-}IDF(query,j)=\sum_{term_i \in query} DF(i)TF(i,j)$

The resulting articles are sorted according to the results of `TF-IDF`, and the top k are returned to the user.