"""
material_balance.py

This module contains the necessary functions to calculate the properties of
graphic and analytical methods.

Libraries:
    - pandas: For data manipulation and analysis.
    - numpy: For numerical operations and handling arrays.
    - matplotlib: For creating static, animated, and interactive visualizations.
    - math: Provides access to mathematical functions.
    - scipy: For scientific and technical computing.
    - warnings: To issue warning messages to the user.

Note:
    Ensure that all required libraries are installed in your environment
    before using this module. You can install missing libraries using
    pip, for example:
        pip install pandas numpy matplotlib scipy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats
from typing import Optional, Union, Tuple
import warnings
from scipy.optimize import fsolve
from pytank.functions.pvt_correlations import Bo_bw, comp_bw_nogas
from pytank.functions.pvt_interp import interp_pvt_matbal
from pytank.functions.utilities import (
    material_bal_var_type,
    material_bal_numerical_data,
)


# This part of this module contains functions that are used to calculate the
# poes through the graphical method (Havlena and Odeh"


def underground_withdrawal(
        data: pd.DataFrame,
        oil_cum_col: str,
        water_cum_col: str,
        gas_cum_col: str,
        oil_fvf: Optional[Union[str, float]] = None,
        water_fvf: Optional[Union[str, float]] = None,
        gas_fvf: Optional[Union[str, float]] = None,
        gas_oil_rs: Optional[Union[str, float]] = None,
        gas_water_rs: Optional[Union[str, float]] = None,
) -> np.array:
    """
    Calculates the total underground withdrawal of a well using its cumulative
    production information and fluid properties.

    This function computes the total underground withdrawal based on the
    cumulative production data for oil, water, and gas, along with the relevant
    fluid properties.

    Args:
        data (DataFrame): A pandas DataFrame containing the production
            information for a single entity.
        oil_cum_col (str): Name of the oil cumulative production column in the
            data [stb].
        water_cum_col (str): Name of the water cumulative production column in
            the data [stb].
        gas_cum_col (str): Name of the gas cumulative production column in the
            data [scf].
        oil_fvf (Optional[Union[str, float]]): Oil formation volume factor
            column in DataFrame or numeric value [rb/stb].
        water_fvf (Optional[Union[str, float]]): Water formation volume factor
            in DataFrame or numeric value [rb/stb].
        gas_fvf (Optional[Union[str, float]]): Gas formation volume factor in
            DataFrame or numeric value [rb/scf].
        gas_oil_rs (Optional[Union[str, float]]): Solution gas-oil ratio in
            DataFrame or numeric value [scf/stb].
        gas_water_rs (Optional[Union[str, float]]): Solution gas-water ratio in
            DataFrame or numeric value [scf/stb].

    Returns:
        uw_array: Returns numpy array with the total underground withdrawal

    Raises:
        TypeError: When the input data is not a pandas DataFrame or the
            required numeric arguments are not numeric.

        ArithmeticError: If the free gas calculation results in a negative
            value.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("The input data should be a pandas dataframe")

    df = data.copy()
    # Define internal names for column in the DataFrame
    oil_fvf_col = "oil_fvf"
    water_fvf_col = "water_fvf"
    gas_fvf_col = "gas_fvf"
    rs_col = "gas_oil_rs_col"
    rsw_col = "gas_water_rs"

    # Dictionary containing the names of some columns of the dataframe
    numeric_or_col_args = {
        oil_fvf_col: oil_fvf,
        water_fvf_col: water_fvf,
        gas_fvf_col: gas_fvf,
        rs_col: gas_oil_rs,
        rsw_col: gas_water_rs,
    }

    # Rename the input dataframe and checking the data types of the function
    # arguments
    df = material_bal_var_type(data, numeric_or_col_args)

    # No check for the column types is needed as pandas will raise an error
    # if the key does not exist for the input DataFrame

    # Calculate the incremental oil, water and gas volumes
    oil_vol_col = "oil_vol"
    water_vol_col = "water_vol"
    gas_vol_col = "gas_vol"

    cols_input = [oil_cum_col, water_cum_col, gas_cum_col]
    cols_output = [oil_vol_col, water_vol_col, gas_vol_col]

    df[cols_output] = df[cols_input].diff().fillna(data[cols_input])

    # Calculate gas withdrawal
    gas_withdrawal = (
                             df[gas_vol_col] - df[oil_vol_col] * df[rs_col] -
                             df[water_vol_col] * df[rsw_col]
                     ) * df[gas_fvf_col]

    if sum(gas_withdrawal < 0) > 0:
        raise ArithmeticError(
            "Gas withdrawal results in negative values. Consider "
            "adjusting solution gas-oil/water ratio to reflect "
            "consistent gas production"
        )

    gas_withdrawal.fillna(0, inplace=True)

    uw = (
            df[oil_vol_col] * df[oil_fvf_col]
            + df[water_vol_col] * df[water_fvf_col]
            + gas_withdrawal
    )

    return uw.cumsum().values


def pressure_vol_avg(
        data: pd.DataFrame,
        entity_col,
        date_col,
        press_col,
        uw_col,
        avg_freq="1MS",
        position="begin",
) -> pd.DataFrame:
    """
    Args:
        data (DataFrame): The pressure information containing pressure data,
            the dates and the underground withdrawal for each well. If there are
            *nan* values in the pressure column these rows will be deleted from
            the DataFrame.
            If nan values are present in the UW columns, they will be replaced
            by zero. The last case is assuming that the recorded pressures were
            obtained without significant underground withdrawal.
        entity_col (str): The column name_tank where the entities are defined,
            i.e: wells
        date_col (str): The column name_tank where the pressure dates are defined.
        press_col (str): The column name_tank where the pressure information is
            defined.
        uw_col (str): The column name_tank where the underground withdrawal
            information.
        avg_freq (str): The time frequency at which the pressure volumetric
            average is required.
        position (str):
            - "begin": dates start at the beginning of the grouped interval
            - "middle": dates start in the middle of the grouped interval
            - "end": dates start at the end of the grouped interval

    Returns:
        press_df (DataFrame): A DataFrame with the grouped dates and pressure
            volumetric averages.


    Raises:
        ValueError: If there are underground withdrawal values that are not
            monotonically increasing.
    """
    # Avoid warnings
    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="'M' is deprecated and will be removed in a future version,"
                " please use 'ME' instead.",
    )

    df = data.copy()

    # Make consistency checks
    # Eliminate rows where pressure contain nan values
    df.dropna(subset=[press_col], inplace=True)
    # Replace nan UW values with zeros
    df.fillna(0, inplace=True)
    # Sort by date and check monotonic increase in UW
    df.sort_values(date_col, inplace=True)
    mono_increase = df.groupby(entity_col)[uw_col].is_monotonic_increasing
    for well, mono in mono_increase.items():
        if not mono:
            raise ValueError(
                f"Well {well} contains underground withdrawal values that "
                f"are not increasing with time"
            )

    pos = ["begin", "middle", "end"]

    # Check if position argument has the correct values
    if position not in pos:
        raise ValueError(
            f"{position} is not an accepted value for 'position' "
            f"argument. Use any of {pos} instead."
        )

    # Calculate the differences in pressure and underground withdrawal per well
    delta_uw_col = "delta_uw"
    delta_press_col = "delta_press"

    df[[delta_uw_col, delta_press_col]] = (
        df.groupby(entity_col)[[uw_col, press_col]]
        .diff()
        .fillna(df[[uw_col, press_col]])
    )

    gr_press = df.groupby(pd.Grouper(key=date_col, freq=avg_freq))
    result_avg_press = {date_col: [], press_col: []}

    for group_name, group in gr_press:
        # Identify which values are zero to avoid division by zero
        cond_1 = group[delta_uw_col].abs() > 0
        cond_2 = group[delta_press_col].abs() > 0
        cond = cond_1 & cond_2
        # Assign np.nan in case there are no values
        avg_1 = np.nan
        avg_2 = np.nan

        # This group will be used to get pressure volumetric average as per the
        # defined equation
        g_1 = group[cond]
        if len(g_1) > 0:
            avg_1 = (
                            g_1[press_col] * g_1[delta_uw_col] / g_1[
                        delta_press_col]
                    ).sum() / (g_1[delta_uw_col] / g_1[delta_press_col]).sum()

        # This group has no UW and pressure changes, the average of these
        # values will be processed normally
        g_2 = group[~cond]
        if len(g_2) > 0:
            avg_2 = g_2[press_col].mean()

        result_avg_press[date_col].append(group_name)
        # Calculate the average between the volumetric averages and the
        # normal ones
        avg_all = np.array([avg_1, avg_2])
        avg_press = np.nan if all(np.isnan(avg_all)) else np.nanmean(avg_all)

        result_avg_press[press_col].append(avg_press)

    result = pd.DataFrame(result_avg_press)

    if position == pos[0]:
        pass
    else:
        # Get the DateOffset object based on the average frequency
        date_offset = pd.tseries.frequencies.to_offset(avg_freq)
        # Get the information to replicate the date grouping and
        # change accordingly
        start_date = result[date_col].min()
        end_date = result[date_col].max()
        # This date range should be the same as the one generated
        # by the Grouper
        new_dates = pd.date_range(start_date, end_date,
                                  freq=avg_freq) + date_offset
        # Calculate the time deltas comparing to the original dates
        dates_delta = new_dates - result[date_col]

        if position == pos[1]:
            result[date_col] = result[date_col] + dates_delta / 2
        else:
            result[date_col] = result[date_col] + dates_delta

    return result


def oil_expansion(
        data: pd.DataFrame,
        oil_fvf: Optional[Union[str, float]] = None,
        gas_fvf: Optional[Union[str, float]] = None,
        gas_oil_rs: Optional[Union[str, float]] = None,
        gas_oil_rs_init: Optional[Union[int, float]] = None,
        oil_fvf_init: Optional[Union[int, float]] = None
) -> pd.Series:
    """Calculates the oil expansion using its cumulative production information
    and fluid properties.

    This function computes the oil expansion based on the provided production
    data and fluid properties. It requires a pandas DataFrame containing the
    production information and optional parameters for the oil formation volume
    factor, gas formation volume factor, solution gas-oil ratio, initial
    solution gas-oil ratio, and initial oil formation volume factor.

    Args:
        data (pd.DataFrame): A pandas DataFrame containing the production
            information for a single entity.
        oil_fvf (Optional[Union[str, float]]): The oil formation volume factor
            column in the DataFrame or a numeric value [rb/stb].
        gas_fvf (Optional[Union[str, float]]): The gas formation volume factor
            column in the DataFrame or a numeric value [rb/scf].
        gas_oil_rs (Optional[Union[str, float]]): The solution gas-oil ratio
            column in the DataFrame or a numeric value [scf/stb].
        gas_oil_rs_init (Optional[Union[int, float]]): The initial solution
            gas-oil ratio [scf/stb].
        oil_fvf_init (Optional[Union[int, float]]): The initial oil formation
            volume factor [rb/stb].

    Returns:
        Oil_Exp: Returns Pandas Series with the oil expansion.

    Raises:
        TypeError: When the input data is not a pandas DataFrame or the required
            numeric arguments are not numeric.
    """

    # Define internal names for column in the DataFrame
    oil_fvf_col = "oil_fvf"
    rs_col = "gas_oil_rs "
    gas_fvf_col = "gas_fvf"

    # Dictionary containing the names of some columns of the dataframe
    numeric_or_col_args = {
        oil_fvf_col: oil_fvf,
        rs_col: gas_oil_rs,
        gas_fvf_col: gas_fvf,
    }

    # Rename the input dataframe and checking the data types of the function
    # arguments
    df = material_bal_var_type(data, numeric_or_col_args)

    # Check the data type of numerical arguments
    num_arg = [gas_oil_rs_init, oil_fvf_init]
    material_bal_numerical_data(num_arg)

    tot_fvf_col = df[oil_fvf_col] + (
            (df[rs_col] - gas_oil_rs_init) * df[gas_fvf_col])
    eo = tot_fvf_col - oil_fvf_init
    return eo


# %%
def gas_expansion(
        data: pd.DataFrame,
        oil_fvf: Optional[Union[str, float]],
        gas_fvf: Optional[Union[str, float]],
        gas_fvf_init: Optional[Union[int, float]],
        tot_fvf_init: Optional[Union[int, float]]
) -> pd.Series:
    """Calculates the gas expansion using its cumulative production information
    and fluid properties.

    This function computes the gas expansion based on the provided production
    data and fluid properties. It requires a pandas DataFrame containing the
    production information and parameters for the oil formation volume factor,
    gas formation volume factor, initial gas formation volume factor, and
    initial total volume factor of 2 phases.

    Parameters:
        data (DataFrame): A pandas DataFrame containing the production
            information for a single entity.
        oil_fvf (Optional[Union[str, float]]): The oil formation volume factor
            column in the DataFrame or a numeric value [rb/stb].
        gas_fvf (Optional[Union[str, float]]): The gas formation volume factor
            column in the DataFrame or a numeric value [rb/scf].
        gas_fvf_init (Optional[Union[int, float]]): The initial gas formation
            volume factor [rb/scf].
        tot_fvf_init (Optional[Union[int, float]]): The initial total volume
            factor of 2 phases [scf/stb].

    Returns:
        Gas_Exp: A pandas Series containing the calculated gas expansion.

    Raises:
        TypeError: If the input data is not a pandas DataFrame or the required
            numeric arguments are not numeric.
    """

    # Define internal names for column in the DataFrame
    oil_fvf_col = "oil_fvf"
    gas_fvf_col = "gas_fvf"

    # Dictionary containing the names of some columns of the dataframe
    numeric_or_col_args = {
        oil_fvf_col: oil_fvf,
        gas_fvf_col: gas_fvf,
    }

    # Rename the input dataframe and checking the data types of the function
    # arguments
    df = material_bal_var_type(data, numeric_or_col_args)

    # Check the data type of numerical arguments
    num_arg = [gas_fvf_init, tot_fvf_init]
    material_bal_numerical_data(num_arg)

    eg = tot_fvf_init * ((df[gas_fvf_col] / gas_fvf_init) - 1)

    return eg


def fw_expansion(
        data: pd.DataFrame,
        oil_fvf: Union[str, float],
        p_col: str,
        water_sat: Union[int, float],
        water_comp: Union[int, float],
        rock_comp: Union[int, float],
        oil_fvf_init: Union[int, float],
        pressure_init: Union[int, float]
) -> pd.Series:
    """Calculates the expansion of connate water and rock(formation) using its
    cumulative production information and fluid properties.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame containing the production
            information for a single entity.
        oil_fvf (Union[str, float]): Oil formation volume factor column in
            DataFrame or numeric value [rb/stb].
        p_col (str): Name of the pressure column in the data [psi].
        water_sat (Union[int, float]): Initial water saturation [%].
        water_comp (Union[int, float]): Water compressibility [psi⁻¹].
        rock_comp (Union[int, float]): Formation (rock) compressibility [psi⁻¹].
        oil_fvf_init (Union[int, float]): Initial oil formation volume factor
            [rb/stb].
        pressure_init (Union[int, float]): Initial reservoir pressure [psi].

    Returns:
        Fw_Exp: A pandas Series containing the calculated expansion of
            connate water and rock(formation).

    Raises:
        TypeError: If the input data is not a pandas DataFrame or the required
            numeric arguments are not numeric.
    """

    # Define internal names for column in the DataFrame
    oil_fvf_col = "oil_fvf"

    # Dictionary containing the oil_fvf column of the dataframe
    numeric_or_col_args = {oil_fvf_col: oil_fvf}

    # Rename the input dataframe and checking the data types of the function
    # arguments
    df = material_bal_var_type(data, numeric_or_col_args)

    # Check the data type of numerical arguments
    num_arg = [water_sat, water_comp, rock_comp, oil_fvf_init, pressure_init]
    material_bal_numerical_data(num_arg)

    efw = (oil_fvf_init * (
            (water_comp * water_sat + rock_comp) / (1 - water_sat))) * (
                  pressure_init - df[p_col]
          )

    return efw


def ho_terms_equation(
        data: pd.DataFrame,
        oil_cum_col: str,
        water_cum_col: str,
        gas_cum_col: str,
        p_col: str,
        oil_fvf,
        gas_fvf,
        gas_oil_rs,
        water_fvf,
        gas_water_rs,
        water_sat,
        water_comp,
        rock_comp,
        oil_fvf_init,
        gas_fvf_init,
        tot_fvf_init,
        gas_oil_rs_init,
        pressure_init,
) -> pd.DataFrame:
    """Calculates the terms of the Havlena and Odeh equation using the
    cumulative production information and fluid properties of some wells and
    reservoirs.

    This function computes the terms of the Havlena and Odeh equation based on
    the provided production data, fluid properties, and reservoir
    characteristics. It requires a pandas DataFrame containing the production
    information, pressure data, and various parameters related to oil, water,
    and gas properties, as well as initial reservoir conditions.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame containing the production
            information for a single entity.
        oil_cum_col (str): Name of the oil cumulative production column in the
            data [stb].
        water_cum_col (str): Name of the water cumulative production column in
            the data [stb].
        gas_cum_col (str): Name of the gas cumulative production column in the
            data [scf].
        p_col (str): Name of the pressure column in the data [Psi].
        oil_fvf (Optional[Union[str, float]]): The oil formation volume factor
            column in the DataFrame or a numeric value [rb/stb].
        water_fvf (Optional[Union[str, float]]): The water formation volume
            factor column in the DataFrame or a numeric value [rb/stb].
        gas_fvf (Optional[Union[str, float]]): The gas formation volume factor
            column in the DataFrame or a numeric value [rb/scf].
        gas_oil_rs (Optional[Union[str, float]]): The solution gas-oil ratio
            column in the DataFrame or a numeric value [scf/stb].
        gas_water_rs (Optional[Union[str, float]]): The solution gas-water ratio
            column in the DataFrame or a numeric value [scf/stb].
        water_sat (Union[int, float]): The initial water saturation [%].
        water_comp (Union[int, float]): The water compressibility [Psi⁻¹].
        rock_comp (Union[int, float]): The formation (rock) compressibility
            [Psi⁻¹].
        oil_fvf_init (Optional[Union[int, float]]): The initial oil formation
            volume factor [rb/stb].
        gas_oil_rs_init (Optional[Union[int, float]]): The initial solution
            gas-oil ratio [scf/stb].
        gas_fvf_init (Optional[Union[int, float]]): The initial gas formation
            volume factor [rb/scf].
        tot_fvf_init (Optional[Union[int, float]]): The initial total volume
            factor of 2 phases [scf/stb].
        pressure_init (Union[int, float]): The initial reservoir pressure [Psi].

    Returns:
        Ho_df: A pandas DataFrame containing the calculated terms of the
            Havlena and Odeh equation.
    """

    # Check the data type of numerical arguments
    num_arg = [
        water_sat,
        water_comp,
        rock_comp,
        oil_fvf_init,
        pressure_init,
        gas_oil_rs_init,
        gas_fvf_init,
        tot_fvf_init,
    ]
    material_bal_numerical_data(num_arg)

    # Call the dataframes of the havlena and odeh equation
    f = underground_withdrawal(
        data,
        oil_cum_col,
        water_cum_col,
        gas_cum_col,
        oil_fvf,
        water_fvf,
        gas_fvf,
        gas_oil_rs,
        gas_water_rs,
    )

    eg = gas_expansion(data, oil_fvf, gas_fvf, gas_fvf_init, tot_fvf_init)

    eo = oil_expansion(
        data, oil_fvf, gas_fvf, gas_oil_rs, gas_oil_rs_init, oil_fvf_init
    )

    efw = fw_expansion(
        data,
        oil_fvf,
        p_col,
        water_sat,
        water_comp,
        rock_comp,
        oil_fvf_init,
        pressure_init,
    )

    data["UW"] = f
    data["Eo"] = eo
    data["Eg"] = eg
    data["Efw"] = efw

    return data


def campbell_function(
        data: pd.DataFrame,
        oil_cum_col: str,
        water_cum_col: str,
        gas_cum_col: str,
        p_col: str,
        uw_col: str,
        eo_col: str,
        efw_col: str,
        oil_fvf: Optional[Union[str, float]],
        water_fvf: Optional[Union[str, float]],
        gas_fvf: Optional[Union[str, float]],
        gas_oil_rs: Optional[Union[str, float]],
        gas_water_rs: Optional[Union[str, float]],
        water_sat: Union[int, float],
        water_comp: Union[int, float],
        rock_comp: Union[int, float],
        oil_fvf_init: Optional[Union[int, float]],
        gas_fvf_init: Optional[Union[int, float]],
        tot_fvf_init: Optional[Union[int, float]],
        gas_oil_rs_init: Optional[Union[int, float]],
        pressure_init: Union[int, float]
):
    """This function is able to plot the Campbell plot for a required reservoir.

    This function plots the Campbell plot based on the provided production data,
    fluid properties, and reservoir characteristics. It requires a pandas
    DataFrame containing the production information, pressure data, and various
    parameters related to oil, water, and gas properties, as well as initial
    reservoir conditions.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame containing the production
            information for a single entity.
        oil_cum_col (str): Name of the oil cumulative production column in the
            data [stb].
        water_cum_col (str): Name of the water cumulative production column in
            the data [stb].
        gas_cum_col (str): Name of the gas cumulative production column in the
            data [scf].
        p_col (str): Name of the pressure column in the data (psi).
        uw_col (str): Name of the underground withdrawals fluids produced column
            in the data.
        eo_col (str): Name of the oil expansion column in the data.
        efw_col (str): Name of the column referencing the expansion of the
            connate water and rock in the data.
        oil_fvf (Optional[Union[str, float]]): The oil formation volume factor
            column in the DataFrame or a numeric value [rb/stb].
        water_fvf (Optional[Union[str, float]]): The water formation volume
            factor column in the DataFrame or a numeric value [rb/stb].
        gas_fvf (Optional[Union[str, float]]): The gas formation volume factor
            column in the DataFrame or a numeric value [rb/scf].
        gas_oil_rs (Optional[Union[str, float]]): The solution gas-oil ratio
            column in the DataFrame or a numeric value [scf/stb].
        gas_water_rs (Optional[Union[str, float]]): The solution gas-water ratio
            column in the DataFrame or a numeric value [scf/stb].
        water_sat (Union[int, float]): The initial water saturation [%].
        water_comp (Union[int, float]): The water compressibility [psi⁻¹].
        rock_comp (Union[int, float]): The formation (rock) compressibility
            [psi⁻¹].
        oil_fvf_init (Optional[Union[int, float]]): The initial oil formation
            volume factor [rb/stb].
        gas_fvf_init (Optional[Union[int, float]]): The initial gas formation
            volume factor [rb/scf].
        tot_fvf_init (Optional[Union[int, float]]): The initial total volume
            factor of 2 phases [scf/stb].
        gas_oil_rs_init (Optional[Union[int, float]]): The initial solution
            gas-oil ratio [scf/stb].
        pressure_init (Union[int, float]): The initial reservoir pressure [Psi].


    """

    # Check the data type of numerical arguments
    num_arg = [
        water_sat,
        water_comp,
        rock_comp,
        oil_fvf_init,
        pressure_init,
        gas_oil_rs_init,
        gas_fvf_init,
        tot_fvf_init,
    ]
    material_bal_numerical_data(num_arg)

    # Call the havlena and odeh terms function
    df = ho_terms_equation(
        data,
        oil_cum_col,
        water_cum_col,
        gas_cum_col,
        p_col,
        oil_fvf,
        gas_fvf,
        gas_oil_rs,
        water_fvf,
        gas_water_rs,
        water_sat,
        water_comp,
        rock_comp,
        oil_fvf_init,
        gas_fvf_init,
        tot_fvf_init,
        gas_oil_rs_init,
        pressure_init,
    )

    vertical_axis = df[uw_col] / (df[eo_col] + df[efw_col])

    # Build the campbell plot
    fig, ax1 = plt.subplots()
    ax1.scatter(df[oil_cum_col], vertical_axis)
    ax1.set_xlabel("Np")
    ax1.set_ylabel("F/Eo+Efw")
    ax1.set_title("Campbell plot")
    plt.show()


def havlena_and_odeh(
        data: pd.DataFrame,
        oil_cum_col: str,
        water_cum_col: str,
        gas_cum_col: str,
        p_col: str,
        uw_col: str,
        eo_col: str,
        eg_col: str,
        oil_fvf: Optional[Union[str, float]],
        gas_fvf: Optional[Union[str, float]],
        gas_oil_rs: Optional[Union[str, float]],
        water_fvf: Optional[Union[str, float]],
        gas_water_rs: Optional[Union[str, float]],
        water_sat: Union[int, float],
        water_comp: Union[int, float],
        rock_comp: Union[int, float],
        oil_fvf_init: Optional[Union[int, float]],
        gas_fvf_init: Optional[Union[int, float]],
        tot_fvf_init: Optional[Union[int, float]],
        gas_oil_rs_init: Optional[Union[int, float]],
        pressure_init: Union[int, float]
):
    """This function is able to plot the Havlena and Odeh straight line, which
    is useful to determine the OOIP and GIIP of a reservoir. This function
    assumes that the reservoir contains a gas cap and neglects the expansion of
    the connate water and rock.

    This function plots the Havlena and Odeh straight line based on the provided
    production data, fluid properties, and reservoir characteristics. It
    requires a pandas DataFrame containing the production information, pressure
    data, and various parameters related to oil, water, and gas properties, as
    well as initial reservoir conditions.

    Parameters:
        data (DataFrame): A pandas DataFrame containing the production
            information for a single entity.
        oil_cum_col (str): Name of the oil cumulative production column in the
            data [stb].
        water_cum_col (str): Name of the water cumulative production column in
            the data [stb].
        gas_cum_col (str): Name of the gas cumulative production column in the
            data [scf].
        p_col (str): Name of the pressure column in the data [psi].
        uw_col (str): Name of the underground withdrawals fluids produced column
            in the data.
        eo_col (str): Name of the oil expansion column in the data.
        eg_col (str): Name of the gas expansion column in the data.
        oil_fvf (Optional[Union[str, float]]): The oil formation volume factor
            column in the DataFrame or a numeric value [rb/stb].
        gas_fvf (Optional[Union[str, float]]): The gas formation volume factor
            column in the DataFrame or a numeric value [rb/scf].
        gas_oil_rs (Optional[Union[str, float]]): The solution gas-oil ratio
            column in the DataFrame or a numeric value [scf/stb].
        water_fvf (Optional[Union[str, float]]): The water formation volume
            factor column in the DataFrame or a numeric value [rb/stb].
        gas_water_rs (Optional[Union[str, float]]): The solution gas-water ratio
            column in the DataFrame or a numeric value [scf/stb].
        water_sat (Union[int, float]): The initial water saturation [%].
        water_comp (Union[int, float]): The water compressibility [psi⁻¹].
        rock_comp (Union[int, float]): The formation (rock) compressibility
            [psi⁻¹].
        oil_fvf_init (Optional[Union[int, float]]): The initial oil formation
            volume factor [rb/stb].
        gas_fvf_init (Optional[Union[int, float]]): The initial gas formation
            volume factor [rb/scf].
        tot_fvf_init (Optional[Union[int, float]]): The initial total volume
            factor of 2 phases [scf/stb].
        gas_oil_rs_init (Optional[Union[int, float]]): The initial solution
            gas-oil ratio [scf/stb].
        pressure_init (Union[int, float]): The initial reservoir pressure [psi].

    """

    # Check the data type of numerical arguments
    num_arg = [
        water_sat,
        water_comp,
        rock_comp,
        oil_fvf_init,
        pressure_init,
        gas_oil_rs_init,
        gas_fvf_init,
        tot_fvf_init,
    ]
    material_bal_numerical_data(num_arg)

    # Call the havlena and odeh terms function
    df = ho_terms_equation(
        data,
        oil_cum_col,
        water_cum_col,
        gas_cum_col,
        p_col,
        oil_fvf,
        gas_fvf,
        gas_oil_rs,
        water_fvf,
        gas_water_rs,
        water_sat,
        water_comp,
        rock_comp,
        oil_fvf_init,
        gas_fvf_init,
        tot_fvf_init,
        gas_oil_rs_init,
        pressure_init,
    )

    # Linear regression to calculate the slope and intercept of this
    # straight line
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df[uw_col] / df[eo_col], df[eg_col] / df[eo_col]
    )

    # Equation of the fitted line using the slope and intercept from
    # linear regression
    y_fit = intercept + (df[eg_col] / df[eo_col] * slope)

    # Build the havlena and odeh straight line
    fig2, ax2 = plt.subplots()
    ax2.plot(
        df[eg_col] / df[eo_col],
        df[uw_col] / df[eo_col],
        marker="o",
        label="original data",
    )
    ax2.plot(df[eg_col] / df[eo_col], y_fit, "r", label="fitted line")
    ax2.set_xlabel("Eg/Eo")
    ax2.set_ylabel("F/Eo")
    ax2.set_title("Havlena and Odeh Straight Line")
    text = "N: %.1f\nmN: %.3f" % (intercept, slope)
    plt.text(0.008, 1, text)
    plt.legend()
    plt.show()


# This part of this module contains functions that are used to calculate the
# poes through the analytical method


def ebm(
        p: float,
        pi: float,
        n_p: float,
        wp: float,
        bo: float,
        cf: float,
        cw: float,
        sw0: float,
        boi: float,
        poes: float,
        we: float,
        bw,
) -> float:
    """Calculates the function for the Energy Balance Method (EBM).

    This function computes the value of the EBM function based on the provided
    reservoir parameters and production data.

    Parameters:
        p (float): Current reservoir pressure [psi].
        pi (float): Initial reservoir pressure [psi].
        n_p (float): Cumulative oil production [stb].
        wp (float): Cumulative water production [bbl].
        bo (float): Oil formation volume factor [rb/stb].
        cf (float): Total compressibility [psi⁻¹].
        cw (float): Water compressibility [psi⁻¹].
        sw0 (float): Initial water saturation [%].
        boi (float): Initial oil formation volume factor [rb/stb].
        poes (float): Inferred Petroleum-in-Place (POES) [bbl].
        we (float): Influx of water [bbl].
        bw (float): Water formation volume factor [rb/bbl].

    Returns:
        ebm: The value of the EBM function.
    """
    eo = bo - boi
    efw = boi * (((cw * sw0) + cf) / (1 - sw0)) * (pi - p)
    f = (n_p * bo) + (wp * bw)
    func_p = (poes * (eo + efw)) + (we * bw) - f
    return func_p


def aquifer_fetkovich(
        aq_radius: float,
        res_radius: float,
        aq_thickness: float,
        aq_por: float,
        ct: float,
        p: float,
        theta: float,
        k: float,
        water_visc: float,
        last_press: float,
        cum: float,
        pi: float,
) -> float:
    """Calculates the accumulated influx of water using a simplified version of
    the Fetkovich class.

    This function computes the cumulative influx of water based on the provided
    aquifer and reservoir parameters using a simplified version of the Fetkovich
    class.

    Parameters:
        aq_radius (float): Aquifer radius value [ft].
        res_radius (float): Reservoir radius value [ft].
        aq_thickness (float): Aquifer thickness [ft].
        aq_por (float): Aquifer porosity (decimal).
        ct (float): Total compressibility [psi⁻¹].
        p (float): Current reservoir pressure [psi].
        theta (float): Aquifer angle [degrees].
        k (float): Permeability value [md].
        water_visc (float): Viscosity value [cp].
        last_press (float): Previous reservoir pressure [psi].
        cum (float): Cumulative influx of water [bbl].
        pi (float): Initial reservoir pressure [psi].

    Returns:
        aq_fet: Cumulative influx of water [bbl].
    """
    delta_t = 365
    wi = (math.pi / 5.615) * (
            aq_radius ** 2 - res_radius ** 2) * aq_thickness * aq_por
    f = theta / 360
    wei = ct * wi * pi * f
    rd = aq_radius / res_radius
    j = (0.00708 * k * aq_thickness * f) / (water_visc * (math.log(abs(rd))))
    pa = pi * (1 - (cum / wei))
    pr_avg = (last_press + p) / 2
    we = (wei / pi) * (1 - np.exp((-1 * j * pi * delta_t) / wei)) * (
            pa - pr_avg)
    cum_water_influx = cum + we
    return cum_water_influx


def fetkovich_press(
        p: float,
        np: float,
        wp: float,
        cf: float,
        t: float,
        salinity: float,
        df_pvt: pd.DataFrame,
        aq_radius: float,
        res_radius: float,
        aq_thickness: float,
        aq_por: float,
        theta: float,
        k: float,
        water_visc: float,
        p_anterior: float,
        cum: float,
        pi: float,
        sw0: float,
        poes: float,
        boi: float,
        ppvt_col: str,
        oil_fvf_col: str,
) -> float:
    """Calculates the reservoir pressure based on oil properties, oil and water
    production, and aquifer influence.

    This function computes the reservoir pressure considering the effects of oil
    and water production, aquifer characteristics, and fluid properties.

    Parameters:
        p (float): Current reservoir pressure [psi].
        np (float): Cumulative oil production [stb].
        wp (float): Cumulative water production [bbl].
        cf (float): Total compressibility [psi⁻¹].
        t (float): Temperature [°F or °C].
        salinity (float): Salinity value [ppm].
        df_pvt (pd.DataFrame): PVT data frame containing fluid properties.
        aq_radius (float): Aquifer radius [ft].
        res_radius (float): Reservoir radius [ft].
        aq_thickness (float): Aquifer thickness [ft].
        aq_por (float): Aquifer porosity [decimal].
        theta (float): Angle of the aquifer [degrees].
        k (float): Permeability [md].
        water_visc (float): Water viscosity [cP].
        p_anterior (float): Previous reservoir pressure [psi].
        cum (float): Cumulative influx of water [bbl].
        pi (float): Initial reservoir pressure [psi].
        sw0 (float): Initial water saturation [%].
        poes (float): Inferred POES (Petroleum-in-Place) [bbl].
        boi (float): Initial oil formation volume factor [rb/stb].
        ppvt_col (str): Column name_tank for pressure in the PVT data frame.
        oil_fvf_col (str): Column name_tank for oil formation volume factor in the
            PVT data frame.

    Returns:
        fet_press: The calculated reservoir pressure [psi].
    """
    # Parameters that depend on pressure
    bo = interp_pvt_matbal(df_pvt, ppvt_col, oil_fvf_col, p)
    bw = Bo_bw(p, t, salinity, unit=1)
    cw = comp_bw_nogas(p, t, salinity, unit=1)
    ct = cw + cf
    we = aquifer_fetkovich(
        aq_radius,
        res_radius,
        aq_thickness,
        aq_por,
        ct,
        p,
        theta,
        k,
        water_visc,
        p_anterior,
        cum,
        pi,
    )
    return ebm(p, pi, np, wp, bo, cf, cw, sw0, boi, poes, we, bw)


def calculated_pressure_fetkovich(
        np_frame: pd.Series,
        wp_frame: pd.Series,
        cf: float,
        t: float,
        salinity: float,
        df_pvt: pd.DataFrame,
        aq_radius: float,
        res_radius: float,
        aq_thickness: float,
        aq_por: float,
        theta: float,
        k: float,
        water_visc: float,
        pi: float,
        sw0: float,
        poes: float,
        ppvt_col: str,
        oil_fvf_col: str,
) -> list:
    """Calculates the reservoir pressure for each record in the df_ta2 dataframe
    using scipy's fsolve function to solve the material balance equations
    iteratively.

    This function computes the reservoir pressure for each record in the df_ta2
    dataframe by iteratively solving the material balance equations using
    scipy's fsolve function. It considers the effects of oil and water
    production, aquifer characteristics, and fluid properties.

    Parameters:
        np_frame (pd.Series): Column of oil cumulative production [stb].
        wp_frame (pd.Series): Column of water cumulative production [bbl].
        cf (float): Total compressibility [psi⁻¹].
        t (float): Temperature [°F or °C].
        salinity (float): Salinity value [ppm].
        df_pvt (pd.DataFrame): PVT data frame containing fluid properties.
        aq_radius (float): Aquifer radius [ft].
        res_radius (float): Reservoir radius [ft].
        aq_thickness (float): Aquifer thickness [ft].
        aq_por (float): Aquifer porosity [decimal].
        theta (float): Angle of the aquifer [degrees].
        k (float): Permeability [md].
        water_visc (float): Water viscosity [cP].
        pi (float): Initial reservoir pressure [psi].
        sw0 (float): Initial water saturation [%].
        poes (float): Inferred POES (Petroleum-in-Place) [bbl].
        ppvt_col (str): Column name_tank for pressure in the PVT data frame.
        oil_fvf_col (str): Column name_tank for oil formation volume factor in the
            PVT data frame.

    Returns:
        calc_press: List containing the calculated reservoir pressure [psi].
    """
    # initial values
    boi = interp_pvt_matbal(df_pvt, ppvt_col, oil_fvf_col, pi)
    cum = 0
    calculated_p = [pi]
    x0 = pi

    # Iteration of each of the years
    for i in range(len(np_frame)):
        np = np_frame[i]
        wp = wp_frame[i]
        p_anterior = calculated_p[i]
        # Calculate current reservoir pressure given all other material
        # balance variables through numeric solving.
        pressure = float(
            fsolve(
                fetkovich_press,
                x0,
                args=(
                    np,
                    wp,
                    cf,
                    t,
                    salinity,
                    df_pvt,
                    aq_radius,
                    res_radius,
                    aq_thickness,
                    aq_por,
                    theta,
                    k,
                    water_visc,
                    p_anterior,
                    cum,
                    pi,
                    sw0,
                    poes,
                    boi,
                    ppvt_col,
                    oil_fvf_col,
                ),
            )[0]
        )
        x0 = pressure
        calculated_p.append(pressure)
        cw = comp_bw_nogas(pressure, t, salinity, unit=1)
        ct = cf + cw
        cum = aquifer_fetkovich(
            aq_radius,
            res_radius,
            aq_thickness,
            aq_por,
            ct,
            pressure,
            theta,
            k,
            water_visc,
            p_anterior,
            cum,
            pi,
        )
    return calculated_p


def aquifer_carter_tracy(
        aq_por: float,
        ct: float,
        res_radius: float,
        aq_thickness: float,
        theta: float,
        k: float,
        water_visc: float,
        pr: float,
        time: float,
        past_time: float,
        we: float,
        pi: float,
) -> float:
    """Calculates the accumulated influx of water using a simplified version of
    the Carter-Tracy class.

    This function computes the cumulative influx of water based on the provided
    aquifer and reservoir parameters using a simplified version of the
    Carter-Tracy class.

    Parameters:
        aq_por (float): Aquifer porosity [decimal].
        ct (float): Total compressibility [psi⁻¹].
        res_radius (float): Reservoir radius [ft].
        aq_thickness (float): Aquifer thickness [ft].
        theta (float): Aquifer angle [degrees].
        k (float): Permeability [md].
        water_visc (float): Water viscosity [cP].
        pr (float): Current reservoir pressure [psi].
        time (float): Current time [days].
        past_time (float): Previous time [days].
        we (float): Cumulative water influx [bbl].
        pi (float): Initial reservoir pressure [psi].

    Returns:
        aq_ct: Cumulative influx of water [bbl].
    """
    pr_array = pr

    # Calculate the van Everdingen-Hurst water influx constant
    f = theta / 360
    b = 1.119 * aq_por * ct * (res_radius ** 2) * aq_thickness * f

    # Estimate dimensionless time (tD)
    cte = 0.006328 * k / (aq_por * water_visc * ct * (res_radius ** 2))
    td = time * cte
    td2 = past_time * cte
    # Calculate the total pressure drop (Pi-Pn) as an array, for each
    # time step n.
    pr_drop = pi - pr_array
    # Estimate the dimensionless pressure
    pr_d = 0.5 * (np.log(td) + 0.80907)
    # Estimate the dimensionless pressure derivative
    """e = 716.441 + (46.7984 * (td**0.5)) + (270.038 * td) + (71.0098 *
                                                            (td**1.5))
    d = ((1296.86 * (td**0.5)) + (1204.73 * td) + (618.618 * (td**1.5)) +
         (538.072 * (td**2)) + (142.41 * (td**2.5)))"""

    pr_deriv = 1 / (2 * td)

    a1 = td - td2
    a2 = b * pr_drop
    a3 = we * pr_deriv
    a4 = pr_d
    a5 = td2 * pr_deriv
    cum_influx_water = we + (a1 * ((a2 - a3) / (a4 - a5)))
    we = cum_influx_water
    return we


def carter_tracy_press(
        p: float,
        np: float,
        wp: float,
        cf: float,
        t: float,
        salinity: float,
        df_pvt: pd.DataFrame,
        res_radius: float,
        aq_thickness: float,
        aq_por: float,
        theta: float,
        k: float,
        water_visc: float,
        time: float,
        past_time: float,
        we: float,
        pi: float,
        sw0: float,
        poes: float,
        boi: float,
        ppvt_col: str,
        oil_fvf_col: str,
) -> float:
    """Calculates the reservoir pressure based on oil properties, oil and water
    production, and aquifer influence.

    This function computes the reservoir pressure considering the effects of oil
    and water production, aquifer characteristics, and fluid properties.

    Parameters:
        p (float): Current reservoir pressure [psi].
        np (float): Cumulative oil production [stb].
        wp (float): Cumulative water production [bbl].
        cf (float): Formation compressibility [psi⁻¹].
        t (float): Temperature [°F or °C].
        salinity (float): Salinity [ppm].
        df_pvt (pd.DataFrame): PVT data frame containing fluid properties.
        res_radius (float): Reservoir radius [ft].
        aq_thickness (float): Aquifer thickness [ft].
        aq_por (float): Aquifer porosity [decimal].
        theta (float): Aquifer angle [degrees].
        k (float): Permeability [md].
        water_visc (float): Water viscosity [cP].
        time (float): Current time [days].
        past_time (float): Previous time [days].
        we (float): Cumulative water influx [bbl].
        pi (float): Initial reservoir pressure [psi].
        sw0 (float): Initial water saturation [%].
        poes (float): Estimated Original Oil in Place (OOIP) [bbl].
        boi (float): Initial oil formation volume factor [rb/stb].
        ppvt_col (str): Column name_tank for pressure in the PVT data frame.
        oil_fvf_col (str): Column name_tank for oil formation volume factor in the
            PVT data frame.

    Returns:
        ct_press: The calculated reservoir pressure [psi].
    """
    bo = interp_pvt_matbal(df_pvt, ppvt_col, oil_fvf_col, p)

    bw = Bo_bw(p, t, salinity, unit=1)
    cw = comp_bw_nogas(p, t, salinity, unit=1)
    ct = cw + cf
    we = aquifer_carter_tracy(
        aq_por,
        ct,
        res_radius,
        aq_thickness,
        theta,
        k,
        water_visc,
        p,
        time,
        past_time,
        we,
        pi,
    )
    return ebm(p, pi, np, wp, bo, cf, cw, sw0, boi, poes, we, bw)


def calculate_pressure_with_carter_tracy(
        np_frame: pd.Series,
        wp_frame: pd.Series,
        cf: float,
        t: float,
        salinity: float,
        df_pvt: pd.DataFrame,
        res_radius: float,
        aq_thickness: float,
        aq_por: float,
        theta: float,
        k: float,
        water_visc: float,
        time_frame: pd.Series,
        pi: float,
        sw0: float,
        poes: float,
        ppvt_col: str,
        oil_fvf_col: str,
) -> list:
    """Calculates the reservoir pressure for each record in the df_ta2 dataframe
    using scipy's fsolve function to solve the material balance equations
    iteratively.

    This function computes the reservoir pressure for each record in the df_ta2
    dataframe by iteratively solving the material balance equations using
    scipy's fsolve function. It considers the effects of oil and water
    production, aquifer characteristics, and fluid properties.

    Parameters:
        np_frame (pd.Series): Column of oil cumulative production [stb].
        wp_frame (pd.Series): Column of water cumulative production [bbl].
        cf (float): Total compressibility [psi⁻¹].
        t (float): Temperature [°F or °C].
        salinity (float): Salinity value [ppm].
        df_pvt (pd.DataFrame): PVT data frame containing fluid properties.
        res_radius (float): Reservoir radius [ft].
        aq_thickness (float): Aquifer thickness [ft].
        aq_por (float): Aquifer porosity [decimal].
        theta (float): Angle of the aquifer [degrees].
        k (float): Permeability [md].
        water_visc (float): Water viscosity [cP].
        time_frame (pd.Series): Column of time steps [days].
        pi (float): Initial reservoir pressure [psi].
        sw0 (float): Initial water saturation [%].
        poes (float): Inferred original petroleum in situ [bbl].
        ppvt_col (str): Column name_tank for pressure in the PVT data frame.
        oil_fvf_col (str): Column name_tank for oil formation volume factor in the
            PVT data frame.

    Returns:
        calc_press: List containing the calculated reservoir pressure [psi].
    """
    boi = interp_pvt_matbal(df_pvt, ppvt_col, oil_fvf_col, pi)
    cum = 0
    x0 = pi
    calculated_p = [pi]
    past_time = 0
    for i in range(len(np_frame)):
        np = np_frame[i]
        wp = wp_frame[i]
        time = time_frame[i]
        pressure = float(
            fsolve(
                carter_tracy_press,
                x0,
                args=(
                    np,
                    wp,
                    cf,
                    t,
                    salinity,
                    df_pvt,
                    res_radius,
                    aq_thickness,
                    aq_por,
                    theta,
                    k,
                    water_visc,
                    time,
                    past_time,
                    cum,
                    pi,
                    sw0,
                    poes,
                    boi,
                    ppvt_col,
                    oil_fvf_col,
                ),
            )[0]
        )
        x0 = pressure
        calculated_p.append(pressure)
        cw = comp_bw_nogas(pressure, t, salinity, unit=1)
        ct = cf + cw
        cum = aquifer_carter_tracy(
            aq_por,
            ct,
            res_radius,
            aq_thickness,
            theta,
            k,
            water_visc,
            pressure,
            time,
            past_time,
            cum,
            pi,
        )
        past_time = time_frame[i]

    return calculated_p
