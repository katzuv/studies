"""
PDF Merger with Table of Contents.
Merges multiple PDF files and creates a clickable table of contents.
"""

import fitz  # PyMuPDF
from pathlib import Path


class PDFMerger:
    """Handles merging PDFs and creating table of contents."""
    
    def __init__(self):
        self.output_doc = None
        self.toc_entries = []
        
    def merge_pdfs(self, pdf_files: list[Path], output_path: Path, 
                   toc_titles: list[str] = None) -> Path:
        """
        Merge multiple PDF files into one with table of contents.
        
        @param pdf_files: List of PDF file paths to merge.
        @param output_path: Path for the output merged PDF.
        @param toc_titles: List of titles for each PDF in the TOC (optional).
        @return: Path to the created merged PDF.
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
        
        # Set the table of contents (before adding TOC page)
        if self.toc_entries:
            self.output_doc.set_toc(self.toc_entries)
            
            # Add visual TOC page at the beginning
            self._add_toc_page()
        
        # Save the merged PDF
        self.output_doc.save(str(output_path))
        self.output_doc.close()
        
        return output_path
    
    def _add_toc_page(self):
        """Add a visual table of contents page at the beginning."""
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
        
        toc_page.insert_text(
            (50, 75),
            "Use the sidebar/bookmarks panel to navigate to sections",
            fontsize=10,
            fontname="helv",
            color=(0.5, 0.5, 0.5)
        )
        
        # Write each entry with page number
        y_position = 110
        toc_page_num = 0
        
        # We'll update TOC entries as we add the page
        updated_toc = []
        
        for level, title, page_num in self.toc_entries:
            # Adjust page number for the TOC page we just added
            adjusted_page = page_num + 1
            updated_toc.append([level, title, adjusted_page])
            
            # Indent based on level
            indent = (level - 1) * 20
            
            # Add text (limit title length to avoid overflow)
            max_title_len = 50 - indent // 2
            display_title = title[:max_title_len]
            dots = '.' * max(3, 50 - len(display_title) - len(str(adjusted_page)))
            text = f"{display_title} {dots} {adjusted_page}"
            
            toc_page.insert_text(
                (50 + indent, y_position),
                text,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0)
            )
            
            y_position += 20
            
            # Add new page if we run out of space
            if y_position > 800:
                toc_page_num += 1
                toc_page = self.output_doc.new_page(toc_page_num, width=595, height=842)
                toc_page.insert_text(
                    (50, 50),
                    "Table of Contents (continued)",
                    fontsize=16,
                    fontname="helv",
                    color=(0, 0, 0)
                )
                y_position = 80
        
        # Update the table of contents with adjusted page numbers
        # The sidebar bookmarks will be clickable
        self.output_doc.set_toc(updated_toc)


def merge_course_pdfs(lectures: list[Path], tirguls: list[Path], 
                      course_folder: Path, parent_folder: Path, 
                      course_name: str) -> dict[str, list[Path]]:
    """
    Merge lecture and tirgul PDFs for a course.
    Outputs PDFs to both the course folder and parent folder.
    
    @param lectures: List of lecture PDF paths.
    @param tirguls: List of tirgul PDF paths.
    @param course_folder: Path to course-specific output folder.
    @param parent_folder: Path to parent folder for all courses.
    @param course_name: Name of the course.
    @return: Dictionary with lists of paths to generated PDFs in both locations.
    """
    course_folder = Path(course_folder)
    parent_folder = Path(parent_folder)
    course_folder.mkdir(parents=True, exist_ok=True)
    parent_folder.mkdir(parents=True, exist_ok=True)
    
    merger = PDFMerger()
    results = {'course': [], 'parent': []}
    
    # Merge lectures
    if lectures:
        lecture_titles = [f"Lecture {i+1}" for i in range(len(lectures))]
        
        # Save to course folder
        lectures_course = course_folder / f"{course_name}_Lectures.pdf"
        merger.merge_pdfs(lectures, lectures_course, lecture_titles)
        results['course'].append(lectures_course)
        print(f"Created: {lectures_course}")
        
        # Save to parent folder
        lectures_parent = parent_folder / f"{course_name}_Lectures.pdf"
        merger.merge_pdfs(lectures, lectures_parent, lecture_titles)
        results['parent'].append(lectures_parent)
        print(f"Created: {lectures_parent}")
    
    # Merge tirguls
    if tirguls:
        tirgul_titles = [f"Tirgul {i+1}" for i in range(len(tirguls))]
        
        # Save to course folder
        tirguls_course = course_folder / f"{course_name}_Tirgul.pdf"
        merger.merge_pdfs(tirguls, tirguls_course, tirgul_titles)
        results['course'].append(tirguls_course)
        print(f"Created: {tirguls_course}")
        
        # Save to parent folder
        tirguls_parent = parent_folder / f"{course_name}_Tirgul.pdf"
        merger.merge_pdfs(tirguls, tirguls_parent, tirgul_titles)
        results['parent'].append(tirguls_parent)
        print(f"Created: {tirguls_parent}")
    
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
        
        # Save to course folder
        full_course = course_folder / f"{course_name}_Full.pdf"
        merger.merge_pdfs(all_files, full_course, all_titles)
        results['course'].append(full_course)
        print(f"Created: {full_course}")
        
        # Save to parent folder
        full_parent = parent_folder / f"{course_name}_Full.pdf"
        merger.merge_pdfs(all_files, full_parent, all_titles)
        results['parent'].append(full_parent)
        print(f"Created: {full_parent}")
    
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
