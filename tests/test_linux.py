from labgridhelper import linux

def test_get_systemd_version(command, monkeypatch):
    systemd_version = 'systemd 249 (249.5-2-arch)\n+PAM +AUDIT -SELINUX\n'

    monkeypatch.setattr(command, 'run_check', lambda cmd: [systemd_version])

    assert linux.get_systemd_version(command) == 249
