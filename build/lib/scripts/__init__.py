# scripts/__init__.py

from .remove_pnum_hilight_title import process_directory as process_directory_high_titles_rmv_txt
from .split_chapters import process_directory as process_directory_split_ch
from .clean_text import process_directory as process_directory_clean_txt
from .fix_lines import process_directory as process_directory_line_fix
from .replace_numbers import process_directory as process_directory_numbers2words
from .liaisons import process_directory as process_directory_liasons
from .ent_ait_fix import process_directory as process_directory_ent_ait_fix
from .replace_words import process_directory as process_directory_replace_words
from .replace_special_chars import process_directory as process_directory_special_chars
from .name_correction import process_directory as process_directory_name_correction