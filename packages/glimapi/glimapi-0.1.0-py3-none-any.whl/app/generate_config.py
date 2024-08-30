import os
import shutil

def generate_toml():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = os.path.join(base_dir, "example_config.toml")
    target_config = os.path.join(os.getcwd(), "config.toml")
    
    if not os.path.exists(target_config):
        shutil.copyfile(default_config, target_config)
        print(f"config.toml file has been created at {target_config}.")
    else:
        print(f"config.toml file already exists at {target_config}.")
        
    default_middleware = os.path.join(os.path.dirname(__file__), "middlewares")
    target_copy_dir = os.path.join(os.getcwd(), "middlewares")
    if not os.path.exists(target_copy_dir):
        print(f"Creating middleware directory: {target_copy_dir}")
        shutil.copytree(default_middleware, target_copy_dir)
