import re  
import deepl  
from pathlib import Path  
from typing import Dict, List, Tuple  

class ChineseCommentTranslator:  
    def __init__(self, auth_key: str, replace_mode: bool = False):  
        self.chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]+')  
        self.special_chars = r'[,;\(\)\[\]\{\}"\'`<>@#$%^&*+=|\\~]'  
        self.translator = deepl.Translator(auth_key)  
        self.replace_mode = replace_mode  
        self.reset_counters()  
        self.translation_cache: Dict[str, str] = {}  

    def reset_counters(self):  
        self.multiline_count = 0  
        self.singleline_count = 0  
        self.xml_doc_count = 0  
        self.total_lines_with_chinese = 0  
        self.total_characters_translated = 0  

    def has_chinese(self, text: str) -> bool:  
        return bool(self.chinese_pattern.search(text))  

    def translate_text(self, text: str) -> str:  
        if not text:  
            return ""  
        
        text = text.strip()  
        if text in self.translation_cache:  
            return self.translation_cache[text]  
        
        try:  
            result = self.translator.translate_text(text, source_lang="ZH", target_lang="EN-US")  
            translated = result.text  
            self.translation_cache[text] = translated  
            self.total_characters_translated += len(text)  
            return translated  
        except Exception as e:  
            print(f"Translation error: {e}")  
            return f"[Translation Error: {str(e)}]"  

    def format_comment(self, chinese_text: str, translated_text: str) -> str:  
        if self.replace_mode:  
            return translated_text  
        else:  
            return f"{chinese_text} {translated_text}"  
        
    def process_xml_block(self, xml_block_lines: List[Tuple[int, str]], start_line: int, end_line: int) -> List[str]:  
        translated_lines = []  
        print(f"XML Doc Lines {start_line:4d}-{end_line:4d}:")  
        
        for line_num, line_content in xml_block_lines:  
            # Try to match text within XML tags first  
            xml_match = re.search(r'<[^>]+>([^<]+)</[^>]+>', line_content)  
            if xml_match and self.has_chinese(xml_match.group(1)):  
                chinese_text = xml_match.group(1).strip()  
                translated = self.translate_text(chinese_text)  
                print(f"Line {line_num + 1:4d}: {translated}")  
                
                if self.replace_mode:  
                    translated_line = line_content.replace(chinese_text, translated)  
                else:  
                    translated_line = f"{line_content} {translated}"  
                
                translated_lines.append((line_num, translated_line))  
                self.total_lines_with_chinese += 1  
            else:  
                # Try to match direct comments without XML tags  
                direct_match = re.search(r'///\s*(.+)$', line_content)  
                if direct_match and self.has_chinese(direct_match.group(1)):  
                    chinese_text = direct_match.group(1).strip()  
                    translated = self.translate_text(chinese_text)  
                    print(f"Line {line_num + 1:4d}: {translated}")  
                    
                    if self.replace_mode:  
                        translated_line = re.sub(r'///\s*.+$', f'/// {translated}', line_content)  
                    else:  
                        translated_line = f"{line_content} {translated}"  
                    
                    translated_lines.append((line_num, translated_line))  
                    self.total_lines_with_chinese += 1  
        
        return translated_lines   

    def extract_and_translate_chinese(self, text: str) -> str:  
        parts = re.split(f'({self.special_chars})', text)  
        results = []  
        
        current_part = ""  
        for part in parts:  
            if self.has_chinese(part):  
                if current_part:  
                    results.append(current_part)  
                    current_part = ""  
                translated = self.translate_text(part)  
                results.append(self.format_comment(part, translated))  
            else:  
                current_part += part  
        
        if current_part:  
            results.append(current_part)  
        
        return ''.join(filter(None, results))  

    def clean_xml_comment(self, comment: str) -> str:  
        clean = re.sub(r'<[^>]+>', '', comment)  
        return clean.strip()  

    def print_summary(self):  
        print("\n" + "=" * 50)  
        print("TRANSLATION SUMMARY")  
        print("=" * 50)  
        print(f"Multi-line comments containing Chinese: {self.multiline_count}")  
        print(f"Single-line comments containing Chinese: {self.singleline_count}")  
        print(f"XML documentation comments containing Chinese: {self.xml_doc_count}")  
        print(f"Total characters translated: {self.total_characters_translated}")  
        print("-" * 50)  
        print(f"Total comments containing Chinese: {self.multiline_count + self.singleline_count + self.xml_doc_count}")  
        print(f"Total lines containing Chinese comments: {self.total_lines_with_chinese}")  
        print(f"Translation mode: {'Replace' if self.replace_mode else 'Append'}")  
        print("=" * 50)  

    def process_file(self, file_path: str, output_path: str = None) -> None:  
        try:  
            self.reset_counters()  

            with open(file_path, 'r', encoding='utf-8') as file:  
                content = file.read()  
                
            print(f"\nAnalyzing and translating file: {file_path}")  
            print("=" * 80)  

            lines = content.splitlines()  
            translated_lines = lines.copy()  
            
            print("\nMulti-line comments containing Chinese:")  
            print("-" * 50)  
            
            # Updated pattern to capture leading whitespace  
            pattern = r'^([ \t]*)/\*+\s*(.*?)\s*\*+/'  
            for match in re.finditer(pattern, content, flags=re.DOTALL|re.MULTILINE):  
                leading_space = match.group(1)  # Capture leading whitespace  
                full_match = match.group(0)     # Complete comment including /**/ markers  
                comment = match.group(2)        # Just the content  
                
                # Remove decorative asterisks from comment content  
                cleaned_comment = re.sub(r'^\s*\**\s*|\s*\**\s*$', '', comment)  
                cleaned_comment = re.sub(r'\n\s*\*+\s*', '\n', cleaned_comment)  
                
                if self.has_chinese(cleaned_comment):  
                    self.multiline_count += 1  
                    start_pos = match.start()  
                    end_pos = match.end()  
                    start_line = content.count('\n', 0, start_pos)  
                    end_line = content.count('\n', 0, end_pos)  
                    
                    translated_comment = self.extract_and_translate_chinese(cleaned_comment)  
                    print(f"Lines {start_line + 1:4d}-{end_line + 1:4d}:")  
                    print(f"Original: {cleaned_comment.strip()}")  
                    print(f"Translated: {translated_comment}")  
                    print("-" * 30)  
                    
                    # Create the replacement comment with same formatting  
                    if self.replace_mode:  
                        # Preserve the original comment structure with leading whitespace  
                        comment_part = full_match[len(leading_space):]  # Get comment part without leading space  
                        replacement = f"{leading_space}{comment_part.replace(comment, translated_comment)}"  
                    else:  
                        # Append translation while preserving structure and leading whitespace  
                        replacement = f"{leading_space}{full_match[len(leading_space):]} {translated_comment}"  
                    
                    # Update the affected lines in translated_lines  
                    original_lines = content[start_pos:end_pos].split('\n')  
                    replacement_lines = replacement.split('\n')  
                    
                    for i in range(len(original_lines)):  
                        line_index = start_line + i  
                        if i < len(replacement_lines):  
                            translated_lines[line_index] = replacement_lines[i]  
                    
                    self.total_lines_with_chinese += (end_line - start_line + 1)  
            
            xml_block_start = None  
            xml_block_lines = []  
            
            print("\nSingle-line and XML comments containing Chinese:")  
            print("-" * 50)  
            
            i = 0  
            while i < len(lines):  
                line = lines[i]  
                if line.strip().startswith('///'):  
                    if xml_block_start is None:  
                        xml_block_start = i  
                        xml_block_lines = []  
                    
                    xml_block_lines.append((i, line))  
                    
                    if i == len(lines) - 1 or not lines[i + 1].strip().startswith('///'):  
                        if any(self.has_chinese(self.clean_xml_comment(l[1])) for l in xml_block_lines):  
                            self.xml_doc_count += 1  
                            translated_block = self.process_xml_block(  
                                xml_block_lines,  
                                xml_block_start + 1,  
                                i + 1  
                            )  
                            for line_num, translated_line in translated_block:  
                                translated_lines[line_num] = translated_line  
                        
                        xml_block_start = None  
                        xml_block_lines = []  
                
                elif '//' in line:  
                    comment_match = re.match(r'^(.*?)//(.+)$', line)  
                    if comment_match:  
                        prefix = comment_match.group(1)  
                        comment = comment_match.group(2)  
                        if self.has_chinese(comment):  
                            self.singleline_count += 1  
                            self.total_lines_with_chinese += 1  
                            translated = self.extract_and_translate_chinese(comment)  
                            print(f"Line {i + 1:4d}: {translated}")  
                            if self.replace_mode:  
                                translated_lines[i] = f"{prefix}//{translated}"  
                            else:  
                                translated_lines[i] = f"{prefix}//{comment} {translated}"  
                
                i += 1  

            if output_path and self.replace_mode:  
                with open(output_path, 'w', encoding='utf-8') as f:  
                    f.write('\n'.join(translated_lines))  
                print(f"\nTranslated file saved to: {output_path}")  

            self.print_summary()  

        except Exception as e:  
            print(f"Error processing file: {e}")

def read_file_paths(file_path):  
    try:  
        # Open and read the file using utf-8-sig to handle BOM  
        with open(r'{}'.format(file_path), 'r', encoding='utf-8-sig') as file:  
            # Read lines, strip whitespace, and filter out empty lines  
            # Store paths as raw strings  
            paths = [r'{}'.format(line.strip()) for line in file if line.strip()]  
        return paths  
    except FileNotFoundError:  
        print(f"Error: File '{file_path}' not found.")  
        return []  
    except Exception as e:  
        print(f"Error reading file: {str(e)}")  
        return [] 

def main():  
    AUTH_KEY = "your-deepl-api-key"
    REPLACE_MODE = True
    
    # read .cs path
    file_paths = read_file_paths("cs_file_path.txt")

    # translation
    for file_path in file_paths:
        print(f"="*50)     
        print(f"=== translating {file_path} ===")     
        print(f"="*50)      
        INPUT_FILE = file_path 
        OUTPUT_FILE = file_path        
        translator = ChineseCommentTranslator(AUTH_KEY, REPLACE_MODE)  
        translator.process_file(INPUT_FILE, OUTPUT_FILE if REPLACE_MODE else None)  

if __name__ == '__main__':  
    main()
