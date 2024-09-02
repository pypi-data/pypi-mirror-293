import re
from setuptools import setup, find_packages


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
    name="twingenio_alfred",
    version="1.0.7",
    packages=["alfred"],
    package_dir={"": "."},
    install_requires=read_requirements(),
    author="hypertrue",
    author_email="info@hypertrue.com",
    description="Client di Twingenio",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Twingenio/alfred",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
