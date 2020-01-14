#Union of companies script
##Command line args
\<path to file\> \[, \<path to file\>\]+ -f \<field name with companies names\>
\[-t \<target path to save union.xlsx and mapper.xlsx\>\]
\[-m \<if you have grouping of companies already you can specify here path to excel file\>\]

1. `-f` field name with company names, should be the same in all files (required arg)!!!
2. `-t` folder to save resulting union.xlsx and mapper.xlsx file, below is a paragraph with info about it (optional argument).
3. `-m` path to mapper file (optional argument)

## Requirements on files with companies data
1. Company names are unique (in the scope of one file) and non empty.
2. Field name corresponding to column with companies names must be the smae in all files.
3. No multiindexes in columns
4. Columns names start in the top left cell.

##How to run
I suggest to create virtual environment in directory with project. Activate virtual environment.
Run `pip3 install -e .`. After installing suggest you running test `py.test -v -s integration_test test`. This is performed once. Whenever you want to run script, you activate virtual environment
and run script.

## Mapper dataframe
It looks like this:

| file_name        | company_name           | group_id  |
| :-------------:  |:-------------:         | :-----:   |
| 1.xlsx           | A                      | 0         |
| 2.xlsx           | A, LLC                 | 0         |
| 2.xlsx           | B                      | 1         |

If you don't specify `-m` argument program will make groups and create this file that will be used to extract
rows from files for companies from the same group. You can use this initial mapping to make some corrections and then run script again with `-m` specified.
Rows are sorted by "company_name" column in order to help tou find groups by "hands".

##Result
union.xlsx is resulting dataframe with columns from all files, as [example](./resources/union.xlsx)