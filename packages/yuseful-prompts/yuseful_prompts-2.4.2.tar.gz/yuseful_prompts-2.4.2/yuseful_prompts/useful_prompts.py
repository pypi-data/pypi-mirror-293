import json
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

DEFAULT_MODEL = "hermes3"


def check_headline_for_stocks_market_relevance(
    headline_text: str, model_name: str = DEFAULT_MODEL, include_reasoning_description: bool = False
):
    template = """You are an expert financial analyst and data scientist specializing in identifying news that could impact stock markets. 
You will be given a news headline: your task is to analyze it and to determine its potential relevance in analyzing stock market short, long, and mid-term trends.

To do your task, consider the following factors:

Consider potential direct impacts on:
- economic indicators
- industry sectors
- overall market sentiment
- specific companies or stocks

Evaluate possible indirect effects, such as:
- changes in consumer behavior
- geopolitical events affecting trade routes and supply chains or happening in regions with strategic natural resources
- long-term trends or societal changes
- ripple effects across industries

The psychological impact of the news on market participants is also an important factor to consider. 

Assess the likelihood and magnitude of any potential impact before making your decision
If the impact is sizable, the headline is relevant. If the impact is minor or unlikely, the headline is irrelevant.
Be mindful of not overestimating the relevance of the headline: only consider the most likely and significant impacts.

Here is the headline text you need to analyze, delimited by dashes:

--------------------------------------------------
{headline_text}
--------------------------------------------------"""
    if include_reasoning_description:
        template += """You will respond with a JSON having as key/value pairs:
- "relevance" as key, with either `true` or `false` (without the backticks) as value
- "reasoning" as key, with a string explaining your decision as value"""
    else:
        template += """You will respond with a JSON having only "relevance" as key and either `true` or `false` (without the backticks) as value."""
    relevance_prompt = PromptTemplate.from_template(template)
    chain = relevance_prompt | ChatOllama(model=model_name, format="json")
    return json.loads(chain.invoke({"headline_text": headline_text}).content)


def classify_headline_category(headline_text: str, model_name: str = DEFAULT_MODEL):
    template = """You are an assets management professional. Your job is to label a news headline with a category.

Here is the headline text you need to label, delimited by dashes:

--------------------------------------------------
{headline_text}
--------------------------------------------------

Here is the list, delimited by commas, of the authorized categories:

,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
analyst-ratings
buybacks
compliance-regulatory
corporate-governance
corporate-strategy
dividends
economic-indicators
earnings
executive-changes
global-events
industry-trends
innovations
lawsuits-settlements
mergers-acquisitions
policy-change
price-targets
product-launches
product-recalls
supply-chain
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

You are to output ONLY ONE DISTINCT CATEGORY, unchanged, from the list of authorized categories.
DON'T MAKE UP CATEGORIES THAT ARE NOT IN THE LIST!
DO NOT comment your output or add additional content, punctuation, quotes, characters, or any formatting."""
    category_prompt = PromptTemplate.from_template(template)
    chain = category_prompt | get_model(model_name)
    output = chain.invoke({"headline_text": headline_text})
    return output.content.strip().lower()


def classify_headline_sentiment(headline_text: str, model_name: str = DEFAULT_MODEL):
    template = """You are a stocks market professional. Your job is to label a headline with a sentiment IN ENGLISH.

Headlines that mention upside range from slightly bullish to very bullish.

Headlines that range from slightly bearish to volatile mention or imply one or more of the following:
- drop in stock prices
- economic slowdown
- factory glut
- increased shares selling pressure
- legal issues or lawsuits
- negative economic indicators
- sales decline
- uncertainty in the market

Legal issues, lawsuits, and any other legal proceedings are NEVER TO BE LABELED AS NEUTRAL and should be classified within the range of slightly bearish to uncertain depending on the severity implied by the headline.

Only label a headline as neutral if it is only informative and not uncertain, and does not allow to derive any negative or positive outlook on the market.

Only label a headline as "very" bearish or bullish if it indicates far-reaching consequences or a significant change in the market.

Uncertainty or mixed signals are never in the range of bullish headlines.

Only label a headline as "volatile" if it clearly indicates a high level of uncertainty and unpredictability in the market, due to the headline's content.

Here is the headline text you need to label, delimited by dashes:

--------------------------------------------------
{headline_text}
--------------------------------------------------

Here is the list of the possible sentiments, delimited by commas:

,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
very bullish
bullish
slightly bullish
neutral
slightly bearish
bearish
very bearish
uncertain
volatile
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

You are to output ONLY ONE DISTINCT SENTIMENT, unchanged, from the list of possible sentiments.
DON'T MAKE UP SENTIMENTS THAT ARE NOT IN THE LIST!
DO NOT add additional content, punctuation, explanation, characters, or any formatting in your output."""
    sentiment_prompt = PromptTemplate.from_template(template)
    chain = sentiment_prompt | get_model(model_name)
    output = chain.invoke({"headline_text": headline_text})
    return output.content.strip().lower()


def get_model(model_name: str = DEFAULT_MODEL):
    return ChatOllama(model=model_name)


def verifies_if_question_is_fully_answered(
    question: str, answer: str, model_name: str = DEFAULT_MODEL
):
    fully_answered_prompt = PromptTemplate(
        template="""You will determine if the provided question is fully answered by the provided answer.\n
Question:
{question}

Answer:
{answer}

You will respond with a JSON having "fully_answered" as key and exactly either "yes" or "no" as value.""",
        input_variables=["question", "answer"],
    )
    fully_answered_chain = fully_answered_prompt | ChatOllama(
        format="json", model=model_name
    )
    return json.loads(
        fully_answered_chain.invoke({"question": question, "answer": answer}).content
    )
