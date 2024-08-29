import pandas as pd
import math

def get_isonymy(surnames_i: pd.Series) -> float:
    """Retorna las isonímia interna de una población segun sus apellidos.

    Args:
        surnames_i (pd.Series): Apellidos de c/u de los miembros de una población

    Returns:
        float: Valor de la isonimia.
    """
    if not isinstance(surnames_i, pd.Series):
        raise TypeError(
            f"Argument must be a pandas Series. Type found: {type(surnames_i)}"
        )

    # get surname | count dataframe
    surnames_i.name = "surname"

    df_surnames_i = (
        surnames_i.value_counts()
        .reset_index()
        .rename(columns=dict(index="surname", surname="counts"))
    )

    df_surnames_i["relative_frequency"] = df_surnames_i["counts"] / len(surnames_i)
    df_surnames_i["relative_frequency_squared"] = (
        df_surnames_i["relative_frequency"] ** 2
    )

    isonymy_value = df_surnames_i["relative_frequency_squared"].sum()

    return isonymy_value


def get_unbiased_random_isonymy(population_surnames: pd.Series) -> float:
    """Calcula la isonimia interna de una población basada en los apellidos de sus miembros.

    La isonimia es una medida de consanguinidad dentro de una población que se basa en 
    la frecuencia de los apellidos.

    Args:
        population_surnames (pd.Series): Una serie de pandas que contiene los apellidos 
            de cada miembro de la población. Cada elemento es un apellido.

    Returns:
        float: El valor calculado de la isonimia para la población dada.

    Raises:
        ValueError: Si la serie está vacía o tiene menos de dos elementos.
    """
    if population_surnames.empty or len(population_surnames) < 2:
        raise ValueError("La población debe contener al menos dos apellidos.")

    # Crear un DataFrame con la frecuencia de cada apellido
    df_surnames = (
        population_surnames.value_counts()
        .reset_index()
        .rename(columns={'index': "surname", 'population_surnames': "frecuencia_abs"})
    )

    # Calcular el término de isonimia para cada apellido
    df_surnames["frecuencia_abs_menos_1"] = df_surnames["frecuencia_abs"] - 1
    df_surnames["producto_de_frecuencias"] = (
        df_surnames["frecuencia_abs"] * df_surnames["frecuencia_abs_menos_1"]
    )

    N = len(population_surnames)
    df_surnames["termino_isonimico"] = df_surnames["producto_de_frecuencias"] / (
        N * (N - 1)
    )

    # Sumar los términos para obtener la isonimia total
    isonymy_value = df_surnames["termino_isonimico"].sum()

    return isonymy_value

def get_distances(surnames_i: pd.Series, surnames_j: pd.Series) -> dict:
    """
    Calculates various isonymic distances between two lists of surnames.

    This function computes and returns a dictionary with the following distances 
    between two lists of surnames:
        
    - I_ij: Isonymy between groups i and j.
    - L_ij: Lasker distance between groups i and j.
    - E_ij: Euclidean distance between groups i and j.
    - N_ij: Nei distance between groups i and j.
    - I_ii: Internal isonymy of group i.
    - I_jj: Internal isonymy of group j.

    Args:
        surnames_i (pd.Series): Pandas series containing the surnames of group i.
        surnames_j (pd.Series): Pandas series containing the surnames of group j.

    Returns:
        dict: A dictionary with the calculated distances:
            - 'I_ij': float, Isonymy between i and j.
            - 'L_ij': float, Lasker distance between i and j.
            - 'E_ij': float, Euclidean distance between i and j.
            - 'N_ij': float, Nei distance between i and j.
            - 'I_ii': float, Internal isonymy in i.
            - 'I_jj': float, Internal isonymy in j.

    Raises:
        ValueError: If either group is empty.
    """

    if surnames_i.empty or surnames_j.empty:
        raise ValueError("Ambos grupos de apellidos deben contener elementos.")

    distance_dict = {
        "I_ii": None,
        "I_jj": None,
        "I_ij": None,
        "L_ij": None,
        "E_ij": None,
        "N_ij": None,
    }

    len_group_i = len(surnames_i)
    len_group_j = len(surnames_j)

    common_surnames = list(set(surnames_i) & set(surnames_j))

    group_i = (
        surnames_i[surnames_i.isin(common_surnames)]
        .value_counts()
        .reset_index()
        .rename(columns={'index': "surname", 'surnames_i': "counts_i"})
    )

    group_i["relative_frequency_i"] = group_i.counts_i / len_group_i

    group_j = (
        surnames_j[surnames_j.isin(common_surnames)]
        .value_counts()
        .reset_index()
        .rename(columns={'index': "surname", 'surnames_j': "counts_j"})
    )

    group_j["relative_frequency_j"] = group_j.counts_j / len_group_j

    assert len(group_i) == len(group_j)

    # Merge los dataframes por apellido:
    distances_df = pd.merge(group_i, group_j, on="surname")

    # Calcular la isonimia I_ij
    distances_df["product_of_frequencies"] = (
        distances_df.relative_frequency_i * distances_df.relative_frequency_j
    )
    distance_dict["I_ij"] = distances_df["product_of_frequencies"].sum()

    # Calcular la distancia de Lasker L_ij
    distance_dict["L_ij"] = -math.log(distance_dict["I_ij"])

    # Calcular la distancia Euclidiana E_ij
    distances_df["sqrt_product_of_frequencies"] = distances_df[
        "product_of_frequencies"
    ].apply(math.sqrt)
    distance_dict["E_ij"] = math.sqrt(
        1 - distances_df["sqrt_product_of_frequencies"].sum()
    )

    # Calcular la isonimia interna I_ii e I_jj
    distance_dict["I_ii"] = get_unbiased_random_isonymy(surnames_i)
    distance_dict["I_jj"] = get_unbiased_random_isonymy(surnames_j)

    # Calcular la distancia de Nei N_ij
    distance_dict["N_ij"] = -math.log(
        distance_dict["I_ij"] / math.sqrt(distance_dict["I_ii"] * distance_dict["I_jj"])
    )

    return distance_dict

def get_a_index(surnames_serie: pd.Series) -> float:
    """Returns the A index.
    
    The A index represents the percentage of the population that is the sole bearer of its surname.

    Args:
        surnames_serie (pd.Series): A pandas series containing surnames of the population.

    Returns:
        float: The A index, representing the percentage of unique surname bearers in the population.

    Raises:
        ValueError: If the input series is empty.
    """
    if surnames_serie.empty:
        raise ValueError("The surnames series must not be empty.")

    # Calculate the number of unique surname bearers
    singles = surnames_serie.value_counts() == 1
    unique_bearers = singles[singles].shape[0]

    # Return the A index, handling the potential division by zero
    return unique_bearers / surnames_serie.shape[0] if surnames_serie.shape[0] > 0 else 0


def get_b_index(surnames_serie: pd.Series, return_seven_list: bool = False) -> float or tuple:
    """Returns the B index.
    
    The B index represents the percentage of the population included in the seven most frequent surnames.

    Args:
        surnames_serie (pd.Series): A pandas series containing surnames of the population.
        return_seven_list (bool): If True, also returns the list of the seven most frequent surnames.

    Returns:
        float: The B index, representing the percentage of the population with the seven most frequent surnames.
        tuple: If return_seven_list is True, returns a tuple with the B index and the list of the seven most frequent surnames.

    Raises:
        ValueError: If the input series has fewer than 7 unique surnames.
    """
    if surnames_serie.nunique() < 7:
        raise ValueError("The surnames series must contain at least 7 unique surnames.")

    N = len(surnames_serie)
    seven_most_frequent = surnames_serie.value_counts().iloc[:7]
    sum_most_frequent = seven_most_frequent.sum()

    b_index = sum_most_frequent / N

    if return_seven_list:
        return b_index, seven_most_frequent
    else:
        return b_index

def get_occurrences_vs_frequencies(surnames_serie: pd.Series) -> pd.DataFrame:
    """Returns a dataset of occurrence-frequency based on the received surnames.

    This function generates a dataset that shows the relationship between the number of occurrences of surnames 
    and their respective frequencies, including the logarithmic transformation of these values.

    Args:
        surnames_serie (pd.Series): A pandas series containing the surnames of a population.

    Returns:
        pd.DataFrame: A dataframe with the following columns:
            - occurrences: The number of times a surname occurs.
            - frequency: The frequency of those occurrences.
            - frequency_log: The natural logarithm of the frequency.
            - occurrences_log: The natural logarithm of the occurrences.
    
    Raises:
        ValueError: If the input series is empty.
    """
    if surnames_serie.empty:
        raise ValueError("The surnames series must not be empty.")

    # Count the occurrences of each surname
    surname_counts = surnames_serie.value_counts()

    # Create a dataframe with occurrences
    occurrences_df = surname_counts.reset_index().rename(
        columns={"index": "surname", surnames_serie.name: "occurrences"}
    )

    # Calculate the frequency of each occurrence count
    occurrences_freq_df = (
        occurrences_df["occurrences"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "occurrences", "occurrences": "frequency"})
    )

    # Add logarithmic transformations
    occurrences_freq_df["frequency_log"] = occurrences_freq_df["frequency"].apply(math.log)
    occurrences_freq_df["occurrences_log"] = occurrences_freq_df["occurrences"].apply(math.log)

    return occurrences_freq_df
