Duplicate Finder

A lightweight desktop application designed to identify and manage duplicate entries within PDF documents. This tool is specifically optimized for collections of quotes, utilizing fuzzy string matching to detect both exact duplicates and entries with minor typographical errors.

Duplicate Finder provides a graphical interface for processing PDF text. It implements the Gestalt Pattern Matching algorithm to calculate similarity ratios between lines of text, allowing users to find near-matches that standard search functions would miss.

Features

    PDF text extraction and line-by-line parsing.

    Adjustable similarity threshold for fuzzy duplicate detection.

    Real-time progress tracking with a visual interface.

    Result exporting to plaintext formats.

    Standalone executable capability for Windows environments.

Installation:

Pre-compiled Executable

    Navigate to the Releases page of this repository.

    Download the DuplicateFinder.exe file.

    Launch the application directly. No Python installation is required for this version.

Running from Source:

If you prefer to run the script manually, ensure you have Python 3.8 or higher installed.

    Clone this repository:

git clone https://github.com/username/duplicate-finder.git

Install the required dependency:

pip install PyPDF2

Execute the script:

    python DuplicateFinder.py

Usage Tutorial
1. Loading a Document

Click the Select PDF button to open the Windows file explorer. Select the document you wish to analyze. The status label will update with the filename once the text has been successfully cached into memory.
2. Configuring Sensitivity

Adjust the Similarity Threshold slider before beginning the scan:

    1.0 Setting: Detects only 100% identical strings.

    0.85 Setting: Recommended for catching typos or punctuation differences.

    0.70 Setting: High sensitivity; may catch quotes that share similar phrasing but are unique.

3. Executing the Scan

The Start Scan button will become active (green) once a file is loaded. Click it to begin the comparison process. The progress bar will indicate the completion percentage of the nested comparison loops.
4. Analyzing Results

Results are displayed in the output area categorized into:

    Exact Duplicates: Groups of identical text found in multiple locations.

    Potential Near-Matches: Pairs of text that fall within the similarity threshold, displaying the percentage of the match.

5. Exporting and Resetting

    Click Export to .txt to save the findings to a local file.

    Click Reset to clear the current session and prepare the application for a new document.

Compilation Instructions

To build your own executable from the source code:

    Install the compiler:

pip install auto-py-to-exe

Launch the utility:

    auto-py-to-exe

    Select DuplicateFinder.py as the script location.

    Choose One File and Window Based (Hide Console) options.

    Click Convert .py to .exe.

License

This project is licensed under the MIT License - see the LICENSE file for details.
