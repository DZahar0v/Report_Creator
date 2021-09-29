### Example of full comment
###### // FINDING: STATUS |MAJOR| NAME |Possible commitment to canceled auction|
###### // DESC |If auction canceled, but users deposit more that minimum commitment, then user lose their assets|
###### // REC_TEXT |We recommend add simple check:|
###### // REC_CODE |require(!marketStatus.finalized, "Auction already finalized");|

### Usage
In command line from root directory of project for audit execute:

`python3 ReportGenerator.py`

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

#### 5.
To specify output file name, base path to directory of project on github and contracts which must be included in scope, see `ReportConfig.json`.