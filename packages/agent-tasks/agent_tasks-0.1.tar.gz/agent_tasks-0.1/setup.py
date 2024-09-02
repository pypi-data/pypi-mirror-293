from setuptools import setup, find_packages

setup(
    name='agent-tasks',  
    version='0.1', 
    packages=find_packages(),
    description='A task package for AI Research Bench', 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_data={
        'agent_tasks': ['prompt_template.j2'],  # Specify the files to include
    },
    install_requires=open('requirements.txt').read().splitlines(),
    author='Algorithmic Research Group',  
    author_email='matt@algorithmicresearchgroup.com', 
    keywords='tasks, agent, benchmark',
    url='http://github.com/ArtifactAI/agent-tasks',
    entry_points={
        'console_scripts': [
            'agent-tasks-run=agent_tasks.run:main',
        ],
    },
)