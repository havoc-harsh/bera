from setuptools import find_packages, setup

setup(
    name = 'Dr-Bera',
    version= '0.1.0',
    author= 'Harsh Ranjan',
    author_email= 'harsh@example.com',
    packages= find_packages(),
    install_requires = [
        'langchain',
        'langchain-google-genai',
        'flask',
        'flask-cors',
        'pinecone-client',
        'python-dotenv',
        'sentence-transformers',
        'gunicorn'
    ]
)