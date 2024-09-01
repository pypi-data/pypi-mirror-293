import os, sys, json, cloudpickle, warnings
import pandas as pd
import urllib.parse
from IPython.core.display import display, HTML
from IPython.display import IFrame

current_path = os.path.dirname(__file__)
base_project = os.path.dirname(current_path)
sys.path.insert(0, current_path)
sys.path.insert(0, base_project)

from spartaqube_plot_session import SpartaqubePlotSession
from spartaqube_utils import get_ws_settings, request_service, process_scalar_args, extract_port
import spartaqube_install as spartaqube_install
warnings.filterwarnings("ignore", category=UserWarning)

class Spartaqube:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_key=None, port=None, silent=False):
        '''
        If api_key specified, no need to specify port
        '''
        self.api_key = api_key
        self.silent = silent
        self.plot_session_obj = SpartaqubePlotSession()

        b_start_local_server = False

        if api_key is None: # Public user with local server
            b_start_local_server = True
            if port is None: # Use default port
                port = spartaqube_install.get_default_port()
            else: # Use the user's port input
                pass
            self.domain_or_ip = f'http://localhost:{port}'
            self.api_token_id = 'public'
            if not silent:
                print("\nWarning: SpartaQube is currently running with the public user.\nTo enhance your experience, consider creating an account to obtain an API key.\n")
        else: # Use api_key for auth
            try:
                self.domain_or_ip, self.api_token_id = get_ws_settings(api_key)
            except:
                raise Exception("Invalid api_key")
            
            if len([elem for elem in ['localhost', '127.0.0.1'] if elem in self.domain_or_ip]) > 0:
                b_start_local_server = True
                port = extract_port(self.domain_or_ip)
            else:
                # No need to start a local spartaqube server in this case, as we'll use a remote one
                pass

        if b_start_local_server:
            spartaqube_install.entrypoint(port=port, silent=silent)

        # Finally test the application
        is_app_running = False
        try:
            app_status_dict = self.get_status()
            if app_status_dict['res'] == 1:
                is_app_running = app_status_dict['output'] == 1
        except:
            pass
    
        if is_app_running:
            if not silent:
                print(f"GUI exposed at {self.domain_or_ip}")
                print(f"SpartaQube documentation at {self.domain_or_ip}/api")
        else: # Application is not running
            error_msg = ''
            if api_key is None: # Public user with local server
                error_msg = f"SpartaQube application is not running on {self.domain_or_ip}. Make sure the port is not already allocated to another application."
            else:
                error_msg = f"SpartaQube application is not running on {self.domain_or_ip}. Please check the api_key"

            raise Exception(error_msg)
            
    def get_common_api_params(self) -> dict:
        return {
            'api_token_id': self.api_token_id,
        }

    def query_service(self, service_name:str, data_dict:dict) -> dict:
        '''
        POST requests
        '''
        return request_service(self, service_name=service_name, data_dict=data_dict)
    
    def get_status(self):
        data_dict = self.get_common_api_params()
        return self.query_service('get_status', data_dict)

    def stop_server(self):
        spartaqube_install.stop_server()

    # ******************************************************************************************************************
    # LIBRARY/WIDGETS
    # ******************************************************************************************************************
    def get_widgets(self) -> list:
        if not self.silent:
            if not hasattr(self, 'api_key'):
                print("\nWarning: SpartaQube is currently running with the public user.\nUse your API key to access your personal widgets.\n")
        data_dict = self.get_common_api_params()
        return self.query_service('get_widgets', data_dict)
    
    def get_widget(self, widget_id, width='60%', height=500):
        if not self.silent:
            if not hasattr(self, 'api_key'):
                print("\nWarning: SpartaQube is currently running with the public user.\nUse your API key to access your personal widgets.\n")
        
        if not self.has_widget_id(widget_id):
            print("You don't have access to this widget")
            return
        
        return HTML(f'<iframe src="{self.domain_or_ip}/plot-widget/{widget_id}/{self.api_token_id}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>')
        # return IFrame(src=f"{self.domain_or_ip}/plot-widget?id={widget_id}&api_token_id={self.api_token_id}", width=width, height=height)
        
    def get_widget_data(self, widget_id) -> list:
        '''
        Get widget data
        '''
        data_dict = self.get_common_api_params()
        data_dict['widget_id'] = widget_id
        res_dict = self.query_service('get_widget_data', data_dict)
        if res_dict['res'] == 1:
            res_list = []
            for json_data in res_dict['data']:
                data_dict = json.loads(json_data)
                res_list.append(pd.DataFrame(data=data_dict['data'], index=data_dict['index'], columns=data_dict['columns']))
            return res_list

        return res_dict

    def has_widget_id(self, widget_id) -> bool:
        data_dict = self.get_common_api_params()
        data_dict['widget_id'] = widget_id
        res_dict = self.query_service('has_widget_id', data_dict)
        if res_dict['res'] == 1:
            return res_dict['has_access']

        return False
    
    # ******************************************************************************************************************
    # PLOTS
    # ******************************************************************************************************************
    def iplot(self, *argv, width='100%', height=750):
        '''
        Interactive plot using GUI
        '''
        if len(argv) == 0:
            raise Exception('You must pass at least one input variable to plot')
        else:
            # args = locals()
            post_data_dict = dict()
            plot_params_dict = dict()
            for key_idx, value in enumerate(argv):
                if value is None:
                    continue

                this_hash = self.plot_session_obj.get_hash(value)
                self.plot_session_obj.add_to_all_hash_notebook(this_hash)
                tmp_post_var_dict = {
                    'hash': this_hash,
                    'is_hash_in_session': True,
                }
                plot_params_dict[key_idx] = this_hash
                if not self.plot_session_obj.is_hash_in_session(this_hash):
                    # print("hash not found, need to pickle data")
                    tmp_post_var_dict['is_hash_in_session'] = False
                    tmp_post_var_dict['var'] = cloudpickle.dumps(value).decode('latin1')

                post_data_dict[key_idx] = tmp_post_var_dict

            data_dict = self.get_common_api_params()
            data_dict['variables'] = post_data_dict
            data_dict['plot_params'] = plot_params_dict
            data_dict['all_hash_server'] = self.plot_session_obj.get_all_hash_server()
            data_dict['all_hash_notebook'] = self.plot_session_obj.get_all_hash_notebook_list()
            res_session_dict = self.query_service('gui_plot_api_variables', data_dict)
            # print("res_session_dict")
            # print(res_session_dict)
            if res_session_dict['res'] == 1:
                # print(res_session_dict)
                session_id = res_session_dict['session_id']
                self.plot_session_obj.set_hash_server_list(res_session_dict['cache_hash'])
                # return IFrame(src=f"{self.domain_or_ip}/plot-gui?session={session_id}&api_token_id={self.api_token_id}", width=width, height=height)
                # return HTML(f'<iframe src="{self.domain_or_ip}/plot-gui?session={session_id}&api_token_id={self.api_token_id}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>')
                return HTML(f'<iframe src="{self.domain_or_ip}/plot-gui/{session_id}/{self.api_token_id}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>')
            else:
                if res_session_dict['status_service'] == 1: # Missing Cache variable, restart
                    # print("Cache was clear, need to reset")
                    self.plot_session_obj.set_hash_server_list(res_session_dict['cache_hash'])
                    return self.iplot(*argv, width=width, height=height)
                else:
                    print("An error occurred, could not start a new SpartaQube plot session...")

    def plot(self, x:list=None, y:list=None, r:list=None, legend:list=None, labels:list=None, ohlcv:list=None, shaded_background:list=None, 
            datalabels:list=None, border:list=None, background:list=None, border_style:list=None, tooltips_title:list=None, tooltips_label:list=None,
            chart_type='line', interactive=True, widget_id=None, title=None, title_css:dict=None, stacked:bool=False, date_format:str=None, time_range:bool=False,
            gauge:dict=None, gauge_zones:list=None, gauge_zones_labels:list=None, gauge_zones_height:list=None, 
            dataframe:pd.DataFrame=None, dates:list=None, returns:list=None, returns_bmk:list=None,
            options:dict=None, width='100%', height=750):
        '''
        Programmatically plot
        '''
        args = locals()
        process_scalar_args(args)

        max_retry = 2

        def start_plot(cnt_retry=0):
            post_data_dict = dict()
            plot_params_dict = dict()
            for key, value in args.items():
                if value is None:
                    continue

                if key != 'self':  # Skip 'self' argument
                    this_hash = self.plot_session_obj.get_hash(value)
                    self.plot_session_obj.add_to_all_hash_notebook(this_hash)
                    tmp_post_var_dict = {
                        'hash': this_hash,
                        'is_hash_in_session': True,
                    }
                    plot_params_dict[key] = this_hash
                    if not self.plot_session_obj.is_hash_in_session(this_hash):
                        # print("hash not found, need to pickle data")
                        tmp_post_var_dict['is_hash_in_session'] = False
                        tmp_post_var_dict['var'] = cloudpickle.dumps(value).decode('latin1')

                    post_data_dict[key] = tmp_post_var_dict

            post_data_dict['chart_type_check'] = chart_type
            data_dict = self.get_common_api_params()
            data_dict['variables'] = post_data_dict
            data_dict['plot_params'] = plot_params_dict
            data_dict['all_hash_server'] = self.plot_session_obj.get_all_hash_server()
            data_dict['all_hash_notebook'] = self.plot_session_obj.get_all_hash_notebook_list()
            vars_html_dict = {
                'interactive_api': 1 if interactive else 0,
                'is_api_template': 1 if widget_id is not None else 0,
                'widget_id': widget_id,
            }
            json_vars_html = json.dumps(vars_html_dict)
            encoded_json_str = urllib.parse.quote(json_vars_html)
            res_session_dict = self.query_service('plot_cache_variables', data_dict)
            # print("res_session_dict")
            # print(res_session_dict)
            if res_session_dict['res'] == 1:
                self.plot_session_obj.set_hash_server_list(res_session_dict['cache_hash'])
                session_id = res_session_dict['session_id']
                return HTML(f'<iframe src="{self.domain_or_ip}/plot-api/{session_id}/{self.api_token_id}/{encoded_json_str}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>')
            else:
                if res_session_dict['status_service'] == 1: # Missing Cache variable, restart
                    self.plot_session_obj.set_hash_server_list(res_session_dict['cache_hash'])
                    if cnt_retry < max_retry:
                        return start_plot(cnt_retry+1)
                    else:
                        print("An error occurred, please try again...")
                else:
                    print("An error occurred, please try again...")
                    if 'errorMsg' in res_session_dict:
                        print(res_session_dict['errorMsg'])

        return start_plot()
        
    def plot_documentation(self, chart_type='line'):
        '''
        This function should display both the command (code) and display the output
        '''
        plot_types_df = self.get_plot_types()
        if len(plot_types_df[plot_types_df['ID'] == chart_type]) > 0:
            url_doc = f"{self.domain_or_ip}/api#plot-{chart_type}"
            print(url_doc)
        else:
            raise Exception("Invalid chart type. Use an ID found in the DataFrame get_plot_types()")

    def plot_template(self, *args, **kwargs):
        '''
        Plot data using existing widget template
        '''
        if len(args) > 0:
            if args[0] is not None:
                kwargs['widget_id'] = args[0]
                return self.plot(**kwargs)

        raise Exception('Missing widget_id')

    def get_plot_types(self) -> pd.DataFrame:
        '''
        Returns the list of available plot type as dataframe
        '''
        data_dict = self.get_common_api_params()
        return pd.DataFrame(self.query_service('get_plot_types', data_dict))
    
    def plot_example(self, chart_type='line') -> dict:
        '''
        TODO SPARTAQUBE: to implement
        '''
        pass 

    def save_plot(self, name, description=None, expose:bool=True, static:bool=False, public:bool=False, password=None):
        '''
        TODO SPARATAQUBE: to implement
        '''
        pass

    def clear_cache(self):
        self.plot_session_obj.clear_cache()
        data_dict = self.get_common_api_params()
        res_dict = self.query_service('clear_cache', data_dict)
        if res_dict['res'] == 1:
            print("Cache cleared!")
        else:
            print("An unexpected error occurred")

        return res_dict

    # ******************************************************************************************************************
    # CONNECTORS
    # ******************************************************************************************************************
    def get_connectors(self):
        '''
        Return the list of available connectors
        '''
        data_dict = self.get_common_api_params()
        return self.query_service('get_connectors', data_dict)

    def get_connector_tables(self, connector_id):
        '''
        Return list of available tables for a connector
        '''
        data_dict = self.get_common_api_params()
        data_dict['connector_id'] = connector_id
        return self.query_service('get_connector_tables', data_dict)
    
    def get_data_from_connector(self, connector_id, table=None, sql_query=None, output_format=None):
        '''
        output_format: dataFrame, raw
        '''
        data_dict = self.get_common_api_params()
        data_dict['connector_id'] = connector_id
        data_dict['table_name'] = table
        data_dict['query_filter'] = sql_query
        data_dict['bApplyFilter'] = 1 if sql_query is not None else 0
        res_data_dict:dict = self.query_service('get_data_from_connector', data_dict)
        if res_data_dict['res'] != 1:
            return res_data_dict
        
        is_df_format = False
        if output_format is None:
            is_df_format = True
        else:
            if output_format == 'dataFrame':
                is_df_format = True

        if is_df_format:
            if res_data_dict['res'] == 1:
                data_dict_ = json.loads(res_data_dict['data'])
            return pd.DataFrame(data_dict_['data'], index=data_dict_['index'], columns=data_dict_['columns'])
        else:
            return json.loads(res_data_dict['data'])
