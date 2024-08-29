
# Irrelevant Content Detection

Irrelevant Content Detection is a Python package for detecting and cleaning irrelevant content from text and HTML. It leverages machine learning techniques such as TF-IDF and KMeans clustering to identify and remove non-relevant information from documents.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Calculate Relevance Scores](#calculate-relevance-scores)
  - [Detect Irrelevant Content in Text](#detect-irrelevant-content-in-text)
  - [Clean Irrelevant Content from Text](#clean-irrelevant-content-from-text)
  - [Extract Text from HTML](#extract-text-from-html)
  - [Detect Irrelevant Content in HTML](#detect-irrelevant-content-in-html)
  - [Clean Irrelevant Content from HTML](#clean-irrelevant-content-from-html)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install the package using pip:

```bash
pip install irrelevant-content-detection
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/berkbirkan/irrelevant-content-detection.git
cd irrelevant-content-detection
pip install .
```

## Usage

The package provides several functions to detect and clean irrelevant content from text and HTML.

### Calculate Relevance Scores

The `calculate_relevance_scores` function calculates the TF-IDF scores for a list of texts.

```python
from irrelevant_content_detection import calculate_relevance_scores

texts = [
    "Python is a programming language.",
    "This text is not relevant."
]

tfidf_scores = calculate_relevance_scores(texts)
print(tfidf_scores)
```

### Detect Irrelevant Content in Text

The `detect_irrelevant_contents` function detects irrelevant content from a list of texts.

```python
from irrelevant_content_detection import detect_irrelevant_contents

texts = [
    "Python is a programming language.",
    "Python is great for data science.",
    "This text is not relevant.",
    "Machine learning with Python is fun.",
    "Unrelated text here."
]

irrelevant_texts = detect_irrelevant_contents(texts)
print(irrelevant_texts)
```

### Clean Irrelevant Content from Text

The `clean_irrelevant_contents` function removes irrelevant content from a list of texts.

```python
from irrelevant_content_detection import clean_irrelevant_contents

texts = [
    "Python is a programming language.",
    "Python is great for data science.",
    "This text is not relevant.",
    "Machine learning with Python is fun.",
    "Unrelated text here."
]

cleaned_texts = clean_irrelevant_contents(texts)
print(cleaned_texts)
```

### Extract Text from HTML

The `extract_text_from_html` function extracts all text from an HTML string.

```python
from irrelevant_content_detection import extract_text_from_html

html = """
<html>
    <body>
        <p>Python is a programming language.</p>
        <p>This text is not relevant.</p>
    </body>
</html>
"""

texts = extract_text_from_html(html)
print(texts)
```

### Detect Irrelevant Content in HTML

The `detect_irrelevant_html` function detects irrelevant content from an HTML string.

```python
from irrelevant_content_detection import detect_irrelevant_html

html = """
<html>
    <body>
        <p>Python is a programming language.</p>
        <p>Python is great for data science.</p>
        <p>This text is not relevant.</p>
        <p>Machine learning with Python is fun.</p>
        <p>Unrelated text here.</p>
    </body>
</html>
"""

irrelevant_html = detect_irrelevant_html(html)
print(irrelevant_html)
```

### Clean Irrelevant Content from HTML

The `clean_irrelevant_html` function removes irrelevant content from an HTML string.

```python
from irrelevant_content_detection import clean_irrelevant_html

html = """
<html>
    <body>
        <p>Python is a programming language.</p>
        <p>Python is great for data science.</p>
        <p>This text is not relevant.</p>
        <p>Machine learning with Python is fun.</p>
        <p>Unrelated text here.</p>
    </body>
</html>
"""

cleaned_html = clean_irrelevant_html(html)
print(cleaned_html)
```

## Testing

To run the tests, you can use `unittest` which is included in the Python Standard Library:

```bash
python -m unittest discover
```

Or you can run the test file directly:

```bash
python test_detector.py
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch with your feature or bugfix.
3. Commit your changes.
4. Push to your branch.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
