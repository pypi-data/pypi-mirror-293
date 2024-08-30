import sys, os, io, subprocess, threading, socket, psutil, json, time, requests, platform, tempfile
import django
import webbrowser
from django.core.management import call_command

thread_failed = False
thread_error_msg = None

# **********************************************************************************************************************
def set_environment_variable(name, value):
    try:
        os.environ[name] = value
    except Exception as e:
        print(f"Error setting environment variable '{name}': {e}")

def set_environment_variable_persist(name, value):
    try:
        subprocess.run(['setx', name, value])
        # print(f"Environment variable '{name}' set to '{value}'")
    except Exception as e:
        # print(f"Error setting environment variable '{name}': {e}")
        pass

def find_process_by_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def is_port_available(port:int) -> bool:
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Try to connect to the specified port
            s.bind(("localhost", port))
            return True
    except socket.error:
        return False
    
def generate_port() -> int:
    port = 8664
    while not is_port_available(port):
        port += 1

    return port
# **********************************************************************************************************************

def set_spartaqube_shortcut():
    '''
    Set spartaqube exec to env
    '''
    current_path = os.path.dirname(__file__)
    base_path = os.path.dirname(current_path)
    spartaqube_exec = os.path.join(base_path, 'cli/spartaqube')
    set_environment_variable_persist('spartaqube', spartaqube_exec)

def db_make_migrations_migrate():
    '''
    
    '''
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    new_stdout, new_stderr = io.StringIO(), io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = new_stdout, new_stderr
    try:
        call_command('makemigrations')
        call_command('migrate')
    finally:
        # Reset stdout and stderr to their original values    
        sys.stdout, sys.stderr = old_stdout, old_stderr
        
def create_public_user():
    '''
    Public user
    '''
    current_path = os.path.dirname(__file__)
    base_project = os.path.dirname(current_path)
    sys.path.insert(0, os.path.join(base_project, '/project/management'))
    from project.management.commands.createpublicuser import Command as CommandCreatePublicUser
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    CommandCreatePublicUser().handle()

def create_admin_user():
    '''
    Admin user
    '''
    current_path = os.path.dirname(__file__)
    base_project = os.path.dirname(current_path)
    sys.path.insert(0, os.path.join(base_project, '/project/management'))
    from project.management.commands.createadminuser import Command as CommandCreateAdminUser
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    CommandCreateAdminUser().handle()

def get_default_port():
    try:
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, 'app_data.json'), "r") as json_file:
            loaded_data_dict = json.load(json_file)
        
        return loaded_data_dict['default_port']
    except:
        return 8664
        
def is_server_live(url):
    '''
    Ping the server to check if it's live
    '''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

def erase_line():
    sys.stdout.write('\r')
    sys.stdout.write(' ' * 80)
    sys.stdout.write('\r')
    sys.stdout.flush()

def get_platform() -> str:
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Linux':
        return 'linux'
    elif system == 'Darwin':
        return 'mac'
    else:
        return None
    
def start_server(port=None, silent=False, b_open_browser=False, is_blocking=True):
    '''
    runserver at port
    '''

    if port is None:
        port = generate_port()
    else:
        if not is_port_available(port):
            # port = generate_port()
            raise Exception(f"{port} port is already used...")

    def thread_job(stderr_file_path):
        global thread_failed, thread_error_msg
        current_path = os.path.dirname(__file__)
        base_path = os.path.dirname(current_path)
        # f"python manage.py runserver 0.0.0.0:{port} &"
        # waitress-serve --threads=4 --port=8000 your_project.wsgi:application
        # gunicorn --workers 4 your_project.wsgi:application
        dev_server = f"python {os.path.join(base_path, 'manage.py')} runserver 0.0.0.0:{port}"
        gunicorn_server = f"gunicorn --workers 3 --bind 0.0.0.0:{port} 'spartaqube_app'.wsgi:application &"
        waitress_server = f"waitress-serve --host=0.0.0.0 --port={port} spartaqube_app.wsgi:application &"
        platform = get_platform()
        server_req = gunicorn_server
        if platform == 'windows':
            server_req = waitress_server

        # server_req = dev_server
        # server_req = f"/usr/local/bin/python3.11 --version"
        # print("server_req > "+str(server_req))
        with open(stderr_file_path, 'w') as stderr_file:
            process = subprocess.Popen(
                server_req, 
                stdout=subprocess.PIPE, 
                stderr=stderr_file,
                # stderr=subprocess.PIPE, 
                shell=True,
                cwd=base_path,
            )
            if is_blocking:
                process.communicate() # This line is important to block the terminal running spartaqube

    # Create a temporary file to hold the stderr output
    stderr_file = tempfile.NamedTemporaryFile(delete=False)
    stderr_file_path = stderr_file.name
    stderr_file.close()

    t = threading.Thread(target=thread_job, args=(stderr_file_path, ))
    t.start()
    # thread_job()
    
    i = 0
    while True:
        if not silent:
            # animation
            if i > 3:
                i = 0
            erase_line()
            sys.stdout.write(f'\rWaiting for server application{i*"."}')
            sys.stdout.flush()
            i += 1

        # Check if the stderr file has any content
        with open(stderr_file_path, 'r') as f:
            stderr_output = f.read()
            if stderr_output is not None:
                if len(stderr_output) > 0:
                    global thread_failed, thread_error_msg
                    thread_failed = True
                    thread_error_msg = stderr_output

        if is_server_live(f"http://127.0.0.1:{port}"):
            break
        
        if thread_failed:  # Check if thread is alive or if it failed
            print("\nThread crashed or command failed. Exiting loop.")
            raise Exception(thread_error_msg)
            # break

        time.sleep(1)  # Wait for a second before pinging again

    # Clean up the temporary file
    try:
        os.unlink(stderr_file_path)
    except:
        pass
    
    if not silent:
        erase_line()
    
    app_data_dict = {'default_port': port}
    current_path = os.path.dirname(__file__)
    with open(os.path.join(current_path, "app_data.json"), "w") as json_file:
        json.dump(app_data_dict, json_file)

    if b_open_browser:
        webbrowser.open(f"http://localhost:{port}")

def stop_server(port=None):
    if port is None:
        port = get_default_port()

    if port is not None:
        process = find_process_by_port(port)
        if process:
            print(f"Found process running on port {port}: {process.pid}")
            process.terminate()
            print(f"SpartaQube server stopped")
        else:
            print(f"No process found running on port {port}.")
    else:
        raise Exception("Port not specify")

def django_setup():
    '''
    Set up Django environment
    '''
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartaqube_app.settings')
    django.setup()

def entrypoint(port, force_startup=False, silent=False, b_open_browser=False):
    '''
    
    '''
    if not silent:
        sys.stdout.write("Preparing SpartaQube, please wait...")
    
    if not is_port_available(port) and not force_startup: 
        # We do nothing as we should already be connected to the required port
        # Application is supposed to be running already on this port. If an error, it will be found in the get_status called after
        pass
    else:
        # set_spartaqube_shortcut()
        django_setup()
        # has_changes = db_make_migrations()
        # print("--- %s seconds db_make_migrations ---" % (time.time() - start_time))
        # if has_changes:
        #     db_migrate()
        db_make_migrations_migrate()
        create_public_user()
        create_admin_user()
        start_server(port=port, silent=silent, b_open_browser=b_open_browser)

if __name__ == '__main__':
    entrypoint()