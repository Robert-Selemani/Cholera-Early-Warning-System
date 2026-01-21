# Contributing to Cholera Early Warning System

Thank you for your interest in contributing to the Climate-Informed Cholera Early Warning and Decision-Support Tool!

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the issue tracker
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

### Development Process

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/CholeraEarlyWarningSystem.git
   cd CholeraEarlyWarningSystem
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Make your changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

5. **Run tests**
   ```bash
   # Run all tests
   pytest tests/

   # Run with coverage
   pytest --cov=src tests/

   # Run code style checks
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Clear description of your changes"
   ```

7. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub

## Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for all functions and classes

### Example
```python
def calculate_risk_score(
    climate_data: pd.DataFrame,
    epi_data: pd.DataFrame
) -> float:
    """
    Calculate cholera risk score from climate and epidemiological data.

    Args:
        climate_data: DataFrame with climate variables
        epi_data: DataFrame with epidemiological data

    Returns:
        Risk score between 0 and 1
    """
    # Implementation
    pass
```

### Documentation
- Update README.md if adding features
- Add docstrings to new functions
- Update relevant documentation in docs/

### Testing
- Write unit tests for new functions
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Areas for Contribution

### High Priority
- Data processing pipelines for new data sources
- Machine learning model improvements
- Validation with real-world data
- Dashboard enhancements
- API endpoint development

### Medium Priority
- Additional visualization features
- Performance optimization
- Documentation improvements
- Integration with external systems

### Good First Issues
- Look for issues tagged "good first issue"
- Documentation updates
- Bug fixes
- Code refactoring

## Data Contribution

If you have access to relevant data:
- Contact the maintainers first
- Ensure data sharing complies with privacy regulations
- Document data sources and collection methods
- Provide metadata and data dictionaries

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Prioritize public health impact

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or inflammatory comments
- Publishing others' private information
- Other unprofessional conduct

## Questions?

- Open an issue for technical questions
- Email the maintainers for sensitive matters
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Contributors will be acknowledged in:
- README.md
- CONTRIBUTORS.md
- Academic publications (for significant contributions)

Thank you for helping improve cholera early warning systems!
