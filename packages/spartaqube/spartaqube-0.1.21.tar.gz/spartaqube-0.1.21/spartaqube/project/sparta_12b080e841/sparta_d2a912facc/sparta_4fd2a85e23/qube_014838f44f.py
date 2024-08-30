_S='year: y, month: M, day: d, quarter: QQQ, week: w, hour: HH, minute: MM, seconds: SS, millisecond: ms'
_R='Example to plot a simple time series with datalabels using chartJS'
_Q='Example to plot a simple time series with custom title using chartJS'
_P='f"label-{round(price,2)}"'
_O='f"title-{round(price,2)}"'
_N='12px'
_M='center'
_L='blue'
_K='font-size'
_J='text-align'
_I='color'
_H='Example to plot a two time series using chartJS'
_G='from spartaqube import Spartaqube as Spartaqube'
_F='from api.spartaqube import Spartaqube as Spartaqube'
_E='Example to plot a simple time series using chartJS'
_D='code'
_C='sub_description'
_B='description'
_A='title'
import json
from django.conf import settings as conf_settings
def sparta_6770f1c775(type='line'):
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	B={_I:_L,_J:_M,_K:_N};C=_O;D=_P;return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Two {type}s with legend",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  legend=['High', 'Low'], 
  height=500
)
plot_example"""},{_A:f"Two stacked {type}s",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  stacked=True,
  height=500
)
plot_example"""},{_A:f"Simple {type} with title",_B:_Q,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  title='Apple Close Prices', 
  title_css={json.dumps(B)},
  height=500
)
plot_example"""},{_A:f"Simple {type} with datalabels",_B:_R,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  datalabels=apple_price_df['Close'],
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with conditional colors",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
apple_price_df['vol_colors'] = 'red'
apple_price_df.loc[apple_price_df['Volume'] > apple_price_df['Volume'].mean(), 'vol_colors'] = 'green'
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  border=apple_price_df['vol_colors'].tolist(), 
  background=apple_price_df['vol_colors'],
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with tooltips",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'],
  tooltips_title=[{C} for price in apple_price_df['Close'].tolist()],
  tooltips_label=[{D} for price in apple_price_df['Close'].tolist()],
  labels=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with date formatting",_B:_E,_C:_S,_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'],
  date_format='yyyy-MM-dd',
  labels=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with time range",_B:f"Example to plot a simple {type} chart with lightweight chart",_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df['Close'], 
  title='Example {type}',
  time_range=True,
  height=500
)
plot_example"""}]
def sparta_d60e1253a8():return sparta_6770f1c775(type='line')
def sparta_42641099d1():return sparta_6770f1c775(type='bar')
def sparta_b9451a4506():return sparta_6770f1c775(type='scatter')
def sparta_f1bfe28a25():
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	type='area';B={_I:_L,_J:_M,_K:_N};C=_O;D=_P;return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Two {type}s with legend",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  legend=['High', 'Low'], 
  height=500
)
plot_example"""},{_A:f"Two stacked {type}s",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  stacked=True,
  height=500
)
plot_example"""},{_A:f"Simple {type} with title",_B:_Q,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  title='Apple Close Prices', 
  title_css={json.dumps(B)},
  height=500
)
plot_example"""},{_A:f"Simple {type} with datalabels",_B:_R,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  datalabels=apple_price_df['Close'],
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with tooltips",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'],
  tooltips_title=[{C} for price in apple_price_df['Close'].tolist()],
  tooltips_label=[{D} for price in apple_price_df['Close'].tolist()],
  labels=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with date formatting",_B:_E,_C:_S,_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'],
  date_format='yyyy-MM-dd',
  labels=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with time range",_B:f"Example to plot a simple {type} chart with lightweight chart",_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df['Close'], 
  title='Example {type}',
  time_range=True,
  height=500
)
plot_example"""}]
def sparta_5558e86c77(type='pie'):
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	D={_I:_L,_J:_M,_K:_N};B='{\n    "datasets": [\n        {\n            "datalabels": {\n                "display": True,\n                "color": "red",\n                "font": {\n                    "family": "Azonix",\n                    "size": 20,\n                }\n            },\n        }\n    ]\n  }';C='{\n    "datasets": [\n        {\n            "backgroundColor": [\'red\', \'blue\', \'green\'],\n            "borderColor": [\'red\', \'blue\', \'green\'],\n        }\n    ]\n  }';return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=[1,2,3], 
  y=[20,60,20], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with labels",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=[1,2,3], 
  y=[20,60,20],
  datalabels=['group 1', 'group 2', 'group 3'],
  height=500
)
plot_example"""},{_A:f"Simple {type} with custom labels",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=[1,2,3], 
  y=[20,60,20],
  options={B},
  height=500
)
plot_example"""},{_A:f"Simple {type} with custom colors",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=[1,2,3], 
  y=[20,60,20],
  options={C},
  height=500
)
plot_example"""}]
def sparta_205d66abf6():return sparta_5558e86c77(type='donut')
def sparta_7512a0910b():return sparta_5558e86c77(type='polar')
def sparta_9c063bec5b():
	type='bubble'
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	B={_I:_L,_J:_M,_K:_N};C=_O;D=_P;return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with radius",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  r=apple_price_df['Volume'], 
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Two {type}s with legend",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  legend=['High', 'Low'], 
  height=500
)
plot_example"""},{_A:f"Two stacked {type}s",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  stacked=True,
  height=500
)
plot_example"""},{_A:f"Simple {type} with title",_B:_Q,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  title='Apple Close Prices', 
  title_css={json.dumps(B)},
  height=500
)
plot_example"""},{_A:f"Simple {type} with datalabels",_B:_R,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  datalabels=apple_price_df['Close'],
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with conditional colors",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
apple_price_df['vol_colors'] = 'red'
apple_price_df.loc[apple_price_df['Volume'] > apple_price_df['Volume'].mean(), 'vol_colors'] = 'green'
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  r=apple_price_df['Volume'], 
  border=apple_price_df['vol_colors'].tolist(), 
  background=apple_price_df['vol_colors'],
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with tooltips",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'],
  r=apple_price_df['Volume'], 
  tooltips_title=[{C} for price in apple_price_df['Close'].tolist()],
  tooltips_label=[{D} for price in apple_price_df['Close'].tolist()],
  labels=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple {type} with date formatting",_B:_E,_C:_S,_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'],
  r=apple_price_df['Volume'], 
  date_format='yyyy-MM-dd',
  labels=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with time range",_B:f"Example to plot a simple {type} chart with lightweight chart",_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df['Close'], 
  r=apple_price_df['Volume'], 
  title='Example {type}',
  time_range=True,
  height=500
)
plot_example"""}]
def sparta_09de17bce0():
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	B={_I:_L,_J:_M,_K:_N};C=_O;D=_P;type='barH';return[{_A:f"Simple horizontal bar",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Two horizontal bars with legend",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  legend=['High', 'Low'], 
  height=500
)
plot_example"""},{_A:f"Two stacked horizontal bars",_B:_H,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=[
      apple_price_df['High'], 
      apple_price_df['Low']
  ], 
  stacked=True,
  height=500
)
plot_example"""},{_A:f"Simple horizontal bar with title",_B:_Q,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  legend=['AAPL'], 
  title='Apple Close Prices', 
  title_css={json.dumps(B)},
  height=500
)
plot_example"""},{_A:f"Simple horizontal bar with datalabels",_B:_R,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'], 
  datalabels=apple_price_df['Close'],
  legend=['AAPL'], 
  height=500
)
plot_example"""},{_A:f"Simple horizontal bar with tooltips",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}', 
  x=apple_price_df.index, 
  y=apple_price_df['Close'],
  tooltips_title=[{C} for price in apple_price_df['Close'].tolist()],
  tooltips_label=[{D} for price in apple_price_df['Close'].tolist()],
  labels=['AAPL'], 
  height=500
)
plot_example"""}]
def sparta_d97d187fda():
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	type='radar';C={_I:_L,_J:_M,_K:_N};D=_O;E=_P;B='{\n    "datasets": [\n        {\n            "tension": 0\n        }\n    ]\n  }';return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f'''{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type=\'{type}\',
  x=["A", "B", "C", "D", "E", "F", "G"], 
  y=[65, 59, 90, 81, 56, 55, 40], 
  height=500
)
plot_example'''},{_A:f"Simple {type} with custom tension",_B:_E,_C:'',_D:f'''{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type=\'{type}\',
  x=["A", "B", "C", "D", "E", "F", "G"], 
  y=[65, 59, 90, 81, 56, 55, 40], 
  options={B},
  height=500
)
plot_example'''}]
def sparta_91f5d65bbb():
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	type='mixed';B='{\n    "datasets": [\n        {\n            "type": \'bar\',\n        },\n        {\n            "type": \'line\',\n        }\n    ]\n  }';return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index, 
  y=[apple_price_df['Close'], apple_price_df['High']], 
  option={B}, 
  height=500
)
plot_example"""}]
def sparta_ca24ee2d78():
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	type='histogram';return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
apple_ret_df = apple_price_df[['Close']].pct_change().dropna()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  y=apple_ret_df['Close'], 
  height=500
)
plot_example"""}]
def sparta_952d3c16ec():
	if conf_settings.IS_DEV:A=_F
	else:A=_G
	type='matrix';B="{'AAPL': apple_ret_df['Close'], 'NVDA': nvda_ret_df['Close'], 'TSLA': tsla_ret_df['Close']}";C='{\n    \'options\': {\n        "gradientColors": {\n            "bGradientMatrix": True,\n            "gradientStart": "#20ff86ff",\n            "gradientMiddle": "#f8e61cff",\n            "gradientEnd": "#ff0000ff",\n            "gradientFixedBorderColor": False,\n            "gradientBorderColor": "#ffffffff",\n            "gradientBorderWidth": 1,\n            "bDisplayHeatbar": True,\n            "heatBarPosition": "Right",\n            "bMiddleColor": True,\n        },\n    }\n  }';return[{_A:f"Simple {type}",_B:_E,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
apple_ret_df = apple_price_df.pct_change().iloc[-10:]
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_ret_df.index, 
  y=apple_ret_df['Close'],
  date_format='yyyy-MM-dd',
  height=500
)
plot_example"""},{_A:f"Correlation matrix example",_B:'Example to plot a simple correlation matrix using chartJS',_C:'',_D:f'''{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker("AAPL").history(period="1y")
apple_ret_df = apple_price_df.pct_change()
nvda_price_df = yf.Ticker("NVDA").history(period="1y")
nvda_ret_df = nvda_price_df.pct_change()
tsla_price_df = yf.Ticker("TSLA").history(period="1y")
tsla_ret_df = tsla_price_df.pct_change()
df = pd.DataFrame({B})
# Compute the correlation matrix
correlation_matrix = df.corr()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type=\'{type}\',
  x=correlation_matrix.index, 
  y=[correlation_matrix[\'AAPL\'], correlation_matrix[\'NVDA\'], correlation_matrix[\'TSLA\']],
  options={C},
  height=500
)
plot_example'''}]