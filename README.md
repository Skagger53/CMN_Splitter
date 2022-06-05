# CMN_Splitter
Highly specific software to split MN Department of Health case mix notice files

This software accepts only MN Case Mix Notice file PDFs, processes them, and outputs a folder containing each case mix notice letter as its own file.
The folder starts with "CM files", then adds the facility ID, and finally the case mix notice date.
Each file has a name with the patient's name, the patient's new case mix code, and the effective date. This is all the needed data from that letter.

Data validation ensures that a true case mix notice has been selected; the software will not attempt to process a PDF that is not a case mix notice.
