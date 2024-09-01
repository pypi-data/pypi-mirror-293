import asyncio

from sentient.core.agent.agent import AgentQ
from sentient.core.models.models import State
from sentient.core.orchestrator.orchestrator import Orchestrator


async def main():
    # Define state machine
    state_to_agent_map = {
        State.BASE_AGENT: AgentQ(),
    }

    orchestrator = Orchestrator(state_to_agent_map=state_to_agent_map)
    await orchestrator.start()


if __name__ == "__main__":
    asyncio.run(main())
