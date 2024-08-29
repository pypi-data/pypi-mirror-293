# detector.py

from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from bs4 import BeautifulSoup

def calculate_relevance_scores(texts: List[str]) -> np.ndarray:
    """
    Metin dizisi için TF-IDF vektörlerini hesaplar.
    :param texts: Metin dizisi
    :return: TF-IDF matrisini döner
    """
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    X = X.toarray()
    return X

def detect_irrelevant_contents(texts: List[str]) -> List[str]:
    """
    Alakasız metinleri tespit eder.
    :param texts: Metin dizisi
    :return: Alakasız metinleri içeren liste
    """
    X = calculate_relevance_scores(texts)
    
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    labels = kmeans.labels_
    
    # Küme boyutlarına göre hangi kümenin alakasız olduğunu belirle
    cluster_sizes = np.bincount(labels)
    irrelevant_cluster = np.argmin(cluster_sizes)
    
    irrelevant_texts = [texts[i] for i in range(len(texts)) if labels[i] == irrelevant_cluster]
    
    return irrelevant_texts

def clean_irrelevant_contents(texts: List[str]) -> List[str]:
    """
    Alakasız metinleri temizler.
    :param texts: Metin dizisi
    :return: Alakasız metinlerin çıkarıldığı temiz metin dizisi
    """
    X = calculate_relevance_scores(texts)
    
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    labels = kmeans.labels_
    
    # Küme boyutlarına göre hangi kümenin alakasız olduğunu belirle
    cluster_sizes = np.bincount(labels)
    irrelevant_cluster = np.argmin(cluster_sizes)
    
    relevant_texts = [texts[i] for i in range(len(texts)) if labels[i] != irrelevant_cluster]
    
    return relevant_texts

def extract_text_from_html(html: str) -> List[str]:
    """
    Verilen HTML yapısından metinleri çıkarır ve bir liste döner.
    :param html: HTML metni
    :return: Metin içeriğinin listesi
    """
    soup = BeautifulSoup(html, 'html.parser')
    texts = [element.strip() for element in soup.stripped_strings]
    
    return texts

def clean_irrelevant_html(html: str) -> str:
    """
    Verilen HTML yapısını alakasız içeriklerden temizler.
    :param html: HTML metni
    :return: Alakasız içeriklerden temizlenmiş HTML metni
    """
    soup = BeautifulSoup(html, 'html.parser')
    texts = extract_text_from_html(html)
    
    irrelevant_texts = detect_irrelevant_contents(texts)
    
    # Orijinal HTML yapısından alakasız olanları ve bunların etiketlerini temizle
    for element in soup.find_all(string=True):
        parent = element.parent
        if element.strip() in irrelevant_texts:
            parent.decompose()  # Etiketi ve içeriğini tamamen kaldır

    return str(soup)

def detect_irrelevant_html(html: str) -> List[str]:
    """
    Verilen HTML yapısı içerisindeki alakasız içerikleri tespit eder.
    :param html: HTML metni
    :return: Alakasız içeriklerin listesi
    """
    texts = extract_text_from_html(html)
    irrelevant_texts = detect_irrelevant_contents(texts)
    
    return irrelevant_texts
