# Contributing to Python Hacktoberfest 2025 🎃

Thank you for your interest in contributing to this repository! This guide will help you get started with your contributions for Hacktoberfest 2025.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Contribution Guidelines](#contribution-guidelines)
- [Project Ideas](#project-ideas)
- [Code Standards](#code-standards)
- [Pull Request Process](#pull-request-process)
- [Hacktoberfest Rules](#hacktoberfest-rules)

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher installed
- Git installed on your system
- A GitHub account
- Basic knowledge of Python programming

### Setting Up Your Development Environment

1. **Fork this repository**
   - Click the "Fork" button at the top right of this repository
   - This creates a copy of the repository in your GitHub account

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/python-hacktoberfest25.git
   cd python-hacktoberfest25
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/chetannihith/python-hacktoberfest25.git
   ```

4. **Create a new branch**
   ```bash
   git checkout -b your-feature-branch
   ```

## 💡 How to Contribute

### Types of Contributions We Accept

1. **New Python Projects/Scripts**
   - Mini games
   - Utility scripts
   - Algorithm implementations
   - Data science projects
   - Web scraping tools
   - Automation scripts

2. **Improvements to Existing Code**
   - Bug fixes
   - Performance optimizations
   - Code refactoring
   - Adding error handling
   - Improving code documentation

3. **Documentation**
   - README improvements
   - Code comments
   - Tutorials
   - Example usage

4. **Testing**
   - Unit tests
   - Integration tests
   - Test coverage improvements

## 📝 Contribution Guidelines

### Do's ✅

- **Write clean, readable code** with proper comments
- **Follow Python naming conventions** (PEP 8)
- **Test your code** before submitting
- **Add a README** if creating a new project folder
- **Include docstrings** for functions and classes
- **Handle errors gracefully** with try-except blocks
- **Use meaningful commit messages**
- **One feature per pull request**

### Don'ts ❌

- **Don't submit spam PRs** (duplicate content, minor text changes)
- **Don't copy-paste code** from other sources without attribution
- **Don't modify .gitignore** or other config files unless necessary
- **Don't submit auto-generated code**
- **Don't create PRs for issues that are already assigned**
- **Don't include large binary files** or dependencies

## 🎯 Project Ideas

Here are some ideas for contributions:

### Beginner Level
- Password strength checker
- BMI calculator with GUI
- File organizer script
- Simple chatbot
- Currency converter
- Word counter
- Palindrome checker

### Intermediate Level
- Web scraper with BeautifulSoup
- Todo list application with database
- Weather application using API
- Email automation script
- PDF merger/splitter
- Image manipulation tool
- CSV data analyzer

### Advanced Level
- Machine learning model implementation
- Rest API with Flask/FastAPI
- Data visualization dashboard
- Web crawler
- Discord/Telegram bot
- Recommendation system
- Blockchain implementation

## 📏 Code Standards

### Python Style Guide (PEP 8)

```python
# Good: Clear function names and docstrings
def calculate_factorial(n):
    """
    Calculate the factorial of a number.
    
    Args:
        n (int): The number to calculate factorial for
        
    Returns:
        int: The factorial of n
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * calculate_factorial(n - 1)
```

### File Structure

For new projects, create a dedicated folder:

```
your-project/
├── README.md           # Project documentation
├── main.py            # Main script
├── test_main.py       # Unit tests (optional)
└── requirements.txt   # Dependencies (if any)
```

### README Template for New Projects

```markdown
# Project Name

Brief description of what your project does.

## Features
- Feature 1
- Feature 2

## Requirements
- Python 3.x
- Dependencies (if any)

## Installation
\```bash
pip install -r requirements.txt
\```

## Usage
\```bash
python main.py
\```

## Example
Provide example usage or screenshots

## Author
Your name
```

## 🔄 Pull Request Process

### Step-by-Step Guide

1. **Sync your fork with upstream**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a new branch**
   ```bash
   git checkout -b add-your-feature
   ```

3. **Make your changes**
   - Write your code
   - Test thoroughly
   - Add documentation

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

   **Commit Message Format:**
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements
   - `Docs:` for documentation changes
   - `Test:` for adding tests

5. **Push to your fork**
   ```bash
   git push origin add-your-feature
   ```

6. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "Compare & pull request"
   - Fill in the PR template
   - Submit the PR

### PR Title Format

- **Good:** `Add: Password generator with strength indicator`
- **Good:** `Fix: Resolve IndexError in binary search`
- **Good:** `Docs: Add contributing guidelines`
- **Bad:** `Update`
- **Bad:** `Fixed stuff`
- **Bad:** `asdfgh`

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Code refactoring
- [ ] Testing

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe how you tested your changes.

## Screenshots (if applicable)
Add screenshots here.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have tested my code
- [ ] I have added documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests (if applicable)

## Related Issues
Closes #issue_number (if applicable)
```

## 🎃 Hacktoberfest Rules

### Official Requirements

To successfully complete Hacktoberfest 2025:

1. **Register at [hacktoberfest.com](https://hacktoberfest.com)** between October 1-31
2. **Submit 4 quality PRs** to public repositories
3. **PRs must be:**
   - Merged by maintainers, OR
   - Labeled `hacktoberfest-accepted`, OR
   - Approved and not closed within 7 days

### Quality Standards

❌ **Spam PRs will be labeled as `invalid` or `spam`**
- PRs that are automated
- PRs that are disruptive
- PRs with little to no value

✅ **Quality contributions include:**
- Meaningful code additions
- Bug fixes with tests
- Documentation improvements
- Feature implementations

### Review Timeline

- PRs are reviewed on a first-come, first-served basis
- Please be patient; maintainers review in their free time
- You can contribute to multiple issues/PRs

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** and inclusive
- **Be collaborative** and help others
- **Be patient** with reviews and feedback
- **Be constructive** in criticism
- **No harassment** or discrimination

### Getting Help

If you need help:

1. **Check existing issues** for similar problems
2. **Read the documentation** carefully
3. **Ask questions** in issue comments
4. **Be specific** about your problem

### Recognition

All contributors will be:
- Listed in the repository contributors
- Acknowledged in release notes
- Part of the Hacktoberfest community

## 📞 Contact

- **Create an issue** for bugs or feature requests
- **Start a discussion** for questions
- **Tag maintainers** for urgent matters

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as this project.

---

**Happy Hacking! 🚀**

Thank you for contributing to Python Hacktoberfest 2025! Your contributions help make this community better for everyone.

Remember: Quality over quantity! Focus on making meaningful contributions that add value to the project.

**#Hacktoberfest2025 #OpenSource #Python**
