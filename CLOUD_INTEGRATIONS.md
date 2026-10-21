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

## 4. Cloud Container Deployment (1-Click)

### Run with Docker locally or on a cloud VM:
```bash
docker build -t socratic-gtm .
docker run -p 8000:8000 socratic-gtm
```

### Deploy to GCP Cloud Run:
```bash
gcloud run deploy socratic-gtm \
  --source . \
  --port 8000 \
  --allow-unauthenticated
```

### Deploy to Railway / Render / Fly.io:
Point your Railway/Render service to the GitHub repository. It will automatically detect the `Dockerfile` and expose port `8000`.

Once deployed, your cloud agents can access:
- **Interactive UI Dashboard with STT/TTS:** `https://your-app.com/ui/index.html`
- **OpenAPI Schema:** `https://your-app.com/openapi.json`
- **REST Endpoints:** `https://your-app.com/api/chat`, `https://your-app.com/api/simulate`, etc.
