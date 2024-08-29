import pandas as pd
import numpy as np
from open_fdd.air_handling_unit.faults.fault_condition import (
    FaultCondition,
    MissingColumnError,
    InvalidParameterError,
)
import operator
import sys


class FaultConditionOne(FaultCondition):
    """Class provides the definitions for Fault Condition 1.
    AHU low duct static pressure fan fault.
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.vfd_speed_percent_err_thres = dict_.get(
            "VFD_SPEED_PERCENT_ERR_THRES", None
        )
        self.vfd_speed_percent_max = dict_.get("VFD_SPEED_PERCENT_MAX", None)
        self.duct_static_inches_err_thres = dict_.get(
            "DUCT_STATIC_INCHES_ERR_THRES", None
        )

        # Validate that threshold parameters are floats
        for param, value in [
            ("vfd_speed_percent_err_thres", self.vfd_speed_percent_err_thres),
            ("vfd_speed_percent_max", self.vfd_speed_percent_max),
            ("duct_static_inches_err_thres", self.duct_static_inches_err_thres),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.duct_static_col = dict_.get("DUCT_STATIC_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.duct_static_setpoint_col = dict_.get("DUCT_STATIC_SETPOINT_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc1_flag = 1 if (DSP < DPSP - εDSP) and (VFDSPD >= VFDSPD_max - εVFDSPD) "
            "for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 1: Duct static too low at fan at full speed \n"
        )
        self.required_column_description = "Required inputs are the duct static pressure, setpoint, and supply fan VFD speed \n"
        self.error_string = f"One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.duct_static_col,
            self.supply_vfd_speed_col,
            self.duct_static_setpoint_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Called from IPython to print out."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [self.supply_vfd_speed_col]
            self.check_analog_pct(df, columns_to_check)

            df["static_check_"] = (
                df[self.duct_static_col]
                < df[self.duct_static_setpoint_col] - self.duct_static_inches_err_thres
            )
            df["fan_check_"] = (
                df[self.supply_vfd_speed_col]
                >= self.vfd_speed_percent_max - self.vfd_speed_percent_err_thres
            )

            # Combined condition check
            df["combined_check"] = df["static_check_"] & df["fan_check_"]

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc1_flag"] = (rolling_sum == self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["static_check_", "fan_check_", "combined_check"], inplace=True
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionTwo(FaultCondition):
    """Class provides the definitions for Fault Condition 2.
    Mix temperature too low; should be between outside and return air.
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.mix_degf_err_thres = dict_.get("MIX_DEGF_ERR_THRES", None)
        self.return_degf_err_thres = dict_.get("RETURN_DEGF_ERR_THRES", None)
        self.outdoor_degf_err_thres = dict_.get("OUTDOOR_DEGF_ERR_THRES", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("mix_degf_err_thres", self.mix_degf_err_thres),
            ("return_degf_err_thres", self.return_degf_err_thres),
            ("outdoor_degf_err_thres", self.outdoor_degf_err_thres),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.mat_col = dict_.get("MAT_COL", None)
        self.rat_col = dict_.get("RAT_COL", None)
        self.oat_col = dict_.get("OAT_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc2_flag = 1 if (MAT + εMAT < min(RAT - εRAT, OAT - εOAT)) and (VFDSPD > 0) "
            "for N consecutive values else 0 \n"
        )
        self.description_string = "Fault Condition 2: Mix temperature too low; should be between outside and return air \n"
        self.required_column_description = (
            "Required inputs are the mix air temperature, return air temperature, outside air temperature, "
            "and supply fan VFD speed \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.mat_col,
            self.rat_col,
            self.oat_col,
            self.supply_vfd_speed_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [self.supply_vfd_speed_col]
            self.check_analog_pct(df, columns_to_check)

            # Fault condition-specific checks / flags
            df["mat_check"] = df[self.mat_col] + self.mix_degf_err_thres
            df["temp_min_check"] = np.minimum(
                df[self.rat_col] - self.return_degf_err_thres,
                df[self.oat_col] - self.outdoor_degf_err_thres,
            )

            df["combined_check"] = (df["mat_check"] < df["temp_min_check"]) & (
                df[self.supply_vfd_speed_col] > 0.01
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc2_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["mat_check", "temp_min_check", "combined_check"], inplace=True
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionThree(FaultCondition):
    """Class provides the definitions for Fault Condition 3.
    Mix temperature too high; should be between outside and return air.
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.mix_degf_err_thres = dict_.get("MIX_DEGF_ERR_THRES", None)
        self.return_degf_err_thres = dict_.get("RETURN_DEGF_ERR_THRES", None)
        self.outdoor_degf_err_thres = dict_.get("OUTDOOR_DEGF_ERR_THRES", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("mix_degf_err_thres", self.mix_degf_err_thres),
            ("return_degf_err_thres", self.return_degf_err_thres),
            ("outdoor_degf_err_thres", self.outdoor_degf_err_thres),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.mat_col = dict_.get("MAT_COL", None)
        self.rat_col = dict_.get("RAT_COL", None)
        self.oat_col = dict_.get("OAT_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc3_flag = 1 if (MAT - εMAT > max(RAT + εRAT, OAT + εOAT)) and (VFDSPD > 0) "
            "for N consecutive values else 0 \n"
        )
        self.description_string = "Fault Condition 3: Mix temperature too high; should be between outside and return air \n"
        self.required_column_description = (
            "Required inputs are the mix air temperature, return air temperature, outside air temperature, "
            "and supply fan VFD speed \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.mat_col,
            self.rat_col,
            self.oat_col,
            self.supply_vfd_speed_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [self.supply_vfd_speed_col]
            self.check_analog_pct(df, columns_to_check)

            # Fault condition-specific checks / flags
            df["mat_check"] = df[self.mat_col] - self.mix_degf_err_thres
            df["temp_max_check"] = np.maximum(
                df[self.rat_col] + self.return_degf_err_thres,
                df[self.oat_col] + self.outdoor_degf_err_thres,
            )

            df["combined_check"] = (df["mat_check"] > df["temp_max_check"]) & (
                df[self.supply_vfd_speed_col] > 0.01
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc3_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["mat_check", "temp_max_check", "combined_check"], inplace=True
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionFour(FaultCondition):
    """Class provides the definitions for Fault Condition 4.

    This fault flags excessive operating states on the AHU
    if it's hunting between heating, econ, econ+mech, and
    a mech clg modes. The code counts how many operating
    changes in an hour and will throw a fault if there is
    excessive OS changes to flag control sys hunting.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc4.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.delta_os_max = dict_.get("DELTA_OS_MAX", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)

        # Validate that delta_os_max can be either a float or an integer
        # if not isinstance(self.delta_os_max, (float, int)):
        if not isinstance(self.delta_os_max, (int)):
            raise InvalidParameterError(
                f"The parameter 'delta_os_max' should be an integer data type, but got {type(self.delta_os_max).__name__}."
            )

        # Validate that ahu_min_oa_dpr is a float
        if not isinstance(self.ahu_min_oa_dpr, float):
            raise InvalidParameterError(
                f"The parameter 'ahu_min_oa_dpr' should be a float, but got {type(self.ahu_min_oa_dpr).__name__}."
            )

        # Other attributes
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.heating_sig_col = dict_.get("HEATING_SIG_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)

        self.equation_string = (
            "fc4_flag = 1 if excessive mode changes (> δOS_max) occur "
            "within an hour across heating, econ, econ+mech, mech clg, and min OA modes \n"
        )
        self.description_string = "Fault Condition 4: Excessive AHU operating state changes detected (hunting behavior) \n"
        self.required_column_description = (
            "Required inputs are the economizer signal, supply fan VFD speed, "
            "and optionally heating and cooling signals \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns, making heating and cooling optional
        self.required_columns = [
            self.economizer_sig_col,
            self.supply_vfd_speed_col,
        ]

        # If heating or cooling columns are provided, add them to the required columns
        if self.heating_sig_col:
            self.required_columns.append(self.heating_sig_col)
        if self.cooling_sig_col:
            self.required_columns.append(self.cooling_sig_col)

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )
        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            # If the optional columns are not present, create them with all values set to 0.0
            if self.heating_sig_col not in df.columns:
                df[self.heating_sig_col] = 0.0
            if self.cooling_sig_col not in df.columns:
                df[self.cooling_sig_col] = 0.0

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.heating_sig_col,
                self.cooling_sig_col,
                self.supply_vfd_speed_col,
            ]

            for col in columns_to_check:
                self.check_analog_pct(df, [col])

            print("=" * 50)
            print("Warning: The program is in FC4 and resampling the data")
            print("to compute AHU OS state changes per hour")
            print("to flag any hunting issue")
            print("and this usually takes a while to run...")
            print("=" * 50)

            sys.stdout.flush()

            # AHU htg only mode based on OA damper @ min oa and only htg pid/vlv modulating
            df["heating_mode"] = (
                (df[self.heating_sig_col] > 0)
                & (df[self.cooling_sig_col] == 0)
                & (df[self.supply_vfd_speed_col] > 0)
                & (df[self.economizer_sig_col] == self.ahu_min_oa_dpr)
            )

            # AHU econ only mode based on OA damper modulating and clg htg = zero
            df["econ_only_cooling_mode"] = (
                (df[self.heating_sig_col] == 0)
                & (df[self.cooling_sig_col] == 0)
                & (df[self.supply_vfd_speed_col] > 0)
                & (df[self.economizer_sig_col] > self.ahu_min_oa_dpr)
            )

            # AHU econ+mech clg mode based on OA damper modulating for cooling and clg pid/vlv modulating
            df["econ_plus_mech_cooling_mode"] = (
                (df[self.heating_sig_col] == 0)
                & (df[self.cooling_sig_col] > 0)
                & (df[self.supply_vfd_speed_col] > 0)
                & (df[self.economizer_sig_col] > self.ahu_min_oa_dpr)
            )

            # AHU mech mode based on OA damper @ min OA and clg pid/vlv modulating
            df["mech_cooling_only_mode"] = (
                (df[self.heating_sig_col] == 0)
                & (df[self.cooling_sig_col] > 0)
                & (df[self.supply_vfd_speed_col] > 0)
                & (df[self.economizer_sig_col] == self.ahu_min_oa_dpr)
            )

            # AHU minimum OA mode without heating or cooling (ventilation mode)
            df["min_oa_mode_only"] = (
                (df[self.heating_sig_col] == 0)
                & (df[self.cooling_sig_col] == 0)
                & (df[self.supply_vfd_speed_col] > 0)
                & (df[self.economizer_sig_col] == self.ahu_min_oa_dpr)
            )

            # Fill non-finite values with zero or drop them
            df = df.fillna(0)

            df = df.astype(int)
            df = df.resample("60min").apply(lambda x: (x.eq(1) & x.shift().ne(1)).sum())

            df["fc4_flag"] = (
                df[df.columns].gt(self.delta_os_max).any(axis=1).astype(int)
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionFive(FaultCondition):
    """Class provides the definitions for Fault Condition 5.
    SAT too low; should be higher than MAT in HTG MODE
    --Broken heating valve or other mechanical issue
    related to heat valve not working as designed
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.mix_degf_err_thres = dict_.get("MIX_DEGF_ERR_THRES", None)
        self.supply_degf_err_thres = dict_.get("SUPPLY_DEGF_ERR_THRES", None)
        self.delta_t_supply_fan = dict_.get("DELTA_T_SUPPLY_FAN", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("mix_degf_err_thres", self.mix_degf_err_thres),
            ("supply_degf_err_thres", self.supply_degf_err_thres),
            ("delta_t_supply_fan", self.delta_t_supply_fan),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.mat_col = dict_.get("MAT_COL", None)
        self.sat_col = dict_.get("SAT_COL", None)
        self.heating_sig_col = dict_.get("HEATING_SIG_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc5_flag = 1 if (SAT + εSAT <= MAT - εMAT + ΔT_supply_fan) and "
            "(heating signal > 0) and (VFDSPD > 0) for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 5: SAT too low; should be higher than MAT in HTG MODE, "
            "potential broken heating valve or mechanical issue \n"
        )
        self.required_column_description = (
            "Required inputs are the mixed air temperature, supply air temperature, "
            "heating signal, and supply fan VFD speed \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.mat_col,
            self.sat_col,
            self.heating_sig_col,
            self.supply_vfd_speed_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [self.supply_vfd_speed_col, self.heating_sig_col]

            for col in columns_to_check:
                self.check_analog_pct(df, [col])

            df["sat_check"] = df[self.sat_col] + self.supply_degf_err_thres
            df["mat_check"] = (
                df[self.mat_col] - self.mix_degf_err_thres + self.delta_t_supply_fan
            )

            df["combined_check"] = (
                (df["sat_check"] <= df["mat_check"])
                & (df[self.heating_sig_col] > 0.01)
                & (df[self.supply_vfd_speed_col] > 0.01)
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc5_flag"] = (rolling_sum == self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(columns=["mat_check", "sat_check", "combined_check"], inplace=True)

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionSix(FaultCondition):
    """Class provides the definitions for Fault Condition 6.

    This fault related to knowing the design air flow for
    ventilation AHU_MIN_CFM_DESIGN which comes from the
    design mech engineered records where then the fault
    tries to calculate that based on totalized measured
    AHU air flow and outside air fraction calc from
    AHU temp sensors. The fault could flag issues where
    flow stations are either not in calibration, temp
    sensors used in the OA frac calc, or possibly the AHU
    not bringing in design air flow when not operating in
    economizer free cooling modes.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc6.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.airflow_err_thres = dict_.get("AIRFLOW_ERR_THRES", None)
        self.ahu_min_oa_cfm_design = dict_.get("AHU_MIN_OA_CFM_DESIGN", None)
        self.outdoor_degf_err_thres = dict_.get("OUTDOOR_DEGF_ERR_THRES", None)
        self.return_degf_err_thres = dict_.get("RETURN_DEGF_ERR_THRES", None)
        self.oat_rat_delta_min = dict_.get("OAT_RAT_DELTA_MIN", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)

        if not isinstance(self.ahu_min_oa_cfm_design, (float, int)):
            raise InvalidParameterError(
                f"The parameter 'ahu_min_oa_cfm_design' should be an integer data type, but got {type(self.ahu_min_oa_cfm_design).__name__}."
            )

        # Validate that threshold parameters are floats
        for param, value in [
            ("airflow_err_thres", self.airflow_err_thres),
            ("outdoor_degf_err_thres", self.outdoor_degf_err_thres),
            ("return_degf_err_thres", self.return_degf_err_thres),
            ("oat_rat_delta_min", self.oat_rat_delta_min),
            ("ahu_min_oa_dpr", self.ahu_min_oa_dpr),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.supply_fan_air_volume_col = dict_.get("SUPPLY_FAN_AIR_VOLUME_COL", None)
        self.mat_col = dict_.get("MAT_COL", None)
        self.oat_col = dict_.get("OAT_COL", None)
        self.rat_col = dict_.get("RAT_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.heating_sig_col = dict_.get("HEATING_SIG_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc6_flag = 1 if |OA_frac_calc - OA_min| > airflow_err_thres "
            "in non-economizer modes, considering htg and mech clg OS \n"
        )
        self.description_string = (
            "Fault Condition 6: Issues detected with OA fraction calculation or AHU "
            "not maintaining design air flow in non-economizer conditions \n"
        )
        self.required_column_description = (
            "Required inputs are the supply fan air volume, mixed air temperature, "
            "outside air temperature, return air temperature, and VFD speed. "
            "Optional inputs include economizer signal, heating signal, and cooling signal \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.supply_fan_air_volume_col,
            self.mat_col,
            self.oat_col,
            self.rat_col,
            self.supply_vfd_speed_col,
            self.economizer_sig_col,
            self.heating_sig_col,
            self.cooling_sig_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.supply_vfd_speed_col,
                self.economizer_sig_col,
                self.heating_sig_col,
                self.cooling_sig_col,
            ]

            for col in columns_to_check:
                self.check_analog_pct(df, [col])

            # Create helper columns
            df["rat_minus_oat"] = abs(df[self.rat_col] - df[self.oat_col])
            df["percent_oa_calc"] = (df[self.mat_col] - df[self.rat_col]) / (
                df[self.oat_col] - df[self.rat_col]
            )

            # Weed out any negative values
            df["percent_oa_calc"] = df["percent_oa_calc"].apply(
                lambda x: x if x > 0 else 0
            )

            df["perc_OAmin"] = (
                self.ahu_min_oa_cfm_design / df[self.supply_fan_air_volume_col]
            )

            df["percent_oa_calc_minus_perc_OAmin"] = abs(
                df["percent_oa_calc"] - df["perc_OAmin"]
            )

            df["combined_check"] = operator.or_(
                # OS 1 htg mode
                (
                    (df["rat_minus_oat"] >= self.oat_rat_delta_min)
                    & (df["percent_oa_calc_minus_perc_OAmin"] > self.airflow_err_thres)
                )
                # Verify AHU is running in OS 1 htg mode in min OA
                & (
                    (df[self.heating_sig_col] > 0.0)
                    & (df[self.supply_vfd_speed_col] > 0.0)
                ),  # OR
                # OS 4 mech clg mode
                (
                    (df["rat_minus_oat"] >= self.oat_rat_delta_min)
                    & (df["percent_oa_calc_minus_perc_OAmin"] > self.airflow_err_thres)
                )
                # Verify AHU is running in OS 4 clg mode in min OA
                & (df[self.heating_sig_col] == 0.0)
                & (df[self.cooling_sig_col] > 0.0)
                & (df[self.supply_vfd_speed_col] > 0.0)
                & (df[self.economizer_sig_col] == self.ahu_min_oa_dpr),
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc6_flag"] = (rolling_sum == self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=[
                    "rat_minus_oat",
                    "percent_oa_calc",
                    "perc_OAmin",
                    "percent_oa_calc_minus_perc_OAmin",
                    "combined_check",
                ],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionSeven(FaultCondition):
    """Class provides the definitions for Fault Condition 7.
    Very similar to FC 13 but uses heating valve.
    Supply air temperature too low in full heating.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc7.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.supply_degf_err_thres = dict_.get("SUPPLY_DEGF_ERR_THRES", None)

        # Validate that threshold parameters are floats
        if not isinstance(self.supply_degf_err_thres, float):
            raise InvalidParameterError(
                f"The parameter 'supply_degf_err_thres' should be a float, but got {type(self.supply_degf_err_thres).__name__}."
            )

        # Other attributes
        self.sat_col = dict_.get("SAT_COL", None)
        self.sat_setpoint_col = dict_.get("SAT_SETPOINT_COL", None)
        self.heating_sig_col = dict_.get("HEATING_SIG_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc7_flag = 1 if SAT < (SATSP - εSAT) in full heating mode "
            "and VFD speed > 0 for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 7: Supply air temperature too low in full heating mode "
            "with heating valve fully open \n"
        )
        self.required_column_description = (
            "Required inputs are the supply air temperature, supply air temperature setpoint, "
            "heating signal, and supply fan VFD speed \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.sat_col,
            self.sat_setpoint_col,
            self.heating_sig_col,
            self.supply_vfd_speed_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [self.supply_vfd_speed_col, self.heating_sig_col]
            self.check_analog_pct(df, columns_to_check)

            # Fault condition-specific checks / flags
            df["sat_check"] = df[self.sat_setpoint_col] - self.supply_degf_err_thres

            df["combined_check"] = (
                (df[self.sat_col] < df["sat_check"])
                & (df[self.heating_sig_col] > 0.9)
                & (df[self.supply_vfd_speed_col] > 0)
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc7_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(columns=["sat_check", "combined_check"], inplace=True)

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionEight(FaultCondition):
    """Class provides the definitions for Fault Condition 8.
    Supply air temperature and mix air temperature should
    be approx equal in economizer mode.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc8.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.delta_t_supply_fan = dict_.get("DELTA_T_SUPPLY_FAN", None)
        self.mix_degf_err_thres = dict_.get("MIX_DEGF_ERR_THRES", None)
        self.supply_degf_err_thres = dict_.get("SUPPLY_DEGF_ERR_THRES", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("delta_t_supply_fan", self.delta_t_supply_fan),
            ("mix_degf_err_thres", self.mix_degf_err_thres),
            ("supply_degf_err_thres", self.supply_degf_err_thres),
            ("ahu_min_oa_dpr", self.ahu_min_oa_dpr),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.mat_col = dict_.get("MAT_COL", None)
        self.sat_col = dict_.get("SAT_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc8_flag = 1 if |SAT - MAT - ΔT_fan| > √(εSAT² + εMAT²) "
            "in economizer mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 8: Supply air temperature and mixed air temperature should "
            "be approximately equal in economizer mode \n"
        )
        self.required_column_description = (
            "Required inputs are the mixed air temperature, supply air temperature, "
            "economizer signal, and cooling signal \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.mat_col,
            self.sat_col,
            self.economizer_sig_col,
            self.cooling_sig_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            df["sat_fan_mat"] = abs(
                df[self.sat_col] - self.delta_t_supply_fan - df[self.mat_col]
            )
            df["sat_mat_sqrted"] = np.sqrt(
                self.supply_degf_err_thres**2 + self.mix_degf_err_thres**2
            )

            df["combined_check"] = (
                (df["sat_fan_mat"] > df["sat_mat_sqrted"])
                & (df[self.economizer_sig_col] > self.ahu_min_oa_dpr)
                & (df[self.cooling_sig_col] < 0.1)
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc8_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["sat_fan_mat", "sat_mat_sqrted", "combined_check"],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionNine(FaultCondition):
    """Class provides the definitions for Fault Condition 9.
    Outside air temperature too high in free cooling without
    additional mechanical cooling in economizer mode.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc9.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.delta_t_supply_fan = dict_.get("DELTA_T_SUPPLY_FAN", None)
        self.outdoor_degf_err_thres = dict_.get("OUTDOOR_DEGF_ERR_THRES", None)
        self.supply_degf_err_thres = dict_.get("SUPPLY_DEGF_ERR_THRES", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("delta_t_supply_fan", self.delta_t_supply_fan),
            ("outdoor_degf_err_thres", self.outdoor_degf_err_thres),
            ("supply_degf_err_thres", self.supply_degf_err_thres),
            ("ahu_min_oa_dpr", self.ahu_min_oa_dpr),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.sat_setpoint_col = dict_.get("SAT_SETPOINT_COL", None)
        self.oat_col = dict_.get("OAT_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc9_flag = 1 if OAT > (SATSP - ΔT_fan + εSAT) "
            "in free cooling mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 9: Outside air temperature too high in free cooling mode "
            "without additional mechanical cooling in economizer mode \n"
        )
        self.required_column_description = (
            "Required inputs are the supply air temperature setpoint, outside air temperature, "
            "cooling signal, and economizer signal \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.sat_setpoint_col,
            self.oat_col,
            self.cooling_sig_col,
            self.economizer_sig_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            # Create helper columns
            df["oat_minus_oaterror"] = df[self.oat_col] - self.outdoor_degf_err_thres
            df["satsp_delta_saterr"] = (
                df[self.sat_setpoint_col]
                - self.delta_t_supply_fan
                + self.supply_degf_err_thres
            )

            df["combined_check"] = (
                (df["oat_minus_oaterror"] > df["satsp_delta_saterr"])
                # verify AHU is in OS2 only free cooling mode
                & (df[self.economizer_sig_col] > self.ahu_min_oa_dpr)
                & (df[self.cooling_sig_col] < 0.1)
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc9_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["oat_minus_oaterror", "satsp_delta_saterr", "combined_check"],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionTen(FaultCondition):
    """Class provides the definitions for Fault Condition 10.
    Outdoor air temperature and mix air temperature should
    be approx equal in economizer plus mech cooling mode.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc10.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.outdoor_degf_err_thres = dict_.get("OUTDOOR_DEGF_ERR_THRES", None)
        self.mix_degf_err_thres = dict_.get("MIX_DEGF_ERR_THRES", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("outdoor_degf_err_thres", self.outdoor_degf_err_thres),
            ("mix_degf_err_thres", self.mix_degf_err_thres),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.oat_col = dict_.get("OAT_COL", None)
        self.mat_col = dict_.get("MAT_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc10_flag = 1 if |OAT - MAT| > √(εOAT² + εMAT²) in "
            "economizer + mech cooling mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 10: Outdoor air temperature and mixed air temperature "
            "should be approximately equal in economizer plus mechanical cooling mode \n"
        )
        self.required_column_description = (
            "Required inputs are the outside air temperature, mixed air temperature, "
            "cooling signal, and economizer signal \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.oat_col,
            self.mat_col,
            self.cooling_sig_col,
            self.economizer_sig_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            df["abs_mat_minus_oat"] = abs(df[self.mat_col] - df[self.oat_col])
            df["mat_oat_sqrted"] = np.sqrt(
                self.mix_degf_err_thres**2 + self.outdoor_degf_err_thres**2
            )

            df["combined_check"] = (
                (df["abs_mat_minus_oat"] > df["mat_oat_sqrted"])
                # verify AHU is running in OS 3 clg mode in min OA
                & (df[self.cooling_sig_col] > 0.01)
                & (df[self.economizer_sig_col] > 0.9)
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc10_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["abs_mat_minus_oat", "mat_oat_sqrted", "combined_check"],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionEleven(FaultCondition):
    """Class provides the definitions for Fault Condition 11.
    Outside air temperature too low for 100% outdoor
    air cooling in economizer cooling mode.
    Economizer performance fault

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc11.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.delta_t_supply_fan = dict_.get("DELTA_T_SUPPLY_FAN", None)
        self.outdoor_degf_err_thres = dict_.get("OUTDOOR_DEGF_ERR_THRES", None)
        self.supply_degf_err_thres = dict_.get("SUPPLY_DEGF_ERR_THRES", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("delta_t_supply_fan", self.delta_t_supply_fan),
            ("outdoor_degf_err_thres", self.outdoor_degf_err_thres),
            ("supply_degf_err_thres", self.supply_degf_err_thres),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.sat_setpoint_col = dict_.get("SAT_SETPOINT_COL", None)
        self.oat_col = dict_.get("OAT_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc11_flag = 1 if OAT < (SATSP - ΔT_fan - εSAT) in "
            "economizer cooling mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 11: Outside air temperature too low for 100% outdoor air cooling "
            "in economizer cooling mode (Economizer performance fault) \n"
        )
        self.required_column_description = (
            "Required inputs are the supply air temperature setpoint, outside air temperature, "
            "cooling signal, and economizer signal \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.sat_setpoint_col,
            self.oat_col,
            self.cooling_sig_col,
            self.economizer_sig_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            df["oat_plus_oaterror"] = df[self.oat_col] + self.outdoor_degf_err_thres
            df["satsp_delta_saterr"] = (
                df[self.sat_setpoint_col]
                - self.delta_t_supply_fan
                - self.supply_degf_err_thres
            )

            df["combined_check"] = (
                (df["oat_plus_oaterror"] < df["satsp_delta_saterr"])
                # verify ahu is running in OS 3 clg mode in 100 OA
                & (df[self.cooling_sig_col] > 0.01)
                & (df[self.economizer_sig_col] > 0.9)
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc11_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["oat_plus_oaterror", "satsp_delta_saterr", "combined_check"],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionTwelve(FaultCondition):
    """Class provides the definitions for Fault Condition 12.
    Supply air temperature too high; should be less than
    mix air temperature in economizer plus mech cooling mode.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc12.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.delta_t_supply_fan = dict_.get("DELTA_T_SUPPLY_FAN", None)
        self.mix_degf_err_thres = dict_.get("MIX_DEGF_ERR_THRES", None)
        self.supply_degf_err_thres = dict_.get("SUPPLY_DEGF_ERR_THRES", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("delta_t_supply_fan", self.delta_t_supply_fan),
            ("mix_degf_err_thres", self.mix_degf_err_thres),
            ("supply_degf_err_thres", self.supply_degf_err_thres),
            ("ahu_min_oa_dpr", self.ahu_min_oa_dpr),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.sat_col = dict_.get("SAT_COL", None)
        self.mat_col = dict_.get("MAT_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc12_flag = 1 if SAT >= MAT + εMAT in "
            "economizer + mech cooling mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 12: Supply air temperature too high; should be less than "
            "mixed air temperature in economizer plus mechanical cooling mode \n"
        )
        self.required_column_description = (
            "Required inputs are the supply air temperature, mixed air temperature, "
            "cooling signal, and economizer signal \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.sat_col,
            self.mat_col,
            self.cooling_sig_col,
            self.economizer_sig_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            # Create helper columns
            df["sat_minus_saterr_delta_supply_fan"] = (
                df[self.sat_col] - self.supply_degf_err_thres - self.delta_t_supply_fan
            )
            df["mat_plus_materr"] = df[self.mat_col] + self.mix_degf_err_thres

            df["combined_check"] = operator.or_(
                # OS4 AHU state clg @ min OA
                (df["sat_minus_saterr_delta_supply_fan"] > df["mat_plus_materr"])
                # verify AHU in OS4 mode
                & (df[self.cooling_sig_col] > 0.01)
                & (df[self.economizer_sig_col] == self.ahu_min_oa_dpr),  # OR
                (df["sat_minus_saterr_delta_supply_fan"] > df["mat_plus_materr"])
                # verify AHU is running in OS 3 clg mode in 100 OA
                & (df[self.cooling_sig_col] > 0.01)
                & (df[self.economizer_sig_col] > 0.9),
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc12_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=[
                    "sat_minus_saterr_delta_supply_fan",
                    "mat_plus_materr",
                    "combined_check",
                ],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionThirteen(FaultCondition):
    """Class provides the definitions for Fault Condition 13.
    Supply air temperature too high in full cooling
    in economizer plus mech cooling mode

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc13.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.supply_degf_err_thres = dict_.get("SUPPLY_DEGF_ERR_THRES", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("supply_degf_err_thres", self.supply_degf_err_thres),
            ("ahu_min_oa_dpr", self.ahu_min_oa_dpr),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.sat_col = dict_.get("SAT_COL", None)
        self.sat_setpoint_col = dict_.get("SAT_SETPOINT_COL", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc13_flag = 1 if SAT > (SATSP + εSAT) in "
            "economizer + mech cooling mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 13: Supply air temperature too high in full cooling "
            "in economizer plus mechanical cooling mode \n"
        )
        self.required_column_description = (
            "Required inputs are the supply air temperature, supply air temperature setpoint, "
            "cooling signal, and economizer signal \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.sat_col,
            self.sat_setpoint_col,
            self.cooling_sig_col,
            self.economizer_sig_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            # Create helper columns
            df["sat_greater_than_sp_calc"] = (
                df[self.sat_col]
                > df[self.sat_setpoint_col] + self.supply_degf_err_thres
            )

            df["combined_check"] = operator.or_(
                ((df["sat_greater_than_sp_calc"]))
                # OS4 AHU state clg @ min OA
                & (df[self.cooling_sig_col] > 0.01)
                & (df[self.economizer_sig_col] == self.ahu_min_oa_dpr),  # OR
                ((df["sat_greater_than_sp_calc"]))
                # verify ahu is running in OS 3 clg mode in 100 OA
                & (df[self.cooling_sig_col] > 0.01)
                & (df[self.economizer_sig_col] > 0.9),
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc13_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["sat_greater_than_sp_calc", "combined_check"],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionFourteen(FaultCondition):
    """Class provides the definitions for Fault Condition 14.
    Temperature drop across inactive cooling coil.
    Requires coil leaving temp sensor.

    py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc14.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.delta_t_supply_fan = dict_.get("DELTA_T_SUPPLY_FAN", None)
        self.coil_temp_enter_err_thres = dict_.get("COIL_TEMP_ENTER_ERR_THRES", None)
        self.coil_temp_leav_err_thres = dict_.get("COIL_TEMP_LEAV_ERR_THRES", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("delta_t_supply_fan", self.delta_t_supply_fan),
            ("coil_temp_enter_err_thres", self.coil_temp_enter_err_thres),
            ("coil_temp_leav_err_thres", self.coil_temp_leav_err_thres),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.clg_coil_enter_temp_col = dict_.get("CLG_COIL_ENTER_TEMP_COL", None)
        self.clg_coil_leave_temp_col = dict_.get("CLG_COIL_LEAVE_TEMP_COL", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.heating_sig_col = dict_.get("HEATING_SIG_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc14_flag = 1 if ΔT_coil >= √(εcoil_enter² + εcoil_leave²) + ΔT_fan "
            "in inactive cooling coil mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 14: Temperature drop across inactive cooling coil "
            "detected, requiring coil leaving temperature sensor \n"
        )
        self.required_column_description = (
            "Required inputs are the cooling coil entering temperature, cooling coil leaving temperature, "
            "cooling signal, heating signal, economizer signal, and supply fan VFD speed \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.clg_coil_enter_temp_col,
            self.clg_coil_leave_temp_col,
            self.cooling_sig_col,
            self.heating_sig_col,
            self.economizer_sig_col,
            self.supply_vfd_speed_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
                self.heating_sig_col,
                self.supply_vfd_speed_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            # Create helper columns
            df["clg_delta_temp"] = (
                df[self.clg_coil_enter_temp_col] - df[self.clg_coil_leave_temp_col]
            )

            df["clg_delta_sqrted"] = (
                np.sqrt(
                    self.coil_temp_enter_err_thres**2 + self.coil_temp_leav_err_thres**2
                )
                + self.delta_t_supply_fan
            )

            df["combined_check"] = operator.or_(
                (df["clg_delta_temp"] >= df["clg_delta_sqrted"])
                # verify AHU is in OS2 only free cooling mode
                & (df[self.economizer_sig_col] > self.ahu_min_oa_dpr)
                & (df[self.cooling_sig_col] < 0.1),  # OR
                (df["clg_delta_temp"] >= df["clg_delta_sqrted"])
                # verify AHU is running in OS 1 at near full heat
                & (df[self.heating_sig_col] > 0.0)
                & (df[self.supply_vfd_speed_col] > 0.0),
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc14_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["clg_delta_temp", "clg_delta_sqrted", "combined_check"],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e


class FaultConditionFifteen(FaultCondition):
    """Class provides the definitions for Fault Condition 15.
    Temperature rise across inactive heating coil.
    Requires coil leaving temp sensor.

    > py -3.12 -m pytest open_fdd/tests/ahu/test_ahu_fc15.py -rP -s
    """

    def __init__(self, dict_):
        super().__init__()

        # Threshold parameters
        self.delta_supply_fan = dict_.get("DELTA_SUPPLY_FAN", None)
        self.coil_temp_enter_err_thres = dict_.get("COIL_TEMP_ENTER_ERR_THRES", None)
        self.coil_temp_leav_err_thres = dict_.get("COIL_TEMP_LEAV_ERR_THRES", None)

        # Validate that threshold parameters are floats
        for param, value in [
            ("delta_supply_fan", self.delta_supply_fan),
            ("coil_temp_enter_err_thres", self.coil_temp_enter_err_thres),
            ("coil_temp_leav_err_thres", self.coil_temp_leav_err_thres),
        ]:
            if not isinstance(value, float):
                raise InvalidParameterError(
                    f"The parameter '{param}' should be a float, but got {type(value).__name__}."
                )

        # Other attributes
        self.htg_coil_enter_temp_col = dict_.get("HTG_COIL_ENTER_TEMP_COL", None)
        self.htg_coil_leave_temp_col = dict_.get("HTG_COIL_LEAVE_TEMP_COL", None)
        self.ahu_min_oa_dpr = dict_.get("AHU_MIN_OA_DPR", None)
        self.cooling_sig_col = dict_.get("COOLING_SIG_COL", None)
        self.heating_sig_col = dict_.get("HEATING_SIG_COL", None)
        self.economizer_sig_col = dict_.get("ECONOMIZER_SIG_COL", None)
        self.supply_vfd_speed_col = dict_.get("SUPPLY_VFD_SPEED_COL", None)
        self.troubleshoot_mode = dict_.get("TROUBLESHOOT_MODE", False)
        self.rolling_window_size = dict_.get("ROLLING_WINDOW_SIZE", None)

        self.equation_string = (
            "fc15_flag = 1 if ΔT_coil >= √(εcoil_enter² + εcoil_leave²) + ΔT_fan "
            "in inactive heating coil mode for N consecutive values else 0 \n"
        )
        self.description_string = (
            "Fault Condition 15: Temperature rise across inactive heating coil "
            "detected, requiring coil leaving temperature sensor \n"
        )
        self.required_column_description = (
            "Required inputs are the heating coil entering temperature, heating coil leaving temperature, "
            "cooling signal, heating signal, economizer signal, and supply fan VFD speed \n"
        )
        self.error_string = "One or more required columns are missing or None \n"

        self.set_attributes(dict_)

        # Set required columns specific to this fault condition
        self.required_columns = [
            self.htg_coil_enter_temp_col,
            self.htg_coil_leave_temp_col,
            self.cooling_sig_col,
            self.heating_sig_col,
            self.economizer_sig_col,
            self.supply_vfd_speed_col,
        ]

        # Check if any of the required columns are None
        if any(col is None for col in self.required_columns):
            raise MissingColumnError(
                f"{self.error_string}"
                f"{self.equation_string}"
                f"{self.description_string}"
                f"{self.required_column_description}"
                f"{self.required_columns}"
            )

        # Ensure all required columns are strings
        self.required_columns = [str(col) for col in self.required_columns]

        self.mapped_columns = (
            f"Your config dictionary is mapped as: {', '.join(self.required_columns)}"
        )

    def get_required_columns(self) -> str:
        """Returns a string representation of the required columns."""
        return (
            f"{self.equation_string}"
            f"{self.description_string}"
            f"{self.required_column_description}"
            f"{self.mapped_columns}"
        )

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Ensure all required columns are present
            self.check_required_columns(df)

            if self.troubleshoot_mode:
                self.troubleshoot_cols(df)

            # Check analog outputs [data with units of %] are floats only
            columns_to_check = [
                self.economizer_sig_col,
                self.cooling_sig_col,
                self.heating_sig_col,
                self.supply_vfd_speed_col,
            ]
            self.check_analog_pct(df, columns_to_check)

            # Create helper columns
            df["htg_delta_temp"] = (
                df[self.htg_coil_leave_temp_col] - df[self.htg_coil_enter_temp_col]
            )

            df["htg_delta_sqrted"] = (
                np.sqrt(
                    self.coil_temp_enter_err_thres**2 + self.coil_temp_leav_err_thres**2
                )
                + self.delta_supply_fan
            )

            df["combined_check"] = (
                (
                    (df["htg_delta_temp"] >= df["htg_delta_sqrted"])
                    # verify AHU is in OS2 only free cooling mode
                    & (df[self.economizer_sig_col] > self.ahu_min_oa_dpr)
                    & (df[self.cooling_sig_col] < 0.1)
                )
                | (
                    (df["htg_delta_temp"] >= df["htg_delta_sqrted"])
                    # OS4 AHU state clg @ min OA
                    & (df[self.cooling_sig_col] > 0.01)
                    & (df[self.economizer_sig_col] == self.ahu_min_oa_dpr)
                )
                | (
                    (df["htg_delta_temp"] >= df["htg_delta_sqrted"])
                    # verify AHU is running in OS 3 clg mode in 100 OA
                    & (df[self.cooling_sig_col] > 0.01)
                    & (df[self.economizer_sig_col] > 0.9)
                )
            )

            # Rolling sum to count consecutive trues
            rolling_sum = (
                df["combined_check"].rolling(window=self.rolling_window_size).sum()
            )
            # Set flag to 1 if rolling sum equals the window size
            df["fc15_flag"] = (rolling_sum >= self.rolling_window_size).astype(int)

            if self.troubleshoot_mode:
                print("Troubleshoot mode enabled - not removing helper columns")
                sys.stdout.flush()

            # Optionally remove temporary columns
            df.drop(
                columns=["htg_delta_temp", "htg_delta_sqrted", "combined_check"],
                inplace=True,
            )

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
        except InvalidParameterError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
