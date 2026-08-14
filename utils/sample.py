from sample_mass_calcs.xas_sample import XRaySample

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
    # setting all to str/None to make input text field making easier.
        self.sample_dict = {
                "formula": {"val": "Cu", "dtype": str},
                "absorber": {"val": "Cu", "dtype": str},
                "edge": {"val": "K", "dtype":str},
                "density": {"val": None, "dtype":float},
                "area": {"val": None, "dtype":float},
                "mass": {"val": None, "dtype":float},
                "thickness": {"val": None, "dtype":float},
                "mu_total": {"val": "2.6", "dtype":float},
                "mass_unit": {"val": "g", "dtype":str},
                "length_unit": {"val": "cm", "dtype":str},
                "energy_unit": {"val": "gev", "dtype":str}
                }

        # to do on sample mass maths end: fix unit conversions - cm to um seems to be wrong.
        
        self.make_sample()

    def sample_dict_to_kwargs(self)->dict:
        """
        Convert `sample_dict` to suitable kwargs for \
        creating an `XRaySample` object.
        """
        kwargs = {}
        for k, v in self.sample_dict.items():
            if v["val"] is None or v["val"] == "None":
                kwargs[k] = None
            else:
                kwargs[k] = v["dtype"](v["val"])
        return kwargs

    def make_sample(self):
        """
        Remake `sample` with current `sample_dict` items.
        """
        values = self.sample_dict_to_kwargs()
        self.sample = XRaySample(**values)

    def update_sample_dict(self):
        """
        Update `sample_dict` such that it is \
        up-to-date with the current `sample` object.
        """
        for k in self.sample_dict.keys():
            val = getattr(self.sample, k)
            if val is None:
                tmp = self.sample_dict[k]
                tmp["val"] = None
                self.sample_dict[k] = tmp
            elif hasattr(val, "value"):
                self.sample_dict[k]["val"] = str(val.value)
            else:
                self.sample_dict[k]["val"] = str(val)

    def on_value_change(self, 
                        name:str,
                        value:str,
                        remake_sample:bool=False):
        """
        Update `sample_dict` and `sample` with new values. \\
        If `remake_sample = True` then a new `sample` object \
        will be created.
        """

        dtype = self.sample_dict[name]["dtype"]

        measurement = getattr(self.sample, name)

        if hasattr(measurement, "unit"):
            try:
                measurement.value = dtype(value)
            except:
                measurement.value = None
        else:
            try:
                measurement = dtype(value)
            except: measurement = None

        setattr(self.sample, name, measurement)

        self.update_sample_dict()

        if remake_sample is True:
            self.make_sample()

        self.calculate_thickness()
        self.calculate_mass()
    
    def get_name_and_unit(self, name:str)\
        ->tuple[str|None, str|None]:
        """
        Get value and unit from given a name.
        
        Returns
            tuple (tuple): tuple containing:
                value (str | None): Value of `name`.
                unit (Unit | str | None): Unit of `name`.
        """
        measurement = getattr(self.sample, name)
        if hasattr(measurement, "unit"):
            unit = measurement.unit; value = measurement.value
        else:
            unit = None; value = measurement
        return value, unit

    def calculate_thickness(self):
        """
        If sample density is known, calculate sample thickness.
        """
        if self.sample.density.value is not None:
            self.sample.calculate_thickness()

    def calculate_mass(self):
        """
        If sample area and sample density (+ thickness) are known, calculate sample mass.
        """
        if self.sample.area.value is not None and self.sample.density.value is not None:
            self.sample.calculate_mass()