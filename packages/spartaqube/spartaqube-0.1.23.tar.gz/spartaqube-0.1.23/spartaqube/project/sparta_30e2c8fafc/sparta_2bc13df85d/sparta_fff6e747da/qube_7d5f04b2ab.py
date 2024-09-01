_M="{'defaultColumn': 'moving_averages'}"
_L="{'defaultColumn': 'oscillators'}"
_K="{'defaultColumn': 'performance'}"
_J="{'blockSize': 'volume|1W'}"
_I="{'blockColor': 'Perf.YTD'}"
_H="{'symbol': 'NASDAQ:NVDA'}"
_G='Example to display a technical indicator chart using TradingView'
_F='from spartaqube import Spartaqube as Spartaqube'
_E='from api.spartaqube import Spartaqube as Spartaqube'
_D='code'
_C='sub_description'
_B='description'
_A='title'
import json
from django.conf import settings as conf_settings
def sparta_a28974d1cf(type='realTimeStock'):
	B='Example to display a real time stock using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	C=_H;return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom symbol",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_4808020e0b():
	B='Example to display a stock heatmap using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='stockHeatmap';C="{'dataSource': 'DAX'}";D=_I;E=_J;return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"YTD performance heatmap",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={D},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom heatmap size",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={E},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom data source",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_eb23da30d1():
	B='Example to display an economic calendar using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='economicCalendar';C="{'countryFilter': 'us, eu, il'}";return[{_A:f"Economic calendar",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"Economic calendar with custom countries",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_7a450a9776():
	B='Example to display a etf heatmap using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='etfHeatmap';C="{'dataSource': 'AllCHEEtf'}";D=_I;E="{'blockSize': 'volume|1M'}";return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"YTD performance heatmap",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={D},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom heatmap size",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={E},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom data source",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_b7d24d0c81():
	B='Example to display a crypto table using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='cryptoTable';C=_K;D=_L;E=_M;return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with performance data source",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with oscillator data",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={D},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with moving average data",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={E},
  height=500
)
plot_example"""}]
def sparta_814353efc9():
	B='Example to display a crypto heatmap using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='cryptoHeatmap';C=_I;D=_J;return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"YTD performance heatmap",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom heatmap size",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={D},
  height=500
)
plot_example"""}]
def sparta_30f8999d27(type='forex'):
	B='Example to display a forex live table using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	C="{'currencies': ['USD', 'EUR', 'CHF', 'GBP', 'JPY']}";return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom currencies",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_629434c85a():
	B='Example to display a market data table using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	C='{\n        "symbolsGroups": [\n            {\n                "name": "Indices",\n                "originalName": "Indices",\n                "symbols": [\n                    {\n                        "name": "FOREXCOM:SPXUSD",\n                        "displayName": "S&P 500",\n                    },\n                    {\n                        "name": "FOREXCOM:NSXUSD",\n                        "displayName": "US 100",\n                    },\n                ],\n            },\n            {\n                "name": "Futures",\n                "originalName": "Futures",\n                "symbols": [\n                    {\n                        "name": "CME_MINI:ES1!",\n                        "displayName": "S&P 500",\n                    },\n                    {\n                        "name": "CME:6E1!",\n                        "displayName": "Euro",\n                    },\n                ],\n            },\n            {\n                "name": "Bonds",\n                "originalName": "Bonds",\n                "symbols": [\n                    {\n                        "name": "CBOT:ZB1!",\n                        "displayName": "T-Bond",\n                    },\n                    {\n                        "name": "CBOT:UB1!",\n                        "displayName": "Ultra T-Bond",\n                    },\n                ],\n            },\n            {\n                "name": "Forex",\n                "originalName": "Forex",\n                "symbols": [\n                    {\n                        "name": "FX:EURUSD",\n                        "displayName": "EUR to USD",\n                    },\n                    {\n                        "name": "FX:GBPUSD",\n                        "displayName": "GBP to USD",\n                    },\n                ],\n            },\n        ]\n    }';type='marketData';return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom data",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_dfbb43e90a():
	B='Example to display a screener table using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='screener';C=_K;D=_L;E=_M;F="{'defaultScreen': 'top_gainers'}";G="{'market': 'switzerland'}";return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with performance data source",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with oscillator data",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={D},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with moving average data",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={E},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} for rising pairs",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={F},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} for custom market",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={G},
  height=500
)
plot_example"""}]
def sparta_d107c6d538():
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='technicalAnalysis';B=_H;C="{'interval': '1h'}";return[{_A:f"{type.capitalize()}",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom symbol",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={B},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom interval (last hour)",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_e4b52ae906():
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='topStories';B=_H;C="{'feedMode': 'market', 'market': 'crypto'}";D="{'feedMode': 'market', 'market': 'stock'}";E="{'feedMode': 'market', 'market': 'index'}";return[{_A:f"{type.capitalize()} (all symbols)",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} custom symbol",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={B},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} for cryptocurrencies",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} for stocks",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={D},
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} for indices",_B:_G,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={E},
  height=500
)
plot_example"""}]
def sparta_3f0f0c4383():
	B='Example to display a symbol overview using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	type='symbolOverview';C=_H;return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom symbol",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_fa6326fb4c(type='tickerTape'):
	B='Example to display a ticker tape using TradingView'
	if conf_settings.IS_DEV:A=_E
	else:A=_F
	C='{\n        "symbols": [\n            {\n                "proName": "FOREXCOM:SPXUSD",\n\t\t\t    "title": "S&P 500",\n            },\n            {\n                "proName": "FOREXCOM:NSXUSD",\n\t\t\t    "title": "US 100",\n            },\n        ]\n}';return[{_A:f"{type.capitalize()}",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  height=500
)
plot_example"""},{_A:f"{type.capitalize()} with custom symbols",_B:B,_C:'',_D:f"""{A}
spartaqube_obj = Spartaqube()
# Plot example
plot_example = spartaqube_obj.plot(
  chart_type='{type}',
  title=['{type} example'], 
  options={C},
  height=500
)
plot_example"""}]
def sparta_d2ec7b930e():return sparta_fa6326fb4c('tickerWidget')