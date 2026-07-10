from services.auth_service import authenticate

print("=" * 50)

user = authenticate(
    "admin",
    "admin123"
)

if user:

    print("LOGIN SUCCESS")

    print(user)

else:

    print("LOGIN FAIL")