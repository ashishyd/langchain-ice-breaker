from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI

from agents.linkedin_lookup import linkedin_lookup_agent
from agents.twitter_lookup import twitter_lookup_agent
from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrap_linkedin_profile
from third_parties.twitter import scrape_user_tweets


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrap_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template = """
           given the information about a person from LinkedIn {information}
           and twitter posts {twitter_posts} I want you to create:
           1. a short summary
           2. two interesting facts about them
           
           Use both information from Twitter and LinkedIn
           \n{format_instructions}
       """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = GoogleGenerativeAI(temperature=0, model="gemini-pro")
    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})
    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Initiates")
    ice_break_with(name="Eden Marco Udemy")
