# Sensitivity Analysis of VADER Sentiment Analyzer

VADER (Valence Aware Dictionary and sEntiment Reader) is a rule-based sentiment analysis tool that is commonly used for social-media sentiment analysis.


Outliine:

1. Intro
2. Explaining the dataset and accumulation method
3. Explain stack (AWS -> Spark -> Pandas)
4. Initial look at data: Example tweets
5. initial word cloud/bar chart of word frequency
6. Explain data cleaning methods (treatments: emoji/non-emoji, stop-words/no stop-words)
7. VADER sentiment example: positive, neutral, negative
8. MVP: for CO: Distribution of sentiments for each search term and each treatment combo
    
    - 2 graphs (emoji/non-emoji), (stopwords/no): dist of means using bootstraps

9. MVP+: do 8 for OR/AR
10. Conclusion
11. references

<p align="center">
    <img src="images/co_0_top25words.png" width='400' />
    <img src="images/co_0_top25words_nostops.png" width = '400' />
</p>
<p align="center">
    <img src="images/co_1_top25words.png" width='400' />
    <img src="images/co_1_top25words_nostops.png" width = '400' />
</p>
<p align="center">
    <img src="images/co_2_top25words.png" width='400' />
    <img src="images/co_2_top25words_nostops.png" width = '400' />
</p>
<p align="center">
    <img src="images/co_3_top25words.png" width='400' />
    <img src="images/co_3_top25words_nostops.png" width = '400' />
</p>
<p align="center">
    <img src="images/co_4_top25words.png" width='400' />
    <img src="images/co_4_top25words_nostops.png" width = '400' />
</p>