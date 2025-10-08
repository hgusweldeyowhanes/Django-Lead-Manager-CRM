# Django Lead Manager CRM

A simple and efficient Customer Relationship Management (CRM) system built with Django.
It allows agents to manage leads — add, update, assign, and track progress — through an easy-to-use web interface.
##  Features
 **User Authentication** — Register, login, and logout

 **Lead Management** — Create, update, and delete leads

 **Agent Assignment** — Assign leads to agents

 **Dashboard View** — View all leads and filter by agent

 **Role-Based Access** — Separate permissions for admin and agent users
## Project Structure
### DjangoCRM/
```bash
├── DjangoCRM/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── agents/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── leads/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/
├── db.sqlite3
├── manage.py
└── README.md
```

## Future Improvements

 Email notifications for lead updates

 API endpoints using Django REST Framework

 Lead analytics and reporting
 
 Docker and production deployment setup
 