# test_detector.py

import unittest
from irrelevant_content_detection import (
    detect_irrelevant_contents, 
    clean_irrelevant_contents,
    detect_irrelevant_html,
    clean_irrelevant_html
)

class TestIrrelevantContentDetection(unittest.TestCase):
    
    def test_detect_irrelevant_contents(self):
        texts = [
            "Python is a programming language.",
            "Python is great for data science.",
            "This text is not relevant.",
            "Machine learning with Python is fun.",
            "Unrelated text here."
        ]
        
        irrelevant_texts = detect_irrelevant_contents(texts)
        print('irrelevant texts : ', str(irrelevant_texts))
        self.assertIn("This text is not relevant.", irrelevant_texts)
        self.assertIn("Unrelated text here.", irrelevant_texts)

    def test_clean_irrelevant_contents(self):
        texts = [
            "Python is a programming language.",
            "Python is great for data science.",
            "This text is not relevant.",
            "Machine learning with Python is fun.",
            "Unrelated text here."
        ]
        
        cleaned_texts = clean_irrelevant_contents(texts)
        print('cleaned texts :' ,str(cleaned_texts))
        self.assertNotIn("This text is not relevant.", cleaned_texts)
        self.assertNotIn("Unrelated text here.", cleaned_texts)

    def test_clean_irrelevant_html(self):
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
        print(' clean irrelevant html:',cleaned_html)
        self.assertNotIn("This text is not relevant.", cleaned_html)
        self.assertNotIn("Unrelated text here.", cleaned_html)

    def test_detect_irrelevant_html(self):
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
        
        irrelevant_texts = detect_irrelevant_html(html)
        print(' detect irreelvant html:',irrelevant_texts)
        self.assertIn("This text is not relevant.", irrelevant_texts)
        self.assertIn("Unrelated text here.", irrelevant_texts)


  
if __name__ == "__main__":
    unittest.main()
