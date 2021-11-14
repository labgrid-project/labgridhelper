from labgridhelper import linux
import pytest

def test_get_systemd_version(command, monkeypatch):
    systemd_version = 'systemd 249 (249.5-2-arch)\n+PAM +AUDIT -SELINUX\n'

    monkeypatch.setattr(command, 'run_check', lambda cmd: [systemd_version])

    assert linux.get_systemd_version(command) == 249

@pytest.mark.parametrize("systemd_version", [230, 240])
def test_get_systemd_status(command, monkeypatch, systemd_version):
    monkeypatch.setattr(linux, 'get_systemd_version', lambda cmd: systemd_version)

    status = {
        230: 'a(ssssssouso) 1 "systemd-resolved.service" "Network Name Resolution" "loaded" "active"' + \
            ' "running" "" "/org/freedesktop/systemd1/unit/systemd_2dresolved_2eservice" 0 "" "/"',
        240: '{"type":"a(ssssssouso)","data":[[["systemd-resolved.service",' + \
            '"Network Name Resolution","loaded","active","running","",' + \
            '"/org/freedesktop/systemd1/unit/systemd_2dresolved_2eservice",0,"","/"]]]}',
    }

    monkeypatch.setattr(command, 'run_check', lambda cmd: [status[systemd_version]])

    status = linux.get_systemd_status(command)

    assert len(status.keys()) == 1
    assert status['systemd-resolved.service']["description"] == 'Network Name Resolution'
    assert status['systemd-resolved.service']["load"] == 'loaded'
    assert status['systemd-resolved.service']["active"] == 'active'
    assert status['systemd-resolved.service']["sub"] == 'running'
    assert status['systemd-resolved.service']["follow"] == ''
    assert status['systemd-resolved.service']["path"] == '/org/freedesktop/systemd1/unit/systemd_2dresolved_2eservice'
    assert status['systemd-resolved.service']["id"] == 0
    assert status['systemd-resolved.service']["type"] == ''
    assert status['systemd-resolved.service']["objpath"] == '/'
