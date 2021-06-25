### Example of comment
FINDING: STATUS |MAJOR| NAME |Possible commitment to canceled auction|
DESC |If auction canceled, but users deposit more that minimum commitment, then user lose their assets|
REC_TEXT |We recommend add simple check:|
REC_CODE |require(!marketStatus.finalized, "Auction already finalized");|

### NOTE
#### 1.
Line with REC_CODE can be empty or can contain several strings.
example:
##### a.
FINDING: STATUS |MAJOR| NAME |Possible commitment to canceled auction|
DESC |If auction canceled, but users deposit more that minimum commitment, then user lose their assets|
REC_TEXT |We recommend check this situation|
##### b.
FINDING: STATUS |MAJOR| NAME |Possible commitment to canceled auction|
DESC |If auction canceled, but users deposit more that minimum commitment, then user lose their assets|
REC_TEXT |We recommend check this situation|
REC_CODE |require(!marketStatus.finalized, "Auction already finalized");|
REC_CODE |require(_addr != address(0), "Incorrect address");|

STATUS, NAME, DESC and REC_TEXT are mandatory fields.

#### 2. 
Several findings can have same name and status. In this case, links to all locations will be added in the description section.

#### 3. 
Possible status: CRITICAL, MAJOR, WARNING, COMMENT.
