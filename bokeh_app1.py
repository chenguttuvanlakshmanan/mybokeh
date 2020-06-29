#General Imports
import numpy as np
import pandas as pd

#Bokeh Imports version 2.1.0
from bokeh.layouts import column,row
from bokeh.models import Button,Select,ColumnDataSource,Slider,TextAreaInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models import Panel, Tabs,DataTable,TableColumn

#tab color customization
template = """
{% block postamble %}
<style>
.bk-root .bk-tab {
    background-color: blue;
    width: 200px;
    color: red;
    font-style: italic;
}

.bk-root .bk-tabs-header .bk-tab.bk-active{
background-color: grey;
color: blue;
font-style: normal;
font-weight: bold;
}

.bk-root .bk-tabs-header .bk-tab:hover{
background-color: yellow
}

</style>
{% endblock %}
"""
#************************************************************************************************************************
#data source
from sklearn.datasets import load_iris
iris = load_iris()
df = pd.DataFrame(iris.data,columns=iris.feature_names)
df["Species"] = pd.DataFrame(iris.target)
df["Species"] = df["Species"].apply(lambda x:"A" if x == 0  else "B" if x == 1 else "C")

#widgets for the model
select_default = "A"
select = Select(title="Product:", value=select_default, options=["A","B","C"])
select.max_width = 200

text_input = TextAreaInput( value = 'A',rows=6, title="Selected Product")
text_input.max_width = 200
text_input.max_height = 70
# text_input.background_fill_color = "beige"

colormap = {'A': 'red', 'B': 'green', 'C': 'blue'}
df['colors'] = [colormap[x] for x in df['Species']]

#dataource for the plots
df1 = df.copy()
df = df[ df["Species"] == select_default ]
source = ColumnDataSource(df)
group = df1.groupby("Species")
source1 = ColumnDataSource(group)

# Function to update the datasource
def update_text(attrname, old, new):
    df = pd.DataFrame(iris.data,columns=iris.feature_names)
    df["Species"] = pd.DataFrame(iris.target)
    df["Species"] = df["Species"].apply(lambda x:"A" if x == 0  else "B" if x == 1 else "C")
    df = df[ df["Species"] == select.value ]
    new = ColumnDataSource(df)
    source.data = dict(new.data)
    text_input.value = select.value
  
select.on_change('value',update_text)

#*****************************************************************************************************************************************
## bokeh create plots from pandas dataframe tab1
#******************************************************************************************************************************
from bokeh.palettes import Spectral4
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT

p = figure(plot_width=1050, plot_height=300, x_axis_type="datetime",toolbar_location=None,scale_both=True)
p.title.text = 'Trend Price'

for data, name, color in zip([AAPL, IBM, MSFT], ["A", "B", "C"], Spectral4):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    p.line(df['date'], df['close'], line_width=2, color=color, alpha=0.8, legend_label=name)

p.legend.location = "top_left"
p.legend.click_policy="hide"
p.border_fill_color = "whitesmoke"
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.yaxis.minor_tick_line_color = None
p.min_border_left =5

# create a plot and style its properties
p1 = figure( toolbar_location=None,width=350,height=200,title = "Chart1",scale_both=True)
p1.circle('sepal length (cm)','sepal width (cm)',size=5,source=source)
p1.yaxis.minor_tick_line_color = None
p1.xaxis.minor_tick_line_color = None
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p1.border_fill_color = "whitesmoke"
p1.min_border_left =5

p2 = figure( toolbar_location=None,width=350,height=200,title="Chart2",scale_both=True)
p2.triangle('sepal length (cm)','sepal width (cm)',size=5,source=source)
p2.yaxis.minor_tick_line_color = None
p2.xaxis.minor_tick_line_color = None
p2.xgrid.grid_line_color = None
p2.ygrid.grid_line_color = None
p2.border_fill_color = "whitesmoke"
p2.min_border_left =5

#the plot is from the grouped data source1
p3 = figure(x_range = ["A","B","C"],toolbar_location=None,width=350,height=200,title="Chart3",scale_both=True)
p3.vbar(x="Species", width=0.5,top="sepal length (cm)_mean",source=source1)
p3.yaxis.minor_tick_line_color = None
p3.xaxis.minor_tick_line_color = None
p3.xgrid.grid_line_color = None
p3.ygrid.grid_line_color = None
p3.border_fill_color = "whitesmoke"
p3.min_border_left =5

#******************************************************************************************************************************
## bokeh create datatable from pandas dataframe tab2 
#******************************************************************************************************************************

columns = [
    TableColumn(field="Species", title="Species"),
    TableColumn(field="sepal length (cm)", title="Sepal_Length"),
    TableColumn(field="sepal width (cm)", title="Sepal_Width"),
]
table = DataTable(source=source,columns=columns, height=800, width=600, name="table", sizing_mode="scale_both")

# tab building for the bokeh server
n1 = column(row(select,text_input),
                    row(p1,p2,p3),
                                row(p))

n2 = column(row(select,text_input),row(table))

tab1 = Panel(child=n1, title="Main Report",)
tab2 = Panel(child=n2, title="Detail Report")

tabs = Tabs(tabs=[tab1,tab2])


#Final tabs addewd the doc element served by the bokeh server
curdoc().add_root(tabs)