"""
PDF Merger with Table of Contents
Merges multiple PDF files and creates a clickable table of contents
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Tuple


class PDFMerger:
    """Handles merging PDFs and creating table of contents"""
    
    def __init__(self):
        self.output_doc = None
        self.toc_entries = []
        
    def merge_pdfs(self, pdf_files: List[Path], output_path: Path, 
                   toc_titles: List[str] = None) -> Path:
        """
        Merge multiple PDF files into one with table of contents
        
        Args:
            pdf_files: List of PDF file paths to merge
            output_path: Path for the output merged PDF
            toc_titles: List of titles for each PDF in the TOC (optional)
            
        Returns:
            Path to the created merged PDF
        """
        if not pdf_files:
            raise ValueError("No PDF files provided for merging")
            
        # Convert to Path objects if needed
        pdf_files = [Path(f) for f in pdf_files]
        output_path = Path(output_path)
        
        # Create titles if not provided
        if toc_titles is None:
            toc_titles = [f.name for f in pdf_files]
        
        # Ensure equal length
        if len(toc_titles) != len(pdf_files):
            raise ValueError("Number of titles must match number of PDFs")
            
        # Create output document
        self.output_doc = fitz.open()
        self.toc_entries = []
        
        # Merge each PDF and track page numbers for TOC
        current_page = 0
        
        for pdf_path, title in zip(pdf_files, toc_titles):
            if not pdf_path.exists():
                print(f"Warning: File not found: {pdf_path}")
                continue
                
            try:
                # Open source PDF
                src_doc = fitz.open(str(pdf_path))
                
                # Add TOC entry (level 1, title, page number)
                self.toc_entries.append([1, title, current_page + 1])
                
                # Insert all pages from source
                self.output_doc.insert_pdf(src_doc)
                
                # Update page counter
                current_page += len(src_doc)
                
                src_doc.close()
                
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
                continue
        
        # Set the table of contents
        if self.toc_entries:
            self.output_doc.set_toc(self.toc_entries)
        
        # Create TOC page at the beginning
        self._add_toc_page()
        
        # Save the merged PDF
        self.output_doc.save(str(output_path))
        self.output_doc.close()
        
        return output_path
    
    def _add_toc_page(self):
        """Add a visual table of contents page at the beginning"""
        # Insert a blank page at the beginning
        toc_page = self.output_doc.new_page(0, width=595, height=842)  # A4 size
        
        # Write TOC title
        toc_page.insert_text(
            (50, 50),
            "Table of Contents",
            fontsize=20,
            fontname="helv",
            color=(0, 0, 0)
        )
        
        # Write each entry with page number
        y_position = 100
        for level, title, page_num in self.toc_entries:
            # Indent based on level
            indent = (level - 1) * 20
            
            # Create clickable link to the page
            link_rect = fitz.Rect(50 + indent, y_position - 5, 
                                 500, y_position + 10)
            
            # Add text
            text = f"{title} {'.' * (50 - len(title))} {page_num + 1}"
            toc_page.insert_text(
                (50 + indent, y_position),
                text,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0.8)
            )
            
            # Add internal link
            link = {
                "kind": fitz.LINK_GOTO,
                "from": link_rect,
                "page": page_num + 1  # +1 because we added TOC page
            }
            toc_page.insert_link(link)
            
            y_position += 20
            
            # Add new page if we run out of space
            if y_position > 800:
                toc_page = self.output_doc.new_page(1, width=595, height=842)
                y_position = 50
        
        # Update all TOC entries to account for the new first page
        updated_toc = [[level, title, page + 1] 
                       for level, title, page in self.toc_entries]
        self.output_doc.set_toc(updated_toc)


def merge_course_pdfs(lectures_folder: Path, tirgul_folder: Path, 
                      output_folder: Path, course_name: str) -> Dict[str, Path]:
    """
    Merge lecture and tirgul PDFs for a course
    
    Args:
        lectures_folder: Path to folder containing lecture PDFs
        tirgul_folder: Path to folder containing tirgul PDFs
        output_folder: Path to output folder
        course_name: Name of the course
        
    Returns:
        Dictionary with paths to generated PDFs
    """
    lectures_folder = Path(lectures_folder)
    tirgul_folder = Path(tirgul_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    
    merger = PDFMerger()
    results = {}
    
    # Get and sort PDF files
    def get_sorted_pdfs(folder: Path) -> List[Path]:
        if not folder.exists():
            return []
        pdfs = sorted(folder.glob('*.pdf'))
        return pdfs
    
    lectures = get_sorted_pdfs(lectures_folder)
    tirguls = get_sorted_pdfs(tirgul_folder)
    
    # Merge lectures
    if lectures:
        lectures_output = output_folder / f"{course_name}_Lectures.pdf"
        lecture_titles = [f"Lecture {i+1}" for i in range(len(lectures))]
        merger.merge_pdfs(lectures, lectures_output, lecture_titles)
        results['lectures'] = lectures_output
        print(f"Created: {lectures_output}")
    
    # Merge tirguls
    if tirguls:
        tirguls_output = output_folder / f"{course_name}_Tirgul.pdf"
        tirgul_titles = [f"Tirgul {i+1}" for i in range(len(tirguls))]
        merger.merge_pdfs(tirguls, tirguls_output, tirgul_titles)
        results['tirgul'] = tirguls_output
        print(f"Created: {tirguls_output}")
    
    # Merge all course files
    if lectures or tirguls:
        all_files = []
        all_titles = []
        
        if lectures:
            all_files.extend(lectures)
            all_titles.extend([f"Lecture {i+1}" for i in range(len(lectures))])
        
        if tirguls:
            all_files.extend(tirguls)
            all_titles.extend([f"Tirgul {i+1}" for i in range(len(tirguls))])
        
        full_output = output_folder / f"{course_name}_Full.pdf"
        merger.merge_pdfs(all_files, full_output, all_titles)
        results['full'] = full_output
        print(f"Created: {full_output}")
    
    return results


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python pdf_merger.py <lectures_folder> <tirgul_folder> <output_folder> [course_name]")
        sys.exit(1)
    
    lectures = sys.argv[1]
    tirgul = sys.argv[2]
    output = sys.argv[3]
    course = sys.argv[4] if len(sys.argv) > 4 else "Course"
    
    results = merge_course_pdfs(lectures, tirgul, output, course)
    print(f"\nMerge complete! Created {len(results)} files.")
