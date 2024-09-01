_N='{\n        "showTicks": True,\n        "renderTicks": {\n            "showTicks": True,\n            "divisions": 10,\n        },\n    }'
_M='Example to plot a simple shaded background chart with lightweight chart'
_L='12px'
_K='center'
_J='blue'
_I='font-size'
_H='text-align'
_G='color'
_F='from spartaqube import Spartaqube as Spartaqube'
_E='from api.spartaqube import Spartaqube as Spartaqube'
_D='code'
_C='sub_description'
_B='description'
_A='title'
import json
from django.conf import settings as conf_settings
def sparta_0fe731071d(type='candlestick'):
	B='Example to plot a simple candlestick chart with lightweight chart'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	C={_G:_J,_H:_K,_I:_L};D=_N;return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  ohlcv=[apple_price_df['Open'], apple_price_df['High'], apple_price_df['Low'], apple_price_df['Close']], 
  title='Example candlestick',
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with volumes",_B:B,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  ohlcv=[apple_price_df['Open'], apple_price_df['High'], apple_price_df['Low'], apple_price_df['Close'], apple_price_df['Volume']], 
  title='Example candlestick',
  height=500
)
plot_example"""}]
def sparta_0a0db59fa8(type='line2'):
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	B={_G:_J,_H:_K,_I:_L};C=_N;return[{_A:f"{type.capitalize()}",_B:f"Example to plot a simple {type} chart with lightweight chart",_C:'',_D:f"""{A}
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
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} two lines",_B:f"Example to plot multiple {type}s with lightweight chart",_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df[['Close', 'Open']], 
  title='Example {type}',
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} two lines stacked",_B:f"Example to plot multiple {type}s with lightweight chart",_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df[['Close', 'Open']],
  stacked=True,
  title='Example {type}',
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
def sparta_54e0fbb01e():return sparta_0a0db59fa8('line2')
def sparta_e336fe4a74():return sparta_0a0db59fa8('bar2')
def sparta_6c0a95c7aa():return sparta_0a0db59fa8('area2')
def sparta_071f487d0d():return sparta_0a0db59fa8('lollipop2')
def sparta_9a97e4ad2d():
	B='Example to plot a simple baseline chart with lightweight chart'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	D={_G:_J,_H:_K,_I:_L};C='{\n    "baseline": [\n      \t{\n          "defaultBaselinePrice": 200,\n        },\n    ]\n    }';type='baseline2';return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df['Close'], 
  title='Example baseline',
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom baseline",_B:B,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df['Close'], 
  title='Example baseline',
  options={C},
  height=500
)
plot_example"""}]
def sparta_3a027970b1():
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	C={_G:_J,_H:_K,_I:_L};B='{\n        "shadedBackground": {\n            "lowColor": "rgb(50, 50, 255)",\n            "highColor": "rgb(255, 50, 50)",\n            "opacity": 0.8,\n        },\n    }';type='shadedBackground2';return[{_A:f"{type.capitalize()}",_B:_M,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df['Close'], 
  shaded_background=apple_price_df['Close'], 
  title='Example',
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom colors",_B:_M,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=apple_price_df['Close'], 
  shaded_background=apple_price_df['Close'], 
  title='Example',
  options={B},
  height=500
)
plot_example"""}]
def sparta_23aa7c8e78():
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	B={_G:_J,_H:_K,_I:_L};C=_N;type='performance';return[{_A:f"{type.capitalize()}",_B:f"Example to plot a simple {type} chart with lightweight chart",_C:'',_D:f"""{A}
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
  height=500
)
plot_example"""}]
def sparta_26880da93a():
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	C={_G:_J,_H:_K,_I:_L};B='{\n        "areaBands": {\n            "fillColor": "#F5A623",\n            "color": "rgb(19, 40, 153)",\n            "lineColor": "rgb(208, 2, 27)",\n            "lineWidth": 3,\n            "custom_scale_axis": "Right",\n        },\n    }';type='areaBands2';return[{_A:f"{type.capitalize()}",_B:_M,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=[apple_price_df['Close'], apple_price_df['High'], apple_price_df['Low']], 
  title='Example',
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom colors",_B:_M,_C:'',_D:f"""{A}
import yfinance as yf
spartaqube_obj = Spartaqube()
# Fetch the data for Apple (ticker symbol: AAPL)
apple_price_df = yf.Ticker(\"AAPL\").history(period=\"1y\")
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  x=apple_price_df.index,
  y=[apple_price_df['Close'], apple_price_df['High'], apple_price_df['Low']], 
  options={B},
  height=500
)
plot_example"""}]