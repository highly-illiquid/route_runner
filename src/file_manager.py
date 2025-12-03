import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Union

class FileManager:
    def __init__(self, input_dir: str = "invoices/input", archive_dir: str = "invoices/archive"):
        self.input_path = Path(input_dir)
        self.archive_path = Path(archive_dir)
        
        # Ensure directories exist
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.archive_path.mkdir(parents=True, exist_ok=True)

    def get_pending_invoices(self) -> List[Path]:
        """
        Scans the input directory for PDF and Image files.
        Returns a list of Path objects.
        """
        if not self.input_path.exists():
            return []
            
        valid_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.webp'}
        
        # Case insensitive search
        files = [
            p for p in self.input_path.iterdir() 
            if p.is_file() and p.suffix.lower() in valid_extensions
        ]
        return sorted(files)

    def read_file(self, file_path: Path) -> bytes:
        """Reads the bytes of a file."""
        return file_path.read_bytes()

    def archive_invoice(self, file_path: Path, success: bool = True) -> Path:
        """
        Moves the file to the archive directory.
        Returns the path to the archived file.
        Structure: archive_dir / YYYY-MM-DD / [success|error] / filename
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        status_dir = "processed" if success else "failed"
        
        target_dir = self.archive_path / date_str / status_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_path = target_dir / file_path.name
        
        # Handle duplicates by appending timestamp if needed
        if target_path.exists():
            timestamp = datetime.now().strftime("%H%M%S")
            stem = file_path.stem
            suffix = file_path.suffix
            target_path = target_dir / f"{stem}_{timestamp}{suffix}"

        print(f"  Archiving to: {target_path}")
        shutil.move(str(file_path), str(target_path))
        return target_path

    def save_json_record(self, archived_pdf_path: Path, data: Union[dict, str]):
        """
        Saves the extracted JSON data to a file with the same name as the PDF
        (but .json extension) in the same folder.
        """
        # Change extension to .json
        json_path = archived_pdf_path.with_suffix('.json')
        
        print(f"  Saving data log: {json_path}")
        
        content = data
        if not isinstance(content, str):
             # If it's a Pydantic model or dict, ensure it's stringified
             content = json.dumps(content, indent=2, default=str)

        json_path.write_text(content, encoding='utf-8')