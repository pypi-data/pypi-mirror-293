import logging
from dataclasses import dataclass

from sonarqube import SonarCloudClient


@dataclass
class SonarCloudProjectReport:
    project_name: str
    last_analysis_date: str
    last_analysis_commit_id: str
    bugs: int
    code_smells: int
    coverage: float
    security_hotspots: int
    vulnerabilities: int
    tag_name: str

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.last_analysis_date = ""
        self.last_analysis_commit_id = ""
        self.bugs = 0
        self.code_smells = 0
        self.coverage = 0
        self.security_hotspots = 0
        self.vulnerabilities = 0
        self.tag_name = ""


def query_sonarcloud_project_report(
    project_name: str, token: str
) -> SonarCloudProjectReport:
    logging.info(f"Querying SonarCloud project info for '{project_name}'")
    client = SonarCloudClient(sonarqube_url="https://sonarcloud.io", token=token)

    project_infos = client.projects.get_project(
        key=f"lupindental_{project_name}", organization="lupindental"
    )

    logging.info(f"Querying latest analysis details for '{project_name}'")
    project_measures = client.measures.get_component_with_specified_measures(
        component=f"lupindental_{project_name}",
        branch="main",
        metricKeys="bugs,code_smells,coverage,security_hotspots,vulnerabilities",
    )
    assert project_measures["component"]["name"] == project_name

    result = SonarCloudProjectReport(project_name)
    result.last_analysis_date = project_infos["lastAnalysisDate"]
    result.last_analysis_commit_id = project_infos["revision"]

    # fill measures
    filled_measures = 0
    for m in project_measures["component"]["measures"]:
        match m["metric"]:
            case "bugs":
                result.bugs = int(m["value"])
                filled_measures += 1
            case "code_smells":
                result.code_smells = int(m["value"])
                filled_measures += 1
            case "coverage":
                result.coverage = float(m["value"])
                assert result.coverage <= 100
                filled_measures += 1
            case "security_hotspots":
                result.security_hotspots = int(m["value"])
                filled_measures += 1
            case "vulnerabilities":
                result.vulnerabilities = int(m["value"])
                filled_measures += 1
    assert filled_measures == 5

    return result
