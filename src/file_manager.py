import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Union, Tuple

class FileManager:
    def __init__(self, root_dir: str = "invoices"):
        self.root = Path(root_dir)
        self.input_dir = self.root / "input"
        self.staging_dir = self.root / "staging"
        self.archive_dir = self.root / "archive"
        self.quarantine_dir = self.root / "quarantine"
        
        # Ensure all directories exist
        for d in [self.input_dir, self.staging_dir, self.archive_dir, self.quarantine_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def get_input_files(self) -> List[Path]:
        """Scans input directory for PDF/Images."""
        valid_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.webp'}
        return sorted([
            p for p in self.input_dir.iterdir() 
            if p.is_file() and p.suffix.lower() in valid_extensions
        ])

    def get_staging_files(self) -> List[Path]:
        """Scans staging directory for JSON files ready for upload."""
        return sorted([
            p for p in self.staging_dir.iterdir() 
            if p.is_file() and p.suffix.lower() == '.json'
        ])

    def read_bytes(self, file_path: Path) -> bytes:
        return file_path.read_bytes()

    def read_json(self, file_path: Path) -> dict:
        return json.loads(file_path.read_text(encoding='utf-8'))

    def save_to_staging(self, original_file: Path, data_json: str) -> Path:
        """
        Saves extracted JSON to staging and moves the original file there too.
        Returns the path to the saved JSON file.
        """
        # 1. Save JSON
        json_filename = original_file.with_suffix('.json').name
        json_path = self.staging_dir / json_filename
        json_path.write_text(data_json, encoding='utf-8')
        
        # 2. Move Original File (PDF/Img) to Staging to keep them together
        dest_file_path = self.staging_dir / original_file.name
        shutil.move(str(original_file), str(dest_file_path))
        
        print(f"  Moved to Staging: {json_path.name}")
        return json_path

    def promote_to_archive(self, json_path: Path):
        """
        Moves JSON and its corresponding source file from Staging to Archive.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        target_dir = self.archive_dir / date_str / "processed"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        self._move_pair(json_path, target_dir)
        print(f"  Archived: {json_path.stem}")

    def move_to_quarantine(self, file_path: Path, error_msg: str):
        """
        Moves a file (and its partner if exists) to Quarantine.
        Also saves a .txt file with the error message.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        target_dir = self.quarantine_dir / date_str
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Move the file(s)
        self._move_pair(file_path, target_dir)
        
        # Save Error Log
        error_log = target_dir / f"{file_path.stem}_error.txt"
        error_log.write_text(error_msg, encoding='utf-8')
        
        print(f"  QUARANTINED: {file_path.stem}")

    def _move_pair(self, primary_file: Path, target_dir: Path):
        """Helper to move a file and its potential partner (json/pdf) together."""
        # Move primary
        self._safe_move(primary_file, target_dir)
        
        # Find partner
        # If primary is .json, look for .pdf/.jpg...
        # If primary is .pdf, look for .json
        
        search_dir = primary_file.parent
        stem = primary_file.stem
        
        # Look for any file with same stem but different extension
        for partner in search_dir.glob(f"{stem}.*"):
            if partner != primary_file:
                self._safe_move(partner, target_dir)

    def _safe_move(self, src: Path, target_dir: Path):
        """Moves file to target_dir, handling name collisions."""
        if not src.exists():
            return
            
        dest = target_dir / src.name
        if dest.exists():
            timestamp = datetime.now().strftime("%H%M%S")
            dest = target_dir / f"{src.stem}_{timestamp}{src.suffix}"
            
        shutil.move(str(src), str(dest))
