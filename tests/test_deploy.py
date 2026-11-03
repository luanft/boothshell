"""POST /deploy chay quyen root voi tham so tu ben ngoai: token + regex + argv."""
import os
import stat

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    script = tmp_path / "update.sh"
    out = tmp_path / "args.txt"
    script.write_text(f'#!/bin/sh\nprintf "%s|" "$@" > {out}\necho done\n')
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PHOTOSHELL_TOKEN", "tok")
    monkeypatch.setenv("UPDATE_SCRIPT", str(script))
    monkeypatch.setattr(main, "DEPLOY_LOG", str(tmp_path / "deploy.log"))
    c = TestClient(main.app)
    c.out = out
    return c


def test_deploy_runs_script_with_version_as_single_argv(client):
    r = client.post("/deploy", json={"version": "1.8.610"}, headers={"X-Photoshell-Token": "tok"})
    assert r.status_code == 200
    assert client.out.read_text() == "1.8.610|"
    log = client.get("/deploy/log", headers={"X-Photoshell-Token": "tok"}).json()
    assert "exit code: 0" in log["log"]


@pytest.mark.parametrize("headers", [{}, {"X-Photoshell-Token": "wrong"}])
def test_deploy_rejects_missing_or_wrong_token(client, headers):
    r = client.post("/deploy", json={"version": "1.8.610"}, headers=headers)
    assert r.status_code == 401
    assert not client.out.exists()


def test_deploy_refuses_everything_when_token_not_configured(client, monkeypatch):
    monkeypatch.delenv("PHOTOSHELL_TOKEN")
    r = client.post("/deploy", json={"version": "1.8.610"}, headers={"X-Photoshell-Token": ""})
    assert r.status_code == 401


@pytest.mark.parametrize("version", ["1.8", "1.8.610; reboot", "$(reboot)", "../x", "1.8.610\n"])
def test_deploy_rejects_bad_version(client, version):
    r = client.post("/deploy", json={"version": version}, headers={"X-Photoshell-Token": "tok"})
    assert r.status_code == 400
    assert not client.out.exists()


def test_deploy_log_needs_token(client):
    assert client.get("/deploy/log").status_code == 401


def test_missing_script_is_logged_not_crashed(client, monkeypatch):
    monkeypatch.setenv("UPDATE_SCRIPT", "/nonexistent/update.sh")
    r = client.post("/deploy", json={"version": "1.8.610"}, headers={"X-Photoshell-Token": "tok"})
    assert r.status_code == 200
    log = client.get("/deploy/log", headers={"X-Photoshell-Token": "tok"}).json()["log"]
    assert "not executable" in log
