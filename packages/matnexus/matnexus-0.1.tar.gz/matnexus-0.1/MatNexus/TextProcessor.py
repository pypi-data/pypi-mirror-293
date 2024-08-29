import re
from string import punctuation


import nltk
import pandas as pd
import spacy
from nltk.corpus import stopwords


class TextProcessor:
    """
    A class to preprocess textual data contained in a DataFrame.
    This class provides functionalities for filtering sentences, lemmatizing,
    and other preprocessing steps.

    Attributes:
        df (pd.DataFrame): Input DataFrame containing text data.
        nlp (spacy.lang): Spacy language model for lemmatization.
        processed_df (pd.DataFrame): DataFrame containing processed text data.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize a TextPreprocessor object.

        Parameters:
            df (pd.DataFrame): The input DataFrame containing text data.
        """
        self.df = df
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        self.processed_df = self.process_dataframe()

    def filter_sentences(self, s: str) -> str:
        """
        Filter sentences in the input string based on certain criteria.

        This method:
            1. Ensures uniform sentence delimiters, excluding decimal numbers.
            2. Removes sentences or parts of sentences containing "©" or "& Co.".

        Parameters:
            s (str): The input string to filter.

        Returns:
            str: The filtered string.
        """
        # Ensure uniform sentence delimiters, excluding decimal numbers
        s = re.sub(r'\.(?!\d)([^\s])', '. \\1', s)

        # Split sentences at period followed by a space
        sentences = s.split('. ')

        # Filter sentences
        filtered_sentences = []
        for sentence in sentences:
            # Check and remove any part containing "©" or "& Co."
            if "©" not in sentence and "& Co." not in sentence:
                filtered_sentences.append(sentence)
            else:
                parts = re.split(r'(©|& Co)', sentence)
                if parts and len(parts) > 1:
                    part_to_keep = ' '.join(
                        parts[:parts.index("©")] if "©" in parts else parts[
                                                                      :parts.index(
                                                                          "& Co.")])
                    if part_to_keep.strip():
                        filtered_sentences.append(part_to_keep)

        # Reconstruct the text
        return '. '.join(filtered_sentences).strip()

    def filter_words(self, s: str) -> str:
        """
        Filter words in the input string based on certain criteria, including
        identification and processing of chemical formulas.
        """

        # Split the sentences into words based on space to preserve formulas
        tokens = s.split()

        # Initialize stopwords set
        stop = set(stopwords.words("english"))

        # Initialize the filtered text list
        filter_text = []

        for word in tokens:
            # Clean word from punctuation if it's not a likely chemical formula
            if not self.is_chemical_formula(word):
                word = ''.join([char for char in word if char not in punctuation])

            # Remove stopwords, digits, and if the word is empty after cleaning
            if word.lower() in stop or word.isdigit() or not word:
                continue

            # Check if the word is a chemical formula and extract elements
            if self.is_chemical_formula(word):
                elements = self.extract_elements(word)
                # For Word2Vec, keeping original case for formulas
                filter_text.append(word)  # Keep original case for formulas
                filter_text.extend(elements)  # Add extracted elements, consider casing
            else:
                doc = self.nlp(word.lower())
                lemmatized = [token.lemma_ for token in doc][0]  # Assuming one word per doc
                filter_text.append(lemmatized)

        # Join the filtered words into a single string
        return " ".join(filter_text)

    @staticmethod
    def is_chemical_formula(word):
        """Check if the token likely represents a chemical formula."""
        # Adjusted to check for the presence of uppercase, lowercase, and digits
        return (any(char.isupper() for char in word) and
                any(char.islower() for char in word) and
                any(char.isdigit() for char in word))

    @staticmethod
    def extract_elements(word):
        """Extract element symbols from a token identified as a chemical formula."""
        periodic_table = [
            "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
            "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
            "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
            "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
            "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
            "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
            "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
            "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
            "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
            "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
            "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
            "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
            ]

        elements = set()
        potential_elements = re.findall(r'[A-Z][a-z]?', word)
        for element in potential_elements:
            if element in periodic_table:
                elements.add(element)
        return elements

    def process_dataframe(self) -> pd.DataFrame:
        """
        Process the input DataFrame with preprocessing steps including filtering and lemmatization.
        """
        processed_df = self.df.copy()
        processed_df["abstract"] = processed_df["abstract"].fillna("").apply(
            self.filter_sentences).apply(self.filter_words)

        return processed_df
