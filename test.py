# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner
import pytest

from click_default_group import DefaultGroup


@click.group(cls=DefaultGroup, invoke_without_command=True)
@click.option('--group-only', is_flag=True)
def cli(group_only):
    # Called if invoke_without_command=True.
    if group_only:
        click.echo('--group-only passed.')


@cli.command(default=True)
@click.option('--foo', default='foo')
def foo(foo):
    click.echo(foo)


@cli.command()
def bar():
    click.echo('bar')


r = CliRunner()


def test_default_command_with_arguments():
    assert r.invoke(cli, ['--foo', 'foooo']).output == 'foooo\n'
    assert 'no such option' in r.invoke(cli, ['-x']).output


def test_default_command_without_arguments():
    assert r.invoke(cli, []).output == 'foo\n'


def test_group_arguments():
    assert r.invoke(cli, ['--group-only']).output == '--group-only passed.\n'


def test_no_more_default_command():
    with pytest.raises(RuntimeError):
        # Default command already defined.
        @cli.command(default=True)
        def baz():
            pass
    assert len(cli.commands) == 2


def test_explicit_command():
    assert r.invoke(cli, ['foo']).output == 'foo\n'
    assert r.invoke(cli, ['bar']).output == 'bar\n'


if __name__ == '__main__':
    cli()