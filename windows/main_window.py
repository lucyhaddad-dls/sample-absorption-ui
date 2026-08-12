# have Sample making utils at top level?

from PySide6.QtWidgets import QMainWindow
from sample_mass_calcs.xas_sample import XRaySample
from .input_window import InputWindow
from sample_mass_calcs.measurements import Measurement

class SampleBuilder:
    """
    Convienience class for holding sample-related properties.

    Attrs:
        sample_dict (dict): Dict. of sample parameters `{"name": {"val", "dtype"}}`
        sample (XRaySample): Sample object.
    
    Methods:
        make_sample(): Make `sample`.
        on_change(key, value): Update `sample_dict`.
    """
    def __init__(self):
        self.sample_dict = {
                "formula": {"val": "Cu", "dtype": str},
                "absorber": {"val": "Cu", "dtype": str},
                "edge": {"val": "K", "dtype":str},
                "density": {"val": None, "dtype":float},
                "area": {"val": None, "dtype":float},
                "mass": {"val": None, "dtype":float},
                "thickness": {"val": None, "dtype":float},
                "mu_total": {"val": 2.6, "dtype":float},
                "mass_unit": {"val": "g", "dtype":str},
                "length_unit": {"val": "cm", "dtype":str},
                "energy_unit": {"val": "gev", "dtype":str}
                }
        
        self.make_sample()

    def make_sample(self):
        values = {k: v["val"] for k, v in self.sample_dict.items()}
        self.sample = XRaySample(**values)

    def on_unit_change(self, unit_name:str, unit_type:str):
        setattr(self.sample, unit_name, unit_type)
        self.sample_dict[unit_name]["val"] = unit_type


    def on_value_change(self, key:str, value:str,
                        remake_sample:bool=False):
        """
        For a change of any sample related values \
        remake `sample_dict` and `sample` object.
        """
        dtype = self.sample_dict[key]["dtype"]
        if value is not None:
            self.sample_dict[key]["val"] = dtype(value)
        else:
            self.sample_dict[key]["val"] = None
 
        if remake_sample is True:
            self.make_sample()
        else:
            measurement = getattr(self.sample, key)
            if hasattr(measurement, "value"):
                if value is not None:
                    measurement.value = dtype(value)
                else: measurement.value = None
            else:
                if value is not None:
                    measurement = dtype(value)
                else: measurement = None
            setattr(self.sample, key, measurement)

    
    def get_name_and_unit(self, name:str)\
                ->tuple[str|None, str|None]:
        """
        Get value and unit from given a name.

        Returns
            value (str | None): Value of `name`.
            unit (Unit | str | None): Unit of `name`.
        """

        measurement = getattr(self.sample, name)
        if hasattr(measurement, "unit"):
            unit = measurement.unit
            value = measurement.value
        else:
            value = measurement
            unit = None
        return value, unit


class MainWindow(QMainWindow):
    """
    Main window for app, all sample information \
    lives here.
    """
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 300, 1000, 600)

        self.setWindowTitle("MAIN WINDOW")

        self.sample = SampleBuilder()
        self.input_window = InputWindow(self)
        self.setCentralWidget(self.input_window)

        self.show()