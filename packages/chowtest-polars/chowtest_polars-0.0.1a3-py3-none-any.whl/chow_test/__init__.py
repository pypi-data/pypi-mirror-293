from sklearn.linear_model import LinearRegression as Lr
from scipy.stats import f
import polars as pl


def _calculate_rss(df: pl.DataFrame, x_field: str = 'x', y_field: str = 'y'):
    """
    Calculate the residual sum of squares (RSS) for a given Polars DataFrame.
    Args:
        df (pl.DataFrame): The input Polars DataFrame.
        x_field (str, optional): The column name for the x values. Defaults to 'x'.
        y_field (str, optional): The column name for the y values. Defaults to 'y'.
    Returns:
        Tuple[pl.DataFrame, float]: A tuple containing the summary result DataFrame and the RSS value.
    Raises:
        TypeError: If the 'df' argument is not a Polars DataFrame.
    """
    
    if not isinstance(df, pl.DataFrame):
        raise TypeError("The 'df' argument should be a Polars DataFrame.")
   
    x_df = pl.DataFrame(df[x_field])
    model = Lr().fit(x_df, df[y_field])
    #y_hat = list(model.predict(x_df))
    summary_result = pl.DataFrame({
            'y_hat': list(model.predict(x_df)),  # type: ignore
            'y_actual': df[y_field]
    })
   
    summary_result = summary_result \
        .with_columns((pl.col('y_actual') - pl.col('y_hat')).alias('residuals')) \
        .with_columns(((pl.col('y_actual') - pl.col('y_hat'))** 2).alias('residuals_sq'))
    rss = float(summary_result['residuals_sq'].sum())
    return summary_result, rss


def _data_preparation(df: pl.DataFrame, last_index: int, first_index: int):
    """
    Prepare the data by slicing a Polars DataFrame based on the given last and first indices.
    Args:
        df (pl.DataFrame): The Polars DataFrame to be sliced.
        last_index (int): The last index (exclusive) for slicing the DataFrame.
        first_index (int): The first index (inclusive) for slicing the DataFrame.
    Raises:
        TypeError: If the 'df' argument is not a Polars DataFrame.
        TypeError: If the 'last_index' or 'first_index' arguments are not of integer type.
    Returns:
        tuple: A tuple containing two sliced Polars DataFrames, 'one' and 'two'.
    """
    
    if not isinstance(df, pl.DataFrame):
        raise TypeError("The 'X_series' argument should be a Polars DataFrame.")
    if not all(isinstance(v, int) for v in [last_index, first_index]):
        raise TypeError("The 'last_index' and 'first_index' arguments must be integer types.")
    
    one = df[:last_index]
    two = df[first_index:]
    return one, two


def _calculate_chow_statistic(pooled_rss_value: int | float, rss_one: int | float, rss_two: int | float,
                              k_value: int, n_one_value: int, n_two_value: int):
    """
    This function calculates the chow test statistic. Firstly the function checks that the input arguments are of the
    correct input type, followed by calculating the numerator argument for th chow test. After this, the denominator
    argument is calculated, and the chow test statistic is attempted. If this fails due to a zero division error, the
    user is warned and the value is returned as 0.

    :param: pooled_rss_value: the sum of squared errors for the whole data series. (float)
    :param: rss_one: the sum of squared errors for the first series. (float)
    :param: rss_two: the sum of squared errors for ths second series. (float)
    :param: k_value: the number of degrees of freedom. (int)
    :param: n_one_value: the length of the first series. (int)
    :param: n_two_value: the length of the second series. (int)
    :return: chow_test: the chow test statistic. (float)
    """
    if not all(isinstance(v, (float, int)) for v in [pooled_rss_value, rss_one, rss_two]):
        raise TypeError("The 'pooled_rss_value', 'rss_one' and 'rss_two' values must be either integers or floats.")
    if not all(isinstance(v, int) for v in [k_value, n_one_value, n_two_value]):
        raise TypeError("The 'k_value', 'n_one_value' and 'n_two_value' arguments must be integer types.")
    numerator = (pooled_rss_value - (rss_one + rss_two)) / k_value
    denominator = (rss_one + rss_two) / (n_one_value + n_two_value - (2 * k_value))
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0


def _determine_p_value_significance(chow_value: int | float, n_one_value: int, n_two_value: int, k_value: int):
    """
    This function determines the statistical significance of the chow_value passed as an input argument. The
    function firstly checks that the input arguments are of the correct type, followed by defining the p-value with
    respect to the f-distribution. The p-value is subsequently assessed against the significance_level argument,
    printing the output if verbose is set to True. The chow_value and corresponding p-value are returned.

    :param: chow_value: the chow statistic for which to assess the p-value. (float)
    :param: n_one_value: the number of observations held within the first subset of data. (int)
    :param: n_two_value: the number of observations held within the second subset of data. (int)
    :param: k_value: the number of degrees of freedom. (int)
    :return: p_value: the p-value associated with the chow statistic. (float)
    """
    if not all(isinstance(v, int) for v in [n_one_value, n_two_value, k_value]):
        raise TypeError("The 'n_one_value', 'n_two_value' and 'k_value' must be integer types.")
    if not isinstance(chow_value, (int, float)):
        raise TypeError("The 'chow_statistic' must be an integer or float type.")
    p_value = float(1 - f.cdf(chow_value, dfn=k_value, dfd=((n_one_value + n_two_value) - 2 * k_value)))
    return p_value


def chow_test(df: pl.DataFrame, last_index: int, first_index: int,
              significance: float, x_field: str = 'x', y_field: str = 'y',
              verbose = False
              ):
    """
    This function acts as the highest level of abstraction for the chow test. The function firstly checks that the
    input arguments are of the correct type, followed by calculating the sum of squared residuals for the entire data
    series, and the two sub-sets of data, as determined by the last_index and first_index arguments. The chow test is
    then computed and assessed against the significance argument. Finally, the chow_test value and p_value are returned
    from the function.

    :param: df: The input Polars DataFrame containing the x and y serieses.
    :param: last_index: The final index value to be included before the data split. (int)
    :param: first_index: The first index value to be included after the data split. (int)
    :param: significance: The significance level against which the p-value is assessed. (float)
    :param: x_field: The column name for the x values. Defaults to 'x'.
    :param: y_field: The column name for the y values. Defaults to 'y'.
    :return: chow_value: The chow test output value. (float)
    :return: p_value: The associated p-value for the chow test. (float)
    """
    if not isinstance(df, pl.DataFrame):
        raise TypeError("The 'X_series' argument should be a Polars DataFrame.")
    if not all(isinstance(v, int)for v in [last_index, first_index]):
        raise TypeError("The 'last_index' and 'first_index' arguments must be integer types.")
    if not isinstance(significance, float):
        raise TypeError("The 'significance' argument must be a float type.")
    if significance not in [0.01, 0.05, 0.1]:
        raise KeyError("The 'significance' argument must be 0.01, 0.05 or 0.1")

    _, rss_pooled = _calculate_rss(df, x_field, y_field)
    one, two = _data_preparation(df=df, last_index=last_index, first_index=first_index)
    _, first_rss = _calculate_rss(one, x_field, y_field)
    _, second_rss = _calculate_rss(two, x_field, y_field)
    k = 2
    n_one = len(one)
    n_two = len(two)
    chow_value = _calculate_chow_statistic(rss_pooled, first_rss, second_rss, k, n_one, n_two)
    p_value = _determine_p_value_significance(chow_value, n_one, n_two, k)

    if p_value <= significance and verbose:
        print("Reject the null hypothesis of equality of regression coefficients in the two periods.")
    elif p_value > significance and verbose:
        print("Fail to reject the null hypothesis of equality of regression coefficients in the two periods.")
    if verbose:
        print("Chow Statistic: {}, P_value: {}".format(chow_value, p_value))

    return chow_value, p_value
