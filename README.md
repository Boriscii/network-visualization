# network-visualization
Python network visualization app using NetworkX, Plotly, Dash origninally created by @jhwang1992.

I've made some updates and now it's able to easily map UK companies. This is useful to see connections between individuals and firms and speed up EDD (enhanced due dilligence). It uses Company House data so works only in the UK.

## Deps
The script depends on the `networkx, dash_core_components, dash_html_components, plotly, dash, pandas, colour, datetime, textwrap, json` modules.

## Run

In the api.py file change API_TOKEN to your Companies House API token. Then run the main file as usual and head to http://127.0.0.1:8050/.
