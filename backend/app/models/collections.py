"""Mongo collection model names and helpers."""


class ScrapedDataModel:
    """Primary scan result collection model."""

    collection_name = "scraped_data"


class AlertsModel:
    """Alert collection model."""

    collection_name = "alerts"


class IOCModel:
    """IOC tracking collection model."""

    collection_name = "iocs"


class MonitorModel:
    """Monitor metadata collection model."""

    collection_name = "monitors"
