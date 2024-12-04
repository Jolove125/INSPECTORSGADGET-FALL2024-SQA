# PROJECT REPORT
## Objective
The main goal of this project is to build a GitHub repository and utilize the tools and knowledge gained from the workshop activities in class.

## Introduction
The first step was to unpack the provided zip compressed folder `MLForensics.zip` and upload it to our GitHub repository titled INSPECTORSGADGET-FALL2024-SQA. Then, each team member was tasked with completing the following software quality assurance activities:  
* Create a Git Hook that will run and report all security weaknesses in the project in a CSV file whenever a Python file is changed and committed.  
* Create a `fuzz.py` file that will automatically fuzz 5 Python methods. Any bug detection should be automatically executed and reported from GitHub Actions.  
* Integrate forensics into the repository by modifying 5 Python methods.  
* Implementing continuous integration with GitHub Actions.  

## Activities Performed
### A. Git Hook 

Git hooks are scripts that are automatically run by Git either before or after specific actions, such as merging, pushing, or committing. They let you automate tasks and modify Git's behavior.

One particular kind of Git hook that operates before creating a commit is called a pre-commit hook. Code formatting, linting, testing, secret checking, and preventing unintentional disclosures of sensitive data are just a few of the activities pre-commit can check for. 

**1. Static Analysis Tool Selection**  

Since this task requires Python files to be scanned for vulnerabilities, we chose Bandit as my static analysis tool to integrate into the pre-commit file. Bandit was created to identify common security flaws in Python code. Each file is processed by Bandit, which then creates an AST from it and applies the relevant plugins to the AST nodes. Bandit creates a report after every file is scanned.

**2. Modification of `pre-commit` file**  

To create a git hook that will run whenever an altered Python file is committed. We must create a pre-commit file and add it to the `.git/hook` folder. These are the following steps taken:
1. **Clone Repository:** Clone the repository to a local machine.
2. **Copy `pre-commit.sample`:** GitHub provides a sample `pre-commit` file in the `.git/hook` folder. Once the .sample extension is removed the `pre-commit` file will be activated. A copy was made and activated, and then we modified the code.
3. **Check for Python Modifications:** Use the If statement to check if the file changed and committed was a Python file; if true, run the Bandit tool.
   ```sh
   if git diff --cached --name-only | grep '\.py$' > /dev/null; then
   ```
4. **Insert Bandit Command:** Then add the command to run the Bandit tool using the flag `-r` with the `-f` and `-o` flags to output the results to our desired file format and file name.
    ```sh
   bandit -r . -f csv -o security_weakness.csv
   ```
5. **Vulnerabilities Detection Alert And Results Location:** Once security vulnerabilities are found, inform the user about the security weakness and inform them of the filename of the results.
   ```sh
   if [ -s security_weakness.csv ]; then
		echo "Security issues found. See security_weakness.csv"
   ```
**3. Testing Implementation**  

We tested the modification by making minor changes to constant.py and committing it. The Bandit tools were executed every time a Python file was changed and was going to be committed. This tool scans all Python files in the repository. A CSV file titled `security-weakness.csv` is generated and reports any security weaknesses detected from the scan. A notification shows us that vulnerabilities were detected and that the result was located in the file named `security-weakness.csv`.

**`pre-commit` Execution Screenshot:** 

![alt text](https://github.com/Jolove125/INSPECTORSGADGET-FALL2024-SQA/blob/main/Hook_Results/Bandit_SA%20Screenshot.jpg?raw=true) 

**Vulnerabilites Detection Results:**  

[security-weakness.csv](https://github.com/Jolove125/INSPECTORSGADGET-FALL2024-SQA/blob/main/Hook_Results/security_weakness.csv)

**4. Key Learnings**

* **Different Static Analysis Tools:** Research the different static analysis tools attributes that can be utilized in our pre-commit.
* **Git Command and GitHub:** Research and learning more about git commands and GitHub
* **Workshops:** Learning that the activities introduced to us in `Workshop 6: Security Weakness Identification with Automation` could be applied/combined with the lab activities we executed in `Workshop 8: Event-driven Static Analysis with Git Hooks`.

### B. Automated Fuzz Testing for Python Methods  
Fuzz testing, or [fuzzing](https://en.wikipedia.org/wiki/Fuzzing), is an automated technique that feeds random or unexpected inputs to
software functions to identify potential bugs and vulnerabilities. In this project, we developed an
automated fuzzing framework targeting five specific Python methods.  

**1. Method Selection**  

We selected the following five methods for fuzzing based on their diverse functionalities and
potential of finding edge cases that would trigger a bug or vulnerability:
1. `makeChunks(the_list, size_)`: Divides a list into chunks of a specified size.
2. `checkIfParsablePython(pyFile)`: Checks if a Python file can be parsed without
syntax errors.
3. `getPythonAtrributeFuncs(pyTree)`: Extracts attribute function calls from an AST
tree.
4. `getLogStatements(pyFile)`: Identifies logging statements within a Python file.
5. `Average(Mylist)`: Calculates the average of a list of numbers.

**2. Implementation of `fuzz.py`**
   
**2.1 Fuzzing Strategy**  
For each target method, we generated a wide range of inputs, including valid data, invalid types,
boundary cases, and malformed structures so we can simulate real-world scenarios and
uncover unexpected behaviors or crashes.

**2.2. Fuzzing Functions**

* **Input Generation:** uses helper functions to create random strings, filenames, lists, and
AST trees with varying types.
* **Method Invocation:** Each fuzzing function invoked the target method with the generated
inputs catching outputs.
* **Logging:** We used Python’s `logging` module to record all test cases, results, and any
exceptions in a `fuzz_report.log` file.
* **Cleanup:** We implemented mechanisms to remove any temporary files or directories
created during testing to maintain a clean environment.

**2.3. GitHub Actions Integration**

To automate the fuzzing process, we integrated `fuzz.py` with GitHub Actions. The workflow
was configured to trigger on code pushes to the `main` branch, pull requests targeting main, and
daily schedules. The workflow steps included:
1. **Checkout Repository:** Cloned the repository.
2. **Set Up Python:** Installed the specified Python version.
3. **Install Dependencies:** Installed required packages from `requirements.txt`.
4. **Run Fuzzing Script:** Executed `fuzz.py`.
5. **Upload Fuzz Report:** Uploaded the `fuzz_report.log` for review.
The integration is done so the fuzzer can provide continuous feedback on code changes.

**3. Key Learnings**

* **Input Coverage:** Generating diverse and edge-case inputs was an important measure
for effective fuzzing, which improves hidden bug discovery. We noticed that the quality of
the generated fuzzing data relies on many factors, but one important factor is mutation.
* **Logging:** logs help with identifying issues uncovered during testing. More logging means
uncovering hidden functionalities.
* **Integration:** Integrating fuzzing with CI tools like GitHub Actions helps timely testing,
and ensures that software quality is always checked on every commit.
* **Clean up:** fuzzing ends up generating tons of logs, so implementing cleanup procedures
helps prevent clutter and maintain a stable testing environment.


**C. Integrated Forensics**
Logging is a crucial part of modern software development, enabling developers to monitor, debug, and maintain applications efficiently. In this project, we implemented logging functionality across key Python methods to enhance transparency, traceability, and debugging capabilities.

**1. Motivation for Adding Logging** 
The integration of logging aimed to address several operational challenges and improve the overall maintainability of the FameML framework. Key motivations included:

Enhanced Debugging: Logging captures detailed information about runtime errors, enabling quicker diagnosis and resolution of issues.
Execution Traceability: With logs, developers can track how input data flows through the system and identify bottlenecks or anomalies in processing.
Audit and Compliance: Logs provide a historical record of operations, supporting transparency and accountability.
Error Recovery: Capturing critical errors in logs ensures they are not overlooked, facilitating smoother recovery and resilience.

**2.Forensics Implementation Details**
2.1. Logger Integration
We used the myLogger module to centralize and standardize logging. A helper function, giveMeLoggingObject(), creates a logger object with consistent formatting and output. The logger records messages at levels such as INFO and ERROR.

2.2. Areas of Integration
Logging functionality was integrated across key modules and methods, ensuring comprehensive coverage:

giveTimeStamp(): Logs each timestamp generated, providing a consistent record of key events.
getCSVData(dic_, dir_repo): Logs details about script analysis, including the number of events identified and aggregated into CSV data.
getAllPythonFilesinRepo(path2dir): Logs the discovery and validation of Python files within a repository.
runFameML(inp_dir, csv_fil): Logs the overall execution process, including subfolder processing and CSV generation.
2.3. Key Logging Points
Start and Completion Logs: Logs are generated at the start and end of significant operations to mark milestones.
Input and Output Logging: Inputs, intermediate results, and outputs are logged for traceability.
Error Handling: Errors, such as issues with saving CSV files, are logged to ensure they are visible and can be addressed promptly.

**Key Learnings**
Log Granularity: The level of detail in logs needs to strike a balance between providing enough information and avoiding excessive verbosity.
Standardized Format: A consistent log format improves readability and facilitates integration with external monitoring tools.
Performance Considerations: Excessive logging in performance-critical paths can lead to bottlenecks, highlighting the need for selective logging.

**D. Continuous Integration with GitHub Actions**  

Continuous integration (CI) is a software practice that involves frequently committing code to a shared repository, detecting errors and reducing debugging time. It also simplifies merging changes, saving developers time. Continuous builds and tests ensure the code doesn't introduce errors, using code linters, security checks, and functional tests. CI requires a server for local builds and testing.  

GitHub Actions provides CI workflows for building code in one's repository and running tests. These workflows can be configured to run when a GitHub event occurs, on a set schedule, or when an external event occurs. GitHub runs CI tests and provides results in pull requests, allowing the user to review changes or merge them. When setting up CI in a repository, GitHub analyzes the code and recommends workflows based on the language and framework. GitHub Actions can also be used to create workflows across the entire software development life cycle.

**1. Tool Selection**
   
For continuous integration with GitHub Actions, we will need a tool that automatically runs when a push or pull is committed. It was decided to use the Codacy Analysis CLI tool as a continuous integration tool for this project. Codacy analyzes over 40 different programming languages, including Python. That suits this project because Python is the only high-level programming language utilized in this repository. 

**2. Integration of Codacy Analysis CLI in GitHub Actions**

In order to integrate this tool into GitHub Actions, we followed these steps:
1. **Create `YAML` file:** Per the developers' [instructions](https://github.com/marketplace/actions/codacy-analysis-cli), a `.yaml` file tile codacy-analysisas as created containing the default setting configuration that was given. 
2. **`.github/workflow`**: Next we created a `.github/workflow` path and placed the `.yaml` file in the subfolder.
3. **Run the Workflow:** We tested the workflow by pushing a committed file to the repository.

The worflow ran successfully and generated a report of error that were detected during the scan.

**3. Key Learnings**   

* **Runtime:** Codacy generates a report everytime a push is made this tools is run accurately with no error or failure message.

## Team Assignments
|SQA Activity    | Team Member |
|    :---         |     :---:      |          
| 5 (a) Create a Git Hook that will run and report all security weaknesses in the project in a CSV file whenever a Python file is changed and committed.    |   Latasha Glover   | 
| 5 (b) Create a fuzz.py file that will automatically fuzz 5 Python methods of your choice. Report any bugs you discovered by the fuzz.py file. fuzz.py will be automatically executed from GitHub actions.      | Alaeddin Almubayed          | 
| 5 (c) Integrate forensics by modifying 5 Python methods of your choice.     | Troy Carson |
| 5 (d) Integrate continuous integration with GitHub Actions.      |Latasha Glover |
|Report|Latasha Glover, Alaeddin Almubayed, Troy Carson|
