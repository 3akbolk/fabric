from fabric import task
import os

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
    import os
    import requests
    from bs4 import BeautifulSoup

    if source.startswith("http"):
        r = requests.get(source)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")  # Extract readable text
        print("Extracted wisdom from URL:")
        print(text[:500])  # Show first 500 chars
    else:
        if os.path.exists(source):
            with open(source) as f:
                text = f.read()
            print("Extracted wisdom from file:")
            print(text[:500])
        else:
            print("Source not found:", source)
