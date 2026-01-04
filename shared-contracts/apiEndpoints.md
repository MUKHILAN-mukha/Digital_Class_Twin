# Backend API Endpoints

## Authentication
POST /auth/login  
POST /auth/signup  

## Profile
GET /profile/me  

## Events
POST /events  

## Digital Twins
GET /twins/self  
GET /twins/child/{child_id}  
GET /twins/class/{class}/{section}  
GET /twins/all  

## Notes
- All endpoints require JWT except login/signup
- Role-based access enforced at backend
- Backend must not compute scores or risk (ML responsibility)
