from pathlib import Path

module_path = Path(__file__).resolve()
module_dir = module_path.parent
dev_dir = module_dir / '..' / 'dev'

# Paths
dev_paths = [
    dev_dir / 'upload',
    dev_dir / 'upload' / 'images',
    dev_dir / 'upload' / 'thumbs',
    dev_dir / 'upload_fakes',
    dev_dir / 'upload_fakes' / 'images',
    dev_dir / 'upload_fakes' / 'thumbs',
    dev_dir / 'session',
    dev_dir / 'cache',
    dev_dir / 'static',
    dev_dir / 'log',
    dev_dir / 'fixtures',
    dev_dir / 'frontend',
]

for dev_path in dev_paths:
    dev_path.mkdir(parents=True, exist_ok=True)
