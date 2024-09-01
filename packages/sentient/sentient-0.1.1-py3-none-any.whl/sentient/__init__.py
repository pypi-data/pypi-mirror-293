from sentient.core.orchestrator.orchestrator import Orchestrator

class Sentient:
    @staticmethod
    async def invoke(command: str):
        return await Orchestrator.invoke(command)

sentient = Sentient()