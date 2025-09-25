from fabric import task
import json
import os
import requests
from bs4 import BeautifulSoup
import copy
from openai import OpenAI

# Import your skeleton templates
from templates.extract_wisdom_skeleton import EXTRACT_WISDOM_SKELETON
from templates.investigate_document_skeleton import INVESTIGATE_DOCUMENT_SKELETON

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_ai(prompt):
    """
    Sends a prompt to the AI model using OpenAI v1.0+.
    Returns the content from the response.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a structured data extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content


# -------------------------------
# Utility / sanity tasks
# -------------------------------
@task
def hello(c):
    """Sanity check to make sure Fabric is working"""
    print("Hello, Fabric project is working!")

@task
def list_data(c):
    """Lists files in the data folder"""
    result = c.run("ls -la data", hide=True, warn=True)
    print(result.stdout)

@task
def make_file(c, name="example.txt"):
    """Creates a file in the data folder"""
    if not os.path.exists("data"):
        os.makedirs("data")
    c.run(f"echo 'This is a test file' > data/{name}")
    print(f"Created data/{name}")

@task
def clean_data(c):
    """Deletes all files in the data folder"""
    if not os.path.exists("data"):
        os.makedirs("data")
    c.run("rm -f data/*", warn=True)
    print("Cleaned data folder")


# -------------------------------
# Extract Wisdom Task
# -------------------------------
@task
def extract_wisdom(c, source="data/input.txt"):
    """
    Extracts wisdom from a local file or a web URL.
    Uses EXTRACT_WISDOM_SKELETON as template.
    """
    # Load content
    if source.startswith("http"):
        r = requests.get(source)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")
        print("Extracted wisdom from URL (first 1000 chars):")
        print(text[:1000])
    else:
        if os.path.exists(source):
            with open(source, "r", encoding="utf-8") as f:
                text = f.read()
            print("Extracted wisdom from file (first 1000 chars):")
            print(text[:1000])
        else:
            print("Source not found:", source)
            return

    # Prepare initial JSON from skeleton
    data_json = copy.deepcopy(EXTRACT_WISDOM_SKELETON)
    data_json["title"] = os.path.basename(source)
    data_json["metadata"]["source_file"] = source
    data_json["metadata"]["length"] = len(text)

    # read source content
    with open(source, "r", encoding="utf-8") as f:
        content = f.read()

    # Load the system prompt from system.md
    with open("my_patterns/extract_wisdom/system.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Build AI prompt
    ai_prompt = f"{system_prompt}\n\nDocument:\n{text}"


    # Query AI
    ai_output = query_ai(ai_prompt)

    # Clean AI output
    import re
    def clean_ai_output(output):
        return re.sub(r"^```(?:json)?|```$", "", output.strip(), flags=re.MULTILINE)

    cleaned_output = clean_ai_output(ai_output)


    # Parse AI output
    try:
        ai_data = json.loads(cleaned_output)
        data_json.update(ai_data)
        print("AI extraction successful.")
    except json.JSONDecodeError:
        print("Error parsing AI output. Saving skeleton only.")
        print("AI output preview:", ai_output[:300])

    # Save JSON
    json_file = os.path.splitext(source)[0] + "_wisdom.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data_json, f, indent=2)

    print(f"Wisdom extraction complete. JSON saved to {json_file}")


# -------------------------------
# Investigate Document Task
# -------------------------------
@task
def investigate_document(c, source):
    """
    Investigates a document for facts, habits, references.
    Uses INVESTIGATE_DOCUMENT_SKELETON as template.
    """
    print(f"Investigating document: {source}")
    if not os.path.exists(source):
        print(f"Error: File {source} does not exist.")
        return

    # read source content
    with open(source, "r", encoding="utf-8") as f:
        content = f.read()

    # Prepare initial JSON from skeleton
    doc_json = copy.deepcopy(INVESTIGATE_DOCUMENT_SKELETON)
    doc_json["title"] = os.path.basename(source)
    doc_json["metadata"]["source_file"] = source
    doc_json["metadata"]["length"] = len(content)
    doc_json["metadata"]["processed_date"] = "2025-09-24"

    print("Initial JSON structure prepared.")


    # Load the system prompt from system.md
    with open("my_patterns/investigate_document/system.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Build AI prompt
    ai_prompt = f"{system_prompt}\n\nDocument:\n{content}"

    # Query AI
    ai_output = query_ai(ai_prompt)

    # Clean AI output
    import re
    def clean_ai_output(output):
        return re.sub(r"^```(?:json)?|```$", "", output.strip(), flags=re.MULTILINE)

    cleaned_output = clean_ai_output(ai_output)

    # Parse AI output
    try:
        ai_data = json.loads(cleaned_output)
        doc_json.update(ai_data)
        print("AI extraction successful.")
    except json.JSONDecodeError:
        print("Error parsing AI output. Saving skeleton only.")
        print("AI output preview:", ai_output[:300])

    # Save JSON
    json_file = os.path.splitext(source)[0] + "_investigate.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(doc_json, f, indent=2)

    print(f"Document investigation complete. JSON saved to {json_file}")
