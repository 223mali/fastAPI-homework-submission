
# TFG Labs Assessment

This project is simple homework submission API. Where students can submit their homework and teachers can grade them

## Get started

**Python** Version= 3.9
**pipenv** version=2022.9.8

### Steps

1. Checkout Project in a new directory

2. open the project in terminal

```
cd api
```
```
pipenv shell
pipenv isntall
```

3. Start the project by running

```
python3 start.py
```





## Endpoints

### Users
#### Create Users: Post(users/user)
This endpoints creates a user. with either Teacher or Student role

##### Inputs

```
{
  "first_name": "test",
  "last_name": "user",
  "password": "12345",
  "email": "derp@mail.com",
  "role": "Teacher"
}
```

#### Expected return
```
{
  "id": 1
  "first_name": "test",
  "last_name": "user",
  "hashed_password": "12345",
  "email": "derp@mail.com",
  "role": "Teacher"
}
```

#### Login: Post(/users/token)

This function authenticates the user

#### Inputs

```
{
    "username": derp@mail.com,
    "password": 1233Password
}
```

#### Expected return

```{
  "access_token": "string",
  "token_type": "string"
}
```

### Assignments

Assignments are contain the requirement of an homework and as such are attached to homework submissions. NB: Assignments can only be created by teachers

#### Create Assignments: Post(/assignments/assignment)

Headers: Authorization: Bearer <JWT token>

#### Inputs

```
{
  "name": "string",
  "description": "string"
}
```
#### Expected return

```
{
  "id": int
  "name": "string",
  "description": "string"
}
```

#### Fetch Assignments: Get(/assignments/)
Fetches all assignments
#### Expected Return 

```
[
    {
        "id": int
        "name": "string",
        "description": "string"
    }
]
```

### homework

#### Upload Homework: Post(homeworks/upload)
this endpoint allows you to upload an attachement file to your homework submission

Headers: Authorization: Bearer <JWT token> content-type: multipar/form-data

#### Create Homework: Post(homeworks/homework)
This endpoint allows students to submit their homeworks.

Headers: Authorization: Bearer <JWT token>

#### Inputs
```
{
  "nassignment_id": "string",
  "file_path": "string",
  "filename": "string"
}
```
#### Expectd return

```
{

    "id": "int"
    "assignment_id":i"nt"
    "homework_name": "string"
    "user_id": "int"
    "student_name": "string"
    "submission_date": "date"
    "grading_date": "date"
    "file_path": "string"
    "finale_grade": "enum grad(A-F, Ungraded, Incomplete)"
    "teacher_notes": "string"
}
```

#### Fetch Homework: Get(homeworks/all)
?name&from_date&to_date&student

#### Filters
```
name = assignment name
from_date = submission from
to_date = submission to
student= student name
```
**Headers**: Authorization: Bearer <JWT token>

This endpoint fetches all homework submissions.

Expected Return

```
[
    {

    "id": "int"
    "assignment_id":i"nt"
    "homework_name": "string"
    "user_id": "int"
    "student_name": "string"
    "submission_date": "date"
    "grading_date": "date"
    "file_path": "string"
    "finale_grade": "enum grad(A-F, Ungraded, Incomplete)"
    "teacher_notes": "string"
    }
]
```

#### Fetch User Homework: Post(homeworks/user/all)
This endpoint allows students to fetch all their submitted homeworks.

**Headers**: Authorization: Bearer <JWT token>

Expected Return

```
[
    {

    "id": "int"
    "assignment_id":i"nt"
    "homework_name": "string"
    "user_id": "int"
    "student_name": "string"
    "submission_date": "date"
    "grading_date": "date"
    "file_path": "string"
    "finale_grade": "enum grad(A-F, Ungraded, Incomplete)"
    "teacher_notes": "string"
    }
]
```

#### Grade Homework: Post(homeworks/homework/grade)
This endpoint allows teachers to grade a submitted homework.
**Headers**: Authorization: Bearer <JWT token>

#### Inputs

```
   {

    "id": "int"
    "assignment_id":i"nt"
    "homework_name": "string"
    "user_id": "int"
    "student_name": "string"
    "submission_date": "date"
    "grading_date": "date"
    "file_path": "string"
    "finale_grade": "enum grad(A-F, Ungraded, Incomplete)"
    "teacher_notes": "string"
    }
```