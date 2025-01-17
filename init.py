import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from browser_use.controller.service import Controller
from pydantic import BaseModel

# Initialize the controller
controller = Controller()

class ArticleSummary(BaseModel):
	title: str
	result: str

@controller.action('Save Article', param_model=ArticleSummary)
async def save_article(params: ArticleSummary):
	with open('articleSummary.md', 'a') as f:
		f.write(f'{params.title}\n --- \n {params.result}')

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key='<Gemini API Key Here>')
task = """ 1. Go to url google.com and search for "nasa universe story" in the search bar. 
         2. Find a NASA weblink with the Universe Stories. 
		 3. Go inside the NASA website and click on the first post and find what the article is about in a 8-9 sentences 
		 4. save the article to a file."""

async def run_search():
	agent = Agent(
		task=task,
		llm=model,
		controller=controller
	)

	history = await agent.run(max_steps=25)
	print(history.final_result())

asyncio.run(run_search())
