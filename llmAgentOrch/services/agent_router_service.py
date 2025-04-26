import asyncio

class ChatBotAgent:
    async def handle(self, request: str):
        await asyncio.sleep(2)  # simulate long response
        return f"ChatBot: Processing your message - {request}"

class CRMSystemAgent:
    async def handle(self, request: str):
        await asyncio.sleep(3)  # simulate long CRM lookup
        return f"CRM: Created support ticket for - {request}"

class AgentRouterService:
    def __init__(self):
        self.agents = {
            "support": CRMSystemAgent(),
            "sales": ChatBotAgent(),
            "billing": CRMSystemAgent(),
            "technical issue": CRMSystemAgent(),
            "feedback": ChatBotAgent(),
        }

    async def route(self, request_type: str, request_text: str):
        agent = self.agents.get(request_type)
        if not agent:
            raise ValueError(f"No agent found for type {request_type}")
        return await agent.handle(request_text)
