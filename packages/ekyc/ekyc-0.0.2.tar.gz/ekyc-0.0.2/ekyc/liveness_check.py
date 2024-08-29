import cv2
import tempfile
import os
from deepface import DeepFace
from .utils import setup_logger

logger = setup_logger(__name__)

def perform_liveness_check(image):
    logger.info("Performing liveness check")
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_filename = temp_file.name
        cv2.imwrite(temp_filename, image)
    
    try:
        result = DeepFace.analyze(temp_filename, actions=['anti_spoofing'], silent=True)
        is_live = result[0]['anti_spoofing']['is_real']
        logger.info(f"Liveness check result: {'Live' if is_live else 'Spoof'}")
        return is_live
    except Exception as e:
        logger.error(f"Error during liveness check: {str(e)}")
        return False
    finally:
        try:
            os.remove(temp_filename)
        except Exception as e:
            logger.warning(f"Failed to remove temporary file: {str(e)}")