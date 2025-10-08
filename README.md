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
 
<p align="center">
  <p align="center">
    <a href="https://justdjango.com/?utm_source=github&utm_medium=logo" target="_blank">
      <img src="https://assets.justdjango.com/static/branding/logo.svg" alt="JustDjango" height="72">
    </a>
  </p>
  <p align="center">
    The Definitive Django Learning Platform.
  </p>
</p>

# Getting started with Django

This is the code from the course "Getting Started With Django", found on YouTube and JustDjango

---

## Getting Started

To run this project you will need to set your environment variables.

1. Create a new file named `.env` inside the `djcrm` folder
2. Copy all of the variables inside `djcrm/.template.env` and assign your own values to them
3. Run `export READ_DOT_ENV_FILE=True` inside your terminal so that your environment variables file will be read.

<div align="center">
<i>Other places you can find us:</i><br>

<a href="https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ" target="_blank"><img src="https://img.shields.io/badge/YouTube-%23E4405F.svg?&style=flat-square&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.twitter.com/justdjangocode" target="_blank"><img src="https://img.shields.io/badge/Twitter-%231877F2.svg?&style=flat-square&logo=twitter&logoColor=white" alt="Twitter"></a>

</div>
