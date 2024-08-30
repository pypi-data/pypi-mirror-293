from dataclasses import dataclass
from enum import Enum

from sonarcloud_report.client import SonarCloudProjectReport


@dataclass
class Thresholds:
    bugs: int = 0
    code_coverage: str = "N/A"
    code_smells: str = "N/A"
    security_hotspots: int = 0
    vulnerabilities: int = 0


class QualityGateStatus(Enum):
    PASS = "🟢 PASS"
    FAIL = "❌ FAIL"
    NA = "⚪ N/A"

    def __str__(self):
        return self.value


@dataclass
class QualityGate:
    bugs: QualityGateStatus = QualityGateStatus.NA
    code_coverage: QualityGateStatus = QualityGateStatus.NA
    code_smells: QualityGateStatus = QualityGateStatus.NA
    security_hotspots: QualityGateStatus = QualityGateStatus.NA
    vulnerabilities: QualityGateStatus = QualityGateStatus.NA


def compare_with_thresholds(project_report: SonarCloudProjectReport) -> QualityGate:
    thresholds = Thresholds()
    quality = QualityGate()

    quality.bugs = (
        QualityGateStatus.FAIL
        if project_report.bugs > thresholds.bugs
        else QualityGateStatus.PASS
    )
    quality.security_hotspots = (
        QualityGateStatus.FAIL
        if project_report.security_hotspots > thresholds.security_hotspots
        else QualityGateStatus.PASS
    )
    quality.vulnerabilities = (
        QualityGateStatus.FAIL
        if project_report.vulnerabilities > thresholds.vulnerabilities
        else QualityGateStatus.PASS
    )

    return quality
