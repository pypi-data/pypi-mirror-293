from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="glimapi",
    version="0.1.0",
    packages=find_packages(include=["app", "app.*"]),
    package_dir={".": "app"},
    install_requires=[
        "fastapi",
        "pydantic",
        "uvicorn",
        "pymongo",
        "jose",
        "passlib[bcrypt]",
        "aioredis",
        "fastapi-limiter",
        "passlib",
        "pydantic_settings",
        "python_jose",
        "redis",
        "starlette",
        "toml",
        "colorama",
        "termcolor"
    ],
    entry_points={
        "console_scripts": [
            "glimapi-start=app.main:run",
            "glimapi-help=app.console_help:show_help",
            "glimapi-generate-toml=app.generate_config:generate_toml",
        ],
    },
    package_data={
        'app': ['example_config.toml', '**/*.py'],
    },
    include_package_data=True,
    license="CC BY-NC-ND 4.0",
    description="A dynamic API generator with JWT, rate limiting and localization support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Glimor/glim-api",
    author="KAAN KAYACI",
    author_email="kayaci.kaan@proton.me"
)
