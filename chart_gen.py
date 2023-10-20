"""serializing data for jinja
"""

from datetime import date, timedelta
import json
import plotly


def ser_data_gen_conf(
    data: list,
    title: str,
    y_axis_title: str = "luovutukset"
) -> dict[str, str]:
    """serializes data + generates a "standrad" config for my selection of barchart

    Args:
        data (list): data to be serialized
        title (str): chart's title

    Returns:
        dict[str, str]: {'data': serialized_data, 'conf': standard_config}
    """
    return {
        'data': json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder),
        'conf': json.dumps({
            'barmode': "relative",
            'scrollZoom': True,
            'xaxis': {
                'range': [
                    date.today() - timedelta(weeks=4*3),
                    # today's donations were only visible half-width :D
                    date.today() + timedelta(days=1)
                ],
                'title': "päivämäärä"
            },
            'yaxis': {'title': y_axis_title},
            'title': title,
            'font': {
                'color': 'red'
            },
            'plot_bgcolor': 'transparent',
            'paper_bgcolor': 'transparent',
        }, cls=plotly.utils.PlotlyJSONEncoder)
    } if len(data) > 0 else None
