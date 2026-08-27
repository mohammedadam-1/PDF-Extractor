import re
from io import BytesIO

def get_file_buffer(fileBytes) -> BytesIO:
    return BytesIO(fileBytes)

def structure_text(raw_text: str) -> list[list]:
    """Structures raw text into structured strings"""
    try:
# 1. Flexible Regex logic:
# \d{1,4}\b    -> Matches an index number that is 1, 2, 3, or 4 digits long
# \s+          -> Matches the spaces immediately following the index number
# [A-Za-z]     -> Ensures the first character after the index is a letter (e.g., "India" or a Name), 
#                 which prevents matching stray random numbers or phone digits.
# .*?          -> Lazily matches all text inside that row block
# (?=\n\d{1,4}\b\s+[A-Za-z]|$) -> Lookahead: Stops right before the next valid row index or end of string.
        pattern = r"(?:^|\n)(\d{1,4}\b\s+[A-Za-z].*?)(?=\n\d{1,4}\b\s+[A-Za-z]|$)"

        # re.DOTALL ensures that the '.' matches newline characters for multi-line cells like row 127
        rows = re.findall(pattern, raw_text, re.DOTALL)
        rows_list = []
        # 2. Output your cleanly isolated row groups
        for idx, row in enumerate(rows, start=1):
            row = [row.strip()]
            rows_list.append(row)
        return rows_list
    except Exception as e:
        print(e)

# import re

# def structure_text(raw_text: str) -> list[list[str]]:
#     """Splits unformatted rows into structured columns by filtering out PDF noise."""
    
#     # 1. Regex to isolate rows (Improved from your previous step)
#     row_pattern = r"(?:^|\n)[ \t]*(\d{1,4}\b[ \t]+[A-Za-z].*?)(?=\n[ \t]*\d{1,4}\b[ \t]+[A-Za-z]|$)"
#     rows = re.findall(row_pattern, raw_text, re.DOTALL)
    
#     rows_list = []
    
#     for row in rows:
#         # Standardise spacing and remove structural artifacts from multi-line rows
#         clean_row = re.sub(r'\s+', ' ', row.strip())
        
#         # 2. Regex to segment the text into columns using anchors
#         # Group 1: Index Number
#         # Group 2: Country
#         # Group 3: Name & Job Title (Captures text up until it sees a phone number pattern)
#         # Group 4: Phone Numbers (Captures digits, dashes, plus signs, brackets, and inner noise)
#         # Group 5: Company Name (The remaining text at the trailing end)
#         split_pattern = r"^(\d+)\s+(India)\s+(.*?)\s+([\d\+\-\s\(\)\,\&\\\|\.\#X]+?)\s*([A-Za-z].*)$"
        
#         match = re.match(split_pattern, clean_row)
        
#         if match:
#             idx, country, name_title, phones, company = match.groups()
            
#             # 3. Data Cleansing
#             # Remove isolated noise symbols, trailing slashes, and pipes from text blocks
#             name_title = re.sub(r'[\s\d\|\=\&\,\\]+$', '', name_title).strip()
#             name_title = re.sub(r'\s*\|\s*', ' ', name_title).strip()
            
#             # Strip noise from phones, preserve commas as item separators, clean up double spaces
#             phones = re.sub(r'[\&\\\|\=\#X\s]+', ' ', phones)
#             phones = ", ".join([p.strip() for p in phones.split(',') if p.strip()])
#             phones = re.sub(r'\s+', ' ', phones).strip()
            
#             # Final clean up for company names
#             company = re.sub(r'[\s\|\=\&\,\\]+$', '', company).strip()
#             company = re.sub(r'^[\|\=\&\,\s\\]+', '', company).strip()
            
#             # Combine back into a list of columns
#             rows_list.append([idx, country, name_title, phones, company])
#         else:
#             # Fallback if a line doesn't perfectly fit the structured sequence
#             rows_list.append([clean_row])
            
#     return rows_list


# import re

# # A phone/mobile cell is either "-" (empty) or a number with a country code,
# # area code, spacing/dashes — but crucially, contains no letters.
# PHONE = r'-|\+?\d[\d\-\s\(\)]{5,}\d'

# ROW_PATTERN = re.compile(
#     r'^\s*(?P<idx>\d{1,4})\s+'          # row index
#     r'(?P<country>India)\s+'            # country column
#     r'(?P<name_title>.*?)\s+'           # last name + title (lazy — stops at first phone-shaped token)
#     r'(?P<phone>' + PHONE + r')\s+'     # phone column
#     r'(?P<mobile>' + PHONE + r')\s+'    # mobile column
#     r'(?P<account>.+?)\s*$',            # account name (greedy to end, handles wraps via DOTALL)
#     re.DOTALL
# )

# def structure_text(raw_text: str) -> list[dict]:
#     # Step 1: isolate each row block (unchanged idea, but require the index
#     # to be followed by "India" specifically — avoids false splits on
#     # phone digits that happen to start a line)
#     row_block_pattern = re.compile(
#         r'(?:^|\n)[ \t]*(\d{1,4})[ \t]+(India\b.*?)(?=\n[ \t]*\d{1,4}[ \t]+India\b|\Z)',
#         re.DOTALL
#     )

#     results = []
#     for idx, block in row_block_pattern.findall(raw_text):
#         clean = re.sub(r'\s+', ' ', block.strip())
#         full_line = f"{idx} {clean}"
#         m = ROW_PATTERN.match(full_line)
#         if m:
#             d = m.groupdict()
#             d['name_title'] = d['name_title'].strip(' |,&\\')
#             d['account'] = d['account'].strip(' |,&\\')
#             results.append(d)
#         else:
#             results.append({'raw': full_line})  # fallback for rows that don't fit
#     return results