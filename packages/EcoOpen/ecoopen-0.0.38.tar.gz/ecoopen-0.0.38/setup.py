from setuptools import setup, find_packages

setup(
    name="EcoOpen",
    version="0.0.38",
    packages=find_packages(),
    install_requires=[
        "habanero",
        "numpy",
        "pandas",
        "scipy",
        "ollama",
        "beautifulsoup4",
        "scikit-learn",
        # "pypaperbot",
        # "ollama",
        # "transformers",
        # "datasets",
        # "torch",
        # "torchvision",
        # "torchaudio",
        # "accelerate",
        "selenium",
        "webdriver_manager",
        "tika",
        "jupyterlab",
        "lxml"
    ],
    # entry_points={
    #     "console_scripts": [
    #         "EcoOpen=EcoOpen.core:main"
    #     ]
    # }
    author="Sciom d.o.o.",
    author_email="domagoj@sciom.hr",
    description="A tool for gathering information about data and data in scientific journals.",
    license="MIT",
    keywords="scientific journals, LLM, open access",
    url="https://sciom.hr"
)
