from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    readme_text: str = f.read()

setup(
    name="newguy103-chatinterface-server",
    version='0.0.1',
    description="A simple centralized, self-hosted server for chatting.",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="NewGuy103",
    author_email="userchouenthusiast@gmail.com",
    install_requires=[
        "msgpack",
        "mysql-connector-python",
        "fastapi",
        "argon2-cffi",
    ],
    license="GPL v2.0",
    packages=find_packages()
)
