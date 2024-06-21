import os
import re
from tqdm import tqdm

def read_input_file():
    with open('input.txt', 'r', encoding='utf-8') as f:
        return f.readlines()

def append_to_file(filename, lines):
    with open(filename, 'a') as f:
        f.writelines(lines)

def write_to_file(filename, lines):
    with open(filename, 'w') as f:
        f.writelines(lines)

def extract_specific_text():
    lines = read_input_file()
    text_to_find = input("Enter the text you want to extract: ").lower()

    
    if not os.path.exists("extractedDomains"):
        os.makedirs("extractedDomains")

    matching_lines = [line for line in lines if text_to_find in line.lower()]
    filename = os.path.join('extractedDomains', f'{text_to_find}.txt')
    append_to_file(filename, matching_lines)

def remove_duplicate_lines():
    lines = read_input_file()
    unique_lines = list(set(lines))
    write_to_file('output.txt', unique_lines)

def extract_emails():
    lines = read_input_file()
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
    emails = re.findall(pattern, ''.join(lines), re.IGNORECASE)
    write_to_file('extracted_emails.txt', emails)

def extract_passwords():
    lines = read_input_file()
    passwords = [line.split(":")[1].strip() if ':' in line else None for line in lines]
    passwords = list(filter(None, passwords))
    write_to_file('extracted_passwords.txt', passwords)

def extract_urls():
    lines = read_input_file()
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(pattern, ''.join(lines))
    urls_with_newlines = [url + '\n' for url in urls]
    append_to_file('extracted_URL.txt', urls_with_newlines)

def organize_alphabetically():
    lines = read_input_file()
    sorted_lines = sorted(lines)
    write_to_file('output.txt', sorted_lines)

def create_directories():
    lines = read_input_file()
    for line in tqdm(lines, desc="Computing..."):
        line = line.strip()
        if not os.path.exists(line):
            os.makedirs(line)

def extract_32_char_line():
    lines = read_input_file()
    matching_lines = [line for line in lines if ':' in line and len(line.split(":")[1].strip()) == 32]
    append_to_file('extracted_hashed.txt', matching_lines)

def combine_files():
    files = os.listdir('toCombine')
    combined_content = []
    for filename in tqdm(files, desc="Computing..."):
        with open(os.path.join('toCombine', filename), 'r') as f:
            combined_content.extend(f.readlines())
    write_to_file('output.txt', combined_content)

def split_by_lines():
    lines_per_file = int(input("Enter the number of lines per split: "))
    filename = input("Enter name to save split files as: ")
    lines = read_input_file()
    
    if not os.path.exists(filename):
        os.makedirs(filename)
        
    for index in tqdm(range(0, len(lines), lines_per_file), desc="Computing..."):
        chunk = lines[index:index + lines_per_file]
        with open(os.path.join(filename, f'{filename}_{index // lines_per_file}.txt'), 'w') as f:
            f.writelines(chunk)

def join_lines():
    with open('extracted_emails.txt', 'r') as e, open('extracted_passwords.txt', 'r') as p:
        emails = e.readlines()
        passwords = p.readlines()
    joined_output = [f'{email.strip()}:{password.strip()}\n' for email, password in zip(emails, passwords)]
    write_to_file('JoinedOutput.txt', joined_output)

def extract_text_around_colon():
    lines = read_input_file()
    pattern = r'\S+:\S+'  # This matches non-space characters before and after the colon
    extracted_lines = [re.search(pattern, line).group(0) + '\n' for line in lines if re.search(pattern, line)]
    append_to_file('cleanedOutput.txt', extracted_lines)
    
def extract_and_save_domain_specific_text():
    lines = read_input_file()
    domain_to_lines_map = {}

    for line in lines:
        match = re.search(r'@(\w+)\.net', line, re.IGNORECASE)    
        if match:
            domain = match.group(1)
            if domain not in domain_to_lines_map:
                domain_to_lines_map[domain] = []
            domain_to_lines_map[domain].append(line)

    if not os.path.exists("autoExtract"):
        os.makedirs("autoExtract")

    for domain, matching_lines in domain_to_lines_map.items():
        filename = os.path.join('autoExtract', f'{domain}.txt')
        append_to_file(filename, matching_lines)

def display_domain_statistics():
    lines = read_input_file()
    total_lines = len(lines)
    domain_counter = {}

    for line in lines:
        match = re.search(r'@(\w+)\.net', line)
        if match:
            domain = match.group(1)
            domain_counter[domain] = domain_counter.get(domain, 0) + 1

    results = []
    for domain, count in domain_counter.items():
        percentage = (count / total_lines) * 100
        results.append((domain, count, percentage))

    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)

    print("\nCombo Details with .net filter:")
    print("\nDomain | Lines | Percentage of Combo")
    
    start_index = 0
    while start_index < len(sorted_results):
        for i in range(start_index, start_index + 50):
            if i < len(sorted_results):
                domain, count, percentage = sorted_results[i]
                print(f"{domain} | {count} | {percentage:.2f}%")

        start_index += 50
        user_input = input("\nDo you wish to see the next set of results? (y/n): ")
        if user_input.lower() != 'y':
            break

def display_general_domain_statistics():
    lines = read_input_file()
    total_lines = len(lines)
    domain_counter = {}

    for line in lines:
        match = re.search(r'@(\w+)\.', line, re.IGNORECASE)
        if match:
            domain = match.group(1)
            domain_counter[domain] = domain_counter.get(domain, 0) + 1

    results = []
    for domain, count in domain_counter.items():
        percentage = (count / total_lines) * 100
        results.append((domain, count, percentage))
            
    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)

    print("\nCombo Details")
    print("\nDomain | Lines | Percentage of Combo")
    
    start_index = 0
    while start_index < len(sorted_results):
        for i in range(start_index, start_index + 50):
            if i < len(sorted_results):
                domain, count, percentage = sorted_results[i]
                print(f"{domain} | {count} | {percentage:.2f}%")
        start_index += 50
        user_input = input("\nDo you wish to see the next set of results? (y/n): ")
        if user_input.lower() != 'y':
            break

    
def main():
    while True:
        print("\nThe information and/or software provided here is intended solely for educational purposes and legal penetration testing purposes. By accessing or using this information and/or software, you acknowledge and agree that you assume full responsibility for your actions and any consequences that may result from those actions. The creators, contributors, and providers of this information and/or software shall not be held liable for any misuse or damage arising from its application. It is your responsibility to ensure that your use complies with all applicable laws and regulations.")
        print("\n\n\n?HELP")
        print("Option 1; To extract all lines for earthlink.net enter @earthlink.net | If you want to extract all .net domains enter .net | This will create text documents named what you enter | When extracting lines are appended and never overwrite.")
        print("Option 2; Remove duplicate lines from input.txt & saves to output.txt | Output.txt gets overwritten so always move it or rename it.") 
        print("Option 3; Splits Email from Password, saves to extracted_emails.txt(is Overwrite each time you run task) | Good for mailing list or if you need to split for dehashing passwords.")
        print("Option 4; Same as option 3 but with passwords, extracted_passwords.txt(is Overwrite each time you run task).")
        print("Option 5; Extract URLs from input.txt | Append save to extracted_URL.txt")  
        print("Option 6; Organize input.txt A-Z | Overwrite output.txt")
        print("Option 7; Use lines from input.txt to name new directorys | Do not use this option unless you have a reason!")
        print("Option 8; Extract lines from input.txt if the password is MD5 hashed | Append save to extracted_hashed.txt | Use to create your own private combo that has not been cracked yet | A popular dehashing script is HASHCAT OCL.") 
        print("Option 9; Drop files in the directory toCombine that you need to combine | Good idea to remove duplicates after | Overwrite output.txt")
        print("Option 10; Enter the number of lines you want to split combo by then name your splits | creates directory to save your splits in.")
        print("Option 11; After dehashing your hashed passwords use this to rejoin back with email addresses | The files it looks for to join are extracted_emails.txt and extracted_passwords.txt | overwrite JoinedOutput.txt")
        print("Option 12; Strip capture results from combo | append save cleanedOutput.txt")
        print("Option 13; Extract all domains by domain to seperate text files | append save")
        print("Option 14; Analyze input.txt and display Top Domains, Number of lines, and the % of combo | Only .net domains")
        print("Option 15; Analyze input.txt and display Top Domains, Number of lines, and the % of combo | All domains")
        print("Option 0; Exit")
        print("\n")
        print("\n")
        print("\nhttps://github.com/noarche/ComboScriptPro/ ")
        print("ComboScriptPro v2.1.6 | Build Date June 20 2024")
        print("\nChoose a task:")
        print("1. Extract lines by specific domain")
        print("2. Remove duplicate lines")
        print("3. Extract/Split email addresses")
        print("4. Extract/Split passwords")
        print("5. Extract URLs")
        print("6. Organize lines alphabetically")
        print("7. Create directory named as each line")
        print("8. Extract lines with MD5 hashed password")
        print("9. Combine all text files from 'toCombine' directory")
        print("10. Split by user-defined number of lines")
        print("11. Join lines from extracted_emails.txt and extracted_passwords.txt")
        print("12. Extract combo from hits with capture")
        print("13. AutoExtract and organize all .net domains by domain")
        print("14. Display Combo Statistics [.net Domains]")
        print("15. Display Combo Statistics [All Domains]")
        print("0. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 0:
            break
        elif choice == 1:
            extract_specific_text()
        elif choice == 2:
            remove_duplicate_lines()
        elif choice == 3:
            extract_emails()
        elif choice == 4:
            extract_passwords()
        elif choice == 5:
            extract_urls()
        elif choice == 6:
            organize_alphabetically()
        elif choice == 7:
            create_directories()
        elif choice == 8:
            extract_32_char_line()
        elif choice == 9:
            combine_files()
        elif choice == 10:
            split_by_lines()
        elif choice == 11:
            join_lines()
        elif choice == 12:
            extract_text_around_colon()
        elif choice == 13:
            extract_and_save_domain_specific_text()
        elif choice == 14:
            display_domain_statistics()
        elif choice == 15:
            display_general_domain_statistics()

if __name__ == "__main__":
    main()
