# A Simple CRUD application in Django with authentication
Initial steps in short,
1. Create a django project,
2. Create an application named account 
3. configure settings file

Now from project root directory, where manage.py file is,

do migrations on DB, via 

To check whether there are any changes'
```
python manage.py makemigrations --dry-run
```
To prepare for migrations,
```
python manage.py makemigrations
```
To check the unapplied migrations
```
python manage.py showmigrations
```
To apply the change/modifications,
```
python manage.py migrate
```
Create a super user via 
```
python manage.py createsuperuser
```
Run server via 
```
python manage.py runserver <port-number>  # here i Have used port number 8001
```
Login to admin portal by visiting 
```
http://localhost:8001/admin
```

Phone number is replaced with *** due to privacy reason, you will get actual values in it.
Login via API, 
```
http://localhost:8001/api/v1/login
Method: POST
Request:
{
    "phone": "<phone-number>",
    "password": "<password>"
}

Response:
{
    "message": "Logged in Successfully",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMzMDcyMzI4LCJqdGkiOiI1YjM2NGFkMGFlZjA0MzA5OGNlMTIxYTE4NzNiNjZkZiIsInVzZXJfaWQiOiIzNTc3M2QwZC1jZTlhLTQ1YTQtYjI5Yi04Yjk1OTgwY2RmYTAifQ.0ELPM6eHzrFxSIpt3VzJFIb1MuAnXITIX4-jsL-AEz0",
    "phone": "******"
}
```


Create an User via http://localhost:8001/api/v1/account/users/
```
Request Method: POST
Request Payload:
{
    "phone": "9922558844",
    "first_name": "Test",
    "last_name": "Name",
    "is_active": true,
    "mode": "A",
    "address_line1": "a1",
    "address_line2": "a2",
    "city": "Chennai",
    "postal_code": "600091",
    "state": null,
    "country": null,
    "role": null
}

Response:
{
    "id": "a24f611d-d936-4261-a683-92992a00fea2",
    "phone": "****",
    "first_name": "Test",
    "last_name": "Name",
    "is_active": true,
    "mode": "A",
    "address_line1": "a1",
    "address_line2": "a2",
    "city": "Chennai",
    "postal_code": "600091",
    "state": null,
    "country": null,
    "role": null
}

```

Get all User by visiting http://localhost:8001/api/v1/account/users
```
Request Method: GET
Response:
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "0ab7267d-e9cf-45e9-afa3-6d6f96ca3d1a",
            "phone": "*****",
            "first_name": "k",
            "last_name": "seven",
            "is_active": true,
            "mode": "D",
            "address_line1": "a1",
            "address_line2": "a2",
            "city": "Chennai",
            "postal_code": "695415",
            "state": "3075da59-9ee3-4942-9d9d-7a916021be34",
            "country": "49251796-2fde-4cc2-bf3a-f6268705b50b",
            "role": null
        },
        {
            "id": "1044328e-f525-48a5-a0cb-b3c32eba3f07",
            "phone": "******",
            "first_name": "karthik",
            "last_name": "indh",
            "is_active": true,
            "mode": "D",
            "address_line1": "",
            "address_line2": "",
            "city": "",
            "postal_code": "",
            "state": "78143a75-7cc3-45a5-9126-a9c9047c72de",
            "country": "49251796-2fde-4cc2-bf3a-f6268705b50b",
            "role": "ffbde77b-5a4b-4308-8e9a-879c246b7f99"
        },
        {
            "id": "35773d0d-ce9a-45a4-b29b-8b95980cdfa0",
            "phone": "********",
            "first_name": "karthik",
            "last_name": "super admin",
            "is_active": true,
            "mode": "A",
            "address_line1": "",
            "address_line2": "",
            "city": "",
            "postal_code": "",
            "state": "58aef1bd-8cf4-48a2-b52a-791dbf1311b1",
            "country": "9958cfa8-7f73-4654-be78-6d76edfc3431",
            "role": "02443506-924c-4511-b7fb-248686532a83"
        },
        {
            "id": "b9168ae5-48dc-432f-b35c-34dfe5df1a03",
            "phone": "********",
            "first_name": "praveen",
            "last_name": "s",
            "is_active": true,
            "mode": "T",
            "address_line1": "",
            "address_line2": "",
            "city": "",
            "postal_code": "",
            "state": null,
            "country": "2fe0af1f-b784-436e-ac7b-dd58473829be",
            "role": "02443506-924c-4511-b7fb-248686532a83"
        }
    ]
}
```
Get individual user via http://localhost:8001/api/v1/account/users/<user-uuid>
```
Method: GET
Response:
{
    "id": "a24f611d-d936-4261-a683-92992a00fea2",
    "phone": "****",
    "first_name": "Test",
    "last_name": "Name",
    "is_active": true,
    "mode": "A",
    "address_line1": "a1",
    "address_line2": "a2",
    "city": "Chennai",
    "postal_code": "600091",
    "state": null,
    "country": null,
    "role": null
}
```
Update an user via http://localhost:8001/api/v1/account/users/<user-uuid>
```
Method: PUT
Request:
{
    "phone": "****",
    "first_name": "Test",
    "last_name": "user",
    "is_active": true,
    "mode": "A",
    "address_line1": "a1",
    "address_line2": "a2",
    "city": "Chennai",
    "postal_code": "600091",
    "state": null,
    "country": null,
    "role": null
}

Response:
{
    "id": "a24f611d-d936-4261-a683-92992a00fea2",
    "phone": "****",
    "first_name": "Test",
    "last_name": "user",
    "is_active": true,
    "mode": "A",
    "address_line1": "a1",
    "address_line2": "a2",
    "city": "Chennai",
    "postal_code": "600091",
    "state": null,
    "country": null,
    "role": null
}
```
Delete an user object, here we have implemented soft delete.
delete via http://localhost:8001/api/v1/account/users/<user-uuid>
```
Method: DELETE
Response: No content 204
```