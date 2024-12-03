# Chinese Comment Translator

A Python tool for automatically translating Chinese comments in C# source files to English using the DeepL Translation API.

## Table of Contents
- [Features](#features)
- [Tool Components](#tool-components)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Workflow](#workflow)
- [Supported Comment Types](#supported-comment-types-and-examples)
- [Translation Modes](#translation-modes)
- [Configuration](#configuration)
- [File Processing](#file-processing)
- [Acknowledgments](#acknowledgments)

## Features
- Translates Chinese comments while preserving code structure and formatting
- Supports multiple comment styles (single-line, multi-line, XML documentation)
- Maintains original Chinese text alongside translations (optional)
- Caches translations to minimize API calls
- Preserves code formatting and indentation
- Recursive file scanning with intelligent filtering

## Tool Components

### 1. CS File Finder (find_cs_file.py)
A utility script that helps prepare files for translation by:
- Recursively scanning directories for C# files
- Automatically filtering out:
  * Files in 'obj' folders
  * Designer.cs files
- Outputting full file paths to a text file

Usage:
```bash
# Run the finder and save results to a file
python find_cs_file.py > cs_file_path.txt
```

Path specification examples:
```python
# For Windows paths
path_to_search = r"C:\Your\Project\Path"
# OR
path_to_search = "C:/Your/Project/Path"
```

The generated cs_file_path.txt will contain the full paths of all relevant .cs files, which will be used as input for the main translation script.

### 2. Comment Translator (comment_translator.py)
The main translation tool that processes the files identified by the CS File Finder.

## Prerequisites
- Python 3.6+
- DeepL API Authentication Key
- Required Python packages:
  ```bash
  pip install deepl
  ```

## Setup
1. Get a DeepL API Authentication Key from [DeepL Developer Portal](https://www.deepl.com/pro-api)
2. Set your AUTH_KEY in the script:
   ```python
   AUTH_KEY = "your-deepl-api-key"
   ```

## Workflow

### Step 1: Find C# Files
1. Run the CS File Finder to generate a list of files:
   ```bash
   python find_cs_file.py > cs_file_path.txt
   ```

### Step 2: Translate Comments
1. Ensure you have set up your DeepL API key
2. Run the translator script:
   ```bash
   python comment_translator.py
   ```

## Supported Comment Types and Examples

### 1. Single-line Comments
```csharp
// Before Translation
// 鸭子在冰面上滑冰
// 熊猫正在竹林里打滚

// After Translation
// Duck is skating on ice
// Panda is rolling in the bamboo forest
```

### 2. Multi-line Comments
```csharp
// Before Translation
/*****************************
 * 小兔子在花园里蹦跳
 * 懒猫在阳光下打盹
 *****************************/

// After Translation
/*****************************
 * Little rabbit is hopping in the garden
 * Lazy cat is napping in the sunshine
 *****************************/
```

### 3. XML Documentation Comments
```csharp
// Before Translation
/// <summary>
/// 松鼠在树上收集松果
/// </summary>
/// <param name="fileDirect">狐狸在追逐自己的尾巴</param>
/// <param name="saveDay">蜜蜂在花丛中跳舞</param>

// After Translation
/// <summary>
/// Squirrel is collecting pinecones in the tree
/// </summary>
/// <param name="fileDirect">Fox is chasing its own tail</param>
/// <param name="saveDay">Bee is dancing among the flowers</param>
```

## Translation Modes

### Replace Mode
Replaces Chinese comments with English translations:
```csharp
// Before
// 小鸟在枝头唱歌

// After
// Little bird is singing on the branch
```

### Append Mode (Default)
Keeps Chinese comments and adds English translations:
```csharp
// Before
// 小狗在追逐自己的影子

// After
// 小狗在追逐自己的影子 Puppy is chasing its own shadow
```

## Configuration
Set `REPLACE_MODE` in the script:
```python
REPLACE_MODE = True  # Replace Chinese with English
REPLACE_MODE = False # Keep Chinese and append English
```

## File Processing
- Supports batch processing of multiple C# files
- Maintains original file structure
- Preserves file encoding (UTF-8)
- Handles various comment styles consistently
- Supports nested and complex comment structures

## Acknowledgments
My first complete Python program developed with the assistance of Claude 3.5 Sonnet (Anthropic). The entire programming and debugging process took less than a day to complete - significantly faster than traditional development would have taken. It's amazing to see how AI assistance can dramatically accelerate the development process while maintaining code quality. Of course, AI wrote this README.md too!

Remember to handle your API key securely and never commit it to version control!
