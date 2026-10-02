# AI Research & Content Writer (CrewAI Multi-Agent App)

A multi-agent AI application built with **CrewAI** that researches any topic on the web and turns the findings into a well-structured, cited blog post, all from a simple **Streamlit** interface.

![App screenshot](screenshot.png)

## How it works

Two AI agents collaborate in a sequential workflow:

```
   Topic  ──►  🔎 Senior Research Analyst  ──►  ✍️ Content Writer  ──►  Blog post (.md)
                 (web search via Serper)          (turns research into
                 fact-checks, cites sources)       an engaging article)
```

1. **Senior Research Analyst**: uses the Serper web search tool to gather recent developments, trends, statistics and expert opinions, then produces a structured research brief with sources.
2. **Content Writer**: transforms the brief into an engaging, accessible blog post in markdown, preserving every fact and citation.

## Features

- Research any topic you type in
- Adjustable LLM temperature (creativity) and search depth
- Output with inline citations linked to original sources
- One-click download of the article as a Markdown file

## Tech stack

- **CrewAI**: multi-agent orchestration (agents, tasks, crew)
- **Google Gemini**: LLM powering both agents
- **Serper API**: Google search tool for the research agent
- **Streamlit**: web UI
- **Python 3.11**

## Getting started

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/crewai-content-writer.git
cd crewai-content-writer

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys
copy .env.example .env       # Windows  (cp on macOS / Linux)
# then open .env and paste your GEMINI_API_KEY and SERPER_API_KEY

# 5. Run the app
streamlit run streamlit_app.py
```

Get your keys at [Google AI Studio](https://aistudio.google.com/apikey) (Gemini) and [serper.dev](https://serper.dev) (Serper).

## Project structure

```
├── streamlit_app.py   # Agents, tasks, crew and Streamlit UI
├── requirements.txt   # Python dependencies
├── .env.example       # Template for API keys
└── README.md
```

## Possible next steps

- Add an editor/fact-checker agent to review the draft
- Stream agent progress live in the UI
- Support other LLMs (OpenAI, local models via Docker Model Runner)
