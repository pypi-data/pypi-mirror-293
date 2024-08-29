import math

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from sklearn import manifold
from sklearn.manifold import TSNE
from scipy.spatial.distance import cdist

from matnexus.VecGenerator import VectorOperations

class Word2VecVisualizer:
    """
    Class for visualizing word embeddings using Word2Vec model.
    """

    def __init__(self, model):
        """
        Initialize the Word2VecVisualizer.

        Parameters:
            model: Pre-trained Word2Vec model used for generating word embeddings.
        """
        self.model = model
        self.property_vectors = None
        self.word_vectors = None
        self.data = None

    def collect_similar_words(self, word, level, top_n_similar, collected=None):
        if collected is None:
            collected = set()  # Initialize a set to keep track of collected words

        if level == 0:
            if word not in collected:
                collected.add(word)
                return [(word, 0)]  # Base word at level 0
            else:
                return []  # Skip if the word is already collected
        else:
            if word not in collected:
                collected.add(word)
                collected_words = [(word, 0)]  # Base word always at level 0
            else:
                collected_words = []

            # Collect similar words at the current level
            similar_words = self.model.model.wv.similar_by_word(word,
                                                                topn=top_n_similar)
            for sim_word, _ in similar_words:
                if sim_word not in collected:
                    # For each similar word, go deeper into the next level
                    deeper_words = self.collect_similar_words(sim_word, level - 1,
                                                              top_n_similar, collected)
                    # Update the level of these deeper words to the current level
                    deeper_words = [(w, l + 1) for w, l in deeper_words]
                    collected_words.extend(deeper_words)

            return collected_words

    def get_property_vectors(self, property_list):
        """
        Compute vectors for a list of properties using the Word2Vec model.

        Parameters:
            property_list (list): List of properties for which to compute vectors.

        Returns:
            list: Vectors corresponding to the given properties.
        """
        self.property_vectors = VectorOperations.generate_property_vectors(
            property_list, self.model
        )
        return self.property_vectors

    def get_words_data(self, property_list, level, top_n_similar):
        """
        Retrieve vectors and data for words related to given properties. This data will
        be used for visualization purposes.

        Parameters:
            property_list (list[str]): List of properties to retrieve related words for.
            level (int, optional): Depth of similarity levels to collect words from.
                Level 0 means only directly similar words to the property will be
                collected.
                Default is 0.
            top_n_similar (int, optional): Number of top similar words to consider at
                each level. Default is 30.

        Returns:
            tuple: A tuple containing the word vectors (numpy.ndarray) and a DataFrame
                with labels, levels, and words.
        """
        self.property_vectors = self.get_property_vectors(property_list)
        word_vectors = []
        word_labels = []
        word_levels = []
        exact_words = []
        distinct_words = set()

        for property_vec, property_name in zip(self.property_vectors, property_list):
            first_level_similar_words = self.model.model.wv.similar_by_vector(
                property_vec, topn=top_n_similar
            )
            for word, similarity in first_level_similar_words:
                words = self.collect_similar_words(word, level, top_n_similar)
                for word_2, word_level in words:
                    if word_2 not in distinct_words:
                        word_vectors.append(self.model.model.wv[word_2])
                        word_labels.append(property_name)
                        word_levels.append(word_level)
                        exact_words.append(word_2)
                        distinct_words.add(word_2)

        self.word_vectors = np.array(word_vectors)

        self.data = pd.DataFrame(
            {
                "label": word_labels,
                "level": word_levels,
                "word": exact_words,
            }
        )
        return self.word_vectors, self.data

    def plot_2d(
        self,
        coordinates,
        property_list,
        width=720,
        height=576,
        marker_size=5,
        textfont_size=10,
        legendfont_size=10,
        axisfont_size=10,
        tickfont_size=10,
        scale_factor=1,
        margin=dict(r=150),
    ):
        """Generate a 2D scatter plot of word embeddings.

        Parameters:

            coordinates (numpy.ndarray): 2D array of x, y coordinates for
                                         each word.

            property_list (list[str]): List of properties to label the words by.

            width (int, optional): Width of the plot. Default is 720.

            height (int, optional): Height of the plot. Default is 576.

            marker_size (int, optional): Size of the markers. Default is 5.

            textfont_size (int, optional): Size of the text font. Default is 10.

            legendfont_size (int, optional): Size of the legend font. Default is 10.

            axisfont_size (int, optional): Size of the axis font. Default is 10.

            tickfont_size (int, optional): Size of the tick font. Default is 10.

            scale_factor (float, optional): Factor to scale the plot sizes
                                            Default is 1.0.

            margin (dict, optional): Margins for the plot. Default is a right margin
                                     of 150.

        Returns:
            plotly.graph_objs._figure.Figure: A 2D scatter plot of the word embeddings.

        """
        width *= scale_factor
        height *= scale_factor
        marker_size *= scale_factor
        textfont_size *= scale_factor
        legendfont_size *= scale_factor
        axisfont_size *= scale_factor
        tickfont_size *= scale_factor

        fig = go.Figure()
        custom_color_list = (
            px.colors.qualitative.Plotly
            + px.colors.qualitative.D3
            + px.colors.qualitative.G10
        )
        shape_list = [
            "circle",
            "square",
            "diamond",
            "cross",
            "x",
            "triangle-up",
            "triangle-down",
            "triangle-left",
            "triangle-right",
            "pentagon",
            "hexagon",
            "star",
            "hexagram",
            "star-triangle-up",
            "star-triangle-down",
            "star-square",
            "star-diamond",
            "diamond-tall",
            "diamond-wide",
            "hourglass",
            "bowtie",
        ]
        num_levels = self.data["level"].max() + 1

        for label, color in zip(property_list, custom_color_list):
            subset = self.data[self.data["label"] == label]
            for level, shape in zip(range(num_levels), shape_list[:num_levels]):
                level_subset = subset[subset["level"] == level]
                hovertext = [
                    f"{label} - Word: {row.word} - Level: {row.level}"
                    for _, row in level_subset.iterrows()
                ]

                fig.add_trace(
                    go.Scatter(
                        x=coordinates[level_subset.index, 0],
                        y=coordinates[level_subset.index, 1],
                        mode="markers",
                        name=f"{label} - Level {level}",
                        marker=dict(color=color, size=marker_size, symbol=shape),
                        text=hovertext,
                        hoverinfo="text",
                        textfont=dict(size=textfont_size),
                        hoverlabel=dict(font_size=textfont_size),
                    )
                )

        fig.update_layout(
            margin=margin,
            title=None,
            width=width,
            height=height,
            legend_font_size=legendfont_size,
            xaxis=dict(
                title_text="t-SNE Dimension 1",
                title_font_size=axisfont_size,
                tickfont_size=tickfont_size,
            ),
            yaxis=dict(
                title_text="t-SNE Dimension 2",
                title_font_size=axisfont_size,
                tickfont_size=tickfont_size,
            ),
        )

        return fig

    def plot_data(
            self,
            property_list,
            plot_method="t_sne",
            level=0,
            top_n_similar=1,
            width=720,
            height=576,
            marker_size=5,
            scale_factor=1,
            textfont_size=10,
            legendfont_size=10,
            axisfont_size=10,
            tickfont_size=10,
            margin=dict(r=150),
            **kwargs,
    ):
        """Visualize word embeddings in 2D using various
        dimensionality reduction techniques.

        Parameters:
            property_list (list[str]): List of properties to visualize
                                       related words for.

            plot_method (str, optional): The dimensionality reduction technique to use.
                                         Options are: 'isomap', 'md_scaling',
                                         'spectral', or 't_sne'. Default is 't_sne'.

            level (int, optional): Depth of similarity levels to collect words from.
                                   Default is 1.

            top_n_similar (int, optional): Number of top similar words to consider.
                                           Default is 30.

            width (int, optional): Width of the plot. Default is 720.

            height (int, optional): Height of the plot. Default is 576.

            marker_size (int, optional): Size of the markers. Default is 5.

            scale_factor (float, optional): Factor to scale the plot sizes.
                                            Default is 1.0.

            textfont_size (int, optional): Size of the text font. Default is 10.

            legendfont_size (int, optional): Size of the legend font. Default is 10.

            axisfont_size (int, optional): Size of the axis font. Default is 10.

            tickfont_size (int, optional): Size of the tick font. Default is 10.

            margin (dict, optional): Margins for the plot. Default is a right margin
                                     of 150.

            **kwargs: Additional keyword arguments for the dimensionality reduction
                      technique.

        Returns:
            plotly.graph_objs._figure.Figure: A 2D scatter plot of the word embeddings.

        """
        self.get_words_data(property_list, level=level, top_n_similar=top_n_similar)
        if plot_method == "isomap":
            isomap = manifold.Isomap(**kwargs)
            coordinates = isomap.fit_transform(self.word_vectors)
        elif plot_method == "md_scaling":
            md_scaling = manifold.MDS(**kwargs)
            coordinates = md_scaling.fit_transform(self.word_vectors)
        elif plot_method == "spectral":
            spectral = manifold.SpectralEmbedding(**kwargs)
            coordinates = spectral.fit_transform(self.word_vectors)
        elif plot_method == "t_sne":
            t_sne = manifold.TSNE(**kwargs)
            coordinates = t_sne.fit_transform(self.word_vectors)
        else:
            raise ValueError(
                "Invalid plot_method. Choose from 'isomap', "
                "'md_scaling', 'spectral', or 't_sne'."
            )

        return self.plot_2d(
            coordinates,
            property_list,
            width=width,
            height=height,
            marker_size=marker_size,
            textfont_size=textfont_size,
            legendfont_size=legendfont_size,
            axisfont_size=axisfont_size,
            tickfont_size=tickfont_size,
            scale_factor=scale_factor,
            margin=margin,
        )

    def plot_vectors(
            self,
            material_list=None,
            property_list=None,
            vecs=None,
            vec_labels=None,
            width=720,
            height=576,
            scale_factor=1,
            marker_size=15,
            textfont_size=5,
            legendfont_size=10,
            axisfont_size=10,
            tickfont_size=10,
            show_legend=True,
            random_state=42,
            **kwargs,
    ):
        """
        Plot a 2D scatter plot of material vectors using t-SNE.

        Parameters:
            material_list (list[str]): List of materials for which the vectors are
                                       to be plotted.
            property_list (list[str]): List of properties for which the vectors are
                                       to be plotted.
            vecs (list[numpy.ndarray], optional): List of custom vectors to plot.
            vec_labels (list[str], optional): List of labels for the custom vectors.
            width (int, optional): Width of the plot. Default is 720.

            height (int, optional): Height of the plot. Default is 576.

            scale_factor (float, optional): Factor to scale the plot sizes.
                                            Default is 1.0.

            marker_size (int, optional): Size of the markers. Default is 15.

            textfont_size (int, optional): Size of the text font. Default is 5.

            legendfont_size (int, optional): Size of the legend font. Default is 10.

            axisfont_size (int, optional): Size of the axis font. Default is 10.

            tickfont_size (int, optional): Size of the tick font. Default is 10.

            **kwargs: Additional keyword arguments for the t-SNE method.

        Returns:
            plotly.graph_objs._figure.Figure: A 2D scatter plot of the material vectors.
        """

        # Scale sizes
        width *= scale_factor
        height *= scale_factor
        marker_size *= scale_factor
        textfont_size *= scale_factor
        legendfont_size *= scale_factor
        axisfont_size *= scale_factor
        tickfont_size *= scale_factor

        vectors_to_plot = []
        labels = []

        if material_list:
            material_vectors = [
                VectorOperations.generate_material_vector(material, self.model)
                for material in material_list
            ]
            material_vectors = np.vstack(material_vectors)
            vectors_to_plot.append(material_vectors)
            labels.extend(material_list)

        if property_list:
            property_vectors = VectorOperations.generate_property_vectors(property_list,
                                                              self.model)
            property_vectors = np.vstack(property_vectors)
            vectors_to_plot.append(property_vectors)
            labels.extend(property_list)

        if vecs is not None:
            if not isinstance(vecs, list) or not all(
                    isinstance(vec, np.ndarray) for vec in vecs):
                raise ValueError("vecs must be a list of numpy arrays.")
            if vec_labels is not None and len(vecs) != len(vec_labels):
                raise ValueError("Every vec must have a corresponding label.")
            elif vec_labels is None:
                vec_labels = ['Custom Vector {}'.format(i) for i in
                              range(len(vecs))]

            for vec, label in zip(vecs, vec_labels):
                vectors_to_plot.append(
                    vec.reshape(1, -1))  # Ensure vec is correctly shaped
                labels.append(label)



        if not vectors_to_plot:
            raise ValueError("No vectors provided for plotting.")

        vectors_to_plot = np.vstack(vectors_to_plot)

        # Perform t-SNE dimensionality reduction
        tsne = TSNE(n_components=2, random_state=random_state, perplexity=2)
        vectors_2d = tsne.fit_transform(vectors_to_plot)

        # Create DataFrame for plotting
        df = pd.DataFrame(
            {"x": vectors_2d[:, 0], "y": vectors_2d[:, 1], "label":labels}
        )


        # Plotting logic remains the same as before
        custom_color_list = (
                px.colors.qualitative.Plotly
                + px.colors.qualitative.D3
                + px.colors.qualitative.G10
        )

        fig = px.scatter(
            df,
            x="x",
            y="y",
            color="label",
            text="label",
            width=width,
            height=height,
            color_discrete_sequence=custom_color_list,
        )




        fig.update_traces(
            textposition="middle center",
            marker_size=marker_size,
            textfont_size=textfont_size,
            hoverlabel=dict(font_size=textfont_size),
        )




        fig.update_layout(
            autosize=False,
            legend_title_text=None,
            showlegend=show_legend,
            legend_font_size=legendfont_size,
            xaxis=dict(
                title_text="t-SNE Dimension 1",
                title_font_size=axisfont_size,
                tickfont=dict(size=tickfont_size),
            ),
            yaxis=dict(
                title_text="t-SNE Dimension 2",
                title_font_size=axisfont_size,
                tickfont=dict(size=tickfont_size),
            ),
            **kwargs
        )

        return fig


    def plot_similarity_scatter(self, data_dict, elements, x_labels=None, y_labels=None, legend_labels=None, cmap_groups=None, element_scale_limits=None, nrows=None, ncols=None, subplot_labels=True):
        """
        Plot scatter plots showing the similarity of materials based on specified elements from multiple DataFrames.

        Parameters:
            data_dict (dict[str, pd.DataFrame]): Dictionary where keys are identifiers for DataFrames and values are the DataFrames containing the materials and their similarity scores.
            elements (list[tuple[str, list[str]]]): List of tuples where each tuple contains a DataFrame identifier and a list of elements to include in the plot.
                                                    Example: [('data1', ['ElementX', 'ElementY']), ('data2', ['ElementZ'])]
            x_labels (dict, optional): A dictionary mapping a common x-axis label to a list of elements.
                                       Example: {'Position X (unit)': ['ElementX', 'ElementY']}
            y_labels (dict, optional): A dictionary mapping a common y-axis label to a list of elements.
                                       Example: {'Position Y (unit)': ['ElementX', 'ElementY']}
            legend_labels (dict, optional): A dictionary mapping a common legend label to a list of elements.
                                            Example: {'Density (unit)': ['ElementX', 'ElementY']}
            cmap_groups (dict, optional): A dictionary where each key is a color map and the value is a list of columns that should use this color map.
                                          Example: {'plasma': ['Similarity', 'Exp1'], 'viridis': ['ElementX', 'ElementY']}
            element_scale_limits (dict, optional): A dictionary mapping each element to its (min, max) scale limit for color normalization.
                                                   Example: {'ElementX': (0.1, 0.9), 'ElementY': (0.2, 0.8)}
            nrows (int, optional): Number of rows in the subplot grid.
            ncols (int, optional): Number of columns in the subplot grid.
            subplot_labels (bool, optional): Whether to add subplot labels (a), (b), (c), etc. to each subplot. Default is True.

        Returns:
            matplotlib.figure.Figure: A scatter plot showing the similarity of materials.
        """
        if cmap_groups is None:
            cmap_groups = {}

        if element_scale_limits is None:
            element_scale_limits = {}

        if x_labels is None:
            x_labels = {}

        if y_labels is None:
            y_labels = {}

        if legend_labels is None:
            legend_labels = {}

        # Invert cmap_groups to map each element to its color map
        element_cmap = {el: cmap for cmap, els in cmap_groups.items() for el in els}

        # Count total number of elements to plot
        total_elements = sum(len(els) for _, els in elements)

        # Determine the number of rows and columns for the subplots if not provided
        if nrows is None or ncols is None:
            ncols = int(math.ceil(math.sqrt(total_elements)))
            nrows = int(math.ceil(total_elements / ncols))

        # Adjust figure size
        figsize = (ncols * 5, nrows * 4)

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

        # Handle case when there is only one subplot
        if total_elements == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        # Helper function to get label for an element
        def get_label(labels_dict, element):
            for label, elements in labels_dict.items():
                if element in elements:
                    return label
            return None

        # Subplot labels like (a), (b), (c), etc., if enabled
        if subplot_labels:
            subplot_labels_list = [f"({chr(97 + i)})" for i in range(total_elements)]

        plot_index = 0
        for df_id, element_list in elements:
            data = data_dict[df_id]
            for element in element_list:
                if plot_index < len(axes):
                    cmap = element_cmap.get(element, "viridis")  # Default to 'viridis' if not specified
                    vmin, vmax = element_scale_limits.get(element, (None, None))  # Get min/max scale limits

                    sc = axes[plot_index].scatter(data["x"], data["y"], c=data[element], cmap=cmap, vmin=vmin, vmax=vmax, marker="o", s=100)
                    axes[plot_index].set_title(element)  # Only show the element name as the title

                    # Set the x and y labels if provided
                    x_label = get_label(x_labels, element)
                    y_label = get_label(y_labels, element)
                    if x_label:
                        axes[plot_index].set_xlabel(x_label)
                    if y_label:
                        axes[plot_index].set_ylabel(y_label)

                    # Update colorbar to show what it represents and the unit if provided
                    legend_label = get_label(legend_labels, element)
                    if legend_label:
                        cbar = fig.colorbar(sc, ax=axes[plot_index])
                        cbar.set_label(legend_label)
                    else:
                        fig.colorbar(sc, ax=axes[plot_index])

                    # Add subplot label if enabled
                    if subplot_labels:
                        axes[plot_index].text(-0.1, 1.1, subplot_labels_list[plot_index], transform=axes[plot_index].transAxes, fontsize=16, fontweight='bold', va='top', ha='right')

                    plot_index += 1

        # Remove any unused axes if the number of elements is less than the number of subplots
        for i in range(plot_index, len(axes)):
            fig.delaxes(axes[i])

        plt.tight_layout()
        return fig
