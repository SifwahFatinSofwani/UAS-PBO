import pandas as pd
from abc import ABC, abstractmethod

class PersistenceRepository(ABC):
    @abstractmethod
    def save(self, df: pd.DataFrame, save_name: str) -> None:
        pass

    @abstractmethod
    def load(self, filename: str) -> pd.DataFrame:
        pass

class JSONRepository(PersistenceRepository):
    def save(self, df: pd.DataFrame, save_name: str) -> None:
        filename = f"{save_name}.json"
        df.to_json(filename, orient="records", indent=4)
        print(f"[SAVED] {filename}")

    def load(self, filename: str) -> pd.DataFrame:
        return pd.read_json(filename)

class CSVRepository(PersistenceRepository):
    def save(self, df: pd.DataFrame, save_name: str) -> None:
        filename = f"{save_name}.csv"
        df.to_csv(filename, index=False)
        print(f"[SAVED] {filename}")

    def load(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(filename)