from __future__ import annotations

import csv
import json
import logging
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class SaleRecord(TypedDict):
    product: str
    quantity: int
    price: float


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "sales.csv"
OUTPUT_PATH = DATA_DIR / "metrics.json"


def ensure_sample_csv(path: Path) -> None:
    if path.exists():
        logger.debug("CSV ya existe, no se crea uno nuevo")
        return

    logger.info("Creando CSV de ejemplo")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["product", "quantity", "price"])
        writer.writerow(["Laptop", 2, 1200.0])
        writer.writerow(["Mouse", 5, 25.0])
        writer.writerow(["Keyboard", 3, 80.0])


def read_sales(path: Path) -> list[SaleRecord]:
    logger.info("Leyendo CSV de ventas")

    records: list[SaleRecord] = []

    with path.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            record: SaleRecord = {
                "product": row["product"],
                "quantity": int(row["quantity"]),
                "price": float(row["price"]),
            }
            records.append(record)

    logger.debug("Registros leídos: %s", records)
    return records


def calculate_metrics(records: Iterable[SaleRecord]) -> dict[str, float]:
    logger.info("Calculando métricas")

    total_revenue = 0.0
    total_items = 0

    for record in records:
        total_items += record["quantity"]
        total_revenue += record["quantity"] * record["price"]

    metrics = {
        "total_items": total_items,
        "total_revenue": round(total_revenue, 2),
    }

    return metrics


def export_metrics(metrics: dict[str, float], path: Path) -> None:
    logger.info("Exportando métricas a JSON")

    output = {
        "generated_at": datetime.now(UTC).isoformat(),
        "metrics": metrics,
    }

    with path.open(mode="w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    logger.info("Archivo generado: %s", path)


def main() -> None:
    logger.info("Inicio del proceso de ingesta")

    ensure_sample_csv(CSV_PATH)

    sales = read_sales(CSV_PATH)
    metrics = calculate_metrics(sales)
    export_metrics(metrics, OUTPUT_PATH)

    logger.info("Proceso finalizado correctamente")


if __name__ == "__main__":
    main()
