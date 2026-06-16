def create_features(df):

    # Green vs Built Ratio
    df["Green_Built_Ratio"] = (
        df["NDVI"] /
        (df["NDBI"] + 0.01)
    )

    # Cooling Potential
    df["Cooling_Potential"] = (
        df["NDVI"] *
        df["Humidity"]
    )

    # Heat Exposure Index
    df["Heat_Exposure_Index"] = (
        df["NDBI"] *
        df["PopulationDensity"]
    )

    return df