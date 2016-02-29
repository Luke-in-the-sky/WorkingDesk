import requests
import pandas as pd
from datetime import datetime
from bokeh.plotting import figure
from bokeh.embed import components

# Day 8: Google Finance ancestor
# ----------------

def plot_stock_data(stock='FB', features_to_plot=['Close']):
    '''
    For a given stock ticker:
      1. Request historical data from Quandle
      2. Plot it with Bokeh
      3. Return the java needed for the plot, so that Flask can render it
    '''
    
    # request data from Quandl
    api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json' % stock
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)

    # Make the dat column into datetime format
    raw_data_js = raw_data.json()['dataset_data']
    data = pd.DataFrame(raw_data_js['data'], columns=raw_data_js['column_names'])
    data['DateTime'] = data['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # Make Bokeh plot
    x = data['DateTime']
    p = figure(title="Historical data for %s" % stock,
               x_axis_label = "Date", 
               x_axis_type = "datetime")
    
    colors = {'Close' : 'navy',
              'Open'  : 'red'}
              
    for feature in features_to_plot:
        p.line(x=x, y=data[feature], line_color=colors[feature], legend=feature)

    p.legend.location = "top_left"
    
    #return components
    return components(p)
