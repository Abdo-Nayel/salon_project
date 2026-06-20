"""PostgreSQL backup & restore helpers."""
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from django.conf import settings


BACKUP_DIR = Path(settings.BASE_DIR) / 'backups'


def _pg_bin(name):
    found = shutil.which(name)
    if found:
        return found
    # Linux (Debian/Ubuntu server)
    for pattern in (
        Path(f'/usr/bin/{name}'),
        Path(f'/usr/local/bin/{name}'),
    ):
        if pattern.exists():
            return str(pattern)
    pg_root = Path('/usr/lib/postgresql')
    if pg_root.is_dir():
        for ver_dir in sorted(pg_root.iterdir(), reverse=True):
            candidate = ver_dir / 'bin' / name
            if candidate.exists():
                return str(candidate)
    # Windows
    for ver in range(20, 10, -1):
        path = Path(f'C:/Program Files/PostgreSQL/{ver}/bin/{name}.exe')
        if path.exists():
            return str(path)
    return None


def _db_params():
    db = settings.DATABASES['default']
    engine = db.get('ENGINE', '')
    if 'postgresql' not in engine:
        raise RuntimeError('النسخ الاحتياطي SQL متاح فقط مع PostgreSQL')
    return {
        'host': db.get('HOST') or 'localhost',
        'port': str(db.get('PORT') or 5432),
        'name': db['NAME'],
        'user': db['USER'],
        'password': db.get('PASSWORD', ''),
    }


def _pg_env(password):
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    return env


def latest_backup_info():
    if not BACKUP_DIR.exists():
        return None
    files = sorted(BACKUP_DIR.glob('salon_backup_*.sql'), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return None
    f = files[0]
    return {
        'filename': f.name,
        'path': f,
        'mtime': datetime.fromtimestamp(f.stat().st_mtime),
    }


def create_backup_sql():
    pg_dump = _pg_bin('pg_dump')
    if not pg_dump:
        raise RuntimeError(
            'لم يتم العثور على pg_dump. ثبّت PostgreSQL أو أضف مجلد bin إلى PATH'
        )
    params = _db_params()
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'salon_backup_{ts}.sql'
    filepath = BACKUP_DIR / filename
    cmd = [
        pg_dump,
        '-h', params['host'],
        '-p', params['port'],
        '-U', params['user'],
        '-d', params['name'],
        '--clean', '--if-exists',
        '--no-owner', '--no-acl',
        '-f', str(filepath),
    ]
    result = subprocess.run(
        cmd, env=_pg_env(params['password']),
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or 'فشل إنشاء النسخة الاحتياطية')
    return filepath


def restore_backup_sql(uploaded_file):
    psql = _pg_bin('psql')
    if not psql:
        raise RuntimeError(
            'لم يتم العثور على psql. ثبّت PostgreSQL أو أضف مجلد bin إلى PATH'
        )
    params = _db_params()
    suffix = Path(uploaded_file.name).suffix or '.sql'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name
    try:
        cmd = [
            psql,
            '-h', params['host'],
            '-p', params['port'],
            '-U', params['user'],
            '-d', params['name'],
            '-v', 'ON_ERROR_STOP=1',
            '-f', tmp_path,
        ]
        result = subprocess.run(
            cmd, env=_pg_env(params['password']),
            capture_output=True, text=True, timeout=600,
        )
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip() or 'فشل الاستعادة'
            raise RuntimeError(err)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
