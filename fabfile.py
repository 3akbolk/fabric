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
def extract_wisdom(c, input_file="data/input.txt"):
    """
    Runs the extract_wisdom pattern on a text file.
    Example: fab extract-wisdom --input-file=data/mydraft.txt
    """
    script_path = "my_patterns/extract_wisdom/extract_wisdom.py"
    if os.path.exists(script_path):
        c.run(f"python3 {script_path} {input_file}")
        print(f"Ran extract_wisdom on {input_file}")
    else:
        print("extract_wisdom pattern not found!")