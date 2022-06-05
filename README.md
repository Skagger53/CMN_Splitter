# CMN_Splitter
Highly specific Python software to split MN Department of Health case mix notice files

Requires Pdfplumber, os, sys, tkinter, tkinter.filedialog, PyPDF2, PIL

This software accepts only MN Case Mix Notice file PDFs, processes them, and outputs a folder containing each case mix notice letter as its own file along with relevant data in the file name.
The created folder name prepends "CM files" and lists the facility ID and the case mix notice date (e.g., "CM files 00123 01012022").
Each file name prepends CMXXX and the patient's name, the patient's new case mix code, and the effective date (e.g., "CM001 John Doe HB1 01-01-2022"). The name contains all needed data from that letter.

Data validation ensures that a true case mix notice has been selected; the software will not attempt to process a PDF that is not a case mix notice.

The uploaded executable was compiled for Windows systems and has no dependencies.

This was my very first software for use in any kind of professional context.
I want to rewrite this software to make a number of changes.
- I'd rather drop pdfplumber entirely and just use PyPDF2.
- I prefer to use tkinter's messagebox for error messages instead of building a function for that myself ( error_message() ).
- I want to position the main window better and fix the focus issue when a new window appers (the process complete notification window and the error message window).
- I'd wrap the code in function(s), rather than have the whole code execute directly within the initial conditional.
- And probably other inefficiencies I'd catch now that I didn't notice when writing this.
