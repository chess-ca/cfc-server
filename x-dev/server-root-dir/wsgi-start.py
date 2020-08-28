
from pathlib import Path
import sys, os

_application_dir = Path(__file__).parent
_application_config = dict(
    APP_CONFIG_DIR=str(Path(_application_dir, 'private', 'config')),
    APP_DATA_DIR=str(Path(_application_dir, 'private', 'data')),
)
_py_version = f'{sys.version_info[0]}.{sys.version_info[1]}'


# ---- Application configuration
os.environ.update(**_application_config)

# ---- Get name of current deployed directory
fn = Path(__file__).with_suffix('.current-deploy.txt')
if not fn.exists():
    print(f'ERROR: File with name of the deploy-dir not found: {fn}')
    exit(9901)
with open(str(fn), 'rt') as f:
    deploy_dirname = (f.read()).strip()
deploy_dir = Path(_application_dir, deploy_dirname)
if not deploy_dir.exists():
    print(f'ERROR: Deployed code directory not found: {deploy_dir}')
    exit(9902)
pylib_dir = Path(deploy_dir, 'lib', f'python{_py_version}')
if not pylib_dir.exists():
    print(f'ERROR: Python library directory not found: {pylib_dir}')
    exit(9903)


# ---- Add libraries of the current deploy to Python's path
sys.path.insert(0, str(pylib_dir))
sys.path.insert(0, str(deploy_dir))

from cfc_server import application
