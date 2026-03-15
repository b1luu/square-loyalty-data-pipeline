from app.client import client


result = client.loyalty.programs.get("main")

if result.errors:
    print(result.errors)
elif result.program is None:
    print("No loyalty program found.")
else:
    print(result.program.id)

