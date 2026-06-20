"""
Create the default deploy superuser if it does not exist.

Username: LyomasTech@{ClientName}  e.g. LyomasTech@Ahmedatef
Password: DEPLOY_SUPERUSER_PASSWORD from .env (default Lyo@22999)

Client name from DEPLOY_CLIENT_NAME, or inferred from the first ALLOWED_HOSTS subdomain.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


def _capitalize_client_name(name: str) -> str:
    name = name.strip()
    if not name:
        return ''
    return name[0].upper() + name[1:]


def resolve_client_name() -> str:
    explicit = os.environ.get('DEPLOY_CLIENT_NAME', '').strip()
    if explicit:
        return _capitalize_client_name(explicit)

    hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '').strip()
    first_host = hosts.split(',')[0].strip() if hosts else ''
    if first_host and '.' in first_host:
        subdomain = first_host.split('.')[0].strip()
        if subdomain and subdomain not in ('localhost', '127', 'www'):
            return _capitalize_client_name(subdomain)

    return ''


def build_deploy_username(client_name: str) -> str:
    return f'LyomasTech@{client_name}'


class Command(BaseCommand):
    help = 'Create LyomasTech@{Client} superuser for automated deploys (idempotent).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--client',
            dest='client_name',
            help='Client name override (e.g. Ahmedatef). Defaults to DEPLOY_CLIENT_NAME or ALLOWED_HOSTS subdomain.',
        )
        parser.add_argument(
            '--password',
            dest='password',
            help='Password override. Defaults to DEPLOY_SUPERUSER_PASSWORD or Lyo@22999.',
        )
        parser.add_argument(
            '--reset-password',
            action='store_true',
            help='Update password if the deploy superuser already exists.',
        )

    def handle(self, *args, **options):
        client_name = options.get('client_name') or resolve_client_name()
        if not client_name:
            raise CommandError(
                'Set DEPLOY_CLIENT_NAME in .env (e.g. Ahmedatef) or use --client Ahmedatef.'
            )

        password = (
            options.get('password')
            or os.environ.get('DEPLOY_SUPERUSER_PASSWORD', '').strip()
            or 'Lyo@22999'
        )
        username = build_deploy_username(client_name)
        User = get_user_model()

        user = User.objects.filter(username=username).first()
        if user:
            if options['reset_password']:
                user.set_plain_password(password)
                user.save(update_fields=['password', 'seen_password'])
                self.stdout.write(self.style.WARNING(f'Password updated for {username}'))
            else:
                self.stdout.write(f'Deploy superuser already exists: {username}')
            return

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                'Another superuser already exists — skipping deploy superuser creation.'
            )
            return

        user_code = User.next_code()
        user = User.objects.create_superuser(
            username=username,
            email='',
            password=password,
            user_code=user_code,
            first_name=client_name,
        )
        user.seen_password = password
        user.save(update_fields=['seen_password'])

        self.stdout.write(self.style.SUCCESS(f'Created deploy superuser: {username}'))
