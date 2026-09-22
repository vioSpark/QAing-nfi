
This repo was created for sharing my solution to the assignment from Nearfield Instruments. 

The assignment in explained in: [Assignments_QA_Engineer.docx](Nearfield%20Instruments%20Assignment_Software_Test_Engineer/Assignment_QA_Engineer/Assignment_QA_Engineer/Assignments_QA_Engineer.docx), and the attached two examples file. It consists of two parts, that are mirrored in this repository: 
* [Create a system test plan](./Create%20a%20system%20test%20plan/Create%20a%20system%20test%20plan.md)
* [Create a test automation script for robot arm movement verification](./Create%20automated%20test/Create%20a%20test%20automation%20script%20for%20robot%20arm%20movement%20verification.md)

These files contain the solution for the two parts repsectively.
## Initial consideration before going into the details
* System test plan
	* First thought is in Jira & Xray, but that's near impossible to share. Therefore it'll need to be constructed directly in md/csv files, something that is 'ready to import'. 
	* Markdown files for descriptions --> Obsidian for a more WYSWYG experience.
	* Csv files for import-ready stuff.
* Test automation script
	* Javascript is a no-no for me
	* Python probably due to token density
		* A very nice follow-up question would be to migrate all to robot framework after stakeholder alignment
	* C# -> I'd love the type-safety & linter. That'll have to be sacrificed. Not a 1:1 replacement, but python type annotations are a good stop-gap measure, especially for enabling the linter to be better
	* VsCode, because that's already installed. 
	* Dependency mgmt: On my wsl it seems that I still have a docker installed -> this gets a container ideally. At least a requirements.txt
* Strategy: "The old Esettan style, with George's spin active": clear the core deliverables, plus add support and scaffolding until it resembles a self-contained project/business capability (so no matrix-org reliance. Adapting to that here:
	* The only prereq here is clockify
	* Core functionality: Obsidian & python
	* Docker container

