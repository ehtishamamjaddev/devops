from pathlib import Path


def test_required_project_files_exist():
    root = Path(__file__).resolve().parents[2]
    assert (root / "backend" / "app.py").is_file()
    assert (root / "backend" / "schema.py").is_file()
    assert (root / "frontend" / "package.json").is_file()
    assert (root / "README.md").is_file()
    assert (root / ".github" / "workflows" / "ci.yml").is_file()


def test_source_dataset_is_present():
    root = Path(__file__).resolve().parents[2]
    assert (root / "covertype.zip").is_file()
