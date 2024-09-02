from setuptools import setup, find_packages

setup(
    name='dialogic-ai',
    version='0.0.3',
    packages=find_packages(include=['dialogic_ai', 'dialogic_ai.*']),
    install_requires=[
    ],
    extras_require={
        'dev': [
            "pytest>=8.3.2",
        "black>=24.8.0"
        ],
    },  
    include_package_data=True,
    license='MIT',
    description="A Python package designed to manage complex, threaded conversations with branching capabilities, much like version control systems manage code branches.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/endybits/dialogic-ai",
    author="Endy Bermudez Rodriguez",
    author_email="endyb.dev@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    keywords="conversational AI, chat, chatbot, threaded conversations, AI, NLP, branching dialogues, dialogicai, dialogic-ai", 
)