### Example of full comment
###### // FINDING: STATUS |MAJOR| NAME |Possible commitment to canceled auction|
###### // DESC |If auction canceled, but users deposit more that minimum commitment, then user lose their assets|
###### // REC_TEXT |We recommend add simple check:|
###### // REC_CODE |require(!marketStatus.finalized, "Auction already finalized");|

### Usage
In command line from root directory of project for audit execute:

`python3 ReportGenerator.py <arg1> <arg2>`

where 
- `<arg1>` - name of file for report (example: Report.md)
- `<arg2>` - base path for git repository of project (it would be used for create scope of audit) (example: https://github.com/akropolisio/akropolis/tree/6dd43f4cee728bad1ebaa7d43ecc24aea46fbd7d)

### NOTE
#### 1.
Line with REC_CODE can be empty or can contain several strings.
example:
##### a.
###### // FINDING: STATUS |MAJOR| NAME |Possible commitment to canceled auction|
###### // DESC |If auction canceled, but users deposit more that minimum commitment, then user lose their assets|
###### // REC_TEXT |We recommend check this situation|
##### b.
###### // FINDING: STATUS |MAJOR| NAME |Possible commitment to canceled auction|
###### // DESC |If auction canceled, but users deposit more that minimum commitment, then user lose their assets|
###### // REC_TEXT |We recommend check this situation|
###### // REC_CODE |require(!marketStatus.finalized, "Auction already finalized");|
###### // REC_CODE |require(_addr != address(0), "Incorrect address");|

STATUS, NAME, DESC and REC_TEXT are mandatory fields.

#### 2. 
Several findings can have same name and status. In this case, links to all locations will be added in the description section.

#### 3. 
Possible status: CRITICAL, MAJOR, WARNING, COMMENT.

#### 4. 
If some part of comment are omitted, then for this comment warning message would be printed in console.