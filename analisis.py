import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod
from typing import List, Optional
import models
import repositories

FormatDataTidakValidError = models.FormatDataTidakValidError
PersistenceRepository = repositories.PersistenceRepository

ANALYSIS_REGISTRY: dict = {}

def register_analysis(name: str):
    def decorator(cls):
        ANALYSIS_REGISTRY[name] = cls
        return cls
    return decorator

class AbstractAnalysis(ABC):
    @property
    @abstractmethod
    def title(self) -> str: pass

    @abstractmethod
    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame: pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(title='{self.title}')>"

class VisualizableMixin(ABC):
    @abstractmethod
    def visualize(self, result_df: pd.DataFrame) -> None: pass

class BaseAnalysis(AbstractAnalysis):
    def __init__(self, description: str) -> None:
        self._description: str = description   

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not value or not value.strip():
            raise FormatDataTidakValidError("Deskripsi analisis tidak boleh kosong.")
        self._description = value.strip()

    def get_summary(self) -> str:
        return f"[{self.__class__.__name__}] {self.title} - {self.description}"

    def __str__(self) -> str:
        return self.get_summary()

@register_analysis("distribusi")
class MentalHealthDistribution(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Menghitung distribusi frekuensi kondisi mental seluruh karyawan.")

    @property
    def title(self) -> str:
        return "Distribusi Kondisi Mental Karyawan"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return df["mental_health_condition"].value_counts().reset_index()

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(
            x=result_df.columns[0], y=result_df.columns[1],
            data=result_df, palette="Set2", hue=result_df.columns[0],
        )
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        plt.title(self.title, fontweight="bold")
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("lokasi")
class MentalHealthByLocation(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Menganalisis kondisi mental karyawan berdasarkan lokasi kerja (Remote/Hybrid/Onsite).")

    @property
    def title(self) -> str:
        return "Kondisi Mental Berdasarkan Lokasi Kerja"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(["work_location", "mental_health_condition"]).size().reset_index(name="count")

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 5))
        sns.barplot(x="work_location", y="count", hue="mental_health_condition", data=result_df, palette="husl")
        plt.title(self.title, fontweight="bold")
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("stres")
class MentalHealthByStressHeatmap(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Membuat crosstab antara tingkat stres dan kondisi mental, disajikan sebagai heatmap.")

    @property
    def title(self) -> str:
        return "Heatmap: Tingkat Stres vs Kondisi Mental"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.crosstab(df["stress_level"], df["mental_health_condition"])

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(8, 5))
        sns.heatmap(result_df, annot=True, fmt="d", cmap="Reds", linewidths=0.5)
        plt.title(self.title, fontweight="bold")
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("isolasi")
class MentalHealthByIsolationBoxplot(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Membandingkan tingkat isolasi sosial antar kondisi mental via boxplot.")

    @property
    def title(self) -> str:
        return "Tingkat Isolasi Sosial per Kondisi Mental"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[["mental_health_condition", "social_isolation_rating"]]

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(9, 5))
        ax = sns.boxplot(
            x="mental_health_condition", y="social_isolation_rating",
            data=result_df, palette="pastel", hue="mental_health_condition",
        )
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        plt.title(self.title, fontweight="bold")
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("aktivitas")
class MentalHealthByPhysicalActivity(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Menghitung proporsi kondisi mental berdasarkan frekuensi aktivitas fisik karyawan.")

    @property
    def title(self) -> str:
        return "Proporsi Kondisi Mental Berdasarkan Aktivitas Fisik"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.crosstab(df["physical_activity"], df["mental_health_condition"], normalize="index") * 100

    def visualize(self, result_df: pd.DataFrame) -> None:
        result_df.plot(kind="barh", stacked=True, figsize=(10, 5), colormap="viridis")
        plt.title(self.title, fontweight="bold")
        plt.legend(title="Kondisi Mental", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("usia")
class MentalHealthByAgeGroup(BaseAnalysis, VisualizableMixin):
    def __init__(self, bins: Optional[List[int]] = None) -> None:
        super().__init__("Mengelompokkan karyawan ke bin usia lalu membandingkan kondisi mental tiap kelompok.")
        self._bins = bins or [0, 30, 40, 50, 100]
        self._labels = ["<30 Tahun", "30-39 Tahun", "40-49 Tahun", ">=50 Tahun"]

    @property
    def title(self) -> str:
        return "Kondisi Mental Berdasarkan Kelompok Usia"

    @property
    def age_bins(self) -> List[int]:
        return list(self._bins)

    @property
    def age_labels(self) -> List[str]:
        return list(self._labels)

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        df_age = df[["mental_health_condition", "age"]].copy()
        df_age = df_age[df_age["age"] > 0]
        df_age["age_group"] = pd.cut(df_age["age"], bins=self._bins, labels=self._labels, right=False)
        return df_age.groupby(["age_group", "mental_health_condition"], observed=False).size().reset_index(name="count")

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 6))
        sns.barplot(x="age_group", y="count", hue="mental_health_condition", data=result_df, palette="Set1")
        plt.title(self.title, fontweight="bold", fontsize=14)
        plt.xlabel("Kelompok Usia")
        plt.ylabel("Jumlah Karyawan")
        plt.legend(title="Kondisi Mental", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("gender")
class MentalHealthByGender(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Membandingkan distribusi kondisi mental antara kelompok gender.")

    @property
    def title(self) -> str:
        return "Kondisi Mental Berdasarkan Gender"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(["gender", "mental_health_condition"]).size().reset_index(name="count")

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 5))
        sns.barplot(x="gender", y="count", hue="mental_health_condition", data=result_df, palette="Set1")
        plt.title(self.title, fontweight="bold")
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("jam_kerja")
class MentalHealthByWorkingHours(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Menghitung statistik deskriptif jam kerja mingguan berdasarkan kondisi mental.")

    @property
    def title(self) -> str:
        return "Statistik Jam Kerja Mingguan vs Kondisi Mental"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby("mental_health_condition")["hours_worked_per_week"].describe().reset_index()

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(
            x="mental_health_condition", y="mean",
            data=result_df, palette="mako", hue="mental_health_condition",
        )
        if ax.get_legend() is not None:
            ax.get_legend().remove()
            
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.1f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', 
                        xytext=(0, 9), 
                        textcoords='offset points')

        plt.title(self.title, fontweight="bold", fontsize=14)
        plt.xlabel("Kondisi Mental")
        plt.ylabel("Rata-rata Jam Kerja Mingguan")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("akses_bantuan")
class MentalHealthByResourcesAccess(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Menganalisis apakah akses ke fasilitas kesehatan mental HRD mempengaruhi kondisi karyawan.")

    @property
    def title(self) -> str:
        return "Kondisi Mental Berdasarkan Akses Bantuan HRD"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.crosstab(df["access_to_mental_health_resources"], df["mental_health_condition"], normalize="index") * 100

    def visualize(self, result_df: pd.DataFrame) -> None:
        result_df.plot(kind="bar", stacked=True, figsize=(9, 5), colormap="Spectral")
        plt.title(self.title, fontweight="bold")
        plt.legend(title="Kondisi Mental", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xticks(rotation=0)
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("tidur")
class MentalHealthBySleepQuality(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Mengevaluasi hubungan antara kualitas tidur karyawan dan kondisi mental mereka.")

    @property
    def title(self) -> str:
        return "Kondisi Mental Berdasarkan Kualitas Tidur"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(["sleep_quality", "mental_health_condition"]).size().reset_index(name="count")

    def visualize(self, result_df: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 5))
        order = ["Poor", "Average", "Good"]
        sns.barplot(x="sleep_quality", y="count", hue="mental_health_condition", data=result_df, order=order, palette="magma")
        plt.title(self.title, fontweight="bold")
        plt.tight_layout()
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight")
        print(f"[SAVED] {filepath}")
        plt.show()

@register_analysis("ringkasan")
class SummaryStatisticsAnalysis(BaseAnalysis):
    def __init__(self) -> None:
        super().__init__("Menghasilkan statistik deskriptif numerik dataset (usia, jam kerja, isolasi sosial).")

    @property
    def title(self) -> str:
        return "Ringkasan Statistik Deskriptif Dataset"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        num_cols = ["age", "hours_worked_per_week", "social_isolation_rating"]
        existing = [c for c in num_cols if c in df.columns]
        return df[existing].describe().T

class AnalysisFactory:
    @staticmethod
    def create_analysis(type_name: str) -> AbstractAnalysis:
        if type_name in ANALYSIS_REGISTRY:
            return ANALYSIS_REGISTRY[type_name]()
        raise FormatDataTidakValidError(
            f"Tipe '{type_name}' tidak valid. Tersedia: {list(ANALYSIS_REGISTRY.keys())}"
        )

class AnalysisLogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass

class ConsoleLogger(AnalysisLogger):
    def log(self, message: str) -> None:
        print(message)

class AnalysisRunner:
    def __init__(
        self,
        analysis: AbstractAnalysis,
        repositories: List[PersistenceRepository],
        logger: Optional[AnalysisLogger] = None
    ) -> None:
        self._analysis = analysis
        self._repositories = repositories
        self._logger = logger or ConsoleLogger()

    @property
    def analysis(self) -> AbstractAnalysis:
        return self._analysis

    @analysis.setter
    def analysis(self, value: AbstractAnalysis) -> None:
        if not isinstance(value, AbstractAnalysis):
            raise FormatDataTidakValidError("analysis harus berupa AbstractAnalysis.")
        self._analysis = value

    @property
    def repository_count(self) -> int:
        return len(self._repositories)

    def run_and_save(self, df: pd.DataFrame, save_name: str) -> pd.DataFrame:
        self._logger.log(f"[RUNNING] {self._analysis.get_summary()}")
        
        result = self._analysis.run_analysis(df)
        save_df = result.reset_index() if not isinstance(result.index, pd.RangeIndex) else result
        for repo in self._repositories:
            repo.save(save_df, save_name)
        return result

@register_analysis("tabel_statistik")
class DescriptiveStatsTable(BaseAnalysis, VisualizableMixin):
    def __init__(self) -> None:
        super().__init__("Menampilkan tabel visual statistik deskriptif untuk data numerik karyawan.")

    @property
    def title(self) -> str:
        return "Tabel Statistik Numerik Karyawan"

    def run_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        num_cols = ["age", "hours_worked_per_week", "social_isolation_rating"]
        existing_cols = [c for c in num_cols if c in df.columns]
        
        df_calc = df[existing_cols].copy()
        for col in existing_cols:
            df_calc[col] = pd.to_numeric(df_calc[col], errors='coerce')
        
        stats_dict = {
            "Statistik": ["Mean", "Median", "Std Dev", "Min", "Max", "Missing"]
        }
        
        for col in existing_cols:
            col_name = col.replace("_", " ").title()
            
            stats_dict[col_name] = [
                round(df_calc[col].mean(), 2) if pd.notna(df_calc[col].mean()) else 0,
                round(df_calc[col].median(), 2) if pd.notna(df_calc[col].median()) else 0,
                round(df_calc[col].std(), 2) if pd.notna(df_calc[col].std()) else 0,
                round(df_calc[col].min(), 2) if pd.notna(df_calc[col].min()) else 0,
                round(df_calc[col].max(), 2) if pd.notna(df_calc[col].max()) else 0,
                df_calc[col].isna().sum()
            ]
            
        return pd.DataFrame(stats_dict)

    def visualize(self, result_df: pd.DataFrame) -> None:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.axis('tight')
        ax.axis('off') 
        
        table = ax.table(
            cellText=result_df.values,
            colLabels=result_df.columns,
            cellLoc='center',
            loc='center'
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 1.8) 
        
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor('#203040')
                cell.set_text_props(color='white', weight='bold')
            elif col == 0:
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#f4f6f9')
            else:
                cell.set_facecolor('#f9f9f9' if row % 2 == 0 else '#ffffff')

        plt.title(self.title, fontweight="bold", fontsize=15, pad=20)
        
        filepath = os.path.join("output_visualisasi", f"visualisasi_{self.__class__.__name__}.png")
        plt.savefig(filepath, bbox_inches="tight", dpi=300)
        print(f"[SAVED] {filepath}")
        plt.show()
        
if __name__ == "__main__":
    pass