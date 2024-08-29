import gensim
import numpy as np
from gensim.models import word2vec
from sklearn.metrics.pairwise import cosine_similarity

import itertools
import pandas as pd
import concurrent.futures
import os

class Corpus:
    """
    Preprocess text from abstracts.
    """

    def __init__(self, df):
        # Drop rows where 'abstract' is NaN or an empty string, then split the remaining abstracts
        self.sentences = [abstract.split() for abstract in df['abstract'].dropna() if abstract.strip()]

    def preprocess(self):
        return self.sentences



class Model:
    """
    Abstract base class for models.
    """

    def fit(self):
        """
        Fit the model.

        Note:
            This method should be overridden by a subclass.
        """
        raise NotImplementedError

    def save(self, filename):
        """
        Save the model to a file.

        Parameters:
            filename: The path of the file to save the model.

        Note:
            This method should be overridden by a subclass.
        """
        raise NotImplementedError

    @classmethod
    def load(cls, filename):
        """
        Load a model from a file.

        Parameters:
            filename: The path of the file to load the model from.

        Returns:
            The loaded model.

        Note:
            This method should be overridden by a subclass.
        """
        raise NotImplementedError

    def __getitem__(self, key):
        """
        Get an item from the model.

        Parameters:
            key: The key of the item to get.

        Note:
            This method should be overridden by a subclass.
        """
        raise NotImplementedError


from gensim.models import word2vec

class Word2VecModel:
    """
    Class representing a Word2Vec model.
    """

    def __init__(self, sentences):
        """
        Initialize the Word2VecModel with sentences.

        Parameters:
            sentences: The sentences to train the model on.
        """
        self.sentences = sentences
        self.model = None

    def fit(self, sg=1, vector_size=200, hs=1, window=5, min_count=1, workers=4):
        """
        Fit the Word2Vec model to the sentences.

        Parameters:
            sg: Training algorithm: 1 for skip-gram; otherwise CBOW.
            vector_size: Dimensionality of the word vectors.
            hs: If 1, hierarchical softmax will be used for model training.
            window: The maximum distance between the current and predicted word within a sentence.
            min_count: Ignores all words with total frequency lower than this.
            workers: The number of worker threads to train the model.
        """
        self.model = word2vec.Word2Vec(
            self.sentences,
            sg=sg,
            vector_size=vector_size,
            hs=hs,
            window=window,
            min_count=min_count,
            workers=workers,
        )

    def save(self, filename):
        """
        Save the Word2Vec model to a file.

        Parameters:
            filename: The path of the file to save the model.
        """
        self.model.save(filename)

    @classmethod
    def load(cls, filename):
        """
        Load a Word2Vec model from a file.

        Parameters:
            filename: The path of the file to load the model from.

        Returns:
            The loaded Word2Vec model.
        """
        instance = cls.__new__(cls)
        instance.model = gensim.models.Word2Vec.load(filename)
        return instance

    def __getitem__(self, key):
        """
        Get a word vector from the Word2Vec model.

        Parameters:
            key: The word to get the vector of.

        Returns:
            The word vector.
        """
        return self.model.wv.__getitem__(key)

    def most_similar(self, word_or_vec, topn=10):
        """
        Calculate the similarity between a word and the topn most similar
        words.

        Parameters:
            word_or_vec: The word or vector to calculate the similarity of.
            topn: The number of most similar words to return.

        Returns:
            list: A list of tuples containing the most similar words and their
                similarity scores.
        """
        return self.model.wv.most_similar(word_or_vec, topn=topn)


class VectorOperations:
    """
    A utility class containing static methods for various operations related
    to vectors, specifically focused on processing chemical formulas and
    generating corresponding vectors.

    The class provides methods to split chemical formulas, generate vectors
    for materials based on their formulas, and obtain vectors for words or phrases.
    """

    @staticmethod
    def split_chemical_formula(word: str) -> list:
        """
        Splits a chemical formula into its constituent elements and their counts.

        For example, the formula 'H2O' would be split into [('H', 2), ('O', 1)].

        Parameters:
            word (str): The chemical formula to split.

        Returns:
            list: A list of tuples where each tuple contains an element
                  from the formula and its count.
        """
        elements_counts = []
        i = 0
        while i < len(word):
            char = word[i]
            if char.isupper():
                j = i + 1
                while j < len(word) and word[j].islower():
                    j += 1
                element = word[i:j]
                i = j
                count = ""
                while i < len(word) and (
                    word[i].isdigit() or word[i] == "." or word[i] == "-"
                ):
                    count += word[i]
                    i += 1
                count = float(count) if count else 1
                elements_counts.append((element, count))
        return elements_counts

    @staticmethod
    def generate_material_vector(formula: str, model) -> np.ndarray:
        """
        Generate a vector representation for a material based on its chemical formula.

        The resultant vector for a formula like 'H2O' would be composition-weighted,
        i.e., weighted twice for 'H' and once for 'O'.

        The mathematical representation is:
            V = Σ(C_i * v_i) / N
        where:
            - C_i: the count of the i-th element in the formula.
            - v_i: the vector representation of the i-th element
                   from the word2vec model.
            - N: the total number of elements in the formula.

        Parameters:
            formula (str): The chemical formula of the material.
            model (gensim.models.Word2Vec): The word2vec model to use for vector
            generation.

        Returns:
            numpy.ndarray: The generated vector for the given formula.
        """
        elements_counts = VectorOperations.split_chemical_formula(formula)
        multiplied_vectors = []
        for element, count in elements_counts:
            element_vec = model.__getitem__(element.lower())
            percentage = count / 100
            multiplied_vector = element_vec * percentage
            multiplied_vectors.append(multiplied_vector)
        material_vec = np.mean(multiplied_vectors, axis=0)
        return material_vec

    @staticmethod
    def get_vector(word_or_phrase: str, model) -> np.ndarray:
        """
        Obtain the vector representation for a word or a phrase.

        If a phrase is provided, the function computes the mean vector representation
        of all the words in the phrase.

        Parameters:
            word_or_phrase (str): The word or phrase for which the vector is needed.
            model: The word2vec model to retrieve the vector from.

        Returns:
            numpy.ndarray: The vector representation of the given word or phrase.
        """
        return np.mean([model.__getitem__(w) for w in word_or_phrase.split()], axis=0)

    @staticmethod
    def generate_property_vectors(property_list: list, model) -> list:
        """
        Generate vectors for a list of properties.

        The function computes vectors for each property in the list using the
        provided word2vec model.

        Parameters:
            property_list (list): A list of properties for which vectors are required.
            model: The word2vec model to use for vector generation.

        Returns:
            list: A list of vectors corresponding to the provided properties.
        """
        return [VectorOperations.get_vector(p, model) for p in property_list]


class MaterialListGenerator:
    def __init__(self, elements_ranges, max_workers=4, combinations_per_batch=4, save_path='./'):
        self.elements_ranges = elements_ranges
        self.max_workers = max_workers
        self.combinations_per_batch = combinations_per_batch
        self.save_path = save_path
        self.log_file = os.path.join(save_path, 'processed_combinations.log')

        os.makedirs(self.save_path, exist_ok=True)

    def load_processed_combinations(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                processed_combinations = set(line.strip() for line in file)
        else:
            processed_combinations = set()
        return processed_combinations

    def log_processed_combination(self, element_combo):
        with open(self.log_file, 'a') as file:
            file.write("_".join(sorted(element_combo)) + '\n')

    def generate_valid_combinations(self, elements, target_sum=100, partial=[]):
        if len(elements) == 1:
            if 1 <= target_sum <= 99:
                yield partial + [target_sum]
            return

        element, rest = elements[0], elements[1:]
        for i in range(1, 100):
            if target_sum - i > 0:
                yield from self.generate_valid_combinations(rest, target_sum - i, partial + [i])

    def save_to_csv(self, element_combo, valid_combinations):
        if not valid_combinations:
            return

        material_df = pd.DataFrame(valid_combinations, columns=element_combo)
        elements_in_combinations = "_".join(sorted(element_combo))
        filename = os.path.join(self.save_path, f'{elements_in_combinations}_material_system.csv')
        material_df.to_csv(filename, index=False)

    def process_combination(self, element_combo):
        elements_in_combinations = "_".join(sorted(element_combo))
        if elements_in_combinations in self.processed_combinations:
            return

        valid_combinations = list(self.generate_valid_combinations(element_combo))
        self.save_to_csv(element_combo, valid_combinations)
        self.log_processed_combination(element_combo)
        self.processed_combinations.add(elements_in_combinations)

    def generate_and_save_all_combinations(self, element_range=(2, None)):
        min_elements, max_elements = element_range
        max_elements = max_elements or len(self.elements_ranges)

        element_combinations = [
            combo for num_elements in range(min_elements, max_elements + 1)
            for combo in itertools.combinations([e for e, r in self.elements_ranges], num_elements)
        ]

        self.processed_combinations = self.load_processed_combinations()

        for i in range(0, len(element_combinations), self.combinations_per_batch):
            batch = element_combinations[i:i + self.combinations_per_batch]
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(self.combinations_per_batch, len(batch))) as executor:
                list(executor.map(self.process_combination, batch))



class MaterialSimilarityCalculator:
    """
    Computes similarity scores between materials based on their vector representations.

    This class utilizes a Word2Vec model to represent materials as vectors and
    then calculates their similarity to target materials or properties.
    """

    def __init__(self, model, property_list=None):
        """
        Initialize the MaterialSimilarityCalculator with a model and property vectors.

        Parameters:
            model (gensim.models.Word2Vec): The word2vec model for generating vector
                                            representations.

            property_list (list, optional): A list of properties for which vectors
                                            are pre-generated. Defaults to None.
        """
        self.model = model
        if property_list is not None:
            self.property_vectors = VectorOperations.generate_property_vectors(
                property_list, self.model
            )
        else:
            self.property_vectors = None

    def _calculate_similarity_vectors(self, material_list):
        """
        Calculate similarity vectors for a list of materials.

        Parameters:
            material_list (list): A list of materials for which similarity vectors
                                  are to be calculated.

        Returns:
            dict: A dictionary mapping each material in the list to its similarity
                  vector. If property_vectors is None, returns the material vectors
                  in their original dimensions.
        """
        material_vectors = [
            VectorOperations.generate_material_vector(material, self.model)
            for material in material_list
        ]

        if self.property_vectors is not None:
            # Calculate similarity vectors by projecting material vectors to the property dimensions
            similarity_vectors = [
                cosine_similarity([material_vector], self.property_vectors)[0]
                for material_vector in material_vectors
            ]
        else:
            # Return the material vectors in their original dimensions if property_vectors is None
            similarity_vectors = material_vectors

        return dict(zip(material_list, similarity_vectors))

    def find_top_similar_materials(self, target_material, material_list, top_n=10):
        """Find the top-n materials most similar to the target material.

        This method calculates the cosine similarity between the
        target material and materials from the provided list and then
        returns the top-n most similar ones.

        Parameters:
            target_material (str): The name of the target material.
            material_list (list): List of materials to compare against the target.
            top_n (int, optional): Number of top materials to return. Default is 10.

        Returns:
            list: List of tuples containing the top-n similar materials and their
                  respective similarity scores.
        """
        material_similarity_vectors = self._calculate_similarity_vectors(material_list)
        material_list = list(material_similarity_vectors.keys())
        target_vec = VectorOperations.generate_material_vector(target_material,
                                                               self.model)

        if self.property_vectors is not None:
            # If property vectors are available, project the target vector into this space
            target_sim_to_properties = cosine_similarity(
                [target_vec], self.property_vectors
            )[0]
            new_target_vec = target_sim_to_properties
        else:
            # If no property vectors, use the target vector as is
            new_target_vec = target_vec

        new_material_vectors = np.array(list(material_similarity_vectors.values()))

        similarities_to_new_target = cosine_similarity(
            new_material_vectors, [new_target_vec]
        ).flatten()
        top_material_indices = similarities_to_new_target.argsort()[-top_n:][::-1]

        top_materials_with_similarity = [
            (material_list[i], similarities_to_new_target[i])
            for i in top_material_indices
        ]

        # Optionally, you could remove the print statements to clean up the output
        print("Top", top_n, "similar materials:")
        for material, similarity in top_materials_with_similarity:
            print(f"{material}: {similarity:.4f}")

        return top_materials_with_similarity

    def calculate_similarity_from_dataframe(
        self,
        df,
        element_columns,
        target_material=None,
        target_property=None,
        target_vec=None,
        percentages_as_decimals=False,
        experimental_indicator_column="Resistance",
        experimental_indicator_func=lambda x: 1 / x,
        add_experimental_indicator=True
    ):

        """Calculate similarity scores for materials in a DataFrame
        compared to a target material.

        This method computes the cosine similarity between each
        material in the DataFrame and the target material. The
        resulting similarity scores are added to the DataFrame.

        Parameters:
            df (pd.DataFrame): DataFrame containing materials and their properties.

            element_columns (list): List of column names in the DataFrame representing
                                    the elements.

            target_material (str): The name of the target material.

            target_property (str, optional): The name of the target property to compare

            target_vec (np.ndarray, optional): The vector representation of the target


            percentages_as_decimals (bool, optional): Whether the percentages in the
                                                      DataFrame are given as decimals.
                                                      Default is False.

            experimental_indicator_column (str, optional): Name of the column used to
                                                           compute the
                                                           'Experimental_Indicator'.
                                                           Default is 'Resistance'.

            experimental_indicator_func (function, optional): Function to compute the
                                                              'Experimental_Indicator'
                                                              value. Default is inverse
                                                              function.
            add_experimental_indicator (bool, optional): Whether to add the experimental
                                                         indicator column to the
                                                         dataframe. Default is True.




        Returns:
            pd.DataFrame or list: If top_n is None, returns DataFrame with similarity
                                  scores. Otherwise, returns list of top-n similar
                                  materials with their scores.

        """

        if target_vec is not None:
            if not isinstance(target_vec, np.ndarray):
                raise TypeError("target_vec must be a numpy array")

            if self.property_vectors is not None:
                target_vec = cosine_similarity(
                    [target_vec], self.property_vectors
                )[0]

        elif target_material is not None:
            target_vec = VectorOperations.generate_material_vector(target_material,
                                                                   self.model)
            if self.property_vectors is not None:
                target_vec = cosine_similarity(
                    [target_vec], self.property_vectors
                )[0]

        elif target_property is not None:
            target_vec = VectorOperations.generate_property_vectors(target_property,
                                                                    self.model)[0]
            if self.property_vectors is not None:
                target_vec = cosine_similarity(
                    [target_vec], self.property_vectors
                )[0]
        else:
            raise ValueError("Either target_material or target_vec or target_property "
                             "must be provided")

        # Convert percentages to decimals if needed
        if not percentages_as_decimals:
            df[element_columns] = df[element_columns].apply(lambda x: x / 100)

        # Vectorized calculation of material vectors
        material_vecs = np.zeros((len(df), len(self.model[element_columns[0].lower()])))
        for element in element_columns:
            material_vecs += np.array(
                [self.model[element.lower()]] * df[element].values.reshape(-1, 1))

        material_vecs /= len(element_columns)

        # Handle absence of property_vectors
        if self.property_vectors is not None:
            # Calculate material vector to properties similarities
            material_vecs= cosine_similarity(
                material_vecs, self.property_vectors
            )

        similarity_scores = cosine_similarity(material_vecs,
                                                  [target_vec]
                                              ).flatten()

        df["Similarity"] = similarity_scores
        df["Material_Vec"] = list(material_vecs)

        # Add the experimental indicator if required
        if add_experimental_indicator and experimental_indicator_column in df.columns:
            df["Experimental_Indicator"] = experimental_indicator_func(
                df[experimental_indicator_column])

        return df

    def calculate_similarity_to_list(
        self, material_list, target_words=None, target_materials=None
    ):
        """Compute similarity scores between a list of materials and
        target words/materials.

        This method calculates the cosine similarity between each
        material in the list and a given set of target words or
        materials. The method then returns the resulting similarity
        scores.

        Parameters:
            material_list (list): List of materials to compute similarity scores for.

            target_words (list, optional): List of target words or phrases to compare
                                           against.

            target_materials (list, optional): List of target materials to compare
                                               against.

        Returns:
            list: List of similarity scores corresponding to each material in the
                  `material_list`.

        """
        target_vectors = []
        if target_words:
            word_vectors = [
                VectorOperations.get_vector(word, self.model) for word in target_words
            ]
            if self.property_vectors is not None:
                word_vectors = [
                    cosine_similarity([word_vector], self.property_vectors)[0]
                    for word_vector in word_vectors
                ]
            target_vectors.extend(word_vectors)
        if target_materials:
            target_material_vectors = [
                VectorOperations.generate_material_vector(material, self.model)
                for material in target_materials
            ]
            if self.property_vectors is not None:
                target_material_vectors = [
                    cosine_similarity([target_material_vector],
                                      self.property_vectors)[0]
                    for target_material_vector in target_material_vectors
                ]
            target_vectors.extend(target_material_vectors)

        average_target_vector = np.mean(target_vectors, axis=0)

        material_vectors = [
            VectorOperations.generate_material_vector(material, self.model)
            for material in material_list
        ]
        if self.property_vectors is not None:
            material_vectors = [
                cosine_similarity([material_vector], self.property_vectors)[0]
                for material_vector in material_vectors
            ]

        similarity_scores = [
            cosine_similarity([material_vector], [average_target_vector])[0][0]
            for material_vector in material_vectors
        ]

        return similarity_scores
