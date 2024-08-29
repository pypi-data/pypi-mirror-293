import numpy as np


class Indicator:
    """Base class for all indicators."""

    def apply(self, dataframe, index):
        raise NotImplementedError("Subclasses should implement this method.")

    def plot_info(self, theme):
        """Returns a list of dictionaries containing plot info for this indicator."""
        raise NotImplementedError("Subclasses should implement this method.")


class BaseIndicator(Indicator):
    """Base class for all indicators with common functionality."""

    def __init__(
        self,
        column_name,
        linewidth=0.5,
        subplot=False,
        subplot_scale=0.5,
        position="bottom",
        y_axis_range=None,
        light_theme_color="black",
        dark_theme_color="white",
        label="",
        parent_indicator=None,  # New parameter to allow overlaying on another indicator
    ):
        self.column_name = column_name
        self.linewidth = linewidth
        self.subplot = subplot
        self.subplot_scale = subplot_scale
        self.position = position
        self.y_axis_range = y_axis_range
        self.light_theme_color = light_theme_color
        self.dark_theme_color = dark_theme_color
        self.label = label
        self.parent_indicator = parent_indicator  # Store parent indicator

    def plot_info(self, theme):
        color = self.light_theme_color if theme == "light" else self.dark_theme_color
        return [
            {
                "column": self.column_name,
                "color": color,
                "label": self.label,
                "linewidth": self.linewidth,
                "subplot": self.subplot,
                "subplot_scale": self.subplot_scale,
                "position": self.position,
                "y_axis_range": self.y_axis_range,
                "parent_indicator": self.parent_indicator,  # Include parent indicator info
            }
        ]


class PeriodHigh(BaseIndicator):
    def __init__(
        self,
        period,
        linewidth=0.5,
        subplot=False,
        subplot_scale=0.5,
        position="bottom",
        y_axis_range=None,
    ):
        column_name = f"{period}_Period_High"
        super().__init__(
            column_name,
            linewidth,
            subplot,
            subplot_scale,
            position,
            y_axis_range,
            light_theme_color="red",
            dark_theme_color="orange",
            label=f"{period}-Period High",
        )
        self.period = period

    def apply(self, dataframe, index):
        if index >= self.period - 1:
            dataframe.at[index, self.column_name] = dataframe["High"][
                index - self.period + 1 : index + 1
            ].max()
        else:
            dataframe.at[index, self.column_name] = np.nan


class PeriodLow(BaseIndicator):
    def __init__(
        self,
        period,
        linewidth=0.5,
        subplot=False,
        subplot_scale=0.5,
        position="bottom",
        y_axis_range=None,
    ):
        column_name = f"{period}_Period_Low"
        super().__init__(
            column_name,
            linewidth,
            subplot,
            subplot_scale,
            position,
            y_axis_range,
            light_theme_color="blue",
            dark_theme_color="cyan",
            label=f"{period}-Period Low",
        )
        self.period = period

    def apply(self, dataframe, index):
        if index >= self.period - 1:
            dataframe.at[index, self.column_name] = dataframe["Low"][
                index - self.period + 1 : index + 1
            ].min()
        else:
            dataframe.at[index, self.column_name] = np.nan


class SimpleMovingAverage(BaseIndicator):
    def __init__(
        self,
        period,
        apply_to="Close",
        linewidth=0.5,
        subplot=False,
        subplot_scale=0.5,
        position="bottom",
        y_axis_range=None,
    ):
        column_name = f"{period}_Period_Moving_Avg"
        super().__init__(
            column_name,
            linewidth,
            subplot,
            subplot_scale,
            position,
            y_axis_range,
            light_theme_color="green",
            dark_theme_color="lime",
            label=f"{period}-Period Moving Avg",
        )
        self.period = period
        self.price_column = apply_to

    def apply(self, dataframe, index):
        if index >= self.period - 1:
            dataframe.at[index, self.column_name] = dataframe[self.price_column][
                index - self.period + 1 : index + 1
            ].mean()
        else:
            dataframe.at[index, self.column_name] = np.nan


class RSI(BaseIndicator):
    def __init__(
        self,
        period,
        price_column="Close",
        linewidth=0.5,
        subplot=True,
        subplot_scale=0.5,
        position="bottom",
        y_axis_range=(0, 100),
    ):
        column_name = f"RSI_{period}"
        super().__init__(
            column_name,
            linewidth,
            subplot,
            subplot_scale,
            position,
            y_axis_range,
            light_theme_color="purple",
            dark_theme_color="magenta",
            label=f"{period}-Period RSI",
        )
        self.period = period
        self.price_column = price_column

    def apply(self, dataframe, index):
        delta = dataframe[self.price_column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        dataframe[self.column_name] = 100 - (100 / (1 + rs))
