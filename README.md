# CMN_Splitter
Highly specific Python software to split MN Department of Health case mix notice files

This was my very first software for use in any kind of professional context.
I want to rewrite this software to make a number of changes.
- I'd rather drop pdfplumber entirely and just use PyPdf2.
- I prefer to use tkinter's messagebox for error messages instead of building a function for that myself
- I want to position the main window better and fix the focus issue when a new window appers (process complete window or error message)
- And probably other inefficiencies I'd catch now that I didn't notice when writing this

This software accepts only MN Case Mix Notice file PDFs, processes them, and outputs a folder containing each case mix notice letter as its own file.
The created folder name starts with "CM files", then adds the facility ID, and finally the case mix notice date.
Each file has a name with the patient's name, the patient's new case mix code, and the effective date. This is all the needed data from that letter.

Data validation ensures that a true case mix notice has been selected; the software will not attempt to process a PDF that is not a case mix notice.
