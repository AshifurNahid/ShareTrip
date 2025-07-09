
# ShareTrip - Travel Booking Platform 🌍

A full-stack travel booking application built with Django, Django REST Framework. Users can register, browse trips, book travel packages, and manage their profiles. Admins and trip creators can manage trips, bookings, and users.

## 🚀 Features

- User registration & login (with password confirmation)
- Custom user model with profile info (bio, avatar, phone, DOB)
- Trip creation, update, and listing (CRUD)
- Trip image gallery (upload multiple images)
- Booking system with participant count, price calculation
- Booking status updates (pending, confirmed, cancelled)
- Admin panel for managing all data
- API-first backend with DRF
- CORS support for React frontend integration

## 🛠️ Tech Stack

**Backend:**
- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite/PostgreSQL (configurable)
- Pillow (image uploads)
- django-cors-headers





## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/AshifurNahid/ShareTrip.git
   
   ```

2. Create virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Create superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the server:

   ```bash
   python manage.py runserver
   ```

7. Access API at: `http://127.0.0.1:8000/api/`

## 📮 API Endpoints (Examples)

| URL                          | Method | Description            |
| ---------------------------- | ------ | ---------------------- |
| `/api/users/register/`       | POST   | Register new user      |
| `/api/trips/create/`         | POST   | Create a trip          |
| `/api/bookings/create/`      | POST   | Book a trip            |
| `/api/bookings/my-bookings/` | GET    | View user’s bookings   |
| `/api/bookings/<id>/cancel/` | POST   | Cancel a booking       |
| `/admin/`                    | GET    | Django admin dashboard |

## 📷 Trip Gallery (Media)

* Trip images are uploaded to `media/trips/`
* User avatars go to `media/avatars/`

## 📌 Todo (Optional Improvements)

* JWT authentication
* Trip reviews & ratings
* Notifications system
* Payment gateway integration



---

Happy Coding ✈️🌍


