from bddcli import stderr, stdout, status, when

from yhttp.markdown import __version__


def test_cli_version(cliapp):
    with cliapp('--version'):
        assert status == 0
        assert stdout.strip() == __version__
        assert str(stderr) == ''

        when('')
        assert status == 0
        assert str(stderr) == ''


if __name__ == '__main__':
    from yhttp.markdown.main import Main
    Main.quickstart(['--version'])
