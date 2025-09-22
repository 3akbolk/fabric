from fabric import task

@task
def hello(c):
    print("Hello, Fabric project is working!")

@task
def list_data(c):
    """Lists files in the data folder"""
    result = c.run("ls -la data", hide=True, warn=True)
    print(result.stdout)

@task
def make_file(c, name="example.txt"):
    """Creates a file in the data folder"""
    c.run(f"echo 'This is a test file' > data/{name}")
    print(f"Created data/{name}")

@task
def clean_data(c):
    """Deletes all files in the data folder"""
    c.run("rm -f data/*", warn=True)
    print("Cleaned data folder")

@task
def build_container(c, service="fabric-project"):
    """Builds the Docker container"""
    c.run(f"docker build -t {service} .")
    print(f"{service} container built!")

@task
def run_container(c, service="fabric-project", port="8000:8000"):
    """Runs the Docker container"""
    c.run(f"docker run -p {port} {service}")
    print(f"{service} container running on port {port}")

@task
def stop_container(c, service="fabric-project"):
    """Stops all running containers with the given name"""
    c.run(f"docker ps -q --filter name={service} | xargs -r docker stop")
    print(f"Stopped all {service} containers")
