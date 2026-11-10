"""Exercise Sapper's graph lifecycle without touching a real project."""
from pathlib import Path
import subprocess
import tempfile

cli = Path(__file__).resolve().parents[2] / 'bin' / 'sapper'
with tempfile.TemporaryDirectory(prefix='ctf-wp-smoke-') as temporary:
    store = Path(temporary) / '.sapper'
    def run(*args):
        return subprocess.check_output([str(cli), '--store', str(store), *args], text=True)
    run('init', '--goal', 'offline environment validation')
    fact = run('fact', 'CLI available', '--kind', 'note').strip()
    intent = run('intent', '--from', fact, 'verify graph lifecycle').strip()
    run('done', intent, '--fact', 'graph lifecycle verified')
    print(run('validate'), end='')
    assert 'offline environment validation' in run('status')
    print('Sapper graph lifecycle passed')
