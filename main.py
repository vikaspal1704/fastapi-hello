from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

def verify_firebase_token(authorization: str = Header(...)) -> str:
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    res = requests.post(url, json={"idToken": authorization})
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
    return res.json()["users"][0]["localId"]

@app.post("/profile")
@app.post("/profile")
def create_profile(data: dict, uid: str = Depends(verify_firebase_token)):
    name = data.get("name")
    email = data.get("email")

    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/profiles",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        },
        json={"uid": uid, "name": name, "email": email}
    )

    if res.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail="Supabase create error")

    return {"message": "Profile created"}

@app.get("/profile")
def get_profile(uid: str = Depends(verify_firebase_token)):
     

    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/profiles?uid=eq.{uid}",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}"
        },
    )

    if res.status_code != 200 or not res.json():
        raise HTTPException(status_code=404, detail="Profile not found")

    return res.json()[0]

@app.put("/profile")
def update_profile(data: dict, uid: str = Depends(verify_firebase_token)):
     

    res = requests.patch(
        f"{SUPABASE_URL}/rest/v1/profiles?uid=eq.{uid}",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        },
        json=data
    )

    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="Supabase update error")

    return res.json()[0]
@app.delete("/profile")
def delete_profile(uid: str = Depends(verify_firebase_token)):
     

    res = requests.delete(
        f"{SUPABASE_URL}/rest/v1/profiles?uid=eq.{uid}",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}"
        },
    )

    if res.status_code != 204:
        raise HTTPException(status_code=500, detail="Supabase delete error")

    return {"message": "Profile deleted"}
