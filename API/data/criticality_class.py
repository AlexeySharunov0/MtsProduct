from __future__ import annotations

from typing import List, Optional

from API.data.config_class import BaseModel


class IntegrationCriticalityClass(BaseModel):
    id: str
    processedAt: Optional[str]
    date: str
    productCode: str
    productName: str
    previousCriticalityClass: str
    receivedCriticalityClass: str


class IntegrationsCriticalityClass(BaseModel):
    integrations_cc: List[IntegrationCriticalityClass]
