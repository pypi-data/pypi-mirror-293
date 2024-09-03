import asyncio

import httpx

from neat import neat
from neat.types import LLMModel
from neat.web_search import ArticleFetcher, search


async def fetch_data(url: str, params: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()


@neat.alm(
    model=LLMModel.GPT_4O_MINI,
    tools=[
        search,
        ArticleFetcher().fetch_article,
    ],
    temperature=0.2,
    conversation=True,
)
async def weather_small_talk():
    return [
        neat.system(
            "You are an excellent web search assistant that is given the ability to search the web for information and read teh contents of webpages. Please assist the user with their question using your tools."
        ),
    ]


async def main():
    conversation = await weather_small_talk()
    print("Weather Small Talk:")
    print(conversation)


if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())
