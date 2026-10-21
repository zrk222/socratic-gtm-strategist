# Cloud Agent & Remote Integration Guide

Socratic GTM Strategist (v3.0) is designed to run seamlessly **both locally on your workstation and integrated into remote cloud agents**.

---

## 1. OpenAI Custom GPTs & Assistants API

You can connect this entire advisory system directly into OpenAI as a Custom GPT or Assistant:

1. Host the server using Docker or deploy to Railway/Render/Cloud Run.
2. In the **OpenAI GPT Builder**:
   - Go to **Configure** -> **Actions** -> **Create New Action**.
   - Import the URL to your [`openapi.json`](./openapi.json) endpoint (e.g. `https://your-domain.com/openapi.json`).
3. Set the Custom GPT Instructions to the contents of [`SKILL.md`](./SKILL.md).
4. The GPT can now autonomously trigger simulations, competitor recon, and issue exports in real time.

---

## 2. LangChain & LangGraph Cloud Agents

Import the native Python tools directly into your LangChain or LangGraph workflows:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from socratic_gtm import get_langchain_tools, get_system_prompt

# 1. Load Socratic GTM Tools & System Instructions
tools = get_langchain_tools()
system_prompt = get_system_prompt()

# 2. Build Agent
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
agent = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 3. Execute
response = executor.invoke({"input": "We are building an AI agent for Shopify merchants..."})
print(response["output"])
```

---

## 3. CrewAI Cloud Agents

```python
from crewai import Agent, Task, Crew
from socratic_gtm import get_langchain_tools, get_system_prompt

gtm_advisor = Agent(
    role="Socratic GTM Strategist",
    goal="Ruthlessly de-risk founder Go-To-Market strategies",
    backstory="Elite AI startup partner enforcing the 8 laws of modern AI distribution.",
    tools=get_langchain_tools(),
    verbose=True
)

audit_task = Task(
    description="Analyze the startup pitch and run Phase 1 through 8 review.",
    expected_output="Risk matrix and interactive simulator.",
    agent=gtm_advisor
)

crew = Crew(agents=[gtm_advisor], tasks=[audit_task])
crew.kickoff()
```

---

## 4. Deployment boundary

The included HTTP adapter is a local, single-user tool without authentication.
Public cloud deployment is not supported by this implementation. Do not expose
it with an unauthenticated cloud service. Use the loopback-published container
example in README.md for local use.

LangChain, LangGraph and CrewAI examples above are illustrative integrations;
their provider calls, costs, versions and host behavior are not covered by
the standard-library regression suite.
