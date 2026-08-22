# IMO Bench Python Library - Examples

This directory contains example scripts demonstrating how to use the IMO Bench Python library.

## Running Examples

Make sure you have installed the library first:

```bash
cd imobench-pylib
pip install -e .
```

## Available Examples

### Quick Start (`quickstart.py`)

Basic usage patterns for loading and working with IMO Bench datasets.

```bash
python examples/quickstart.py
```

**Topics covered:**
- Basic loading of datasets
- Filtering by category, subcategory, and level
- Category and subcategory analysis
- Working with ProofBench
- Efficient GradingBench processing with lazy loading
- Analyzing problem sources

### Advanced Usage (`advanced.py`)

More sophisticated patterns for working with the datasets.

```bash
python examples/advanced.py
```

**Topics covered:**
- Custom data directories
- Data validation and error handling
- Cross-dataset analysis
- Performance optimization techniques
- Statistical analysis
- Difficulty pattern analysis

## Common Patterns

### Loading Data

```python
from imobench import load_answerbench, load_proofbench, load_gradingbench

# Load all problems
problems = load_answerbench()

# Filter by category
algebra = load_answerbench(category="Algebra")

# Lazy loading for efficiency
for grading in load_gradingbench(lazy=True):
    process(grading)
```

### Custom Data Directory

```python
from imobench import IMOBenchLoader
from pathlib import Path

loader = IMOBenchLoader(data_dir=Path("/path/to/data"))
problems = loader.load_answerbench()
```

### Error Handling

```python
from imobench.exceptions import ValidationError, DataLoadError

try:
    problems = load_answerbench(validate=True)
except ValidationError as e:
    print(f"Invalid data: {e}")
except DataLoadError as e:
    print(f"Loading failed: {e}")
```

## Tips

1. **Use lazy loading** for GradingBench (186K entries) to avoid memory issues
2. **Disable validation** (`validate=False`) for faster loading if data is trusted
3. **Filter early** using built-in parameters rather than loading everything
4. **Use type hints** to get IDE autocomplete and type checking

## More Information

See the main [README.md](../README.md) for complete API documentation.
