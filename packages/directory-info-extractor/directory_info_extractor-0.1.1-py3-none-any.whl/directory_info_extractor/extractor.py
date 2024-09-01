import os
import fnmatch
from typing import List, Optional
import logging

def get_directory_info(
    dir_path: str,
    include_project_structure: bool = True,
    include_file_contents: bool = True,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    recursive: bool = True,
    log_path: Optional[str] = None
) -> str:
    """
    Retrieves information from a local directory.

    Args:
        dir_path (str): Path to the local directory.
        include_project_structure (bool): Include project structure.
        include_file_contents (bool): Include file contents.
        include_patterns (List[str], optional): Patterns to include (e.g., ["*.py", "specific_folder/*"]).
        exclude_patterns (List[str], optional): Patterns to exclude.
        recursive (bool): Whether to recursively search subdirectories.
        log_path (str, optional): Path to save the log.

    Returns:
        str: Formatted directory information.
    """
    logger = logging.getLogger(__name__)
    
    try:
        dir_name = os.path.basename(dir_path)
        output = [f"Directory Name: {dir_name}"]

        if include_project_structure:
            project_structure = _get_project_structure(dir_path, include_patterns, exclude_patterns, recursive)
            output.append("\nProject Structure:")
            output.append(project_structure)

        if include_file_contents:
            file_contents = _get_file_contents(dir_path, include_patterns, exclude_patterns, recursive)
            output.append("\nFile Contents:")
            output.append(file_contents)

        result = "\n".join(output)
        
        if log_path:
            with open(log_path, 'w', encoding='utf-8') as file:
                file.write(result)

        return result

    except Exception as e:
        logger.error(f"Error retrieving directory information: {str(e)}")
        raise

def _get_project_structure(
    dir_path: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    recursive: bool = True
) -> str:
    """
    Retrieves the project structure, including specified patterns and excluding others.
    """
    include_patterns = include_patterns or ["*"]
    exclude_patterns = exclude_patterns or []
    structure = []

    for root, dirs, files in os.walk(dir_path):
        level = root.replace(dir_path, '').count(os.sep)
        indent = '    ' * level
        rel_path = os.path.relpath(root, dir_path)

        if _should_exclude(rel_path, exclude_patterns):
            dirs[:] = []  # Don't recurse into this directory
            continue

        if rel_path != '.':
            structure.append(f"{indent}{os.path.basename(root)}/")

        subindent = '    ' * (level + 1)
        for f in files:
            if _should_include(os.path.join(rel_path, f), include_patterns, exclude_patterns):
                structure.append(f"{subindent}{f}")

        if not recursive:
            break  # Stop after processing the top-level directory

    return '\n'.join(structure)

def _get_file_contents(
    dir_path: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    recursive: bool = True
) -> str:
    """
    Retrieves the contents of files, including and excluding specified patterns.
    """
    logger = logging.getLogger(__name__)
    include_patterns = include_patterns or ["*"]
    exclude_patterns = exclude_patterns or []
    contents = []

    for root, dirs, files in os.walk(dir_path):
        rel_path = os.path.relpath(root, dir_path)

        if _should_exclude(rel_path, exclude_patterns):
            dirs[:] = []  # Don't recurse into this directory
            continue

        for file in files:
            file_path = os.path.join(rel_path, file)
            if _should_include(file_path, include_patterns, exclude_patterns):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    contents.append(f"\nFile: {file_path}\n{file_content}")
                except Exception as e:
                    logger.warning(f"Could not read file {file_path}: {str(e)}")

        if not recursive:
            break  # Stop after processing the top-level directory

    return "\n".join(contents)

def _should_include(path: str, include_patterns: List[str], exclude_patterns: List[str]) -> bool:
    """
    Determines if a path should be included based on include and exclude patterns.
    """
    return any(fnmatch.fnmatch(path, pattern) for pattern in include_patterns) and \
           not _should_exclude(path, exclude_patterns)

def _should_exclude(path: str, exclude_patterns: List[str]) -> bool:
    """
    Determines if a path should be excluded based on exclude patterns.
    """
    return any(fnmatch.fnmatch(path, pattern) for pattern in exclude_patterns)
