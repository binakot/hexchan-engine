from pathlib import Path

module_path = Path(__file__).resolve()
module_dir = module_path.parent

# Paths
dev_dir = module_dir / '..' / 'dev'
upload_dir = dev_dir / 'upload'
upload_fake_dir = dev_dir / 'upload_fakes'
session_dir = dev_dir / 'session'
cache_dir = dev_dir / 'cache'
log_dir = dev_dir / 'log'
fixtures_dir = dev_dir / 'log'

# Create dirs
upload_dir.mkdir(parents=True, exist_ok=True)
upload_fake_dir.mkdir(parents=True, exist_ok=True)
session_dir.mkdir(parents=True, exist_ok=True)
cache_dir.mkdir(parents=True, exist_ok=True)
log_dir.mkdir(parents=True, exist_ok=True)
fixtures_dir.mkdir(parents=True, exist_ok=True)
