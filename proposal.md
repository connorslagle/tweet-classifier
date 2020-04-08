# Capstone 1 Proposal
## Has COVID-19 been infected by politics?
A novel coronavirus (COVID-19) has thrown the world into panic. The pandemic has forced governments across the world to take drastic measures to mitigate the transmission of the disease. The United States has encouraged 'essential-only' travel measures which have effectively trapped people inside their homes, flocking to social media for news and solace.

I'm not sure if you've been on Twitter, but in my opinion it's the last place I would go for news OR solace. The small character limit brings the worst out of peolpe. However, this got me thinking:
- Would a global pandemic bring people on Twitter together? 
- Would the ever increasing political divide pause during the outbreak?

To answer these questions I collected tweets from politically distinct geographical areas that were tagged wtih a prominent conservative/liberal politician and/or the COVID19 hashtag: 

- Oregon (liberal), Colorado (mixed), and Arkansas (conservative).
- Donald Trump (@realdonaldtrump), Joe Biden (@joebiden)
- #COVID19

I will score the sentiment of these tweets and aggregate the data based on geographical location. Then I will compare the sentiment statistics of those who tagged each presidential candidate and those who tagged both a presidential candidate and COVID-19. 

## Preliminary EDA
Currently, I have ~1000 tweets for each combination of state and keyword (15 treatments). Each tweet is a json with 36 key/value pairs with several NaN values. The 'text' field includes many characters that have to be removed: punctuation, non-English characters, and commonly used words.

## Minimum Viable Product

The MVP scope for this project will be the following:

- Implement data pipeline to collect and clean tweets (Twitter API, mongoDB, pymongo, pandas)
- Clean text for bag-of-word sentiment analysis with ntlk (Tweet str > dict of {'Word': Count} > (positive words-negative words)/total)
- Compare sentiment between treatments (5) in ONE state (Are the means of sentiment statistically different (alpha=0.05)?)

MVP+

- Bayesian analysis on sentiment for one state (what is the probability Tweet came @COVID set vs @joebiden set given sentiment data?)
- Compare sentiment between states (15 treatments)

# notes: presenters for france tweets
 - Chris Moran, Andy, me, others I cannot remember!!
