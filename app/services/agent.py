import os
import httpx

AGENT_SERVICE_URL = os.getenv(
    "AGENT_SERVICE_URL",
    "http://127.0.0.1:9000/process"
)


class AgentServiceError(Exception):
    pass


async def invoke_agent(
    *,
    query: str,
    history: list[dict],
    timeout: int = 60
) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AGENT_SERVICE_URL,
                json={
                    "input": query,
                    "history": history
                },
                timeout=timeout
            )
            response.raise_for_status()

        data = response.json()
        output = data.get("output")

        if not output:
            raise AgentServiceError("Empty agent response")

        return output

    except httpx.TimeoutException:
        raise AgentServiceError("Agent timeout")
    except httpx.HTTPError as e:
        raise AgentServiceError(f"Agent HTTP error: {e}")
    except Exception as e:
        raise AgentServiceError(str(e))
