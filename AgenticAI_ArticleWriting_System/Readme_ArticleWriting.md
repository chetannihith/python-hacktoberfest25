# Agentic AI Article Writer 🤖

This project demonstrates an **Agentic AI System** built using **CrewAI** that automates the process of researching, analyzing, and writing a structured report on a given topic. It utilizes a custom tool for web searching powered by **Google Gemini** for real-time, grounded information retrieval and leverages a powerful Groq-powered LLM for agent reasoning and execution.

---

## ✨ Features

* **Three-Agent Pipeline:** A workflow consisting of a **Researcher**, an **Analysis**, and a **Report Writer** agent.
* **Gemini-Powered Web Search:** Includes a custom `GeminiSearchTool` to perform **real-time web searches** with Google's Gemini, ensuring the retrieved information is up-to-date and grounded.
* **Structured Output:** The final agent generates a report strictly formatted in Markdown with predefined sections: `Topic`, `Key Findings`, `Conclusion`, and `References`.
* **Modular and Extensible:** Built on the CrewAI framework, making it easy to swap LLMs, add new tools, or modify agent roles and tasks.

---

## 🛠️ Installation

### Prerequisites

* Python 3.9+
* A **Groq API Key**
* A **Gemini API Key** (set as `GEMINI_API_KEY`)

### Setup

1.  **Install the necessary libraries:**

    The notebook installs `crewai`, `crewai_tools`, `python-dotenv`, and `docling`.
    ```bash
    !pip install crewai
    !pip install crewai_tools
    !pip install python-dotenv
    # !pip install docling
    ```

2.  **Set API Keys:**
    The notebook uses `google.colab.userdata.get()` to securely retrieve API keys. You must ensure your environment variables (`GROQ_API_KEY` and `GEMINI_API_KEY`) are correctly set.

    ```python
    from google.colab import userdata
    import os
    os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")
    os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")
    ```

---

## 🧠 Agent Architecture & Workflow

The system is organized into a sequential CrewAI workflow with three specialized agents:

| Agent Role | Goal | Responsibility |
| :--- | :--- | :--- |
| **Researcher** | Search the web for information on the given topic and find accurate information. | Executes the `GeminiSearchTool` to gather raw, factual data. |
| **Analysis** | Take the raw content and find the key insights, research findings, and important points. | Processes the raw data into a structured, numbered list of key findings. |
| **Report Writer** | Get the content from the analysis agent and write it down in the form of a formal Markdown report. | Formats the analyzed data into the final Markdown report structure. |

### Custom Tool: `GeminiSearchTool`

The custom tool allows the **Researcher** agent to perform web searches using Google Gemini and its grounding capability:

```python
class GeminiSearchTool(BaseTool):
    # ... tool definition ...
    def _run(self, query: str) -> str:
        client = genai.Client()
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config = types.GenerateContentConfig(tools=[grounding_tool], temperature=0.0)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=config,
        )
        return response.text