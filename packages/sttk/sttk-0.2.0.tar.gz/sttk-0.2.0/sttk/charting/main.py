import pandas as pd
import sttk.charting.indicators as ind
import sttk.charting.plot as plot


def plot_chart(
    path_to_csv: str = "",
    show_chart: bool = True,
    indicators: list = None,
    theme: str = "light",
):

    # Ensure indicators is a list
    if indicators is None:
        indicators = []

    # Load the historical market data
    historical_market_data = pd.read_csv(
        path_to_csv, usecols=["Date", "Open", "High", "Low", "Close"]
    )
    historical_market_data["Date"] = pd.to_datetime(historical_market_data["Date"])

    # Apply indicators if any are provided
    if indicators:
        # Iterate over each row using iterrows
        for i, row in historical_market_data.iterrows():
            for indicator in indicators:
                indicator.apply(historical_market_data, i)

    # Show the chart if required
    if show_chart:
        plot.print_chart(historical_market_data, indicators, theme=theme)


if __name__ == "__main__":

    quickstart_example = [
        ind.PeriodHigh(50, linewidth=0.5),
        ind.PeriodLow(50, linewidth=0.5),
        ind.RSI(14, linewidth=0.7, position="top"),
        ind.SimpleMovingAverage(50, linewidth=0.5),
    ]

    plot_chart(
        "../../sttk-data/ABR_historical_2023-01-01_2023-12-31_1d.csv",
        indicators=quickstart_example,
        theme="dark",
    )
