# CMN Splitter copyright 2022
# By Matt Skaggs
# Distribution of this software without the explicit permission of the author is prohibited.

if __name__ == '__main__':
    import pdfplumber, os, sys
    import tkinter as tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfile
    from PyPDF2 import PdfFileReader, PdfFileWriter
    from PIL import Image, ImageTk

    # This function allows this program to include and still find image files (here new_logo.jpg) when compiled as a single file (not a directory).
    # This function is modified from the function provided by auto-py-to-exe author Brent Vollebregt (https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/#additional-information-and-explanations).
    # He got it from a Stack Overflow post (https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile).
    def resource_path(relative_path):
        try: base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS
        except: base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Accepts file path as argument. Parses data in the file to create list of file names to use when creating PDFs.
    # First runs two error checks.
    # Called in open_pdf()
    def evaluate_pages(path):
        with pdfplumber.open(path) as full_case_mix_file:
            # Check number of pages (must be even) and headers (must match standard header text).
            # Upon failure, returns error message, which is displayed in error window.
            if len(full_case_mix_file.pages) % 2 != 0: return "Error: PDF has an odd number of pages. Valid Case Mix Notices have an even number of pages.", ""
            if full_case_mix_file.pages[0].extract_text().split("\n", 1)[0] != "MINNESOTA DEPARTMENT OF HEALTH" or full_case_mix_file.pages[0].extract_text().split("\n", 2)[1] != "Case Mix Review Program, Health Regulation Division": return "Error: File header check failed. Is this a valid Case Mix Notice?", ""

            # Evaluate only odd pages (indices 0, 2...). These have the relevant data.
            file_name_list = []
            for page in range(0, len(full_case_mix_file.pages), 2):
                # Create list to be able to isolate first 12 lines. These have the relevant data.
                page_text = list(full_case_mix_file.pages[page].extract_text().split("\n", 12))

                # Extract the 3 pieces of needed data.
                name = page_text[4][:len(page_text[4]) - 11].title()
                case_mix = page_text[10][-3:]
                eff_date = page_text[11][-10:].replace("/", "-") # Replace illegal file name character.
                folder_code = f"{page_text[7][-5:]} {page_text[4][-10:].replace('/', '')}"  # Used in folder name creation for output to ensure that when processing multiple notices, new folders are created and previously created PDFs are not overwritten.

                file_name_list.append(f"{name} {case_mix} {eff_date}") # Concatenated extracted data will be used for file names. Concatenated data is appended to file name list.

            return file_name_list, folder_code

    # Creates each PDF. Called from open_pdf()
    def output_pdfs(file_dir_and_name, file_name_list, notice_date): # file_name_list is the list used for output file names.
        new_dir = os.path.join(os.path.dirname(file_dir_and_name), f"CM files {notice_date}") # Defines intended output directory
        if os.path.exists(new_dir) == False: os.mkdir(new_dir) # Creates output directory if it doesn't exist

        with open(file_dir_and_name, "rb") as CM_file:
            pdf = PdfFileReader(CM_file, "rb")

            # Iterating by every other page to export two pages at once
            for page in range(0, pdf.getNumPages(), 2):
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                pdf_writer.addPage(pdf.getPage(page + 1))
                output_filename = f"{new_dir}/CM{int(page / 2 + 1):03} {file_name_list[int(page / 2)]}.pdf" # Creates output file names as "CM[###] [Patient name] [Case mix] [Effective date]"

                with open(output_filename, "wb") as out: pdf_writer.write(out)

    # Displays window for any error message that is needed. Does not need to return any values.
    # Called in open_pdf()
    def error_message(message, title = "Error", window_width = 100):
        error_window = tk.Tk()
        error_window.geometry(f"{window_width}x100")
        error_window.wm_title(title)
        label = ttk.Label(error_window, anchor=tk.CENTER, text=message)
        label.pack(side="top", fill="x", pady=15)
        OK_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
        OK_button.pack()
        error_window.mainloop()

    # Main window for user
    root = tk.Tk()
    root.title("Case Mix Notice Splitter")

    canvas = tk.Canvas(root, width = 450, height = 375)
    canvas.grid(rowspan = 5)

    # Runs when the browse button is pressed.
    def open_pdf():
        pdf_file = askopenfile(parent = root, mode = "rb", title = "Choose the Case Mix Notice PDF", filetype = [("PDF file", "*.pdf")])
        if pdf_file:
            full_file_name = os.path.abspath(pdf_file.name)
            if os.path.splitext(pdf_file.name)[1] == ".pdf": # Checks to ensure that file is a PDF.
                try: # Checks for errors from parsing file. This is unlikely to happen unless someone picks the wrong PDF and no other error checks succeed.
                    evaluate_pages(full_file_name)
                except:
                    pdf_file.close()
                    error_message("Error: Parsing failed. Is this a valid Case Mix Notice?", "Parsing error", 400)
                else:
                    file_name_list, notice_date = evaluate_pages(full_file_name)
                    if file_name_list[:5] != "Error": # If errors found in evaluate_pages(), list will be prepended with "Error:"; otherwise it have the file names.
                        try:
                            output_pdfs(full_file_name, file_name_list, notice_date)
                        except: # Triggers if creating PDFs fails. This should not happen due to previous error checks.
                            pdf_file.close()
                            error_message("PDF creation failed.", "File output error", 200)
                        else: # Creates individual files and notifies user upon completion.
                            output_pdfs(full_file_name, file_name_list, notice_date)
                            pdf_file.close()
                            completed_window = tk.Tk()
                            completed_window.geometry("325x130")
                            completed_window.wm_title("Task completed")
                            message1 = ttk.Label(completed_window, anchor=tk.CENTER, text="Case Mix Notice file was split successfully!")
                            message1.pack(side="top", fill="x", pady=8)
                            message2 = ttk.Label(completed_window, anchor=tk.CENTER, text="All notices are in the \"CM files\" folder.")
                            message2.pack(side="top", fill="x", pady=10)
                            OK_button = ttk.Button(completed_window, text="OK", command=completed_window.destroy)
                            OK_button.pack()
                            completed_window.mainloop()
                    else: # Triggers if a parsing error occured. Error text is returned from the evaluate_pages() function.
                        pdf_file.close()
                        error_message(file_name_list, "Parsing error", 650)
            else:
                # Triggers when selected file extension is not .pdf
                pdf_file.close()
                error_message("Please choose a PDF.", "File type error", 280)

    # Placing logo
    logo = Image.open(resource_path("logo2.jpg"))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo)
    logo_label.Image = logo
    logo_label.grid(row=0)

    # Main window instructions
    instructions = tk.Label(root, pady = 10, text="Choose a Case Mix Notice file.")
    instructions.grid(row=1)

    # Browse button
    browse_text = tk.StringVar()
    browse_button = tk.Button(root, font = "sans 11 bold", textvariable = browse_text, command = lambda:open_pdf())
    browse_text.set("Browse")
    browse_button.grid(pady = 10, row = 2)

    #Exit button
    exit_text = tk.StringVar()
    exit_button = tk.Button(root, font = "sans 11", textvariable=exit_text, command=root.destroy)
    exit_text.set("Exit")
    exit_button.grid(pady = 20, row=3)

    root.mainloop()

else:
    print("This is not a module. Execute directly.")