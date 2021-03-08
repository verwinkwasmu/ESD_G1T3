from invokes import invoke_http
from os import environ

# getting the url from the environment, if not get from an input
book_URL = environ.get('bookURL') or input("Enter Book service URL: ")  


# invoke book microservice to get all books
results = invoke_http(book_URL, method='GET')

print( type(results) )
print()
print(results)

# invoke book microservice to create a book
isbn = '9213213213213'
book_details = { "availability": 5, "price": 213.00, "title": "ESD" }
create_results = invoke_http(
        book_URL + "/" + isbn, method='POST', 
        json=book_details
)

print()
print( create_results )
