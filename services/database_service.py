import os
import json
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image
from config import Config

class DatabaseService:
    """
    Serviço de persistência relacional SQLite para gerenciamento de plantas,
    histórico de diagnósticos fitossanitários, diário de regas e comparações.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Config.DB_PATH
        Config.initialize_dirs()
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Cria e retorna uma conexão configurada com row_factory."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Cria as tabelas do sistema se não existirem."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabela de Plantas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT,
                scientific_name TEXT,
                primary_image_path TEXT,
                created_at TEXT NOT NULL,
                notes TEXT,
                health_status TEXT DEFAULT 'Aparentemente saudável',
                watering_frequency_days INTEGER DEFAULT 3,
                last_watered_date TEXT,
                last_fertilized_date TEXT
            )
            """)

            # Tabela de Diagnósticos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER,
                created_at TEXT NOT NULL,
                image_path TEXT NOT NULL,
                tm_top_class TEXT,
                tm_confidence REAL,
                tm_predictions_json TEXT,
                gemini_status TEXT,
                gemini_severity TEXT,
                gemini_full_json TEXT,
                notes TEXT,
                FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE SET NULL
            )
            """)

            # Tabela de Diário de Cuidados (Regas, Adubações, etc.)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS care_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                care_type TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE CASCADE
            )
            """)

            # Tabela de Acompanhamento / Comparações Temporais
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS comparisons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER NOT NULL,
                before_diag_id INTEGER NOT NULL,
                after_diag_id INTEGER NOT NULL,
                evolution_status TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE CASCADE,
                FOREIGN KEY (before_diag_id) REFERENCES diagnoses (id),
                FOREIGN KEY (after_diag_id) REFERENCES diagnoses (id)
            )
            """)
            conn.commit()

    def save_image_to_disk(self, pil_image: Image.Image, prefix: str = "img") -> str:
        """Salva a imagem da planta no diretório de uploads do sistema."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{prefix}_{timestamp}.jpg"
        target_path = Config.UPLOADS_DIR / filename
        pil_image.save(target_path, format="JPEG", quality=Config.JPEG_COMPRESSION_QUALITY)
        return str(target_path)

    # ==========================
    # CRUD de Plantas
    # ==========================
    def create_plant(
        self,
        name: str,
        species: str = "",
        scientific_name: str = "",
        image_path: str = "",
        notes: str = "",
        health_status: str = "Aparentemente saudável",
        watering_days: int = 3
    ) -> int:
        now_str = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO plants (name, species, scientific_name, primary_image_path, created_at, notes, health_status, watering_frequency_days)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, species, scientific_name, image_path, now_str, notes, health_status, watering_days))
            conn.commit()
            return cursor.lastrowid

    def get_all_plants(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM plants ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_plant_by_id(self, plant_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM plants WHERE id = ?", (plant_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_plant(self, plant_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        fields = []
        values = []
        for k, v in kwargs.items():
            fields.append(f"{k} = ?")
            values.append(v)
        values.append(plant_id)
        sql = f"UPDATE plants SET {', '.join(fields)} WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

    def delete_plant(self, plant_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
            conn.commit()
            return cursor.rowcount > 0

    # ==========================
    # Diagnósticos
    # ==========================
    def save_diagnosis(
        self,
        image_path: str,
        plant_id: Optional[int] = None,
        tm_top_class: str = "",
        tm_confidence: float = 0.0,
        tm_predictions: Optional[Dict[str, float]] = None,
        gemini_status: str = "",
        gemini_severity: str = "",
        gemini_data: Optional[Dict[str, Any]] = None,
        notes: str = ""
    ) -> int:
        now_str = datetime.now().isoformat()
        tm_json_str = json.dumps(tm_predictions or {}, ensure_ascii=False)
        gemini_json_str = json.dumps(gemini_data or {}, ensure_ascii=False)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO diagnoses (
                plant_id, created_at, image_path, tm_top_class, tm_confidence,
                tm_predictions_json, gemini_status, gemini_severity, gemini_full_json, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plant_id, now_str, image_path, tm_top_class, tm_confidence,
                tm_json_str, gemini_status, gemini_severity, gemini_json_str, notes
            ))
            diag_id = cursor.lastrowid
            
            # Se vinculado a uma planta, atualizar status de saúde da planta
            if plant_id and gemini_status:
                cursor.execute("UPDATE plants SET health_status = ? WHERE id = ?", (gemini_status, plant_id))
            
            conn.commit()
            return diag_id

    def get_diagnoses_for_plant(self, plant_id: int) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM diagnoses WHERE plant_id = ? ORDER BY id DESC", (plant_id,))
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["tm_predictions"] = json.loads(item.get("tm_predictions_json") or "{}")
                item["gemini_data"] = json.loads(item.get("gemini_full_json") or "{}")
                results.append(item)
            return results

    def get_recent_diagnoses(self, limit: int = 15) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT d.*, p.name as plant_name, p.species as plant_species 
            FROM diagnoses d
            LEFT JOIN plants p ON d.plant_id = p.id
            ORDER BY d.id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["tm_predictions"] = json.loads(item.get("tm_predictions_json") or "{}")
                item["gemini_data"] = json.loads(item.get("gemini_full_json") or "{}")
                results.append(item)
            return results

    # ==========================
    # Diário de Cuidados
    # ==========================
    def log_care(self, plant_id: int, care_type: str, notes: str = "") -> int:
        now_str = datetime.now().isoformat()
        today_date = date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO care_logs (plant_id, timestamp, care_type, notes)
            VALUES (?, ?, ?, ?)
            """, (plant_id, now_str, care_type, notes))
            
            # Atualizar datas de rega ou adubação na tabela de plantas
            if care_type.lower() == "rega":
                cursor.execute("UPDATE plants SET last_watered_date = ? WHERE id = ?", (today_date, plant_id))
            elif "aduba" in care_type.lower():
                cursor.execute("UPDATE plants SET last_fertilized_date = ? WHERE id = ?", (today_date, plant_id))
                
            conn.commit()
            return cursor.lastrowid

    def get_care_logs(self, plant_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM care_logs WHERE plant_id = ? ORDER BY id DESC LIMIT ?
            """, (plant_id, limit))
            return [dict(r) for r in cursor.fetchall()]

    # ==========================
    # Comparações de Evolução
    # ==========================
    def record_comparison(
        self,
        plant_id: int,
        before_diag_id: int,
        after_diag_id: int,
        evolution_status: str,
        notes: str = ""
    ) -> int:
        now_str = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO comparisons (plant_id, before_diag_id, after_diag_id, evolution_status, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (plant_id, before_diag_id, after_diag_id, evolution_status, notes, now_str))
            conn.commit()
            return cursor.lastrowid
