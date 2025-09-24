from fabric import task
import json
import os
import requests
from bs4 import BeautifulSoup

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_ai(prompt):
    """
    Sends a prompt to the AI model using OpenAI v1.0+.
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

@task
def check_model(c):
    print("AI settings:", config.settings.get("ai"))


@task
def hello(c):
    """Sanity check to make sure Fabric is working"""
    print("Hello, Fabric project is working!")

# -------------------------------
# File helpers
# -------------------------------
@task
def list_data(c):
    """Lists files in the data folder"""
    result = c.run("ls -la data", hide=True, warn=True)
    print(result.stdout)

@task
def make_file(c, name="example.txt"):
    """Creates a file in the data folder"""
    
    # Step 1: Ensure the data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")  # creates the folder if it doesn't exist

    # Step 2: Create the file
    c.run(f"echo 'This is a test file' > data/{name}")
    print(f"Created data/{name}")

@task
def clean_data(c):
    """Deletes all files in the data folder"""

    # Step 1: Ensure the data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")  # creates the folder if it doesn't exist
    
    # Step 2: Remove all files in the data folder
    c.run("rm -f data/*", warn=True)
    print("Cleaned data folder")

# -------------------------------
# Pattern helpers
# -------------------------------
   
@task
def extract_wisdom(c, source="data/input.txt"):
    """
    Extracts wisdom from a local file or a web URL.
    Cleans HTML if source is a URL.
    """

    if source.startswith("http"):
        r = requests.get(source)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")  # Extract readable text
        print("Extracted wisdom from URL:")
        print(text[:1000])  # Show first 500 chars
    else:
        if os.path.exists(source):
            with open(source) as f:
                text = f.read()
            print("Extracted wisdom from file:")
            print(text[:1000])
        else:
            print("Source not found:", source)
from fabric import task
import json
import os
from openai import OpenAI

# initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_ai(prompt):
    """Send prompt to AI and return the content"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a structured data extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

@task
def investigate_document(c, source):
    print(f"Investigating document: {source}")

    if not os.path.exists(source):
        print(f"Error: File {source} does not exist.")
        return

    # load the document
    with open(source, "r", encoding="utf-8") as f:
        content = f.read()

    # initial JSON skeleton
    doc_json = {
        "title": os.path.basename(source),
        "source_type": "document",
        "facts": [],
        "habits": [],
        "references": [
            {"title": os.path.basename(source), "type": "document", "link": None}
        ],
        "metadata": {"extracted_date": "2025-09-24"}
    }

    print("Initial JSON structure prepared.")

    # AI prompt with enforced JSON output
    ai_prompt = f"""
Extract key insights from the following document.
Return only valid JSON in this format:

{{
  "facts": [{{"description": "...", "context": "..."}}],
  "habits": [{{"description": "...", "context": "..."}}],
  "references": [{{"title": "...", "type": "...", "link": "..."}}
  ]
}}

Document:
{content}
"""

    # query AI
    ai_output = query_ai(ai_prompt)

    # attempt to parse AI output
    try:
        ai_data = json.loads(ai_output)
        doc_json["facts"] = ai_data.get("facts", [])
        doc_json["habits"] = ai_data.get("habits", [])
        doc_json["references"].extend(ai_data.get("references", []))
        print("AI extraction successful.")
    except json.JSONDecodeError:
        print("Error parsing AI output. Saving JSON skeleton only.")
        print("AI output preview:", ai_output[:300])  # preview first 300 chars

    # save final JSON
    json_file = os.path.splitext(source)[0] + ".json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(doc_json, f, indent=2)

    print(f"Document investigation complete. JSON saved to {json_file}")