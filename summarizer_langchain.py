# from langchain_openai import ChatOpenAI  # (swapped out in favor of Groq below)
from langchain_groq import ChatGroq  # Groq's chat model wrapper for LangChain
from langchain_core.prompts import ChatPromptTemplate  # for building reusable prompt templates
from langchain_core.output_parsers import StrOutputParser  # converts model output into a plain string
from dotenv import load_dotenv  # loads environment variables from a .env file
from scraper import get_website_text  # custom function that fetches/extracts text from a website

# Load environment variables (e.g. GROQ_API_KEY) from .env into the environment
load_dotenv()

# Define the prompt template — {website} will be replaced with the actual scraped text
prompt = ChatPromptTemplate.from_template(
    "Give a short friendly summary of this website:\n\n{website}")

# Initialize the Groq-hosted LLM
# - model: which model Groq should serve (Llama 3.3 70B here)
# - temperature: lower = more focused/deterministic, higher = more creative
model = ChatGroq(model='llama-3.3-70b-versatile', temperature=0.3)

# Parses the raw model response into a plain string (instead of a structured message object)
parser = StrOutputParser()

# Build the chain: prompt -> model -> parser
# Each step's output feeds into the next step's input
chain = prompt | model | parser

def summarizer(url):
    # Scrape the website's text content, then run it through the chain to get a summary
    return chain.invoke({"website": get_website_text(url)})

# Run the summarizer on a sample URL and print the result
print(summarizer("https://anthropic.com"))