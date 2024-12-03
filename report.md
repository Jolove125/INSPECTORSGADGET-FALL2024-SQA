## PROJECT REPORT
## Objective
The main goal of this project is to build a GitHub repository and utilize the tools and knowledge gained from the workshop activities in class.
## Introduction
The first step was to unpack the provided zip compressed folder `MLForensics.zip` and upload it to our GitHub repository titled INSPECTORSGADGET-FALL2024-SQA. Then, each team member was tasked with completing the following software quality assurance activities:  
* Create a Git Hook that will run and report all security weaknesses in the project in a CSV file whenever a Python file is changed and committed.  
* Create a fuzz.py file that will automatically fuzz 5 Python methods. Any bug detection should be automatically executed and reported from GitHub Actions.  
* Integrate forensics into the repository by modifying 5 Python methods.  
* Implementing continuous integration with GitHub Actions.  

## Activities Performed
**A. Git Hook**  
To create a git hook that will run whenever a change Python file is committed. I must modify the pre-commit file, which is located in the `.git/hook` folder. Pre-commit maintains the repository’s quality by running checks before each commit. Since this task requires Python files to be scanned for vulnerabilities, I chose Bandit as my static analysis tool to integrate into the pre-commit file.   
The first step taken was to clone the repository to my local machine. Once cloned, I inserted code that would execute the bandit tool every time a Python file was changed and was going to be committed. This tool scans all Python files in the repository and reports any security weaknesses in a CSV file titled `weaknesses.csv`. When the user commits a Python file, a notification will instruct them that vulnerabilities were detected and that they should look for the `weaknesses.csv` file to see the results. I tested my implementation by making minor changes to constant.py and committing it. The tool worked, and my work was recorded.

**Lesson Learned:**  
When researching different tools to use in my pre-commit, I learned that a multitude of tools could be used for this task. Still, Bandit seemed like a good fit, especially since it was designed for scanning Python files, and many feel it is effective.

**B. Fuzz Testing**  
<Placeholder>  

**Lesson Learned:**
<Placeholder>

**C. Integrated Forensics**
<Placeholder>

**Lesson Learned:**
<Placeholder>

**D. Continuous Integration GitHub Actions**  
For Continuous integration with GitHub Actions, we will need a tool that automatically runs when a push or pull is committed. I decided to use the Codacy Analysis CLI tool as a continuous integration tool for this project. Codacy analyzes over 40 different programming languages, including Python. That suits this project because Python is the only high-level programming language utilized in this repository.  In order to integrate this tool into GitHub Actions, I followed the developers' instructions. I created a `.yaml` file containing the default setting configuration that was given. Then I place the file in `.github/workflow` and test the workflow by pushing a committed file to the repository. The run was a success and documented.  

## Team Assignments
|SQA Activity    | Team Member |
|    :---         |     :---:      |          
| 5 (a) Create a Git Hook that will run and report all security weaknesses in the project in a CSV file whenever a Python file is changed and committed.    |   Latasha Glover   | 
| 5 (b) Create a fuzz.py file that will automatically fuzz 5 Python methods of your choice. Report any bugs you discovered by the fuzz.py file. fuzz.py will be automatically executed from GitHub actions.      | Alaeddin Almubayed          | 
| 5 (c) Integrate forensics by modifying 5 Python methods of your choice.     | Troy Carson |
| 5 (d) Integrate continuous integration with GitHub Actions.      |Latasha Glover |
|Report|Latasha Glover, Alaeddin Almubayed, Troy Carson|
