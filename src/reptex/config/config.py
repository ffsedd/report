import shutil
from pathlib import Path
from typing import Any

import tomllib  # type: ignore
from pydantic import BaseModel, DirectoryPath, FilePath, model_validator


class AppConfig(BaseModel):
    """Application configuration.

    Attributes:
        default_report_config_path: Path to the default report configuration TOML file.
    """

    default_report_config_path: FilePath


class ReportPaths(BaseModel):
    """Paths used in the report configuration.

    Attributes:
        data_dir: Base directory for data.
        image_dir: Directory where images are stored.
        output_dir: Directory for report output files.
        template_dir: Directory containing report templates.
    """

    data_dir: DirectoryPath
    image_dir: DirectoryPath
    output_dir: DirectoryPath
    template_dir: DirectoryPath

    @model_validator(mode="before")
    def resolve_relative_paths(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Resolve relative paths to absolute paths based on data_dir.

        Args:
            values: Dictionary of initial field values.

        Returns:
            Dictionary with resolved paths.

        Raises:
            FileNotFoundError: If any resolved path does not exist.
        """
        base = Path(values["data_dir"])
        resolved = {}
        for key, value in values.items():
            if isinstance(value, str) and not value.startswith(("/", "~")):
                resolved_path = (base / value).resolve()
                if not resolved_path.exists():
                    raise FileNotFoundError(f"Path for '{key}' does not exist: {resolved_path}")
                resolved[key] = resolved_path
            else:
                resolved[key] = value
        return resolved


class ReportConfig(BaseModel):
    """Report configuration model.

    Attributes:
        paths: Paths used in the report.
    """

    paths: ReportPaths


class Config(BaseModel):
    """Full application configuration combining app and report configs.

    Attributes:
        app: Application-level configuration.
        report: Report-specific configuration.
    """

    app: AppConfig
    report: ReportConfig


def read_toml_file(path: Path) -> dict[str, Any]:
    """Read and parse a TOML file.

    Args:
        path: Path to the TOML file.

    Returns:
        Parsed TOML content as a dictionary.
    """

    with path.open("rb") as f:
        raw: dict[str, Any] = tomllib.load(f)
    return raw


def copy_default_report_config_if_missing(app_config: AppConfig, target_path: Path) -> None:
    """Copy the default report configuration file to the target path if it does not exist.

    Args:
        app_config: Application configuration containing the default report config path.
        target_path: Target path where the report config should be copied.
    """
    if not target_path.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(app_config.default_report_config_path, target_path)


def load_app_config(app_config_path: Path) -> AppConfig:
    """Load the application configuration from a TOML file.

    Args:
        app_config_path: Path to the app configuration TOML file.

    Returns:
        An AppConfig instance loaded from the file.
    """
    raw = read_toml_file(app_config_path)
    return AppConfig(**raw)


def load_report_config(report_config_path: Path, data_dir: Path) -> ReportConfig:
    """Load the report configuration from a TOML file, resolving relative paths.

    Args:
        report_config_path: Path to the report configuration TOML file.
        data_dir: Base data directory to resolve relative paths.

    Returns:
        A ReportConfig instance loaded and resolved.
    """
    raw = read_toml_file(report_config_path)
    raw["paths"]["data_dir"] = data_dir
    return ReportConfig(**raw)


def load_config(app_config_path: Path, data_dir: Path) -> Config:
    """Load the full configuration combining app and report configs.

    This will copy the default report config file if it does not exist in the data directory.

    Args:
        app_config_path: Path to the application config TOML file.
        data_dir: Base directory for data and report config.

    Raises:
        FileNotFoundError: If app_config_path or data_dir do not exist.

    Returns:
        A Config instance combining both configurations.
    """
    if not app_config_path.exists():
        raise FileNotFoundError(f"App config not found: {app_config_path}")
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    app_config = load_app_config(app_config_path)
    report_config_path = data_dir / "report_config.toml"

    copy_default_report_config_if_missing(app_config, report_config_path)
    report_config = load_report_config(report_config_path, data_dir)

    return Config(app=app_config, report=report_config)
