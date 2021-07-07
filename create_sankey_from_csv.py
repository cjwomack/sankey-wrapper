import pandas as pd
import sankey_wrapper_plotly as swp


if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    swp.plot_sankey(df)
