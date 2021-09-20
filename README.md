# club-review
A web application where users can go online and make a pitch within one minute, and other users can review, upvote, downvote, and comment on them

# description
club review is a web application that enables a user to create pitches, in form of posts. Other users can then upvote, downvote or comment on this post so as to give feedback.
To unlock features such as upvoting, downvoting, commenting and even create a pitch, a user requires to have an account.

this web application is developed using the following technologies:
* front-end
    * html
    * css
    * bootstrap
* back-end
    * flask
* database
    * sql

visit live site [here](https://pervez-flask-review.herokuapp.com/)

# bugs and solutions
#### 1. jinja2.exceptions.TemplateRuntimeError: extended multiple times
this bug is caused when you try to extend many template files in a html file
for example:
```
{% extends 'layout.html' %}
{% extends 'base.html' %}
```

to fix this issue, instead of extending one file, you can use __include__ instead
```
{% extends 'layout.html' %}
{% include 'base.html' %}
```

#### 2. Exception: Install 'email_validator' for email validation support.
this error, as for me, occurred when i tried to use Email validator from flask-wtf

```
from wtf.validators import Email
```

an easy fix is just to install email_validator using ```pip install email_validator```

# contributing
As a continously developing web application, we encourage and accept other developers to contribute. 
if you have anything of importance, feel free to email me at pervezismailnagi@gmail.com

# Lincence
this product is MIT lincenced


__all rights reserved copyrights &copy; club review__
