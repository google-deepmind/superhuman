# Contributing to IMO Bench Python Library

Thank you for your interest in contributing to the IMO Bench Python library!

## Repository Structure

This library (`imobench-pylib`) is part of the larger [Superhuman Reasoning](https://github.com/google-deepmind/superhuman) repository by Google DeepMind.

## Types of Contributions

### Bug Reports

If you find a bug, please open an issue with:
- Clear description of the problem
- Minimal reproducible example
- Expected vs actual behavior
- Python version and environment details
- Relevant error messages and stack traces

### Feature Requests

For new features:
- Describe the use case
- Explain why it would benefit users
- Provide example API usage if possible

### Code Contributions

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/superhuman.git
   cd superhuman/imobench-pylib
   ```

2. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**
- Follow existing code style
   - Use type hints
   - Add docstrings
   - Keep functions focused and testable

5. **Write Tests**
   ```bash
   # Add tests in tests/
   pytest tests/
   ```

6. **Check Code Quality**
   ```bash
   # Format code
   black src/ tests/
   
   # Type checking
   mypy src/
   
   # Linting
   ruff check src/ tests/
   ```

7. **Run All Tests**
   ```bash
   pytest tests/ -v --cov=imobench
   ```

8. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   git push origin feature/your-feature-name
   ```

9. **Open a Pull Request**
   - Describe your changes clearly
   - Link any related issues
   - Ensure CI passes

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable names

### Testing

- Write tests for new functionality
- Maintain or improve test coverage
- Test edge cases and error conditions
- Use pytest fixtures for common setup

### Documentation

- Add docstrings to all public functions/classes
- Update README if adding new features
- Add examples for new functionality
- Keep docstrings clear and concise

### Type Hints

```python
from typing import Optional, List

def load_data(
    category: Optional[str] = None,
    validate: bool = True
) -> List[Problem]:
    """Load problems with optional filtering.
    
    Args:
        category: Filter by category
        validate: Enable validation
    
    Returns:
        List of Problem objects
    """
    pass
```

## Project Structure

```
imobench-pylib/
├── src/imobench/          # Source code
│   ├── __init__.py        # Public API
│   ├── types.py           # Type definitions
│   ├── loader.py          # Data loading
│   ├── validators.py      # Validation logic
│   └── exceptions.py      # Custom exceptions
├── tests/                 # Test suite
├── examples/              # Usage examples
├── docs/                  # Documentation
└── setup.py              # Package configuration
```

## Commit Message Guidelines

Use clear, descriptive commit messages:

- `Add: new feature or functionality`
- `Fix: bug fix`
- `Update: modify existing functionality`
- `Refactor: code restructuring`
- `Docs: documentation changes`
- `Test: add or modify tests`
- `Chore: maintenance tasks`

Example:
```
Add: lazy loading support for gradingbench

- Implement iterator-based loading
- Add lazy parameter to load_gradingbench()
- Update tests and documentation
```

## Questions?

For questions about:
- **Library usage**: Open a GitHub issue
- **Dataset content**: See main repository
- **Research paper**: Check IMO Bench website

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
