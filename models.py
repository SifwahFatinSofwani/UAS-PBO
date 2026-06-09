import pandas as pd
from typing import List
from dataclasses import dataclass

class AnalisisDataError(Exception):
    pass

class DataTidakDitemukanError(AnalisisDataError):
    pass

class FormatDataTidakValidError(AnalisisDataError):
    pass

_VALID_STRESS_LEVELS = frozenset(["High", "Medium", "Low", "None"])

@dataclass(slots=True, frozen=True)
class EmployeeRecord:
    employee_id: str
    work_location: str
    stress_level: str
    mental_health: str
    social_isolation: str
    physical_activity: str
    age: int
    gender: str
    hours_worked: float
    resource_access: str
    sleep_quality: str

    def __post_init__(self) -> None:
        normalized = str(self.stress_level).capitalize()
        
        if normalized not in _VALID_STRESS_LEVELS and pd.notna(self.stress_level) and str(self.stress_level) not in ["N/A", "None"]:
            raise FormatDataTidakValidError(f"Stress level '{self.stress_level}' tidak valid.")

        if self.age < 0:
            raise FormatDataTidakValidError(f"Nilai usia tidak boleh negatif ({self.age}).")

        if self.hours_worked < 0:
            raise FormatDataTidakValidError(f"Nilai jam kerja tidak boleh negatif ({self.hours_worked}).")

    @classmethod
    def from_dataframe_row(cls, row: dict) -> "EmployeeRecord":
        return cls(
            employee_id=str(row.get("employee_id", "N/A")),
            work_location=str(row.get("work_location", "N/A")),
            stress_level=str(row.get("stress_level", "N/A")),
            mental_health=str(row.get("mental_health_condition", "N/A")),
            social_isolation=str(row.get("social_isolation_rating", "N/A")),
            physical_activity=str(row.get("physical_activity", "N/A")),
            age=int(row.get("age", 0)),
            gender=str(row.get("gender", "N/A")),
            hours_worked=float(row.get("hours_worked_per_week", 0.0)),
            resource_access=str(row.get("access_to_mental_health_resources", "N/A")),
            sleep_quality=str(row.get("sleep_quality", "N/A")),
        )

    @staticmethod
    def records_to_dataframe(records: List["EmployeeRecord"]) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "employee_id": r.employee_id,
                "work_location": r.work_location,
                "stress_level": r.stress_level,
                "mental_health_condition": r.mental_health,
                "social_isolation_rating": r.social_isolation,
                "physical_activity": r.physical_activity,
                "age": r.age,
                "gender": r.gender,
                "hours_worked_per_week": r.hours_worked,
                "access_to_mental_health_resources": r.resource_access,
                "sleep_quality": r.sleep_quality,
            }
            for r in records
        ])

    def __str__(self) -> str:
        return (
            f"EmployeeRecord(id={self.employee_id}, gender={self.gender}, "
            f"age={self.age}, stress={self.stress_level}, "
            f"mental_health={self.mental_health})"
        )

if __name__ == "__main__":
    pass