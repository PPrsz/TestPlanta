import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from PIL import Image
from config import Config
from services.image_quality_service import ImageQualityService
from services.teachable_machine_service import TeachableMachineService
from services.database_service import DatabaseService

class TestPlantDoctorPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_image_path = Path("plantas_1.jpg")
        cls.assertTrue(cls.test_image_path.exists(), "Imagem de teste plantas_1.jpg deve existir.")
        cls.image = Image.open(cls.test_image_path)

    def test_image_quality_service(self):
        """Valida que o auditor de qualidade analisa resolução, iluminação e nitidez."""
        audit = ImageQualityService.inspect_and_validate(self.image)
        self.assertIn("is_acceptable", audit)
        self.assertIn("quality_rating", audit)
        self.assertGreater(audit["width"], 0)
        self.assertGreater(audit["height"], 0)
        
        # Testar compressão e otimização
        opt_img = ImageQualityService.prepare_for_ai(self.image, max_dimension=800)
        self.assertLessEqual(max(opt_img.size), 800)

    def test_teachable_machine_service(self):
        """Valida carregamento do modelo local e predição."""
        tm = TeachableMachineService()
        self.assertTrue(tm.is_loaded, f"Modelo TM deve carregar com sucesso: {tm.load_error}")
        self.assertGreater(len(tm.labels), 0)
        
        result = tm.predict(self.image)
        self.assertTrue(result["success"])
        self.assertIn(result["top_class"], tm.labels)
        self.assertGreaterEqual(result["top_confidence"], 0.0)
        self.assertLessEqual(result["top_confidence"], 1.0)

    def test_database_service(self):
        """Valida operações de persistência relacional."""
        db = DatabaseService()
        p_id = db.create_plant(
            name="Orquídea Teste Unitário",
            species="Phalaenopsis",
            scientific_name="Phalaenopsis amabilis"
        )
        self.assertIsInstance(p_id, int)
        
        plant = db.get_plant_by_id(p_id)
        self.assertEqual(plant["name"], "Orquídea Teste Unitário")
        
        # Testar diagnóstico
        d_id = db.save_diagnosis(
            image_path=str(self.test_image_path),
            plant_id=p_id,
            tm_top_class="Plantas Saudáveis",
            tm_confidence=0.92,
            gemini_status="Aparentemente saudável"
        )
        self.assertIsInstance(d_id, int)
        
        # Limpar
        db.delete_plant(p_id)
        self.assertIsNone(db.get_plant_by_id(p_id))

if __name__ == "__main__":
    unittest.main()
