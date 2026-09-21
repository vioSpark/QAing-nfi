
# Broader Context

[[Liam]] have forwarded me an assignment from [[Nearfield]] over [email](https://mail.google.com/mail/u/0/#inbox/FMfcgzQhWTvgMNhQHtTvhRTXBWflxtMM).
Main entry point is: [[Assignments_QA_Engineer.docx]]

The assignment has two parts: 
* [[Create a system test plan]]
* [[Create a test automation script]]
## Stack to use
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