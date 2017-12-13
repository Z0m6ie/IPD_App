from bokeh.plotting import figure, curdoc
from bokeh.models import NumeralTickFormatter
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox
from bokeh.models import BoxAnnotation
from bokeh.layouts import layout
from bokeh.models import Slider, Label, Select
from bokeh.models.widgets import Div
import numpy as np
import pandas as pd
import pandas_datareader.data as web


df = pd.read_excel(
    'https://github.com/Z0m6ie/IPD_App/blob/master/basis.xlsx?raw=true')

# add base_cost_total column
df['Base_cost_total'] = df['SNC-Lavalin_cost'] + \
    df['Construction_Partner_cost'] + df['OEM_cost']

# Risk Reward Pool
df['SNC-Lavalin_R&R'] = df['SNC-Lavalin_cost'] * df['Profit_percent']
df['Construction_Partner_R&R'] = df['Construction_Partner_cost'] * df['Profit_percent']
df['OEM_R&R'] = df['OEM_cost'] * df['Profit_percent']


# Base Cost GRAPH
################################################################################
###############################################################################
# Get the current slider values
# Engineering
a = df['Base_cost_total'][0]
# Procurement
b = df['Base_cost_total'][1]
# Construction
c = df['Base_cost_total'][2]
# Commissioning
d = df['Base_cost_total'][3]
# Start-up_support
e = df['Base_cost_total'][4]

# Calculate Top & Bottom
ab = 0
at = a
bb = a
bt = a + b
cb = a + b
ct = a + b + c
db = a + b + c
dt = a + b + c + d
eb = a + b + c + d
et = a + b + c + d + e
az = sum(df['Base_cost_total'])
increasepool = az - et
# New sources
engsource = ColumnDataSource(data=dict(x=[ab], y=[at], desc=['Engineering'],
                                       info=[at]))
prosource = ColumnDataSource(data=dict(x=[bb], y=[bt], desc=['Procurement'],
                                       info=[bt - at]))
constsource = ColumnDataSource(data=dict(x=[cb], y=[ct],
                                         desc=['Construction'], info=[ct - bt]))
commsource = ColumnDataSource(data=dict(x=[db], y=[dt], desc=['Commissioning'],
                                        info=[dt - ct]))
stasource = ColumnDataSource(data=dict(x=[eb], y=[et], desc=['Start-up_support'],
                                       info=[et - dt]))
tarsource = ColumnDataSource(data=dict(x=[ab], y=[sum(df['Base_cost_total'])], desc=['Target Value Design'],
                                       info=[sum(df['Base_cost_total']) - ab]))


# HoverTool Label
phover = HoverTool(
    tooltips=[
        ('Item', '@desc'),
        ('Cost', '@info{$ 0.00 a}'),
    ],
)


# Other Tools
TOOLS = 'box_zoom, box_select, reset'


# Figure
p = figure(title="Base Costs - No Profit", title_location="above",
           plot_width=300, plot_height=300, x_range=(-2, 2),
           tools=[TOOLS, phover])


# Plots
engbar = p.vbar(x=0, width=2, bottom='x',
                top='y', alpha=0.75, color="darkslategrey",
                legend="Engineering", source=engsource)

probar = p.vbar(x=0, width=2, bottom='x',
                top='y', alpha=0.75, color="teal", legend="Procurement",
                source=prosource)

constbar = p.vbar(x=0, width=2, bottom='x',
                  top='y', alpha=0.75, color="cyan", legend="Construction",
                  source=constsource)

commbar = p.vbar(x=0, width=2, bottom='x',
                 top='y', alpha=0.75, color="powderblue", legend="Commissioning",
                 source=commsource)

stabar = p.vbar(x=0, width=2, bottom='x',
                top='y', alpha=0.75, color="lavender", legend="Start-up Support",
                source=stasource)

tarbar = p.vbar(x=0, width=2, bottom='x',
                top='y', fill_alpha=0, line_alpha=1, color="firebrick", line_dash='dashed', legend="Target Value Design",
                source=tarsource)


# Format
p.yaxis[0].formatter = NumeralTickFormatter(format="$0,000")
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.xaxis.ticker = []

# sliders
#############################################################################
############################################################################
# Set up widgets
eng_slider = Slider(start=0, end=500000000,
                    value=df['Base_cost_total'][0], step=50000, title="Engineering $", format="$0,000")
pro_slider = Slider(start=0, end=500000000,
                    value=df['Base_cost_total'][1], step=50000, title="Procurement $", format="$0,000")
const_slider = Slider(start=0, end=1000000000,
                      value=df['Base_cost_total'][2], step=50000, title="Construction $", format="$0,000")
comm_slider = Slider(start=0, end=500000000,
                     value=df['Base_cost_total'][3], step=50000, title="Commissioning $", format="$0,000")
sta_slider = Slider(start=0, end=500000000,
                    value=df['Base_cost_total'][4], step=50000, title="Start-up Support $", format="$0,000")


# Partner Risk & Reward
#############################################################################
#############################################################################
# Data Transfer
sncprofit = sum(df['SNC-Lavalin_R&R'])
constprofit = sum(df['Construction_Partner_R&R'])
oemprofit = sum(df['OEM_R&R'])

zsncprofit = sum(df['SNC-Lavalin_R&R'])
zconstprofit = sum(df['Construction_Partner_R&R'])
zoemprofit = sum(df['OEM_R&R'])

# Total Pool Value
RR_Pool = sncprofit + constprofit + oemprofit
zRR_Pool = zsncprofit + zconstprofit + zoemprofit
sunprofit = RR_Pool - (sncprofit + constprofit + oemprofit)
sncprofitperct = sncprofit / RR_Pool
constprofitperct = constprofit / RR_Pool
oemprofitperct = oemprofit / RR_Pool

# Data source
sncsource = ColumnDataSource(data=dict(x=[1], y=[sncprofit], desc=['Actual SNC-Lavalin Profit'],
                                       info=[sncprofit]))
constuctionpartsource = ColumnDataSource(data=dict(x=[2], y=[constprofit], desc=['Actual Construction Partner Profit'],
                                                   info=[constprofit]))
oemsource = ColumnDataSource(data=dict(x=[3], y=[oemprofit],
                                       desc=['Actual OEM Profit'], info=[oemprofit]))
sunsource = ColumnDataSource(data=dict(x=[4], y=[sunprofit],
                                       desc=['Benefit to Suncor'], info=[sunprofit]))
# Target data
tarsncsource = ColumnDataSource(data=dict(x=[1], y=[zsncprofit], desc=['Target SNC-Lavalin Profit'],
                                          info=[zsncprofit]))
tarconstuctionpartsource = ColumnDataSource(data=dict(x=[2], y=[zconstprofit], desc=['Target Construction Partner Profit'],
                                                      info=[zconstprofit]))
taroemsource = ColumnDataSource(data=dict(x=[3], y=[zoemprofit],
                                          desc=['Target OEM Profit'], info=[zoemprofit]))


# R&R Plots
R = figure(title="Risk & Reward Share for IPD Partners", title_location="above",
           plot_width=300, plot_height=300, tools=[TOOLS, phover])

sncbar = R.vbar(x=1, width=0.75, bottom='x',
                top='y', alpha=0.75, color="darkslategrey",
                legend="SNC-Lavalin", source=sncsource)

conpbar = R.vbar(x=2, width=0.75, bottom='x',
                 top='y', alpha=0.75, color="teal", legend="Construction Partner",
                 source=constuctionpartsource)

oembar = R.vbar(x=3, width=0.75, bottom='x',
                top='y', alpha=0.75, color="cyan", legend="OEM",
                source=oemsource)

sunbar = R.vbar(x=4, width=0.75, bottom='x',
                top='y', alpha=0.75, color="darkorange", legend="Suncor",
                source=sunsource)

tarsncbar = R.vbar(x=1, width=0.75, bottom='x',
                   top='y', fill_alpha=0, line_alpha=1, color="firebrick", line_dash='dashed', source=tarsncsource)

tarconpbar = R.vbar(x=2, width=0.75, bottom='x',
                    top='y', fill_alpha=0, line_alpha=1, color="firebrick", line_dash='dashed', source=tarconstuctionpartsource)

taroembar = R.vbar(x=3, width=0.75, bottom='x',
                   top='y', fill_alpha=0, line_alpha=1, color="firebrick", line_dash='dashed', source=taroemsource)

# Format
R.yaxis[0].formatter = NumeralTickFormatter(format="$0,000")
R.xgrid.grid_line_color = None
R.ygrid.grid_line_color = None
R.xaxis.ticker = []

# Total Project Cost GRAPH
##############################################################################
#############################################################################
totalsourceval = et + RR_Pool
ztotalsourceval = et + zRR_Pool

# color
colorz = 'teal'
# New sources
totalsource = ColumnDataSource(data=dict(x=[0], y=[totalsourceval], desc=['Actual Capital Cost'],
                               info=[totalsourceval], color=[colorz]))
totaltargetsource = ColumnDataSource(data=dict(x=[0], y=[ztotalsourceval], desc=['Target Capital Cost'],
                                     info=[ztotalsourceval]))


# HoverTool Label
phover = HoverTool(
    tooltips=[
        ('Item', '@desc'),
        ('Cost', '@info{$ 0.00 a}'),
    ],
)


# Other Tools
TOOLS = 'box_zoom, box_select, reset'


# Figure
t = figure(title="Total Project Cost", title_location="above",
           plot_width=300, plot_height=300, x_range=(-2, 2),
           tools=[TOOLS, phover])


# Plots
tvbar = t.vbar(x=0, width=2, bottom='x',
                top='y', alpha=0.75, color='color',
                legend="Actual Capital Cost", source=totalsource)

tartvbar = t.vbar(x=0, width=2, bottom='x',
                top='y', fill_alpha=0, line_alpha=1, color="firebrick", line_dash='dashed', legend="Target Capital Cost",
                source=totaltargetsource)


# Format
t.yaxis[0].formatter = NumeralTickFormatter(format="$0,000")
t.xgrid.grid_line_color = None
t.ygrid.grid_line_color = None
t.xaxis.ticker = []


# Txtbox
###########################################################################
##########################################################################

lab = figure(plot_width=500, plot_height=150, x_range=(0, 3), y_range=(1, 3))


label1 = Label(x=0.25, y=2.70, text='Base Cost Target $: {:,}' .format(az),
              text_font_size='15pt', text_color='black')
label2 = Label(x=0.25, y=2.40, text='Base Cost Actual $: {:,}' .format(et),
              text_font_size='15pt', text_color='black')
label3 = Label(x=0.25, y=2.10, text='Profit Pool $: {:,}' .format(RR_Pool),
               text_font_size='15pt', text_color='black')
label4 = Label(x=0.25, y=1.80, text='Benefit To Suncor $: {:,}' .format(sunprofit),
               text_font_size='15pt', text_color='black')
label5 = Label(x=0.25, y=1.50, text='Total CAPEX $: {:,}' .format(totalsourceval),
               text_font_size='15pt', text_color='black')

lab.add_layout(label1)
lab.add_layout(label2)
lab.add_layout(label3)
lab.add_layout(label4)
lab.add_layout(label5)

lab.xgrid.grid_line_color = None
lab.ygrid.grid_line_color = None
lab.xaxis.visible = False
lab.yaxis.visible = False
lab.background_fill_color = "white"
# Intro Para
####################################
# Text
# div = Div(text="""<h3 style="text-align: left;"><strong><span style="color: #333333;">David Peabody</span></strong></span></h3>
# <h1 style="text-align: left;"><span style="text-decoration: underline;"><strong><span style="color: #333333; text-decoration: underline;">CAPEX &amp; OPEX Dashboard</span></strong></span></h1>
# <h2><span style="color: #333333;">Move the sliders to investigate the effects of CAPEX and OPEX on the projects rate of return. For a full list of references and assumption please see the following link.&nbsp;<a title="Link to References" href="https://github.com/Z0m6ie/App_Capex/tree/master" target="_blank">References</a></span></h2>
# <h5><span style="color: #333333;">To buy the developer a well deserved coffee please click the following link.&nbsp;<a title="paypal" href="https://www.paypal.me/DPeabody63" target="_blank">paypal</a></span></h5>""", width=400, height=300)
div = Div(text="""<h1 style="text-align: left;"><strong><span style="color: #333333;"><img src="http://www.snclavalin.com/en/files/images/SNC-Logo_Desktop.png" alt="Logo" width="107" height="47" /></span> <style="text-align: left;"><span style="text-decoration: underline;"><strong><span style="color: #333333; text-decoration: underline;">IPD Partnership</span></strong></span></h1>
<h2><span style="color: #333333;">Move the sliders to investigate the effects of a change in the estimated base cost on the profit each IPD member recieves and the effect on total project cost. For a full list of references and assumption please see the following link.&nbsp;<a title="Link to References" href="https://github.com/Z0m6ie/App_Capex/tree/master" target="_blank">References</a></span></h2>
<h5><span style="color: #333333;">To buy the developer a well deserved coffee please click the following link.&nbsp;<a title="paypal" href="https://www.paypal.me/DPeabody63" target="_blank">paypal</a></span></h5>""", width=800, height=150)

div1 = Div(text="""<h2><span style="color: #333333;">A collaborative contracting approach shares the benefit of executing the project below the target price with members of the risk and reward pool. When members of the pool do not achieve their targets, the group's profit is eroded but the project is provided some protection before the total project capital cost starts to increase.</a></span></h2>""", width=600, height=150)
# UPDATE FUNCTION
####################################
def update_data(attrname, old, new):
    # capex function
    ################################

    # Get the current slider values
    a = eng_slider.value
    b = pro_slider.value
    c = const_slider.value
    d = comm_slider.value
    e = sta_slider.value

    # Calculate Top & Bottom
    ab = 0
    at = a
    bb = a
    bt = a + b
    cb = a + b
    ct = a + b + c
    db = a + b + c
    dt = a + b + c + d
    eb = a + b + c + d
    et = a + b + c + d + e

    # New sources
    engsource.data = dict(x=[ab], y=[at], desc=['Engineering'], info=[at])
    prosource.data = dict(x=[at], y=[bt], desc=['Procurement'], info=[bt - at])
    constsource.data = dict(x=[bt], y=[ct], desc=['Construction'],
                            info=[ct - bt])
    commsource.data = dict(x=[ct], y=[dt], desc=[
                           'Commissioning'], info=[dt - ct])
    stasource.data = dict(x=[dt], y=[et], desc=[
                          'Start-up Support'], info=[et - dt])
    tarsource.data = dict(x=[ab], y=[sum(df['Base_cost_total'])], desc=['Target Value Design'],
                          info=[sum(df['Base_cost_total']) - ab])

    # Profit pool calc
    az = sum(df['Base_cost_total'])
    profit_pool_change = az - (et)
    RR_Pool_updated = RR_Pool + profit_pool_change
    if profit_pool_change >= 0:
        RR_Pool_updated = RR_Pool + (profit_pool_change * 0.85)
        sunprofit = profit_pool_change * 0.15
    else:
        sunprofit = 0

    # New R&R Calc
    if RR_Pool_updated <= 0:
            sncprofit = 0
            constprofit = 0
            oemprofit = 0
    else:
        sncprofit = RR_Pool_updated * sncprofitperct
        constprofit = RR_Pool_updated * constprofitperct
        oemprofit = RR_Pool_updated * oemprofitperct

    # New R&R sources
    sncsource.data = dict(x=[1], y=[sncprofit], desc=['Actual SNC-Lavalin Profit'],
                          info=[sncprofit])
    constuctionpartsource.data = dict(x=[2], y=[constprofit], desc=['Actual Construction Partner Profit'],
                                      info=[constprofit])
    oemsource.data = dict(x=[3], y=[oemprofit],
                          desc=['Actual OEM Profit'], info=[oemprofit])
    sunsource.data = dict(x=[4], y=[sunprofit],
                                           desc=['Benefit to Suncor'], info=[sunprofit])

    # New Total cost sources
    if profit_pool_change >= 0:
        totalsourceval = az + RR_Pool - sunprofit
    elif profit_pool_change < 0 and RR_Pool_updated > 0:
        totalsourceval = az + RR_Pool
    else:
        totalsourceval = et

    # colorz
    if totalsourceval < ztotalsourceval:
        colorz = 'springgreen'
    elif totalsourceval > ztotalsourceval:
        colorz = 'indianred'
    else:
        colorz = 'teal'
    # New sources
    totalsource.data = dict(x=[0], y=[totalsourceval], desc=['Actual Capital Cost'],
                                   info=[totalsourceval], color=[colorz])

    # Labels
    label1.text = 'Base Cost Target $: {:,}' .format(az)
    label2.text = 'Base Cost Actual $: {:,}' .format(et)
    label3.text = 'Profit Pool $: {:,}' .format(RR_Pool_updated)
    label4.text = 'Benefit To Suncor $: {:,}' .format(sunprofit)
    label5.text = 'Total CAPEX $: {:,}' .format(totalsourceval)


for w in [eng_slider, pro_slider, const_slider, comm_slider, sta_slider]:
    w.on_change('value', update_data)

#  CAPEX Set up layouts and add to document
inputs = widgetbox(eng_slider, pro_slider, const_slider, comm_slider, sta_slider,
                   width=200)


# PAYBACK Set up layouts and add to document

para = widgetbox(div)
para1 = widgetbox(div1, sizing_mode='fixed')
l = layout([
    [para,inputs],
    [p, R, t],
    [para1, lab],
], sizing_mode='scale_width')


# Show!
curdoc().add_root(l)
curdoc().title = "IPD App"
