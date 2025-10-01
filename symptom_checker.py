import os
from typing import Dict, List

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

# Ensure your GROQ_API_KEY is set in your environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not set. Using default model.")
    groq_model = None  # Will use default model
else:
    from google.adk.models.lite_llm import LiteLlm
    groq_model = LiteLlm(model="groq/gemma2-9b-it")


# DEMO: Symptom Checker with Context Sharing between Tools
# This demonstrates how to pass context from one tool to another


def symptom_lookup(symptoms: str) -> Dict[str, str]:
    """Analyze symptoms and return possible conditions.
    
    Args:
        symptoms: Patient's symptoms (e.g., "fever and sore throat")
        
    Returns:
        dict with status, condition, and confidence level
    """
    # Parameter validation
    if not symptoms or not isinstance(symptoms, str):
        return {"status": "error", "error_message": "Symptoms must be a non-empty string"}
    
    symptoms_lower = symptoms.lower()
    
    # Mock symptom-to-condition mapping
    if any(word in symptoms_lower for word in ["fever", "chills", "sore throat", "cough", "headache"]):
        if "fever" in symptoms_lower and "sore throat" in symptoms_lower:
            condition = "Flu-like symptoms"
            confidence = "High"
        elif "fever" in symptoms_lower and "cough" in symptoms_lower:
            condition = "Common cold or respiratory infection"
            confidence = "Medium"
        else:
            condition = "General viral infection"
            confidence = "Medium"
    elif any(word in symptoms_lower for word in ["headache", "nausea", "dizziness"]):
        condition = "Possible migraine or tension headache"
        confidence = "Medium"
    elif any(word in symptoms_lower for word in ["stomach", "abdominal", "nausea", "vomiting"]):
        condition = "Gastrointestinal issue"
        confidence = "Medium"
    else:
        condition = "Unclear - may need professional evaluation"
        confidence = "Low"
    
    return {
        "status": "success",
        "condition": condition,
        "confidence": confidence,
        "symptoms_analyzed": symptoms
    }


def medication_suggestion(condition: str, patient_age: str = "adult") -> Dict[str, str]:
    """Recommend medications and care instructions based on condition.
    
    Args:
        condition: The condition identified by symptom lookup
        patient_age: Age group (adult/child/elderly)
        
    Returns:
        dict with medication recommendations and care instructions
    """
    # Parameter validation
    if not condition or not isinstance(condition, str):
        return {"status": "error", "error_message": "Condition must be a non-empty string"}
    if not patient_age or not isinstance(patient_age, str):
        patient_age = "adult"
    
    condition_lower = condition.lower()
    
    if "flu" in condition_lower or "cold" in condition_lower:
        if "respiratory" in condition_lower:
            meds = "Paracetamol (acetaminophen) for fever, throat lozenges, warm saline gargle"
            care = "Rest, plenty of fluids, steam inhalation, avoid cold drinks"
        else:
            meds = "Paracetamol for fever and body aches, rest"
            care = "Rest, hydration with warm fluids, maintain room temperature"
    elif "headache" in condition_lower or "migraine" in condition_lower:
        meds = "Ibuprofen or paracetamol, avoid caffeine"
        care = "Rest in a dark, quiet room, apply cold compress to forehead"
    elif "gastrointestinal" in condition_lower:
        meds = "Antacids, oral rehydration solution"
        care = "BRAT diet (banana, rice, apple, toast), small frequent meals, avoid spicy food"
    else:
        meds = "Consult healthcare provider for specific medication"
        care = "Monitor symptoms, rest, stay hydrated"
    
    # Age-specific adjustments
    if patient_age.lower() == "child":
        meds += " (use pediatric dosage)"
        care += ", ensure child is comfortable and well-hydrated"
    elif patient_age.lower() == "elderly":
        meds += " (consider lower dosage, check for drug interactions)"
        care += ", monitor closely for any complications"
    
    return {
        "status": "success",
        "medications": meds,
        "care_instructions": care,
        "condition_treated": condition,
        "age_group": patient_age
    }


# Wrap functions as tools to ensure proper function signatures
symptom_lookup_tool = FunctionTool(func=symptom_lookup)
medication_suggestion_tool = FunctionTool(func=medication_suggestion)

root_agent = LlmAgent(
    name="symptom_checker",
    model=groq_model if groq_model else "gemini-2.0-flash",  # Fallback to default model
    description="Health assistant that analyzes symptoms and suggests appropriate care with context sharing.",
    instruction=(
        "You are a helpful health assistant. When a patient describes symptoms: "
        "1. First use symptom_lookup to analyze the symptoms and identify possible conditions. "
        "2. Then use medication_suggestion with the identified condition to recommend appropriate care. "
        "3. Share the condition context between tools - pass the condition from step 1 to step 2. "
        "4. Provide a clear summary: Symptoms → Possible Condition → Recommended Action. "
        "Always emphasize that this is not a substitute for professional medical advice."
    ),
    tools=[symptom_lookup_tool, medication_suggestion_tool],
)


def chat_once(query: str) -> str:
    """Run a single interaction with the symptom checker."""
    runner = InMemoryRunner(agent=root_agent)
    events = runner.run(
        user_id="patient",
        session_id="consultation",
        new_message=types.Content(role="user", parts=[types.Part(text=query)]),
    )
    output = []
    for e in events:
        if e.content and e.content.parts:
            for part in e.content.parts:
                if getattr(part, "text", None):
                    output.append(part.text)
    return "\n".join(output).strip()


if __name__ == "__main__":
    print("=== Symptom Checker Health Assistant ===")
    print("Describe your symptoms and I'll help analyze them.")
    print("Example: 'I have a fever and sore throat'")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            symptoms = input("Patient: ")
            if symptoms.lower() in ['quit', 'exit', 'q']:
                break
            print(f"Assistant: {chat_once(symptoms)}\n")
        except EOFError:
            break
