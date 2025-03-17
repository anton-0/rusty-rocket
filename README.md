

## Run app
``` {bash}
make start
```
Swagger UI should be available at `localhost:8000/docs`.

## Example usage

### Add a book

``` {bash}
curl --location --request POST 'localhost:8000/books' --header 'Content-Type: application/json' --data-raw \
'{
    "id": "001122",
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee"
}'
```

### Add a user

``` {bash}
curl --location --request POST 'localhost:8000/users' --header 'Content-Type: application/json' --data-raw \
'{
    "id": "112233",
    "name": "Anthony"
}'
```

### Get all books

``` {bash}
curl --location --request GET 'localhost:8000/books'
```

### Get details of a book

``` {bash}
curl --location --request GET 'localhost:8000/books/001122'
```


### Mark book as rented

``` {bash}
curl --location --request PUT 'localhost:8000/books/001122/rental/112233'
```

### Mark book as returned

``` {bash}
curl --location --request PUT 'localhost:8000/books/001122/return'
```

### Delete a book
``` {bash}
curl --location --request DELETE 'localhost:8000/books/001123'
```
