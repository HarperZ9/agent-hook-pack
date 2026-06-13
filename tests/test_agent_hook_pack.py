from pathlib import Path

from agent_hook_pack import hook_pack


def test_audit_finds_expected_hooks() -> None:
    hooks = hook_pack.discover_hooks(hook_pack.HOOK_DIR)
    assert len(hooks) >= 5
    assert any(path.name == "block-secrets.py" for path in hooks)


def test_install_hooks(tmp_path: Path) -> None:
    target = tmp_path / "hooks"
    count = hook_pack.install_hooks(hook_pack.HOOK_DIR, target)
    assert count >= 5
    assert (target / "block-secrets.py").exists()
    assert (target / "check-branch.sh").exists()
    assert (target / "lint-on-save.sh").exists()
