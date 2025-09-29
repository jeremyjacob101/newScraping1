import logging, os, sys
import pathlib, time, threading

logger = logging.getLogger("sel")


def dump_artifacts(driver, prefix: str = "fail", note: str | None = None) -> tuple[str, str]:
    """
    Saves a screenshot and page_source into utils/logger_artifacts/.
    Returns (png_path, html_path).
    """
    artifact_dir = pathlib.Path("utils/logger_artifacts")
    # Clean up old artifacts on each run
    if artifact_dir.exists():
        for f in artifact_dir.glob("*"):
            try:
                f.unlink()
            except Exception:
                pass
    artifact_dir.mkdir(parents=True, exist_ok=True)

    ts = time.strftime("%Y%m%d-%H%M%S")
    thread_name = threading.current_thread().name.replace(" ", "_")
    safe_prefix = prefix.replace(" ", "_")
    base = artifact_dir / f"{safe_prefix}-{thread_name}-{ts}"
    if note:
        base = str(base) + f"-{note}"
    else:
        base = str(base)

    png_path = f"{base}.png"
    html_path = f"{base}.html"

    try:
        if getattr(driver, "save_screenshot", None):
            driver.save_screenshot(png_path)
    except Exception as e:
        logger.warning("Failed to save screenshot: %s", e)

    try:
        src = getattr(driver, "page_source", "") or ""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(src)
    except Exception as e:
        logger.warning("Failed to save page_source: %s", e)

    return png_path, html_path


def setup_logging(level: str | int = None) -> None:
    if level is None:
        level = os.getenv("LOG_LEVEL", "DEBUG")
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.DEBUG)

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
    logger.setLevel(level)


def artifactPrinting(obj=None, *, driver=None, prefix=None, url=None, note: str | None = None):
    try:
        name = prefix or (getattr(obj, "CINEMA_NAME", None) or (obj.__class__.__name__ if obj else "Unknown"))
    except Exception:
        name = "Unknown"

    drv = driver or (getattr(obj, "driver", None) if obj is not None else None)
    if url is None:
        try:
            url = getattr(drv, "current_url", "?")
        except Exception:
            url = "?"

    logger.error(
        "\n\n\n\t\t-------- ERROR --------\n\n\n[%s] unhandled error at url=%s\n\n\n\t\t-------- ERROR --------\n\n\n",
        name,
        url,
        exc_info=True,
    )

    try:
        png, html = dump_artifacts(drv, prefix=name, note=note)
        print(f"[{name}] Saved artifacts:\n  screenshot: {png}\n  html:       {html}")
        return png, html
    except Exception as capture_err:
        print(f"[{name}] Failed to dump artifacts: {capture_err}")
        return None, None
