from __future__ import annotations

from pathlib import Path
import re

HOOK_EXTENSIONS = (".py", ".sh")
SENSITIVE_PATTERNS = (
    r"ghp_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"BEGIN [A-Z ]*PRIVATE KEY-----",
)

HOOK_DIR = Path(__file__).resolve().parent / "hooks"


def discover_hooks(source_dir: Path | str = HOOK_DIR) -> list[Path]:
    root = Path(source_dir)
    hooks: list[Path] = []
    if not root.exists():
        return hooks
    for path in sorted(root.iterdir()):
        if path.is_file() and path.suffix in HOOK_EXTENSIONS:
            hooks.append(path)
    return hooks


def audit_hooks(source_dir: Path | str = HOOK_DIR) -> list[tuple[str, str]]:
    root = Path(source_dir)
    if not root.exists():
        return [(str(root), "hook_dir_missing")]

    findings: list[tuple[str, str]] = []
    compiled = [re.compile(item) for item in SENSITIVE_PATTERNS]
    for hook in discover_hooks(root):
        text = hook.read_text(encoding="utf-8", errors="ignore")
        for index, pattern in enumerate(compiled):
            if pattern.search(text):
                findings.append((str(hook), f"secret_pattern_{index}"))
    return findings


def install_hooks(source_dir: Path | str, target_dir: Path | str) -> int:
    src = Path(source_dir)
    dst = Path(target_dir)
    dst.mkdir(parents=True, exist_ok=True)
    copied = 0
    for hook in discover_hooks(src):
        dst.joinpath(hook.name).write_text(
            hook.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        copied += 1
    return copied
