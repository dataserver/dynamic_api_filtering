
# Dynamic create a SQLAlchemy Statement from query string

Inspired by the text :

"How to implement dynamic API filtering using query parameters with Flask-SQLAlchemy"

https://mindee.com/blog/flask-sqlalchemy/


This is my implementation for a personal project without any security concerns. 
All the columns in the table are searchable which is **BAD IDEA** if it is open to 
the public!

## Query string

    api.example.com/collection/?id[between]=1:100&created_at[startswith]=2001&name[ilike]=john

    SQL query:
       SELECT ... WHERE id BETWEEN 1 AND 100
                  AND created_at LIKE '2001%'
                  AND lower(name) LIKE lower('john')

## Example

Check in the main.py for an example

## Query String Parameters

Only the most commonly used operations have been included.


    EQ (equal / default):
        string: column[eq] = 456 ou column = 456
        sql   : column = 456

    NE (not equal):
        string: column[ne] = 456
        sql   : column != 456

    GT (greater than)
        string: column[gt] = 1
        sql   : column > 1

    GTE (equal or greater than)
        string: column[gte] = 1
        sql   : column >= 1

    LT (less than):
        string: column[lt] = 1
        sql   : column < 1

    LTE (equal or less than):
        string: column[lte] = 1
        sql   : column <= 1

    IN:
        string: column[in] = 1,2,3,4  
        sql   : column IN (1,2,3,4)

    NOTIN:
        string: column[notin] = 1,2,3,4  
        sql   : column NOT IN (1,2,3,4)

    BETWEEN
        string: column[between] = 16:18
        sql   : column BETWEEN 16 AND 18

    LIKE
        string: column[like] = ali
        sql   : column LIKE = ali

    ILIKE (the letter I stands for case insenstive)
        string: column[like] = ali
        sql   : lower(column) LIKE lower(ali)

    STARTSWITH, ISTARTSWITH
        string: column[startswith] = ali
        sql   : column LIKE = ali%

    ENDSWITH, IENDSWITH
        string: column[endswith] = ali
        sql   : column LIKE = %ali

    CONTAINS, ICONTAINS
        string: column[contains] = ali
        sql   : column LIKE = %ali%
    
    ISNULL (value is ignored)
        string: column[isnull] = 1
        sql   : column IS NULL

    ISNOTNULL (value is ignored)
        string: column[isnotnull] = 1
        sql   : column IS NOT NULL


## License ##

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.