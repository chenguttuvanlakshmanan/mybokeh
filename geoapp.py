
# from bokeh.plotting import figure, output_file, show
# from bokeh.tile_providers import CARTODBPOSITRON, get_provider

# # output_file("tile.html")

# tile_provider = get_provider(CARTODBPOSITRON)

# # range bounds supplied in web mercator coordinates
# p = figure(x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
#            x_axis_type="mercator", y_axis_type="mercator")

# p = q.circle(x=[10,20,30],y=[10,20,20],size =5)

# # q.add_tile(tile_provider)

# show(p)

##*********************************************************************************************************************************
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties

palette = tuple(reversed(palette))

counties = {
    code: county for code, county in counties.items() if county["state"] == "tx"
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]
color_mapper = LogColorMapper(palette=palette)

data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"

q = figure(
    title="Texas Unemployment, 2009", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Unemployment rate", "@rate%"), ("(Long, Lat)", "($x, $y)")
    ])
q.grid.grid_line_color = None
q.hover.point_policy = "follow_mouse"

q.patches('x', 'y', source=data,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

show(q)