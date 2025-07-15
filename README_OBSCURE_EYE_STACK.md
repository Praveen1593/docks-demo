# Obscure Eye Full Stack Scaffold

This project contains a FastAPI backend, a React web dashboard, and a Flutter mobile app for the Obscure Eye AI system.

---

## 1. Backend (FastAPI)

**Location:** `backend/`

### Install dependencies:
```
pip install fastapi uvicorn python-jose[cryptography] fastapi[all] pydantic
```

### Run the backend:
```
uvicorn main:app --reload --port 8000
```

---

## 2. Web Dashboard (React)

**Location:** `frontend/obscure-eye-dashboard/`

### Install dependencies:
```
npm install
```

### Run the dashboard:
```
npm start
```

The dashboard will be available at [http://localhost:3000](http://localhost:3000)

---

## 3. Flutter Mobile App

**Location:** `obscure_eye_app/`

### Install dependencies:
```
flutter pub get
```

### Run the app:
```
flutter run
```

- Use `10.0.2.2` for the backend URL on Android emulator.
- For iOS or real devices, use your machine's IP address.

---

## 4. Notes
- The backend uses mock data for alerts and video stream.
- Replace the mock endpoints with your real AI backend when ready.
- Expand the apps with authentication, settings, and more features as needed.