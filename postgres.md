
## regex

### simple lazy eval doesn't work

```sql
-- match to first underscore, then capture the rest
'.*?_(.*)' -- typical regex lazy evalutation doesn't work
'(?<=_).*' -- positive lookbehind surprisingly does
```

### matching in select

- regexp_match
    - returns the matches as a text array column
    - won't filter results
- regexp_matches
    - returns the matches as rows
    - **will** filter results

## array to string

- array_to_string
    - performs a concat/string join with a delimiter
    - won't filter results
- unnest
    - joins the array into a string with no delimter
    - **will** filter results

```sql
```