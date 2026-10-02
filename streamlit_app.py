import os
import re

from dotenv import load_dotenv
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

load_dotenv()

MODEL = "gemini/gemini-3.6-flash"

st.set_page_config(page_title="AI Research & Content Writer", page_icon="📝")
st.title("📝 AI Research & Content Writer")
st.markdown(
    "A multi-agent app built with **CrewAI**: a research agent searches the web, "
    "then a writer agent turns the findings into a cited blog post."
)

# Sidebar
with st.sidebar:
    st.markdown("### Content Settings")
    topic = st.text_area("Enter the topic", height=100,
                         placeholder="e.g. Generative AI in healthcare")
    st.markdown("### LLM Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7,
                            help="Higher = more creative writing, lower = more factual.")
    n_results = st.slider("Search results to read", 3, 10, 5,
                          help="More results = deeper research, but slower.")

    with st.expander("How it works"):
        st.write(
            "1. The **Research Analyst** agent searches the web (Serper) and writes "
            "a research brief with sources.\n"
            "2. The **Content Writer** agent turns the brief into a blog post in "
            "markdown, keeping the citations."
        )


def build_crew(topic: str, temperature: float, n_results: int) -> Crew:
    llm = LLM(model=MODEL, temperature=temperature)
    search_tool = SerperDevTool(n_results=n_results)

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Research, analyze and synthesize comprehensive information on {topic}",
        backstory="""You are an expert research analyst with advanced web research skills.
        You excel at finding, analyzing, and synthesizing information from across the internet
        using search tools. You are skilled at distinguishing reliable sources from unreliable
        ones, fact-checking, cross-referencing information, and identifying key patterns and
        insights. You provide well-organized research.""",
        allow_delegation=False,
        verbose=True,
        tools=[search_tool],
        llm=llm,
    )

    content_writer = Agent(
        role="Content Writer",
        goal="Transform research findings into engaging blog posts while maintaining accuracy",
        backstory="""You are a skilled content writer specialized in creating engaging, accessible
        content from technical research. You work closely with the senior research analyst and excel
        at maintaining the perfect balance between informative and entertaining writing, while ensuring
        all facts and citations from the research are preserved. You have a talent for making complex
        topics approachable without oversimplifying.""",
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )

    research_task = Task(
        description=f"""Conduct comprehensive research on {topic}. Cover recent developments and news,
        key industry trends and innovations, expert opinions and analysis, statistical data and market
        insights. Evaluate for credibility and fact-check all information. Organize findings into a
        structured research brief. Include all relevant citations and sources.""",
        expected_output="""A detailed research report containing:
        - Executive summary of key findings
        - Comprehensive analysis of current trends and developments
        - List of verified facts and statistics
        - All citations and links to original sources
        - Clear categorization of main themes and patterns
        Format with clear sections and bullet points for easy reference.""",
        agent=researcher,
    )

    writing_task = Task(
        description="""Transform the technical information into accessible content. Maintain all
        factual accuracy and citations from the research. Write an attention-grabbing introduction.
        Create well-structured body sections with clear headings. Preserve all citations in source
        URL format.""",
        expected_output="""A polished blog post in markdown format that engages readers while
        maintaining accuracy. Content properly structured into sections. Includes inline citations
        hyperlinked to original source URLs. Presents information in an accessible yet informative
        way. Use H1 for title and H3 for subsections.""",
        agent=content_writer,
    )

    return Crew(
        agents=[researcher, content_writer],
        tasks=[research_task, writing_task],
        verbose=True,
    )


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "content"


missing = [k for k in ("GEMINI_API_KEY", "SERPER_API_KEY") if not os.getenv(k)]

if st.button("Generate Content", type="primary"):
    if missing:
        st.error(f"Missing API key(s): {', '.join(missing)}. Add them to your .env file.")
    elif not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner("Agents are researching and writing... this can take a minute."):
                result = build_crew(topic, temperature, n_results).kickoff(inputs={"topic": topic})
            content = str(result)
            st.markdown(content)
            st.download_button(
                label="Download as Markdown",
                data=content,
                file_name=f"{slugify(topic)}.md",
                mime="text/markdown",
            )
        except Exception as e:
            st.error(f"Something went wrong while generating content: {e}")
