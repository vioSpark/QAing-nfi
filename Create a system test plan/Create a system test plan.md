
RAID log:
* 09/21 16:40 - Risk: There are now two set of features with the assignment linking both the pdf, then giving specs below.
	* Decided to treat the pdf as example, and the word-doc specs as authoritative in case there's a disagreement. 
	* 17:03 - revisited this point, implications are better understood: There are indeed differences here, mostly scope-wise the word-doc doesn't include power consumption ("electrical"), standards/compliance ("listings"), and "security dealer features" related features. This seems scoping-only, therefore I didn't amend this decision, the word doc is still authoritative.
* 09/21 16:50 - Decision: There are quite many features, that warrant an intermediate level of abstraction. These are going to supply the basis of our test suites (so in that case the test plan will be: execute the following test-suites)
* 09/21 16:57 - Issue: There are no id-s for the VISTA-20P requirements. I (MarkL) have decided that I need to have requirement id-s, so we can do traceability. No time to do fancy things with the id-s, so I'll just number them in a 01-99 style.
	* Delegated off to AI with reminder to "The final set should be jira-importable"
	* [[VISTA-Requirements-with-id.csv]]





# Defined test suites

_Intermediate abstraction level_:

Already two parts given by the specs:
* "**Features/system functions:**"
* "**Valuable End-User Features/functions:**"

There's one more, that almost certainly will get asked for, the "fast-mode", aka scope-cut, aka smoke-test set. These shall contain the test for the most important features only.









