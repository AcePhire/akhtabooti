import os
import subprocess
from pathlib import Path
import shutil

class UniversalPDFConverter:
    """
    Convert documents to PDF using LibreOffice (all-in-one solution).
    Handles: Word, Excel, PowerPoint, images, and more.
    """
    
    def __init__(self, output_dir="converted_pdfs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.libreoffice_path = self._find_libreoffice()
        
        if not self.libreoffice_path:
            raise EnvironmentError(
                "LibreOffice not found. Please install LibreOffice:\n"
                "  - Ubuntu/Debian: sudo apt-get install libreoffice\n"
                "  - macOS: brew install --cask libreoffice\n"
                "  - Windows: Download from https://www.libreoffice.org/download"
            )
    
    def _find_libreoffice(self):
        """Locate LibreOffice executable on different platforms."""
        possible_paths = [
            # Linux
            '/usr/bin/libreoffice',
            '/usr/bin/soffice',
            # macOS
            '/Applications/LibreOffice.app/Contents/MacOS/soffice',
            # Windows (common locations)
            r'C:\Program Files\LibreOffice\program\soffice.exe',
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
        ]
        
        # Try common paths
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try finding in PATH
        if shutil.which('libreoffice'):
            return shutil.which('libreoffice')
        if shutil.which('soffice'):
            return shutil.which('soffice')
        
        return None
    
    def convert_to_pdf(self, input_file):
        """
        Convert any supported file to PDF using LibreOffice.
        
        Supported formats:
        - Documents: DOC, DOCX, ODT, RTF, TXT
        - Spreadsheets: XLS, XLSX, ODS, CSV
        - Presentations: PPT, PPTX, ODP
        - Images: Most common formats via LibreOffice Draw
        
        Args:
            input_file: Path to input file
            
        Returns:
            Path to generated PDF file
        """
        input_path = Path(input_file).absolute()
        
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_file}")
        
        if input_path.suffix.lower() == '.pdf':
            print(f"File is already a PDF: {input_path.name}")
            return input_path
        
        print(f"Converting: {input_path.name}")
        
        # LibreOffice command for headless PDF conversion
        cmd = [
            self.libreoffice_path,
            '--headless',  # Run without GUI
            '--convert-to', 'pdf',
            '--outdir', str(self.output_dir),
            str(input_path)
        ]
        
        try:
            # Run LibreOffice conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if result.returncode != 0:
                raise Exception(f"Conversion failed: {result.stderr}")
            
            # Determine output PDF path
            output_pdf = self.output_dir / f"{input_path.stem}.pdf"
            
            if output_pdf.exists():
                print(f"✓ Saved to: {output_pdf}")
                return output_pdf
            else:
                raise Exception("PDF was not created")
                
        except subprocess.TimeoutExpired:
            raise Exception("Conversion timed out (file too large or complex)")
        except Exception as e:
            raise Exception(f"Error during conversion: {str(e)}")
    
    def convert_batch(self, input_files, verbose=True):
        """
        Convert multiple files to PDF.
        
        Args:
            input_files: List of file paths
            verbose: Print progress messages
            
        Returns:
            Dictionary with successful and failed conversions
        """
        results = {
            'successful': [],
            'failed': []
        }
        
        for file in input_files:
            try:
                pdf_path = self.convert_to_pdf(file)
                results['successful'].append({
                    'input': file,
                    'output': pdf_path
                })
            except Exception as e:
                if verbose:
                    print(f"✗ Error converting {file}: {str(e)}")
                results['failed'].append({
                    'input': file,
                    'error': str(e)
                })
        
        if verbose:
            print(f"\n{'='*50}")
            print(f"Conversion complete!")
            print(f"✓ Successful: {len(results['successful'])}")
            print(f"✗ Failed: {len(results['failed'])}")
            print(f"{'='*50}")
        
        return results
    
    def convert_directory(self, directory, pattern="*.*", recursive=False):
        """
        Convert all files in a directory matching a pattern.
        
        Args:
            directory: Directory path
            pattern: File pattern (e.g., "*.docx", "*.*")
            recursive: Search subdirectories
            
        Returns:
            Dictionary with conversion results
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        # Find files
        if recursive:
            files = list(dir_path.rglob(pattern))
        else:
            files = list(dir_path.glob(pattern))
        
        # Filter out PDFs and hidden files
        files = [f for f in files if f.suffix.lower() != '.pdf' and not f.name.startswith('.')]
        
        print(f"Found {len(files)} file(s) to convert")
        
        return self.convert_batch([str(f) for f in files])


# Example usage
if __name__ == "__main__":
    try:
        # Initialize converter
        converter = UniversalPDFConverter(output_dir="converted_pdfs")
        
        # Example 1: Convert a single file
        # pdf_path = converter.convert_to_pdf("example.docx")
        
        # Example 2: Convert multiple files
        # files_to_convert = [
        #     "document.docx",
        #     "spreadsheet.xlsx",
        #     "presentation.pptx",
        #     "data.csv"
        # ]
        # results = converter.convert_batch(files_to_convert)
        
        # Example 3: Convert all files in a directory
        # results = converter.convert_directory("my_documents", pattern="*.*")

        pdf_path = converter.convert_to_pdf("/home/acephire/Downloads/Capstone 2 Presentation.pptx")
        
        print("\n✓ Converter ready!")
        print("Usage examples:")
        print('  converter.convert_to_pdf("file.docx")')
        print('  converter.convert_batch(["file1.xlsx", "file2.pptx"])')
        print('  converter.convert_directory("folder_path")')
        
    except EnvironmentError as e:

        print(f"\n✗ Setup Error: {e}")
