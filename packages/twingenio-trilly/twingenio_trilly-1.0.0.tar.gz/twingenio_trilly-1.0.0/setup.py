import re
from setuptools import setup


# Funzione per leggere il contenuto di requirements.txt
def read_requirements():
    with open("requirements.txt") as req:
        content = req.read()
        requirements = []
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                # Gestisce le dipendenze Git
                if line.startswith("git+"):
                    egg_match = re.search(r"#egg=(\w+)", line)
                    if egg_match:
                        requirements.append(egg_match.group(1))
                elif line.startswith("-e"):
                    # Ignora i requisiti che iniziano con -e
                    continue
                else:
                    # Rimuove i commenti alla fine della riga
                    req = line.split("#")[0].strip()
                    if req:
                        # Rimuove eventuali commenti di data dopo la versione
                        req = re.sub(r"\s+#.*$", "", req)
                        requirements.append(req)
    return requirements


setup(
    name="twingenio_trilly",
    version="1.0.0",
    packages=["trilly"],
    package_dir={"": "."},
    install_requires=read_requirements(),
    author="hypertrue",
    author_email="info@hypertrue.com",
    description="Supporto per servizi audio speech-to-text e text-to-speech",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Twingenio/trilly",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)


# import logging
# import sys


# def writeinfo(message):
#     log_to_file(message)


# def log_to_file(message):
#     with open("/home/site/wwwroot/setup_log.txt", "a") as f:
#         f.write(f"{message}\n")
#     sys.stdout.write(f"{message}\n")
#     sys.stdout.flush()


# def check_repo_access(repo_url):
#     try:
#         subprocess.check_call(
#             ["git", "ls-remote", repo_url],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL,
#         )
#         return True
#     except subprocess.CalledProcessError:
#         return False


# # Funzione per ottenere l'URL del repository con il token
# def get_repo_url(repo_name):
#     github_token = os.getenv("GITHUB_TOKEN", "")
#     writeinfo(f"Getting repo URL for {repo_name}")
#     if github_token:
#         writeinfo("GITHUB_TOKEN is set")
#         return f"https://{github_token}@github.com/Twingenio/{repo_name}.git"
#     else:
#         writeinfo("WARNING! - GITHUB_TOKEN is not set")
#         return f"https://github.com/Twingenio/{repo_name}.git"


# def install_extra_dependencies():
#     writeinfo("Starting install_extra_dependencies function")
#     writeinfo(
#         f"Pip version: {subprocess.check_output(['pip', '--version'], universal_newlines=True).strip()}"
#     )
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
#     env = os.getenv("REQENVIRONMENT", "local")
#     writeinfo(f"REQENVIRONMENT is set to: {env}")
#     req_file = f"requirements-{env}.txt"
#     writeinfo(f"Looking for requirements file: {req_file}")

#     if os.path.exists(req_file):
#         writeinfo(f"Found {req_file}, proceeding with installation")
#         github_token = os.getenv("GITHUB_TOKEN", "")
#         writeinfo("GITHUB_TOKEN is " + ("set" if github_token else "not set"))

#         # Leggi il contenuto del file
#         with open(req_file, "r") as file:
#             content = file.read()
#         writeinfo(f"DEBUG - Content of {req_file}: {content}")

#         # Sostituisci ${GITHUB_TOKEN} con il valore effettivo
#         content = content.replace("${GITHUB_TOKEN}", github_token)
#         writeinfo("Replaced GITHUB_TOKEN in requirements content")

#         # Crea un file temporaneo con il contenuto modificato
#         with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
#             temp_file.write(content)
#             temp_file_path = temp_file.name
#         writeinfo(f"Created temporary file: {temp_file_path}")

#         # All'interno di install_extra_dependencies()
#         for repo in ["alfred", "trilly"]:
#             repo_url = f"https://{github_token}@github.com/Twingenio/{repo}.git"
#             if check_repo_access(repo_url):
#                 writeinfo(f"Repository {repo} is accessible")
#             else:
#                 writeinfo(f"WARNING: Cannot access repository {repo}")

#         for line in content.splitlines():
#             if line.strip() and not line.startswith("#"):
#                 try:
#                     # Installa i requisiti dal file temporaneo
#                     writeinfo("Attempting to install requirements")
#                     command = ["pip", "install", line, "--force-reinstall", "--verbose"]
#                     output = subprocess.check_output(
#                         command,
#                         stderr=subprocess.STDOUT,
#                         universal_newlines=True,
#                     )
#                     writeinfo(f"Executing command: {' '.join(command)}")
#                     writeinfo(f"Successfully installed {line}")
#                     writeinfo(f"Output: {output}")
#                 except subprocess.CalledProcessError as e:
#                     writeinfo(f"Failed to install {line}")
#                     writeinfo(f"Error output: {e.output}")
#                 finally:
#                     # Rimuovi il file temporaneo
#                     os.unlink(temp_file_path)
#                     writeinfo("Temporary file removed")
#     else:
#         writeinfo(f"WARNING - {req_file} not found")


# try:

#     env_vars = ["GITHUB_TOKEN", "REQENVIRONMENT"]
#     for var in env_vars:
#         value = os.getenv(var, "Not set")
#         log_to_file(f"{var}: {value}")

#     with open("/home/site/wwwroot/setup_started.txt", "w") as f:
#         f.write("Setup started")

#     # Configura il logging
#     logging.basicConfig(
#         level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
#     )

#     setup(
#         name="your_project_name",
#         version="0.1",
#         packages=find_packages(),
#         include_package_data=True,
#         # install_requires=[
#         #     f"alfred @ {get_repo_url('alfred')}",
#         #     f"trilly @ {get_repo_url('trilly')}",
#         # ],
#         entry_points={
#             "console_scripts": [
#                 "post_install=setup:install_extra_dependencies",
#             ],
#         },
#     )
#     # Esegui install_extra_dependencies al momento dell'installazione
#     writeinfo("Executing install_extra_dependencies")
#     install_extra_dependencies()

#     with open("/home/site/wwwroot/setup_completed.txt", "w") as f:
#         f.write("Setup completed")
# except Exception as e:
#     with open("/home/site/wwwroot/setup_error.txt", "w") as f:
#         f.write(f"An error occurred: {str(e)}")


# # Funzione per leggere il contenuto di requirements.txt
# def read_requirements():
#     with open("requirements.txt") as req:
#         content = req.read()
#         requirements = []
#         for line in content.split("\n"):
#             line = line.strip()
#             if line and not line.startswith("#"):
#                 # Gestisce le dipendenze Git
#                 if line.startswith("git+"):
#                     egg_match = re.search(r"#egg=(\w+)", line)
#                     if egg_match:
#                         requirements.append(egg_match.group(1))
#                 elif line.startswith("-e"):
#                     # Ignora i requisiti che iniziano con -e
#                     continue
#                 else:
#                     # Rimuove i commenti alla fine della riga
#                     req = line.split("#")[0].strip()
#                     if req:
#                         # Rimuove eventuali commenti di data dopo la versione
#                         req = re.sub(r"\s+#.*$", "", req)
#                         requirements.append(req)
#     return requirements


# setup(
#     name="trilly",
#     version="0.0.2",
#     packages=find_packages(),
#     package_dir={"": "."},
#     install_requires=read_requirements(),
#     author="hypertrue",
#     author_email="info@hypertrue.com",
#     description="Un pacchetto per interfacciarsi con servizi TTS e STT",
#     long_description=open("README.md").read(),
#     long_description_content_type="text/markdown",
#     url="https://github.com/Twingenio/trilly",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.11",
#     entry_points={
#         "console_scripts": [
#             "post_install=setup:install_extra_dependencies",
#         ],
#     },
# )
