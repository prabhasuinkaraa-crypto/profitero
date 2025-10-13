import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

ARTIFACTS_DIR_ENV = "ARTIFACTS_DIR"


def before_all(context):
    # Load env
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(env_path)

    context.base_url = os.getenv('BASE_URL', 'https://www.profitero.com')
    context.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    context.browser = os.getenv('BROWSER', 'chrome').lower()
    context.implicit_wait = int(os.getenv('IMPLICIT_WAIT', '0'))
    context.explicit_wait = int(os.getenv('EXPLICIT_WAIT', '15'))
    context.pageload_timeout = int(os.getenv('PAGELOAD_TIMEOUT', '60'))
    context.request_timeout = int(os.getenv('REQUEST_TIMEOUT', '20'))

    # Artifacts directory
    artifacts_dir = os.getenv(ARTIFACTS_DIR_ENV, 'artifacts')
    context.artifacts_dir = Path(artifacts_dir)
    context.artifacts_dir.mkdir(parents=True, exist_ok=True)


def after_step(context, step):
    # Capture diagnostics on failure (if a WebDriver exists)
    if step.status == 'failed' and getattr(context, 'driver', None):
        scenario_name = getattr(context, 'scenario', None).name if getattr(context, 'scenario', None) else 'scenario'
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        base = f"{scenario_name}__{step.name}__{timestamp}"
        safe_base = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in base)[:180]
        png_path = context.artifacts_dir / f"{safe_base}.png"
        html_path = context.artifacts_dir / f"{safe_base}.html"
        try:
            context.driver.save_screenshot(str(png_path))
        except Exception:
            pass
        try:
            html = context.driver.page_source
            html_path.write_text(html, encoding='utf-8', errors='ignore')
        except Exception:
            pass


def before_scenario(context, scenario):
    # Track current scenario for artifact naming in after_step
    context.scenario = scenario


def after_scenario(context, scenario):
    # Save scenario on context for after_step naming and ensure driver teardown
    driver = getattr(context, 'driver', None)
    if driver:
        try:
            driver.quit()
        except Exception:
            pass
