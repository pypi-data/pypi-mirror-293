"""
analysis.py

This module provides the POES class, which is designed to calculate the
petroleum initially-in-place using the material balance equation. The class
takes into account various reservoir and fluid properties to estimate the
POES and generate plots for visualization.

Libraries used:
    - pandas: For data manipulation and analysis.
    - matplotlib: For creating plots and visualizations.
    - pydantic: For data validation and settings management.
    - pandera: For defining and validating DataFrame schemas.
    - scipy: For numerical calculations and interpolation.
    - typing: For type hinting and annotations.
"""

import pandas as pd
import pandera as pa
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FuncFormatter
from pandera.typing import Series
from matplotlib import pyplot as plt
from pydantic import BaseModel
from scipy import stats
from scipy.interpolate import UnivariateSpline
from typing import Union, Optional
from pytank.constants.constants import (
    OIL_FVF_COL,
    GAS_FVF_COL,
    RS_COL,
    PRESSURE_COL,
    OIL_CUM_COL,
    GAS_CUM_COL,
    WATER_CUM_COL,
    DATE_COL,
    WELL_COL,
    WATER_FVF_COL,
    RS_W_COL,
    TANK_COL,
    UW_COL,
    PRESSURE_PVT_COL,
    OIL_CUM_TANK,
    WATER_CUM_TANK,
    GAS_CUM_TANK,
    OIL_EXP,
    RES_EXP,
    WE,
    OIL_RATE_COL,
    WATER_RATE_COL,
)
from pytank.functions.utilities import interp_dates_row
from pytank.functions.material_balance import (
    underground_withdrawal,
    pressure_vol_avg,
    ho_terms_equation,
    calculated_pressure_fetkovich,
    calculate_pressure_with_carter_tracy,
)
from pytank.tank import Tank
from pytank.aquifer_model import Fetkovich, CarterTracy


class _PressSchema(pa.DataFrameModel):
    """Private class to validate data for the df_press_int method in the Tank
    class.

    This class defines the schema for validating pressure-related data in
    the Tank class. It ensures that the required fields are present and
    correctly typed for pressure data processing.
    """

    PRESSURE_DATUM: Series[float] = pa.Field(nullable=False)
    WELL_BORE: Series[str] = pa.Field(nullable=False)
    START_DATETIME: Series[pd.Timestamp] = pa.Field(nullable=False)
    Bo: Series[float] = pa.Field(nullable=False)
    Bg: Series[float] = pa.Field(nullable=True)
    GOR: Series[float] = pa.Field(nullable=False)
    Bw: Series[float] = pa.Field(nullable=False)
    RS_bw: Series[float] = pa.Field(nullable=False)
    Tank: Series[str] = pa.Field(nullable=False)


class _ProdSchema(pa.DataFrameModel):
    """Private class to validate data for the df_prod_int method in the Tank
    class.

    This class defines the schema for validating production-related data in
    the Tank class. It ensures that the required fields are present and
    correctly typed for production data processing.
    """

    OIL_CUM: Series[float] = pa.Field(nullable=False)
    WATER_CUM: Series[float] = pa.Field(nullable=False)
    GAS_CUM: Series[float] = pa.Field(nullable=False)
    LIQ_CUM: Series[float] = pa.Field(nullable=False)
    WELL_BORE: Series[str] = pa.Field(nullable=False)
    START_DATETIME: Series[pd.Timestamp] = pa.Field(nullable=False)
    Tank: Series[str] = pa.Field(nullable=False)


class _DFMbalSchema(pa.DataFrameModel):
    Tank: Series[str] = pa.Field(nullable=False)
    START_DATETIME: Series[pd.Timestamp] = pa.Field(nullable=False)
    PRESSURE_DATUM: Series[float] = pa.Field(nullable=False)
    OIL_CUM_TANK: Series[float] = pa.Field(nullable=False)
    WATER_CUM_TANK: Series[float] = pa.Field(nullable=False)
    GAS_CUM_TANK: Series[float] = pa.Field(nullable=False)
    Bo: Series[float] = pa.Field(nullable=False)
    Bg: Series[float] = pa.Field(nullable=True)
    RS_bw: Series[float] = pa.Field(nullable=False)
    Bw: Series[float] = pa.Field(nullable=False)
    GOR: Series[float] = pa.Field(nullable=False)
    Time_Step: Series[float] = pa.Field(nullable=False)
    UW: Series[float] = pa.Field(nullable=False)
    Eo: Series[float] = pa.Field(nullable=False)
    Efw: Series[float] = pa.Field(nullable=False)


class Analysis(BaseModel):
    """Class to calculate POES graphically and analytically.

    It allows to project graphics:
        - DataFrame with necessary information to material balance
        - Campbell
        - Exploratory data analysis (EDA) through graphics
    """

    tank_class: Tank
    freq: str
    position: str
    smooth: Optional[bool]
    s: Optional[float]
    k: Optional[int]

    class Config:
        arbitrary_types_allowed = True

    def __init__(
            self,
            tank_class,
            freq: str,
            position: str,
            smooth: bool = False,
            k: int = 2,
            s: float = 10e5,
    ):
        """
        Args:
            tank_class (BaseModel): Instance of the Tank class.
            freq (str): Frequency of data for the material balance equation.
            position (str): Position of the frequency of the date.
            smooth (Optional[bool]): Determines if the user wants to adjust the
                data. Default is False.
            k (Optional[int]): Degree of the cubic spline. Default is 2.
            s (Optional[int]): Smoothing factor. Default is 10e5.
        """
        super().__init__(
            tank_class=tank_class, freq=freq, position=position, smooth=smooth,
            k=k, s=s
        )

    def _calc_uw(self) -> pd.DataFrame:
        """Calculates underground withdrawal (F) per well.

        This internal method computes the underground withdrawal for each well
        using the `underground_withdrawal()` function. It aggregates the results
        and returns them in a DataFrame format.

        Returns:
            df_uw: A DataFrame containing the underground withdrawal (F)
                information for each well.
        """

        # Call the internal methods that process production and pressure data
        df_press = self.tank_class.get_pressure_df()
        df_prod = self.tank_class.get_production_df()

        # Validate df_press and df_prod
        df_press_validate = pd.DataFrame(_PressSchema.validate(df_press))
        df_prod_validate = pd.DataFrame(_ProdSchema.validate(df_prod))

        # Calculate the accumulated production in the pressure dataframe,
        # based on the production dataframe.
        for col in [OIL_CUM_COL, WATER_CUM_COL, GAS_CUM_COL]:
            df_press_validate[col] = df_press_validate.apply(
                lambda x: interp_dates_row(
                    x,
                    DATE_COL,
                    df_prod_validate,
                    DATE_COL,
                    col,
                    WELL_COL,
                    WELL_COL,
                    left=0.0,
                ),
                axis=1,
            )
            # For wells not available in the production data frame,
            # fill nans with 0
            df_press_validate.fillna({col: 0.0}, inplace=True)

        uw_well = []  # Empty list to uw values
        for well, group in df_press_validate.groupby(WELL_COL):
            group[UW_COL] = underground_withdrawal(
                group,
                OIL_CUM_COL,
                WATER_CUM_COL,
                GAS_CUM_COL,
                OIL_FVF_COL,
                WATER_FVF_COL,
                GAS_FVF_COL,
                RS_COL,
                RS_W_COL,
            )
            uw_well.append(group)

        df_press_validate = pd.concat(uw_well, ignore_index=True)
        return df_press_validate

    def _pressure_vol_avg(self) -> pd.DataFrame:
        """Calculates the average pressure per tank.

        This internal method computes the average pressure for each tank using
        the `press_vol_avg()` function. It returns the results in a DataFrame
        format.

        Returns:
            df_press_avg: A DataFrame containing the average pressure for each
                tank.
        """
        # Encapsulation of DataFrame from internal private method

        df_press = self._calc_uw()
        df_press_avg = (
            df_press.groupby(TANK_COL)
            .apply(
                lambda g: pressure_vol_avg(
                    g,
                    WELL_COL,
                    DATE_COL,
                    PRESSURE_COL,
                    UW_COL,
                    self.freq,
                    self.position,
                )
            )
            .reset_index(0)
        )
        if self.smooth is False:
            df_press_avg[PRESSURE_COL] = df_press_avg[PRESSURE_COL].interpolate(
                method="linear"
            )
        else:
            df_press_avg["DAYS"] = (
                    df_press_avg[DATE_COL] - df_press_avg[DATE_COL].min()
            ).dt.days
            valid_data = df_press_avg.dropna(subset=[PRESSURE_COL])
            spline = UnivariateSpline(
                valid_data["DAYS"], valid_data[PRESSURE_COL], s=self.s, k=self.k
            )
            x_fit = np.linspace(
                min(df_press_avg["DAYS"]),
                max(df_press_avg["DAYS"]),
                len(df_press_avg[DATE_COL]),
            )
            y_fit = spline(x_fit)
            df_press_avg["AVG_PRESS"] = df_press_avg[PRESSURE_COL]
            df_press_avg[PRESSURE_COL] = y_fit

        return df_press_avg

    def mat_bal_df(self) -> pd.DataFrame:
        """Obtains the material balance parameters at a certain frequency.

        This method retrieves the material balance parameters for each tank at
        specified time intervals. It compiles the relevant data into a DataFrame
        for further analysis and reporting.

        Returns:
            mat_bal_df:
                - Tank: Name of the tank.
                - START_DATETIME: Date of the measurement.
                - PRESSURE_DATUM: Pressure value in psi.
                - OIL_CUM_TANK: Cumulative oil production.
                - WATER_CUM_TANK: Cumulative water production.
                - GAS_CUM_TANK: Cumulative gas production.
                - Bo: Oil volumetric factor.
                - Bg: Gas volumetric factor.
                - GOR: Gas-to-oil ratio.
                - Bw: Water volumetric factor.
                - Rs_bw: Water solubility.
                - Time_Step: Time lapses in days.
                - UW: Underground withdrawal.
                - Eo: Oil expansion.
                - Eg: Gas expansion.
                - Efw: Rock-fluid expansion.
                - Cumulative We: Cumulative influx of water.
        """
        # Encapsulation of DataFrame from internal private method
        avg = self._pressure_vol_avg()

        #  Validate df_prod from _prod_df_int
        prod = pd.DataFrame(_ProdSchema.validate(self.tank_class.
                                                 get_production_df()))

        # Linear interpolated of average pressure

        cols_input = [OIL_CUM_COL, WATER_CUM_COL, GAS_CUM_COL]
        cols_output = ["oil_vol", "water_vol", "gas_vol"]
        prod[cols_output] = (
            (prod.groupby(WELL_COL)[cols_input]).diff().fillna(prod[cols_input])
        )
        cols_group = [DATE_COL, TANK_COL, "oil_vol", "water_vol", "gas_vol"]
        df_tank = (
            prod[cols_group]
            .groupby(cols_group[0:2])
            .sum()
            .groupby(TANK_COL)
            .cumsum()
            .reset_index()
        )

        # Rename of columns of DataFrame
        df_tank.rename(
            columns={
                "oil_vol": OIL_CUM_COL,
                "water_vol": WATER_CUM_COL,
                "gas_vol": GAS_CUM_COL,
            },
            inplace=True,
        )

        oil_cum_per_tank = OIL_CUM_COL + "_TANK"
        water_cum_per_tank = WATER_CUM_COL + "_TANK"
        gas_cum_per_tank = GAS_CUM_COL + "_TANK"

        # Interpolated Cumulative production
        for col, cum_col in zip(
                [oil_cum_per_tank, water_cum_per_tank, gas_cum_per_tank],
                [OIL_CUM_COL, WATER_CUM_COL, GAS_CUM_COL],
        ):
            avg[col] = avg.apply(
                lambda g: interp_dates_row(
                    g, DATE_COL, df_tank, DATE_COL, cum_col, TANK_COL, TANK_COL
                ),
                axis=1,
            )

        # Sort by dates of DataFrame
        df_mbal = avg.sort_values(DATE_COL)

        # Interpolated PVT properties from pres_avg
        df_mbal[OIL_FVF_COL] = self.tank_class.oil_model.get_bo_at_press(
            df_mbal[PRESSURE_COL]
        )
        df_mbal[GAS_FVF_COL] = self.tank_class.oil_model.get_bg_at_press(
            df_mbal[PRESSURE_COL]
        )
        df_mbal[RS_COL] = self.tank_class.oil_model.get_rs_at_press(
            df_mbal[PRESSURE_COL]
        )

        # In case properties are calculated using correlations
        if (
                self.tank_class.water_model.salinity is not None
                and self.tank_class.water_model.temperature is not None
                and self.tank_class.water_model.unit is not None
        ):
            df_mbal[
                WATER_FVF_COL] = self.tank_class.water_model.get_bw_at_press(
                df_mbal[PRESSURE_COL]
            )
            df_mbal[RS_W_COL] = self.tank_class.water_model.get_rs_at_press(
                df_mbal[PRESSURE_COL]
            )

            # In case there are default values for Bw and Rs_w
        else:
            df_mbal[WATER_FVF_COL] = (self.tank_class.water_model.
                                      get_default_bw())
            df_mbal[RS_W_COL] = self.tank_class.water_model.get_default_rs()

        # Creation of time lapses columns
        first_time_lapse = pd.Timedelta(
            days=pd.to_timedelta(df_mbal[DATE_COL].diff().iloc[2],
                                 unit="D").days
        )
        df_mbal["Time_Step"] = first_time_lapse.days
        df_mbal["Time_Step"] = df_mbal["Time_Step"].cumsum()
        df_mbal[GAS_FVF_COL] = df_mbal[GAS_FVF_COL].fillna(0.0)

        # Calculated values of Eo, Eg, Efw and F columns
        mbal_term = ho_terms_equation(
            df_mbal,
            OIL_CUM_TANK,
            WATER_CUM_TANK,
            GAS_CUM_TANK,
            PRESSURE_COL,
            OIL_FVF_COL,
            GAS_FVF_COL,
            RS_COL,
            WATER_FVF_COL,
            RS_W_COL,
            self.tank_class.swo,
            self.tank_class.cw,
            self.tank_class.cf,
            float(self.tank_class.oil_model.get_bo_at_press(self.
                                                            tank_class.pi)),
            float(self.tank_class.oil_model.get_bg_at_press(self.
                                                            tank_class.pi)),
            float(self.tank_class.oil_model.get_bo_at_press(self.
                                                            tank_class.pi)),
            float(self.tank_class.oil_model.get_rs_at_press(self.
                                                            tank_class.pi)),
            self.tank_class.pi,
        )
        mbal_final_per_tank = mbal_term

        # Creation of WE value according to the aquifer model
        if self.tank_class.aquifer is None:
            mbal_final_per_tank[WE] = 0.0

        elif isinstance(self.tank_class.aquifer, Fetkovich):
            # If the aquifer instance is Fetkovich, take the pressure and -
            # time values that Fetkovich needs from mbal_final_per_tank
            pr = list(mbal_final_per_tank[PRESSURE_COL])
            time_step = list(mbal_final_per_tank["Time_Step"])
            self.tank_class.aquifer._set_pr_and_time_step(pr, time_step)
            df = self.tank_class.aquifer.we()
            mbal_final_per_tank = mbal_final_per_tank.join(df["Cumulative We"])

        elif isinstance(self.tank_class.aquifer, CarterTracy):
            # If the aquifer instance is Fetkovich, take the pressure and -
            # time values that Fetkovich needs from mbal_final_per_tank
            pr = list(mbal_final_per_tank[PRESSURE_COL])
            time_step = list(mbal_final_per_tank["Time_Step"])
            self.tank_class.aquifer._set_pr_and_time_step(pr, time_step)
            df = self.tank_class.aquifer.we()
            mbal_final_per_tank = mbal_final_per_tank.join(df["Cumulative We"])

        # final mbal DataFrame
        return mbal_final_per_tank

    # ---------------------- CAMPBELL GRAPH --------------------------------
    def campbell_plot(
            self,
            custom_line: bool = False,
            x1: float = None,
            y1: float = None,
            x2: float = None,
            y2: float = None,
    ) -> plt.Figure:
        """Generates a Campbell plot to visualize the energy contribution of
        the aquifer.

        This method creates a Campbell graph, which allows for a graphical
        representation of the energy contribution from the aquifer. Optionally,
        it can draw a custom line between two specified points on the plot.

        Parameters:
            custom_line (bool): If False, no custom line will be drawn. If True,
                a line will be drawn between the specified points (x1, y1) and
                (x2, y2).
            x1 (float): The x-coordinate of the first point for the custom line.
            y1 (float): The y-coordinate of the first point for the custom line.
            x2 (float): The x-coordinate of the second point for the custom
                line.
            y2 (float): The y-coordinate of the second point for the custom
                line.

        Returns:
            Campbell_Plot: A matplotlib Figure object containing the plot with
                the selected data.
        """
        mbal_df = self.mat_bal_df()
        y = mbal_df[UW_COL] / (mbal_df[OIL_EXP] + mbal_df[RES_EXP])
        x = mbal_df[OIL_CUM_TANK]
        data = pd.DataFrame({"Np": x, "F/Eo+Efw": y})
        fig, ax1 = plt.subplots()
        ax1.scatter(x, y)

        # Graph
        if custom_line is False:
            slope, intercept, r, p, se = stats.linregress(data["Np"],
                                                          data["F/Eo+Efw"])
            reg_line = (slope * data["Np"]) + intercept
            ax1.plot(data["Np"], reg_line, color="green",
                     label="Regression line")

        else:
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            x_values = np.linspace(min(data["Np"]), max(data["Np"]), 100)
            y_values = slope * x_values + intercept
            ax1.plot(x_values, y_values, color="red", label="Custom Line")

        ax1.set_xlabel("Np Cumulative Oil Production [MMStb]")
        ax1.set_ylabel("F/Eo+Efw")
        ax1.set_title("Campbell plot of " + str(self.tank_class.name_tank.
                                                replace("_", " ")))
        textstr = (
            "Graph that gives an "
            "\nidea of the energy "
            "\ncontribution of an aquifer"
        )
        props = dict(boxstyle="round", facecolor="grey", alpha=0.5)
        ax1.text(
            0.05,
            0.95,
            textstr,
            transform=ax1.transAxes,
            fontsize=9,
            verticalalignment="top",
            horizontalalignment="left",
            bbox=props,
        )
        ax1.legend(frameon=True, framealpha=0.9, loc="upper right")
        plt.grid(True, linestyle="--", alpha=0.7)

        formattery = FuncFormatter(lambda x, pos: "{:.1f}KM".format(x * 1e-9))
        ax1.yaxis.set_major_formatter(formattery)

        formatterx = FuncFormatter(lambda x, pos: "{:.1f}M".format(x * 1e-6))
        ax1.xaxis.set_major_formatter(formatterx)
        return fig

    def campbell_data(self) -> pd.DataFrame:
        """Retrieves the data required for generating a Campbell plot.

        This method calculates the necessary data points for creating a Campbell
        graph. It uses the material balance DataFrame generated by the
        `mat_bal_df` method to compute the required columns and returns them in
        a new DataFrame.

        Returns:
            Campbell_Data:
                - Np: Cumulative oil production.
                - F/Eo+Efw: Ratio of underground withdrawal to oil and
                    rock-fluid expansion.
        """
        mbal_df = self.mat_bal_df()
        y = mbal_df[UW_COL] / (mbal_df[OIL_EXP] + mbal_df[RES_EXP])
        x = mbal_df[OIL_CUM_TANK]
        data = pd.DataFrame({"Np": x, "F/Eo+Efw": y})
        return data

    # ------------------ HAVLENA AND ODEH METHOD ----------------------------
    def havlena_odeh_plot(
            self,
            custom_line: bool = False,
            x1: float = None,
            y1: float = None,
            x2: float = None,
            y2: float = None,
    ) -> plt.Figure:
        """Calculates results based on the Havlena and Odeh methods and displays
        a graph.

        This method generates a plot illustrating the relationship between
        underground withdrawal (F) and effective time (Et) as calculated using
        the Havlena and Odeh methods. Optionally, a custom line can be drawn
        between two specified points on the graph.

        Parameters:
            custom_line (bool): If False, no custom line will be drawn. If True,
                a line will be drawn between the specified points (x1, y1) and
                (x2, y2).
            x1 (float): The x-coordinate of the first point for the custom line.
            y1 (float): The y-coordinate of the first point for the custom line.
            x2 (float): The x-coordinate of the second point for the custom
                line.
            y2 (float): The y-coordinate of the second point for the custom
                line.

        Returns:
            Havlena&Odeh_Plot: A matplotlib Figure object containing the plot
                of underground withdrawal (F) versus effective time (Et).
        """
        name_aquifer = ""
        # Creation of WE value according to the aquifer model
        if self.tank_class.aquifer is None:
            name_aquifer = " without Aquifer"

        elif isinstance(self.tank_class.aquifer, Fetkovich):
            name_aquifer = " with Fetkovich Aquifer Model"

        elif isinstance(self.tank_class.aquifer, CarterTracy):
            name_aquifer = " with Carter Tracy Aquifer Model"

        # Data Processing
        mbal_df = self.mat_bal_df()
        y = mbal_df[UW_COL] - mbal_df[WE]
        x = mbal_df[OIL_EXP] + mbal_df[RES_EXP]
        data = pd.DataFrame({"Eo+Efw": x, "F-We": y})
        fig, ax2 = plt.subplots()
        ax2.scatter(data["Eo+Efw"], data["F-We"], color="blue")

        slope, intercept, r, p, se = stats.linregress(data["Eo+Efw"],
                                                      data["F-We"])

        # Graphic
        # Without points selected
        if custom_line is False:
            reg_line = (slope * data["Eo+Efw"]) + intercept
            ax2.plot(data["Eo+Efw"], reg_line, color="red",
                     label="Regression line")
            # Text in the graph
            textstr = "N [MMSTB]: {:.2f}".format(slope / 1000000)
            props = dict(boxstyle="round", facecolor="yellow", alpha=0.5)
            ax2.text(
                0.05,
                0.95,
                textstr,
                transform=ax2.transAxes,
                fontsize=10,
                verticalalignment="top",
                horizontalalignment="left",
                bbox=props,
            )
            ax2.legend(frameon=True, framealpha=0.9, loc="upper right")

        # With points selected
        else:
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            x_values = np.linspace(min(data["Eo+Efw"]), max(data["Eo+Efw"]),
                                   100)
            y_values = slope * x_values + intercept
            ax2.plot(x_values, y_values, color="green",
                     label="Custom Line")
            # Text in the graph
            textstr = "N [MMStb]: {:.2f}".format(slope / 1000000)
            props = dict(boxstyle="round", facecolor="yellow", alpha=0.5)
            ax2.text(
                0.05,
                0.95,
                textstr,
                transform=ax2.transAxes,
                fontsize=10,
                verticalalignment="top",
                horizontalalignment="left",
                bbox=props,
            )
            ax2.legend(frameon=True, framealpha=0.9, loc="upper right")

        ax2.set_xlabel("Eo+Efw")
        ax2.set_ylabel("F-We")
        ax2.set_title(
            "Havlena y Odeh plot of "
            + str(self.tank_class.name_tank.replace("_", " "))
            + name_aquifer
        )

        plt.grid(True, linestyle="--", alpha=0.7)

        # formatter for the axes in M
        formatter = FuncFormatter(lambda x, pos: "{:.2f}M".format(x * 1e-6))
        ax2.yaxis.set_major_formatter(formatter)
        return fig

    def havlena_oded_data(self) -> pd.DataFrame:
        """Calculates values based on the Havlena and Odeh methods and returns
        a DataFrame.

        This method computes the necessary values for the Havlena and Odeh
        methods and returns them in a DataFrame format. The resulting DataFrame
        contains two columns: "F-We" (underground withdrawal minus cumulative
        water influx) and "Eo+Efw" (oil expansion plus rock-fluid expansion).

        Returns:
            HO_Data:
                - F-We: Underground withdrawal minus cumulative water influx.
                - Eo+Efw: Oil expansion plus rock-fluid expansion.
        """
        mbal_df = self.mat_bal_df()
        y = mbal_df[UW_COL] - mbal_df[WE]
        x = mbal_df[OIL_EXP] + mbal_df[RES_EXP]
        data = pd.DataFrame({"Eo+Efw": x, "F-We": y})
        return data

    # ----------------------- ANALYTIC METHOD -------------------------------
    def analytic_method(
            self, poes: float, option: str
    ) -> Union[pd.DataFrame, plt.Figure]:
        """Calculates the POES through an inferred POES to match observed
        pressure.

        This method calculates the Petroleum Initially-in-Place (POES) by
        ensuring the best match between the observed pressure and the
        calculated pressure.

        The calculation is performed using the `calculated_pressure_fetkovich`
        and `calculated_pressure_carter_tracy` functions.

        Args:
            poes (float): Inferred POES (Petroleum-in-Place) value [MMSTB].
            option (str): Determines the type of result to be returned. Can be
                either "data" or "plot".

        Returns:
            Analytic_Method:
                - If option is "data", returns a pandas DataFrame containing the
                  Date, Observed Pressure, and Calculated Pressure.
                - If option is "plot", returns a matplotlib Figure object
                  containing a plot of the observed and calculated pressure over
                  time.

        Raises:
            ValueError: If the option is not "data" or "plot".
    """

        # Encapsulation of material balance DataFrame from mat_bal_df() method
        df = self.mat_bal_df()
        press_calc = []

        # name_tank of aquifer model:
        model_aq_name = ""
        # Fetkovich Aquifer Model
        if isinstance(self.tank_class.aquifer, Fetkovich):
            model_aq_name = "Fetkovich Aquifer Model"
            # Call the function to calculate the new pressure
            press_calc = calculated_pressure_fetkovich(
                df[OIL_CUM_TANK],
                df[WATER_CUM_TANK],
                self.tank_class.cf,
                self.tank_class.water_model.temperature,
                self.tank_class.water_model.salinity,
                self.tank_class.oil_model.data_pvt,
                self.tank_class.aquifer.aq_radius,
                self.tank_class.aquifer.res_radius,
                self.tank_class.aquifer.aq_thickness,
                self.tank_class.aquifer.aq_por,
                self.tank_class.aquifer.theta,
                self.tank_class.aquifer.k,
                self.tank_class.aquifer.water_visc,
                self.tank_class.pi,
                self.tank_class.swo,
                poes,
                PRESSURE_PVT_COL,
                OIL_FVF_COL,
            )

        # Carter Tracy Aquifer Model
        elif isinstance(self.tank_class.aquifer, CarterTracy):
            model_aq_name = "Carter Tracy Aquifer Model"
            press_calc = calculate_pressure_with_carter_tracy(
                df[OIL_CUM_TANK],
                df[WATER_CUM_TANK],
                self.tank_class.cf,
                self.tank_class.water_model.temperature,
                self.tank_class.water_model.salinity,
                self.tank_class.oil_model.data_pvt,
                self.tank_class.aquifer.res_radius,
                self.tank_class.aquifer.aq_thickness,
                self.tank_class.aquifer.aq_por,
                self.tank_class.aquifer.theta,
                self.tank_class.aquifer.aq_perm,
                self.tank_class.aquifer.water_visc,
                df["Time_Step"],
                self.tank_class.pi,
                self.tank_class.swo,
                poes,
                PRESSURE_PVT_COL,
                OIL_FVF_COL,
            )

        # Aad the first date to initial pressure
        dates = df[[DATE_COL, PRESSURE_COL]]
        new_date = df[DATE_COL].min() - pd.Timedelta(days=365)
        n_row = pd.DataFrame({DATE_COL: new_date}, index=[0])
        data = pd.concat([n_row, dates]).reset_index(drop=True)
        data.loc[0, PRESSURE_COL] = self.tank_class.pi

        # Add the Calculated Pressure column
        data["PRESS_CALC"] = press_calc

        if option == "data":
            return data[[DATE_COL, PRESSURE_COL, "PRESS_CALC"]]

        elif option == "plot":
            fig8, ax8 = plt.subplots(figsize=(15, 10))
            ax8.scatter(
                data[DATE_COL].dt.year, data[PRESSURE_COL],
                label="Observed Pressure"
            )
            ax8.plot(
                data[DATE_COL].dt.year, press_calc, c="g",
                label="Calculated Pressure"
            )
            plt.title(f"Pressure vs Time with {model_aq_name}",
                      fontsize=25)
            plt.xlabel("Time (Years)", fontsize=17)
            plt.ylabel("Pressure (PSI)", fontsize=17)
            ax8.set_ylim(0, 4000)
            plt.yticks(fontsize=15)
            plt.xticks(fontsize=15)
            ax8.grid(axis="both", color="lightgray", linestyle="dashed")
            plt.legend(fontsize=15)
            plt.gcf().autofmt_xdate()
            fig8.suptitle("ANALYTIC METHOD", fontsize=22)
            return fig8

        else:
            raise ValueError("Option no validate. Use 'data' or 'plot'.")

    # The following methods are to do an exploratory data analysis -
    # (EDA) of the Tank:
    # ---------------------- GRAPH SECTION ----------------------------
    def plot_cum_prod_well(self) -> plt.Figure:
        """Generates a graph of cumulative production per well in the tank.

        This method creates a plot that illustrates the cumulative production
        for each well associated with the tank. It provides a visual
        representation of the production performance over time.

        Returns:
            Figure: A matplotlib Figure object containing the graph of
                cumulative production per well in the tank.
        """
        # Production Data
        df_prod = self.tank_class.get_production_df()
        df_prod[DATE_COL] = pd.to_datetime(df_prod[DATE_COL])
        df_prod = df_prod.sort_values(by=DATE_COL)
        # Well Group
        df_prod_well = df_prod.groupby(WELL_COL)[
            [OIL_CUM_COL, WATER_CUM_COL]].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        well_ind = df_prod_well.index
        bar_witd = 0.35
        r1 = range(len(well_ind))
        r2 = [x + bar_witd for x in r1]

        ax.bar(
            r1,
            df_prod_well[OIL_CUM_COL],
            color="black",
            width=bar_witd,
            edgecolor="grey",
            label="Oil Cumulative",
        )
        ax.bar(
            r2,
            df_prod_well[WATER_CUM_COL],
            color="blue",
            width=bar_witd,
            edgecolor="grey",
            label="Water Cumulative",
        )

        ax.set_title(
            "Cumulative Production per Well - "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax.set_xlabel("Well", fontsize=14)
        ax.set_ylabel("Cumulative Production [Stb]", fontsize=14)
        ax.set_xticks([r + bar_witd / 2 for r in range(len(well_ind))])
        ax.set_xticklabels(
            well_ind,
            rotation=45,
            fontproperties=FontProperties(size=8.5, weight="bold"),
        )
        ax.legend(loc="upper left", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.7)

        # formatter for the axes in M
        formatter = FuncFormatter(lambda x, pos: "{:.0f}M".format(x * 1e-6))
        ax.yaxis.set_major_formatter(formatter)
        plt.tight_layout()
        return fig

    def plot_flow_rate_well(self) -> plt.Figure:
        """Generates a graph of flow rate versus time per well in the tank.

        This method creates a plot that displays the flow rate over time for
        each well associated with the tank. It provides a visual representation
        of the production rates for the wells.

        Returns:
            Figure: A matplotlib Figure object containing the graph of flow
                rate versus time per well in the tank.
        """
        # Production Data
        df_prod = self.tank_class.get_production_df()
        df_prod[DATE_COL] = pd.to_datetime(df_prod[DATE_COL])
        df_prod = df_prod.sort_values(by=DATE_COL)

        # days
        # df_prod["Days"] = df_prod[DATE_COL].diff().dt.days.fillna(0)
        # df_prod.loc[df_prod["Days"] == 0, "Days"] = 365

        # Calculate daily production rates from cumulative productions.
        df_prod[OIL_RATE_COL] = df_prod.groupby(WELL_COL)[
            OIL_CUM_COL].diff().fillna(0)
        df_prod[WATER_RATE_COL] = (
            df_prod.groupby(WELL_COL)[WATER_CUM_COL].diff().fillna(0)
        )

        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 12), sharex=True)

        wells = df_prod[WELL_COL].unique()
        colors = plt.cm.get_cmap("tab10", len(wells))

        # Plot of Oil Flow Rate
        for i, well in enumerate(wells):
            well_data = df_prod[df_prod[WELL_COL] == well]
            dates = well_data[DATE_COL]

            # Oil rate
            ax1.plot(dates, well_data[OIL_RATE_COL], label=f"{well}",
                     color=colors(i))
            ax1.set_title(
                "Oil Flow Rate vs Time by Well - " +
                str(self.tank_class.name_tank.replace("_", " ").upper()),
                fontsize=16,
            )
            ax1.set_ylabel("Flow Rate [Stb/year]", fontsize=14)
            ax1.legend(loc="upper left", fontsize=12)
            ax1.grid(True, linestyle="--", alpha=0.7)

            # Water rate
            ax2.plot(dates, well_data[WATER_RATE_COL], label=f"{well}",
                     color=colors(i))
            ax2.set_title(
                "Water Flow Rate vs Time by Well - " +
                str(self.tank_class.name_tank.replace("_", " ").upper()),
                fontsize=16,
            )
            ax2.set_ylabel("Flow Rate [Stb/year]", fontsize=14)
            ax2.set_xlabel("Date", fontsize=14)
            ax2.legend(loc="upper left", fontsize=12)
            ax2.grid(True, linestyle="--", alpha=0.7)

        fig.autofmt_xdate()
        plt.tight_layout()

        # Set Y-axis limit'
        y_max = max(df_prod[OIL_RATE_COL].max(), df_prod[WATER_RATE_COL].max())
        y_max = (y_max // 20000 + 1) * 20000

        ax1.set_ylim(0, y_max)
        ax1.set_yticks(np.arange(0, y_max + 1, 20000))

        ax2.set_ylim(0, y_max)
        ax2.set_yticks(np.arange(0, y_max + 1, 20000))

        # formatter for the axes in K
        formatter = FuncFormatter(lambda x, pos: "{:.0f}K".format(x * 1e-3))
        ax1.yaxis.set_major_formatter(formatter)

        # formatter for the axes in K
        formatter = FuncFormatter(lambda x, pos: "{:.0f}K".format(x * 1e-3))
        ax2.yaxis.set_major_formatter(formatter)
        return fig

    def plot_cum_prod_time(self) -> plt.Figure:
        """Generates a graph of cumulative oil and water production versus time.

        This method creates a plot that illustrates the cumulative production of
        oil and water over time. It provides a visual representation of the
        production trends for both fluids.

        Returns:
            Figure: A matplotlib Figure object containing the graph of
                cumulative oil and water production versus time.
        """
        # Average Pressure Data
        df_press_avg = self.mat_bal_df()
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        colors = ["black", "blue"]
        columns = [OIL_CUM_TANK, WATER_CUM_TANK]

        for i, col in enumerate(columns):
            ax1.plot(
                df_press_avg[DATE_COL], df_press_avg[col],
                color=colors[i], label=col
            )

        ax1.set_title(
            "Cumulative Production per Date - "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax1.set_xlabel("Date", fontsize=14)
        ax1.set_ylabel("Cumulative Production [MMSTB]", fontsize=14)
        ax1.legend(loc="upper left", fontsize=12)

        plt.gcf().autofmt_xdate()
        plt.grid(True, linestyle="--", alpha=0.7)

        # formatter for the axes in M
        formatter = FuncFormatter(lambda x, pos: "{:.1f}M".format(x * 1e-6))
        ax1.yaxis.set_major_formatter(formatter)
        return fig1

    def plot_cum_prod_tot_time(self) -> plt.Figure:
        """Generates a graph of total liquid cumulative production versus time.

        This method creates a plot that illustrates the total liquid cumulative
        production over time. It provides a visual representation of the overall
        production trends for liquids from the tank.

        Returns:
            Figure: A matplotlib Figure object containing the graph of total
                liquid cumulative production versus time.
        """
        # Average Pressure Data
        df_press_avg = self.mat_bal_df()

        fig2, ax2 = plt.subplots(figsize=(10, 6))
        colors = "skyblue"
        total_liquid = df_press_avg[OIL_CUM_TANK] + df_press_avg[WATER_CUM_TANK]

        ax2.plot(
            df_press_avg[DATE_COL], total_liquid, color=colors,
            label="Total Liquid"
        )

        ax2.set_title(
            "Cumulative Total Liquid Production per Date - "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax2.set_xlabel("Date", fontsize=14)
        ax2.set_ylabel("Cumulative Production [MMStb]", fontsize=14)
        ax2.legend(loc="upper left", fontsize=12)

        plt.gcf().autofmt_xdate()
        plt.grid(True, linestyle="--", alpha=0.7)

        # formatter for the axes in M
        formatter = FuncFormatter(lambda x, pos: "{:.1f}M".format(x * 1e-6))
        ax2.yaxis.set_major_formatter(formatter)
        return fig2

    def plot_press_time(self) -> plt.Figure:
        """Generates a graph of normal pressure versus time.

        This method creates a plot that illustrates the normal pressure
        in the tank over time. It provides a visual representation of the
        pressure trends, allowing for easy analysis of pressure changes.

        Returns:
            Figure: A matplotlib Figure object containing the graph of
                normal pressure versus time.
        """
        # Pressure Data
        df_press = self.tank_class.get_pressure_df()
        df_press[DATE_COL] = pd.to_datetime(df_press[DATE_COL])
        df_press = df_press.sort_values(by=DATE_COL)

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        color = "green"

        ax3.scatter(
            df_press[DATE_COL], df_press[PRESSURE_COL], color=color,
            label="Pressure"
        )

        ax3.set_title(
            "Pressure per Date - "
            + str(df_press[TANK_COL][0].replace("_", " ").upper()),
            fontsize=16,
        )
        ax3.set_xlabel("Date", fontsize=14)
        ax3.set_ylabel("Pressure [PSI]", fontsize=14)
        ax3.legend(loc="upper left", fontsize=12)

        plt.gcf().autofmt_xdate()
        plt.grid(True, linestyle="--", alpha=0.7)
        return fig3

    def plot_press_avg_time(self) -> plt.Figure:
        """Generates a graph of average pressure versus time.

        This method creates a plot that illustrates the average pressure 
        in the tank over time. It provides a visual representation of the 
        pressure trends, allowing for easy analysis of pressure changes.

        Returns:
            Figure: A matplotlib Figure object containing the graph of average 
                pressure versus time.
        """        # Average Pressure Data
        df_press_avg = self.mat_bal_df()
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        color = "red"
        if self.smooth is True:
            ax4.scatter(
                df_press_avg[DATE_COL],
                df_press_avg["AVG_PRESS"],
                color=color,
                label=" Avg Pressure",
            )
            ax4.plot(
                df_press_avg[DATE_COL],
                df_press_avg[PRESSURE_COL],
                color="blue",
                label="Avg Pressure (Smoothed)",
            )
        else:
            ax4.scatter(
                df_press_avg[DATE_COL],
                df_press_avg[PRESSURE_COL],
                color=color,
                label=" Avg Pressure",
            )

        ax4.set_title(
            "Pressure per Date - "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax4.set_xlabel("Date", fontsize=14)
        ax4.set_ylabel("Average Pressure[PSI]", fontsize=14)
        ax4.legend(loc="upper left", fontsize=12)

        plt.gcf().autofmt_xdate()
        plt.grid(True, linestyle="--", alpha=0.7)
        return fig4

    def plot_press_liq_cum(self) -> plt.Figure:
        """Generates a graph of pressure versus cumulative liquids (oil and 
        water).

        This method creates a plot that illustrates the relationship between 
        pressure and the cumulative production of liquids (oil and water) in 
        the tank. It provides a visual representation of how pressure changes 
        with increasing liquid production.

        Returns:
            Figure: A matplotlib Figure object containing the graph of pressure
                versus cumulative liquids (oil and water).
        """        # Pressure date with Cumulative Production
        df_press_cum = self._calc_uw()
        df_press_cum[DATE_COL] = pd.to_datetime(df_press_cum[DATE_COL])
        df_press_cum = df_press_cum.sort_values(by=PRESSURE_COL)

        fig6, ax6 = plt.subplots(figsize=(10, 6))
        colors = ["black", "blue"]
        columns = [OIL_CUM_COL, WATER_CUM_COL]

        for i, col in enumerate(columns):
            ax6.scatter(
                df_press_cum[PRESSURE_COL],
                df_press_cum[col],
                color=colors[i],
                label=col,
            )

        ax6.set_title(
            "Pressure vs Cumulative Production - "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax6.set_xlabel("Pressure", fontsize=14)
        ax6.set_ylabel("Cumulative Production", fontsize=14)
        ax6.legend(loc="upper left", fontsize=12)

        plt.gcf().autofmt_xdate()
        plt.grid(True, linestyle="--", alpha=0.7)

        # formatter for the axes in M
        formatter = FuncFormatter(lambda x, pos: "{:.1f}M".format(x * 1e-6))
        ax6.yaxis.set_major_formatter(formatter)
        return fig6

    def plot_press_avg_liq_cum(self) -> plt.Figure:
        """Generates a graph of average pressure versus cumulative liquids (oil
        and water).

        This method creates a plot that illustrates the relationship between
        average pressure and the cumulative production of liquids (oil and
        water) in the tank. It provides a visual representation of how average
        pressure changes with increasing liquid production.

        Returns:
            Figure: A matplotlib Figure object containing the graph of average
                pressure versus cumulative liquids (oil and water).
        """
        # Average Pressure Data
        df_press_avg = self.mat_bal_df()
        df_press_avg[DATE_COL] = pd.to_datetime(df_press_avg[DATE_COL])
        df_press_avg = df_press_avg.sort_values(by=PRESSURE_COL)
        fig7, ax7 = plt.subplots(figsize=(10, 6))
        colors = ["black", "blue"]
        columns = [OIL_CUM_TANK, WATER_CUM_TANK]

        for i, col in enumerate(columns):
            ax7.scatter(
                df_press_avg[PRESSURE_COL],
                df_press_avg[col],
                color=colors[i],
                label=col,
            )

        ax7.set_title(
            "Average Pressure vs Cumulative Production - "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax7.set_xlabel("Average Pressure", fontsize=14)
        ax7.set_ylabel("Cumulative Production", fontsize=14)
        ax7.legend(loc="upper left", fontsize=12)

        plt.gcf().autofmt_xdate()
        plt.grid(True, linestyle="--", alpha=0.7)

        # formatter for the axes in M
        formatter = FuncFormatter(lambda x, pos: "{:.1f}M".format(x * 1e-6))
        ax7.yaxis.set_major_formatter(formatter)
        return fig7

    def plot_flow_rate_tank(self) -> plt.Figure:
        """Generates a graph of flow rate versus time by tank.

        This method creates a plot that displays the flow rate over time for 
        each tank. It provides a visual representation of the production rates 
        for the tanks.

        Returns:
            Figure: A matplotlib Figure object containing the graph of flow rate 
                versus time by tank.
        """        # Production Data
        # Average Pressure Data
        df_prod = self.mat_bal_df()
        df_prod[DATE_COL] = pd.to_datetime(df_prod[DATE_COL])
        df_prod = df_prod.sort_values(by=DATE_COL)

        # Days
        # df_prod["Days"] = df_prod[DATE_COL].diff().dt.days.fillna(0)
        # df_prod.loc[df_prod["Days"] == 0, "Days"] = 365

        # Calculate daily production rates from cumulative productions.
        df_prod[OIL_RATE_COL] = df_prod[OIL_CUM_TANK].diff().fillna(0)
        df_prod[WATER_RATE_COL] = df_prod[WATER_CUM_TANK].diff().fillna(0)

        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 12), sharex=True)

        # Oil rate
        ax1.plot(
            df_prod[DATE_COL],
            df_prod[OIL_RATE_COL],
            color="black",
            label="Oil flow Rate",
        )
        ax1.set_title(
            "Oil Flow Rate vs Time by "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax1.set_ylabel("Flow Rate [Stb/year]", fontsize=14)
        ax1.legend(loc="upper left", fontsize=12)
        ax1.grid(True, linestyle="--", alpha=0.7)

        # Water rate
        ax2.plot(
            df_prod[DATE_COL],
            df_prod[WATER_RATE_COL],
            color="blue",
            label="Water flow rate",
        )
        ax2.set_title(
            "Water Flow Rate vs Time by "
            + str(self.tank_class.name_tank.replace("_", " ").upper()),
            fontsize=16,
        )
        ax2.set_ylabel("Flow Rate [Stb/year]", fontsize=14)
        ax2.set_xlabel("Date", fontsize=14)
        ax2.legend(loc="upper left", fontsize=12)
        ax2.grid(True, linestyle="--", alpha=0.7)

        # formatter for the axes in K
        formatter = FuncFormatter(lambda x, pos: "{:.0f}K".format(x * 1e-3))
        ax1.yaxis.set_major_formatter(formatter)

        # formatter for the axes in K
        formatter = FuncFormatter(lambda x, pos: "{:.0f}K".format(x * 1e-3))
        ax2.yaxis.set_major_formatter(formatter)

        fig.autofmt_xdate()
        plt.tight_layout()

        return fig
