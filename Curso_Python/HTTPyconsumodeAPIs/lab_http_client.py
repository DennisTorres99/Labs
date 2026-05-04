from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Final

import httpx

BASE_DIR = Path(__file__).parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

RESOURCE_URL: Final[str] = "https://httpbin.org/bytes/10485760"
OUTPUT_FILE = DOWNLOAD_DIR / "resource.bin"

TIMEOUT_SECONDS: Final[float] = 5.0
MAX_RETRIES: Final[int] = 3
RETRY_DELAY_SECONDS: Final[float] = 2.0


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("http.client")


def download_resource(
    *,
    url: str,
    output_path: Path,
    timeout: float,
    max_retries: int,
) -> None:

    for attempt in range(1, max_retries + 1):
        try:
            logger.info("Intento %s de descarga: %s", attempt, url)

            with httpx.Client(timeout=timeout, http2=True) as client:
                with client.stream("GET", url) as response:
                    response.raise_for_status()

                    with output_path.open("wb") as file:
                        for chunk in response.iter_bytes(chunk_size=8_192):
                            file.write(chunk)

            logger.info("Descarga completada correctamente")
            return

        except httpx.TimeoutException:
            logger.warning(
                "Timeout durante la descarga (intento %s/%s)",
                attempt,
                max_retries,
            )

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            # Errores del cliente: no se reintentan
            if 400 <= status_code < 500:
                logger.error(
                    "Error del cliente (%s). No se reintenta.",
                    status_code,
                )
                raise

            # Errores del servidor: posibles reintentos
            logger.warning(
                "Error del servidor (%s). Puede ser transitorio.",
                status_code,
            )

        except httpx.HTTPError as exc:
            logger.warning("Error HTTP genérico: %s", exc)

        if attempt < max_retries:
            logger.info(
                "Reintentando en %s segundos...",
                RETRY_DELAY_SECONDS,
            )
            time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError("No fue posible descargar el recurso tras varios intentos")


def main() -> None:
    logger.info("Inicio del proceso de descarga")

    download_resource(
        url=RESOURCE_URL,
        output_path=OUTPUT_FILE,
        timeout=TIMEOUT_SECONDS,
        max_retries=MAX_RETRIES,
    )

    logger.info("Proceso finalizado correctamente")


if __name__ == "__main__":
    main()
