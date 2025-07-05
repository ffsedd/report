import shutil
import tomllib
from pathlib import Path
from typing import Any, List

from pydantic import BaseModel, DirectoryPath, FilePath, model_validator


class AppConfig(BaseModel):
    default_template_path: FilePath
    default_report_config_path: FilePath


class Metadata(BaseModel):
    title: str
    author: str


class ReportPaths(BaseModel):
    data_dir: DirectoryPath
    image_dir: DirectoryPath
    output_dir: DirectoryPath
    template_dir: DirectoryPath

    @model_validator(mode="before")
    def resolve_relative_paths(cls, values: dict[str, Any]) -> dict[str, Any]:
        base = Path(values["data_dir"])
        resolved = {}
        for key, value in values.items():
            # Resolve only string-like values that look like paths
            if isinstance(value, str) and not value.startswith(("/", "~")):
                resolved[key] = (base / value).resolve()
                print(key, value, resolved[key])
                if not resolved[key].exists():
                    raise FileNotFoundError(resolved[key])
            else:
                resolved[key] = value

        return resolved


class ImageOptions(BaseModel):
    include_thumbnails: bool = False
    caption_prefix: str = "Figure"
    extensions: List[str] = [".png", ".jpg", ".jpeg"]


class LayoutOptions(BaseModel):
    margin_mm: float = 25.0
    font_size_pt: int = 11
    page_size: str = "A4"


class ReportConfig(BaseModel):
    metadata: Metadata
    paths: ReportPaths
    images: ImageOptions = ImageOptions()
    layout: LayoutOptions = LayoutOptions()


class Config(BaseModel):
    app: AppConfig
    report: ReportConfig


def load_app_config(app_config_path: Path) -> AppConfig:
    with app_config_path.open("rb") as f:
        raw = tomllib.load(f)
    return AppConfig(**raw)


def load_report_config(report_config_path: Path, data_dir: Path) -> ReportConfig:
    with report_config_path.open("rb") as f:
        raw = tomllib.load(f)

    # Inject `_data_dir` to resolve relative paths inside validator
    raw["paths"]["data_dir"] = data_dir

    return ReportConfig(**raw)


def load_config(
    app_config_path: Path,
    data_dir: Path,
) -> Config:

    if not app_config_path.exists():
        raise FileNotFoundError(app_config_path)
    if not data_dir.exists():
        raise FileNotFoundError(data_dir)

    app_config = load_app_config(app_config_path)

    report_config_path = data_dir / "report_config.toml"

    # Copy default report_config if missing
    if not report_config_path.exists():
        report_config_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(app_config.default_report_config_path, report_config_path)

    report_config = load_report_config(report_config_path, data_dir=data_dir)

    return Config(app=app_config, report=report_config)
