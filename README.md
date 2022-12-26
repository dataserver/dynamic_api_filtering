
# Dynamic create a SQLAlchemy Statement from query string


## Query string

    api.example.com/coollection/?id[between]=1:100&created_at[startswith]=2001&name[ilike]=john

    SQL query:
       SELECT ... WHERE id BETWEEN 1 AND 100
                  AND created_at LIKE '2001%'
                  AND lower(name) LIKE lower('john')

## Example

Check in the main.py for an example of output.

## Query String Parameters

    EQ (equal / default):
        string: variable[eq] = 456 ou variable = 456
        sql   : variable = 456

    NE (not equal):
        string: variable[ne] = 456
        sql   : variable != 456

    GT (greater than)
        string: variable[gt] = 1
        sql   : variable > 1

    GTE (equal or greater than)
        string: variable[gte] = 1
        sql   : variable >= 1

    LT (less than):
        string: variable[lt] = 1
        sql   : variable < 1

    LTE (equal or less than):
        string: variable[lte] = 1
        sql   : variable <= 1

    IN:
        string: variable[in] = 1,2,3,4  
        sql   : IN (1,2,3,4)

    NOTIN:
        string: variable[notin] = 1,2,3,4  
        sql   : NOT IN (1,2,3,4)

    BETWEEN
        string: variable[between] = 16:18
        sql   : BETWEEN 16 AND 18

    LIKE
        string: variable[like] = ali
        sql   : variable LIKE = ali

    ILIKE (the letter I stands for case insenstive)
        string: variable[like] = ali
        sql   : lower(variable) LIKE lower(ali)

    STARTSWITH, ISTARTSWITH
        string: variable[startswith] = ali
        sql   : variable LIKE = ali%

    ENDSWITH, IENDSWITH
        string: variable[endswith] = ali
        sql   : variable LIKE = %ali

    CONTAINS, ICONTAINS
        string: variable[contains] = ali
        sql   : variable LIKE = %ali%
    
    ISNULL (value is ignored)
        string: variable[isnull] = 1
        sql   : variable IS NULL

    ISNOTNULL (value is ignored)
        string: variable[isnotnull] = 1
        sql   : variable IS NOT NULL


## License ##

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.