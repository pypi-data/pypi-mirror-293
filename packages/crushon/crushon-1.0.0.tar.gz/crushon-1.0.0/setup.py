from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()
setup(
    name="crushon",
    version="1.0.0",
    author_email="Redpiar.official@gmail.com",
    description="Crushon provides access to the Crushon.Ai API.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/RedPiarOfficial/Crushon-Ai",
    author="RedPiar",
    license="MIT",
    keywords=[
        "artificial-intelligence",
        "crushonAi",
        "charactersAi",
        "ai"
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "cloudscraper"
    ],
    project_urls={
        "Source": "https://github.com/RedPiarOfficial/Crushon-Ai",
    },
)
