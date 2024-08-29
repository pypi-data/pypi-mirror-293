import pandas as pd
import numpy as np
from open_fdd.air_handling_unit.faults.fault_condition import (
    FaultCondition,
    MissingColumnError,
)
import sys


class FaultConditionFifteen(FaultCondition):
    """Class provides the definitions for Fault Condition 15.
    Temperature rise across inactive heating coil.
    Requires coil leaving temp sensor.
    """

    def __init__(self, dict_):
        super().__init__()
        self.delta_supply_fan = float
        self.coil_temp_enter_err_thres = float
        self.coil_temp_leav_err_thres = float
        self.htg_coil_enter_temp_col = str
        self.htg_coil_leave_temp_col = str
        self.ahu_min_oa_dpr = float
        self.cooling_sig_col = str
        self.heating_sig_col = str
        self.economizer_sig_col = str
        self.supply_vfd_speed_col = str
        self.troubleshoot_mode = bool  # default to False
        self.rolling_window_size = int

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
        self.error_string = f"One or more required columns are missing or None \n"

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
                del df["htg_delta_temp"]
                del df["htg_delta_sqrted"]
                del df["combined_check"]

            return df

        except MissingColumnError as e:
            print(f"Error: {e.message}")
            sys.stdout.flush()
            raise e
