import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter


def print_chart(
    backtest_dataframe: pd.DataFrame,
    indicators=None,
    dynamic_aspect_ratio=True,
    y_axis_density=10,
    x_axis_density=20,
    theme="light",
):
    if indicators is None:
        indicators = []

    # Theme settings
    if theme == "dark":
        background_color = "#181818"
        text_color = "#FFFFFF"
        grid_color = "#444444"
        grid_linewidth = 0.3
    else:
        background_color = "#FFFFFF"
        text_color = "#000000"
        grid_color = "#CCCCCC"
        grid_linewidth = 0.1

    # Sort the DataFrame by the 'Date' column
    backtest_dataframe = backtest_dataframe.sort_values("Date")
    backtest_dataframe["Index"] = backtest_dataframe.index

    # Separate indicators into main plot and subplots, including those with a parent_indicator
    main_plot_indicators = []
    top_subplots = []
    bottom_subplots = []
    subplot_overlays = {}  # New dictionary to handle overlays on subplots

    for indicator in indicators:
        for plot_data in indicator.plot_info(theme=theme):
            parent_indicator = plot_data.get("parent_indicator")
            if parent_indicator:
                if parent_indicator not in subplot_overlays:
                    subplot_overlays[parent_indicator] = []
                subplot_overlays[parent_indicator].append(plot_data)
            else:
                if plot_data.get("subplot", False):
                    if plot_data.get("position", "bottom") == "top":
                        top_subplots.append(plot_data)
                    else:
                        bottom_subplots.append(plot_data)
                else:
                    main_plot_indicators.append(plot_data)

    # Combine top and bottom subplots
    subplot_indicators = top_subplots + bottom_subplots

    # Calculate the total height ratios
    top_ratios = [plot_data.get("subplot_scale", 0.5) for plot_data in top_subplots]
    bottom_ratios = [
        plot_data.get("subplot_scale", 0.5) for plot_data in bottom_subplots
    ]
    total_height_ratios = top_ratios + [1] + bottom_ratios

    # Aspect ratio for the main plot is 16:9, so calculate the base height
    base_width = 16
    base_height = 9

    # Calculate the overall height for the figure based on subplot_scale
    if dynamic_aspect_ratio:
        total_height = base_height * (1 + sum(top_ratios) + sum(bottom_ratios))
    else:
        total_height = base_height

    # Create subplots with adjustable heights
    fig, axs = plt.subplots(
        len(total_height_ratios),
        1,
        figsize=(base_width, total_height),
        dpi=300,
        sharex=True,
        gridspec_kw={"height_ratios": total_height_ratios},
    )

    # Adjust the space between plots
    plt.subplots_adjust(hspace=0)  # Remove space between subplots

    # If there's only one subplot, `axs` will not be a list, so make it a list
    if len(total_height_ratios) == 1:
        axs = [axs]

    # Set background and text colors
    fig.patch.set_facecolor(background_color)
    for ax in axs:
        ax.set_facecolor(background_color)

    # Plot the top subplots
    for i, plot_data in enumerate(top_subplots):
        ax = axs[i]
        _plot_data_on_ax(
            backtest_dataframe,
            ax,
            plot_data,
            subplot_overlays,
            text_color,
            grid_color,
            grid_linewidth,
            y_axis_density,
        )

    # Plot the main plot (price, etc.)
    main_ax = axs[len(top_subplots)]
    main_ax.vlines(
        backtest_dataframe["Index"],
        backtest_dataframe["Low"],
        backtest_dataframe["High"],
        color="black" if theme == "light" else "white",
        linewidth=0.5,
    )

    for plot_data in main_plot_indicators:
        _plot_data_on_ax(
            backtest_dataframe,
            main_ax,
            plot_data,
            subplot_overlays,
            text_color,
            grid_color,
            grid_linewidth,
            y_axis_density,
        )

    # Add legend to the main plot
    handles, labels = main_ax.get_legend_handles_labels()
    if labels:
        main_ax.legend(
            fontsize=6,
            facecolor=background_color,
            edgecolor=background_color,
            labelcolor=text_color,
        )
    main_ax.grid(
        True,
        which="both",
        axis="both",
        color=grid_color,
        linestyle="--",
        linewidth=grid_linewidth,
    )
    main_ax.tick_params(axis="y", labelsize=6, colors=text_color)
    main_ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    main_y_locator = MaxNLocator(nbins=y_axis_density)
    main_ax.yaxis.set_major_locator(main_y_locator)

    # Determine the number of x-axis labels based on the central x_axis_density parameter
    num_labels = min(x_axis_density, len(backtest_dataframe))
    step = max(1, len(backtest_dataframe) // num_labels)

    ticks = backtest_dataframe["Index"][::step]

    # Disable x-axis labels for all except the bottom-most plot
    for ax in axs[:-1]:
        ax.tick_params(axis="x", labelbottom=False)

    # Plot the bottom subplots
    for i, plot_data in enumerate(bottom_subplots):
        ax = axs[len(top_subplots) + 1 + i]
        _plot_data_on_ax(
            backtest_dataframe,
            ax,
            plot_data,
            subplot_overlays,
            text_color,
            grid_color,
            grid_linewidth,
            y_axis_density,
        )

    # Set x-axis labels only on the bottom-most subplot
    axs[-1].set_xticks(ticks)
    axs[-1].set_xticklabels(
        backtest_dataframe["Date"].dt.strftime("%Y-%m-%d")[::step],
        rotation=90,
        fontsize=6,
        color=text_color,
    )
    axs[-1].tick_params(axis="x", colors=text_color)

    plt.show()


def _plot_data_on_ax(
    backtest_dataframe,
    ax,
    plot_data,
    subplot_overlays,
    text_color,
    grid_color,
    grid_linewidth,
    y_axis_density,
):
    """Helper function to plot data on a given axis."""
    if plot_data.get("narrow_plot", False):
        signal_data = backtest_dataframe[backtest_dataframe[plot_data["column"]] == 1]
        ax.scatter(
            signal_data["Index"],
            [0.5] * len(signal_data),
            color=plot_data["color"],
            s=plot_data["size"],
            marker=plot_data["marker"],
        )
        ax.get_yaxis().set_visible(False)
        ax.set_ylim(0, 1)
        ax.set_yticks([])

        ax.legend(
            [plot_data["label"]],
            loc="upper right",
            fontsize=6,
            frameon=False,
            labelcolor=text_color,
        )
    else:
        ax.plot(
            backtest_dataframe["Index"],
            backtest_dataframe[plot_data["column"]],
            color=plot_data["color"],
            label=plot_data["label"],
            linewidth=plot_data["linewidth"],
        )
        ax.legend(
            fontsize=6,
            facecolor=ax.get_facecolor(),
            edgecolor=ax.get_facecolor(),
            labelcolor=text_color,
        )
    ax.grid(
        True,
        which="both",
        axis="both",
        color=grid_color,
        linestyle="--",
        linewidth=grid_linewidth,
    )
    ax.tick_params(axis="y", labelsize=6, colors=text_color)
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    subplot_y_locator = MaxNLocator(
        nbins=int(y_axis_density * plot_data.get("subplot_scale", 0.5))
    )
    ax.yaxis.set_major_locator(subplot_y_locator)

    if plot_data.get("y_axis_range"):
        ax.set_ylim(plot_data["y_axis_range"])

    # Handle overlayed plots
    parent_indicator = plot_data.get("column")
    if parent_indicator in subplot_overlays:
        for overlay_plot_data in subplot_overlays[parent_indicator]:
            ax.plot(
                backtest_dataframe["Index"],
                backtest_dataframe[overlay_plot_data["column"]],
                color=overlay_plot_data["color"],
                label=overlay_plot_data["label"],
                linewidth=overlay_plot_data["linewidth"],
            )
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(
            fontsize=6,
            facecolor=ax.get_facecolor(),
            edgecolor=ax.get_facecolor(),
            labelcolor=text_color,
        )
