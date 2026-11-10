from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from tools import search_products,calculate_order_total
import os

def create_multiple_agents():
    client = OpenAIChatCompletionClient(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("KEY"),
        model=os.getenv("MODEL")
    )

    search_inventory_agent = Agent(
        client=client,
        name="SearchInventoryAgent",
        instructions=(
            "You are a product inventory search specialist. "
            "Use search_products to find products "
            "matching the user's requested topic. "
            "List the matching product IDs and details. "
            "Do not calculate total group fees."
        ),
        tools = [search_products]
    )

    pricing_agent = Agent(
        client=client,
        name="PricingAgent",
        instructions=(
            "You are a product pricing specialist. "
        "Read the previous search results and user request. "
        "Use only product IDs returned by SearchInventoryAgent. "
        "Use calculate_order_total with the requested quantity. "
        "Report verified totals. Never invent prices."
        ),
        tools = [calculate_order_total]
    )

    recommendation_agent = Agent(
        client=client,
        name="RecommendationAgent",
        instructions=(
            "You are a product recommendation specialist. "
            "Read the search and pricing results. "
            "Recommend the best matching workshop "
            "within the user's budget. "
            "Explain your choice briefly. "
            "Use only verified workshop data and totals."
        )
    )

    return search_inventory_agent, pricing_agent, recommendation_agent