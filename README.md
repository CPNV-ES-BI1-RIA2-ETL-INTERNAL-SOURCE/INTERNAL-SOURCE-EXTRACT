# INTERNAL-SOURCE-EXTRACT

## Description

The aim of this project is to create an **extract** component in an [ELT](https://en.wikipedia.org/wiki/Extract,_load,_transform) project. This part extracts data from PDF files and provides them through a [REST API](https://en.wikipedia.org/wiki/REST).

---

## Getting Started

### Prerequisites

* [PyCharm 2024.3](https://www.jetbrains.com/pycharm/)
* [Python 3.12.2](https://www.python.org/downloads/release/python-3122/)
* [Git 2.47.1](https://git-scm.com/downloads)
* [Pipenv 2024.4.0](https://pipenv.pypa.io/en/latest/)
* [pdf2text 25.02.0](https://www.xpdfreader.com/pdftotext-man.html)

### Installation

1. Install pdf2text 25.02.0 from [xpdfreader.com](https://www.xpdfreader.com/download.html)

2. Verify the installation:
   ```shell
   pdftotext -v
   ```
   Expected output:
   ```
    pdftotext version 25.03.0
    Copyright 2005-2025 The Poppler Developers - http://poppler.freedesktop.org
    Copyright 1996-2011, 2022 Glyph & Cog, LLC
   ```

3. Clone the repository and navigate to the project directory

4. Install dependencies:
   ```shell
   pipenv shell
   pipenv install
   ```
   Expected output:
   ```
   Installing dependencies from Pipfile.lock...
   ✓ Success!
   ```

5. For development environment, install dev dependencies:
   ```shell
   pipenv shell
   pipenv install --dev
   ```
   Expected output:
   ```
   Installing dependencies from Pipfile.lock...
   ✓ Success!
   ```

6. Validate installation:
   ```shell
   pipenv run python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
   ```
   Expected output:
   ```
   FastAPI version: 0.115.11
   ```

## Project Structure

```
internal-source-extract/
├── app/                    
│   ├── api/                # API endpoints
│   ├── core/               # Core functionality
│   ├── responses/          # Response models and handlers
│   ├── __init__.py
│   ├── config.py          
│   ├── exceptions.py      
│   └── schemas.py         
├── tests/                  
├── diagrams/              
├── .github/               
├── .dockerignore         
├── .gitignore            
├── Dockerfile            
├── LICENSE               
├── Pipfile              
├── Pipfile.lock         
├── README.md            
└── main.py              
```

## Running the Application

### Development Environment

1. Activate the virtual environment:
   ```shell
   pipenv shell
   ```

2. Run the application using FastAPI CLI:
   ```shell
   fastapi run main.py
   ```
   Expected output:
   ```
   FastAPI   Starting production server 🚀
   
   module   🐍 main.py
   
   server   Server started at http://0.0.0.0:8000
   server   Documentation at http://0.0.0.0:8000/docs
   ```

### Production Environment

1. Run the application in production mode:
   ```shell
   fastapi run main.py
   ```
   Expected output:
   ```
   FastAPI   Starting production server 🚀
   
   module   🐍 main.py
   
   server   Server started at http://0.0.0.0:8000
   server   Documentation at http://0.0.0.0:8000/docs
   ```

### Docker Environment

Build and run the Docker container:
```shell
  docker build -t internal-source-extract .
  docker run -p 8000:8000 internal-source-extract
```
Expected output:
```
Successfully built [container_id]
Successfully tagged internal-source-extract:latest
```

## Testing

The project uses [pytest](https://docs.pytest.org/) as its testing framework.

1. Make sure you're in your virtual environment:
   ```shell
   pipenv shell
   ```

2. Run all tests:
   ```shell
   pytest
   ```
   Expected output:
   ```
   ============================= test session starts ==============================
   platform darwin -- Python 3.12.2, pytest-7.4.0, pluggy-1.2.0
   rootdir: /path/to/internal-source-extract
   collected 10 items
   
   tests/test_api.py ....                                                  [ 40%]
   tests/test_services.py ......                                           [100%]
   
   ============================== 10 passed in 1.23s ==============================
   ```

3. Run a specific test file:
   ```shell
   pytest tests/test_api.py
   ```
   Expected output:
   ```
   ============================= test session starts ==============================
   platform darwin -- Python 3.12.2, pytest-7.4.0, pluggy-1.2.0
   rootdir: /path/to/internal-source-extract
   collected 4 items
   
   tests/test_api.py ....                                                  [100%]
   
   ============================== 4 passed in 0.45s ===============================
   ```

4. Run a specific test function:
   ```shell
   pytest tests/test_api.py::test_read_main
   ```
   Expected output:
   ```
   ============================= test session starts ==============================
   platform darwin -- Python 3.12.2, pytest-7.4.0, pluggy-1.2.0
   rootdir: /path/to/internal-source-extract
   collected 1 item
   
   tests/test_api.py::test_read_main PASSED                                [100%]
   
   ============================== 1 passed in 0.12s ===============================
   ```

5. Run tests with coverage report:
   ```shell
   pytest --cov=app tests/
   ```
   Expected output:
   ```
   ============================= test session starts ==============================
   platform darwin -- Python 3.12.2, pytest-7.4.0, pluggy-1.2.0
   rootdir: /path/to/internal-source-extract
   collected 10 items
   
   tests/test_api.py ....                                                  [ 40%]
   tests/test_services.py ......                                           [100%]
   
   ---------- coverage: platform darwin, python 3.12.2-final-0 ----------
   Name                  Stmts   Miss  Cover
   -----------------------------------------
   app/__init__.py           0      0   100%
   app/api/__init__.py       0      0   100%
   app/main.py              15      0   100%
   -----------------------------------------
   TOTAL                    15      0   100%
   
   ============================== 10 passed in 1.35s ==============================
   ```

## Coding Standards

This project follows strict coding standards and principles:

1. **[SOLID Principles](https://en.wikipedia.org/wiki/SOLID)**
   - Single Responsibility Principle (SRP)
   - Open-Closed Principle (OCP)
   - Liskov Substitution Principle (LSP)
   - Interface Segregation Principle (ISP)
   - Dependency Inversion Principle (DIP)

2. **Clean Code Practices**
   - [Meaningful names](https://www.martinfowler.com/bliki/TwoHardThings.html)
   - Small functions with single responsibility
   - [DRY (Don't Repeat Yourself)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
   - [KISS (Keep It Simple, Stupid)](https://en.wikipedia.org/wiki/KISS_principle)
   - Comments only when necessary
   - Proper error handling

3. **Python Specific Standards**
   - Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
   - Use [type hints](https://docs.python.org/3/library/typing.html)
   - Document functions and classes with [docstrings](https://peps.python.org/pep-0257/)
   - Maximum line length of 88 characters ([Black formatter](https://black.readthedocs.io/))

## Source References

This project relies on the following technologies and frameworks:

1. **PDF Processing**
   - [pdf2text 25.02.0](https://www.xpdfreader.com/pdftotext-man.html) - For PDF text extraction

2. **API Framework**
   - [FastAPI 0.110.0](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs

3. **Testing**
   - [pytest 7.4.0](https://docs.pytest.org/) - Testing framework
   - [pytest-cov 4.1.0](https://pytest-cov.readthedocs.io/) - Coverage reporting

4. **Development Tools**
   - [pipenv 2024.4.0](https://pipenv.pypa.io/) - Python dev workflow tool
   - [Black 24.3.0](https://black.readthedocs.io/) - Code formatter
   - [isort 5.13.2](https://pycqa.github.io/isort/) - Import sorter

## Collaborate

### Workflow
* Gitflow workflow
* Conventional Commits
* Feature branches should be created from develop
* Pull requests are open to merge into the develop branch

### Commits
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
```bash
<type>(<scope>): <subject>
```

- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **feat**: Adding a new feature
- **fix**: Bug fixes
- **perf**: Performance improvements
- **refactor**: Code changes that neither fix a bug nor add a feature
- **style**: Changes that do not affect code functionality
- **docs**: Documentation only changes
- **test**: Adding or correcting tests

Examples:
```bash
feat(pdf-parser): add support for multi-column layouts
```
```bash
fix(api): correct response status code for empty results
```

## License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for details.

## Contact

If you have any questions or issues, please create an issue on GitHub and we will respond as quickly as possible.