from fabric import task
from invoke import Collection  # ✅ import from invoke, not fabric

@task
def hello(c):
    print("Hello, Memory Engine!")

@task
def list_data(c):
    """Lists files in the data folder"""
    result = c.run("ls -la data", hide=True)
    print(result.stdout)

# Explicitly register tasks
ns = Collection(hello, list_data)
