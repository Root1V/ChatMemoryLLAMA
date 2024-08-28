from pathlib import Path
import json


class Config:
    _config = None

    @classmethod
    def get_all(cls, filepath="config-model.json"):
        """Carga y devuelve todos los valores del archivo config-model.json."""
        if cls._config is None:
            # Obtener la ruta absoluta del archivo en relación al archivo actual (config.py)
            base_path = Path(__file__).parent  # Directorio donde está config.py
            full_path = base_path / filepath  # Ruta completa del archivo

            with open(full_path, "r") as f:
                cls._config = json.load(f)

        return cls._config
