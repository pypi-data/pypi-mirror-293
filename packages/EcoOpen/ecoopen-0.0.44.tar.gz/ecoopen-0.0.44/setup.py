from setuptools import setup, find_packages

setup(
    name="EcoOpen",
    version="0.0.44",
    packages=find_packages(),
    install_requires=[
        "habanero",
        "numpy",
        "pandas",
        "scipy",
        "pdfplumber",
        "beautifulsoup4",
        "scikit-learn",
        "selenium",
        "webdriver_manager",
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
    keywords="scientific journals, open access, data_mining",
    url="https://sciom.hr"
)
