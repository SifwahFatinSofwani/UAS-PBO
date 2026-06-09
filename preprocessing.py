import pandas as pd
from typing import List, Callable, Any
from abc import ABC, abstractmethod
import time
import functools
import models
EmployeeRecord = models.EmployeeRecord
FormatDataTidakValidError = models.FormatDataTidakValidError
DataTidakDitemukanError = models.DataTidakDitemukanError

def execution_logger(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(self, *args, **kwargs)
        duration = time.time() - start_time
        print(f"{self.__class__.__name__} selesai dalam {duration:.4f} detik")
        return result
    return wrapper

class PreprocessingStep(ABC):
    @abstractmethod
    def process(self, df: pd.DataFrame) -> pd.DataFrame: pass

class MissingValueHandler(PreprocessingStep):
    @execution_logger
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        cat_cols = [
            "mental_health_condition", "stress_level", "physical_activity",
            "work_location", "gender", "access_to_mental_health_resources", "sleep_quality",
        ]
        for col in cat_cols:
            if col in df.columns:
                df[col] = df[col].fillna("None")
        num_cols = ["social_isolation_rating", "hours_worked_per_week", "age"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df

class ColumnStandardizer(PreprocessingStep):
    @execution_logger
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [str(col).lower() for col in df.columns]
        return df

class DuplicateRowRemover(PreprocessingStep):
    @execution_logger
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        if removed:
            print(f"\n{removed} baris duplikat dihapus.")
        return df

class EmployeeRecordConverter(PreprocessingStep):
    @execution_logger
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        records: List[EmployeeRecord] = [
            EmployeeRecord.from_dataframe_row(row)
            for row in df.to_dict(orient="records")
        ]
        print(f"\n{len(records)} baris dikonversi ke EmployeeRecord.")
        for rec in records[:2]:
            print(f"  -> {rec}")
        return EmployeeRecord.records_to_dataframe(records)

class PreprocessingPipeline:
    def __init__(self) -> None:
        self.__steps: List[PreprocessingStep] = []  

    def add_step(self, step: PreprocessingStep) -> None:
        if not isinstance(step, PreprocessingStep):
            raise FormatDataTidakValidError("Step harus berupa PreprocessingStep.")
        self.__steps.append(step)

    @property
    def step_count(self) -> int:
        return len(self.__steps)

    def __len__(self) -> int:
        return len(self.__steps)

    def __str__(self) -> str:
        return f"PreprocessingPipeline(steps={len(self.__steps)})"

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            raise DataTidakDitemukanError("Dataset kosong.")
        processed_df = df.copy()
        for step in self.__steps:
            processed_df = step.process(processed_df)
        return processed_df

if __name__ == "__main__":
    pass