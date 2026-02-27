"""
Seed the users table from the PARENTS, CHARGE_PARENTS, and ADMIN lists.

Run with:
    uv run python seed.py

Rules:
  - Every entry in PARENTS      → is_parent=True
  - Every entry in CHARGE_PARENTS → is_charge_parent=True
  - Elizabeth Blevins, Jason Schatz, Chelsea Royaltea → is_admin=True
  - A user in both PARENTS and CHARGE_PARENTS gets both flags True
  - Existing rows are upserted (flags are refreshed on re-run)
"""

from app import ADMIN, CHARGE_PARENTS, PARENTS, User, app, db

ADMIN_EMAILS = {u["email"] for u in ADMIN}

with app.app_context():
    # Build a merged dict keyed by email
    users: dict[str, dict] = {}

    for p in PARENTS:
        entry = users.setdefault(
            p["email"],
            {"email": p["email"], "name": p["name"], "is_parent": False, "is_charge_parent": False, "is_admin": False},
        )
        entry["is_parent"] = True

    for p in CHARGE_PARENTS:
        entry = users.setdefault(
            p["email"],
            {"email": p["email"], "name": p["name"], "is_parent": False, "is_charge_parent": False, "is_admin": False},
        )
        entry["is_charge_parent"] = True

    # Admin users may not appear in PARENTS or CHARGE_PARENTS (e.g. Chelsea Royaltea)
    for a in ADMIN:
        entry = users.setdefault(
            a["email"],
            {"email": a["email"], "name": a["name"], "is_parent": False, "is_charge_parent": False, "is_admin": False},
        )
        entry["is_admin"] = True

    # Also mark any PARENTS/CHARGE_PARENTS whose email is in ADMIN_EMAILS
    for email, entry in users.items():
        if email in ADMIN_EMAILS:
            entry["is_admin"] = True

    # Upsert into the database
    for data in users.values():
        user = db.session.get(User, data["email"])
        if user is None:
            user = User(email=data["email"])
            db.session.add(user)
        user.name = data["name"]
        user.is_parent = data["is_parent"]
        user.is_charge_parent = data["is_charge_parent"]
        user.is_admin = data["is_admin"]

    db.session.commit()
    print(f"Seeded {len(users)} users.")

    # Summary
    rows = User.query.order_by(User.name).all()
    print(f"\n{'Name':<30} {'Email':<35} {'Parent':<8} {'Charge':<8} {'Admin'}")
    print("-" * 90)
    for u in rows:
        print(f"{u.name:<30} {u.email:<35} {str(u.is_parent):<8} {str(u.is_charge_parent):<8} {u.is_admin}")
