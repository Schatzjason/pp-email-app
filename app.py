import uuid
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///substitutions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db = SQLAlchemy(app)

# ---------------------------------------------------------------------------
# Hardcoded parent list
# ---------------------------------------------------------------------------

PARENTS = [
    {"name": "Aaron Rufff", "email": "aruff@madeup.com"},
    {"name": "Abigail Gryder", "email": "agryder@zmail.com"},
    {"name": "Alicia Gilbreth", "email": "agilbreth@fakemail.com"},
    {"name": "Anna Znyder", "email": "aznyder@zmail.com"},
    {"name": "Asa Wynn-Graunt", "email": "awyngrant@madeup.com"},
    {"name": "Brittany Dobz", "email": "bdobz@fakemail.com"},
    {"name": "Brooke Mclellan", "email": "bmclellan@fakemail.com"},
    {"name": "Cannon Dobz", "email": "cdobz@madeup.com"},
    {"name": "Casey Davis-Van Ata", "email": "cdavisvanata@zmail.com"},
    {"name": "Cathy Chang", "email": "cchang@madeup.com"},
    {"name": "Charli Ziebert", "email": "cziebert@madeup.com"},
    {"name": "Chloe Tietzon", "email": "ctietzon@zmail.com"},
    {"name": "Cole Dullar", "email": "cdullar@zmail.com"},
    {"name": "Dawn Bickit", "email": "dbickit@fakemail.com"},
    {"name": "Dennis Guiney", "email": "dguiney@fakemail.com"},
    {"name": "Domingo Benitez", "email": "dbenitez@fakemail.com"},
    {"name": "Drew Zanchez", "email": "dzanchez@zmail.com"},
    {"name": "Drew Znyder", "email": "dznyder@fakemail.com"},
    {"name": "Elizabeth Blevinz", "email": "eblevins@madeup.com"},
    {"name": "Elizabeth Ozborne", "email": "eozborne@fakemail.com"},
    {"name": "Gwyn Waller", "email": "gwaller@madeup.com"},
    {"name": "James Monacho", "email": "jmonacho@madeup.com"},
    {"name": "Jason Schatz", "email": "jschatz@fakemail.com"},
    {"name": "Jen Monacho", "email": "jmonacho2@zmail.com"},
    {"name": "Jess Wynn-Graunt", "email": "jwyngraunt@zmail.com"},
    {"name": "Jesse Kiel", "email": "jkiel@zmail.com"},
    {"name": "John Greer", "email": "jgreer@madeup.com"},
    {"name": "Karina TenBruggencayt", "email": "ktenbruggencayt@madeup.com"},
    {"name": "Kristina Dreemz", "email": "kdreemz@zmail.com"},
    {"name": "Lia Weast", "email": "lweast@zmail.com"},
    {"name": "Lianna Flynn", "email": "lflynn@madeup.com"},
    {"name": "Melissa Marten", "email": "mmarten@zmail.com"},
    {"name": "Micaela Garzia", "email": "mgarzia@zmail.com"},
    {"name": "Mikayla C.", "email": "mikaylac@zmail.com"},
    {"name": "Monica Doherty", "email": "mdoherty@madeup.com"},
    {"name": "Nick Fyzke", "email": "nfyzke@fakemail.com"},
    {"name": "Noah Chapmen", "email": "nchapmen@madeup.com"},
    {"name": "Paige Pattersun", "email": "ppattersun@madeup.com"},
    {"name": "Rachael Sharcland", "email": "rsharcland@fakemail.com"},
    {"name": "Rachel Duller", "email": "rduller@fakemail.com"},
    {"name": "Rachel Kafele", "email": "rkafele@madeup.com"},
    {"name": "Raphaël Wayde", "email": "rwayde@fakemail.com"},
    {"name": "Ryan Vong", "email": "rvong@fakemail.com"},
    {"name": "Sally Zee", "email": "szee@zmail.com"},
    {"name": "Sam Sharcland", "email": "ssharcland@madeup.com"},
    {"name": "San La", "email": "sla@fakemail.com"},
    {"name": "Sarah Postma", "email": "spostma@zmail.com"},
    {"name": "Soufiane Chami", "email": "schami@fakemail.com"},
    {"name": "Susanne Bach", "email": "sbach@zmail.com"},
    {"name": "Taylor Ludi", "email": "tludi@madeup.com"},
    {"name": "Tess Roholt", "email": "troholt@fakemail.com"},
    {"name": "Zachary Ziebert", "email": "zziebert@zmail.com"},
]

CHARGE_PARENTS = [
    {"name": "Aaron Rufff", "email": "aruff@madeup.com"},
    {"name": "Chloe Tietzon", "email": "ctietzon@zmail.com"},
    {"name": "James Monacho", "email": "jmonacho@madeup.com"},
    {"name": "Katy Wayde", "email": "kwayde@fakemail.com"},
    {"name": "San La", "email": "sla@fakemail.com"},
]

PARENT_NAMES = [p["name"] for p in PARENTS]


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class SubstitutionRequest(db.Model):
    __tablename__ = "substitution_requests"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False)
    requesting_parent_name = db.Column(db.String(100), nullable=False)
    shift_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    accepting_parent_name = db.Column(db.String(100), nullable=True)
    accepted_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), nullable=False, default="open")  # 'open' | 'filled'


# ---------------------------------------------------------------------------
# Email stub
# ---------------------------------------------------------------------------

SEP = "=" * 64


def send_substitution_email(sub: SubstitutionRequest, base_url: str) -> None:
    accept_url = f"{base_url}/accept/{sub.token}"
    date_str = sub.shift_date.strftime("%A, %B %d, %Y")

    print(f"\n{SEP}")
    print("  SIMULATED EMAIL — Substitution Request Notification")
    print(SEP)

    for parent in CHARGE_PARENTS:
        if parent["name"] == sub.requesting_parent_name:
            continue  # requesting parent doesn't need to cover their own shift

        print(f"\nTO:      {parent['name']} <{parent['email']}>")
        print(f"SUBJECT: Sub Request — Coverage needed for {date_str}")
        print(f"BODY:")
        print(f"  Hi {parent['name']},")
        print()
        print(f"  {sub.requesting_parent_name} is unable to work their scheduled shift")
        print(f"  on {date_str} and is looking for a substitute.")
        print()
        print(f"  Reason: {sub.reason}")
        print()
        print(f"  To volunteer to cover this shift, click the link below:")
        print(f"  {accept_url}")
        print()
        print(f"  The first parent to confirm will be recorded as the substitute.")
        print()
        print(f"  Thank you,")
        print(f"  Peter Pan Coop Preschool")
        print(f"\n{SEP}")

    print()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        shift_date_str = request.form.get("shift_date", "").strip()
        reason = request.form.get("reason", "").strip()

        if not name or not shift_date_str or not reason:
            return render_template(
                "index.html",
                parents=PARENT_NAMES,
                error="All fields are required.",
                form=request.form,
            )

        try:
            shift_date = datetime.strptime(shift_date_str, "%Y-%m-%d").date()
        except ValueError:
            return render_template(
                "index.html",
                parents=PARENT_NAMES,
                error="Invalid date.",
                form=request.form,
            )

        sub = SubstitutionRequest(
            token=str(uuid.uuid4()),
            requesting_parent_name=name,
            shift_date=shift_date,
            reason=reason,
        )
        db.session.add(sub)
        db.session.commit()

        base_url = request.url_root.rstrip("/")
        send_substitution_email(sub, base_url)

        return render_template(
            "index.html",
            parents=PARENT_NAMES,
            success=True,
            requesting_parent=name,
            shift_date=shift_date,
        )

    return render_template("index.html", parents=PARENT_NAMES)


@app.route("/accept/<token>", methods=["GET", "POST"])
def accept(token):
    sub = SubstitutionRequest.query.filter_by(token=token).first_or_404()

    if sub.status == "filled":
        return render_template("accept.html", sub=sub, already_filled=True)

    if request.method == "POST":
        accepting_name = request.form.get("accepting_name", "").strip()

        if not accepting_name or accepting_name not in PARENT_NAMES:
            return render_template(
                "accept.html",
                sub=sub,
                already_filled=False,
                parents=PARENT_NAMES,
                error="Please select your name.",
            )

        # Refresh to guard against a race condition
        db.session.refresh(sub)
        if sub.status == "filled":
            return render_template("accept.html", sub=sub, already_filled=True)

        sub.accepting_parent_name = accepting_name
        sub.accepted_at = datetime.utcnow()
        sub.status = "filled"
        db.session.commit()

        return render_template("accept.html", sub=sub, already_filled=False, success=True)

    available_parents = [n for n in PARENT_NAMES if n != sub.requesting_parent_name]
    return render_template(
        "accept.html",
        sub=sub,
        already_filled=False,
        parents=available_parents,
    )


@app.route("/report")
def report():
    from_date_str = request.args.get("from_date", "")
    to_date_str = request.args.get("to_date", "")
    name_search = request.args.get("name", "").strip()

    query = SubstitutionRequest.query

    if from_date_str:
        try:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
            query = query.filter(SubstitutionRequest.shift_date >= from_date)
        except ValueError:
            pass

    if to_date_str:
        try:
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()
            query = query.filter(SubstitutionRequest.shift_date <= to_date)
        except ValueError:
            pass

    if name_search:
        query = query.filter(
            db.or_(
                SubstitutionRequest.requesting_parent_name.ilike(f"%{name_search}%"),
                SubstitutionRequest.accepting_parent_name.ilike(f"%{name_search}%"),
            )
        )

    subs = query.order_by(SubstitutionRequest.shift_date.desc()).all()

    return render_template(
        "report.html",
        subs=subs,
        from_date=from_date_str,
        to_date=to_date_str,
        name_search=name_search,
    )


# ---------------------------------------------------------------------------
# Init DB on startup
# ---------------------------------------------------------------------------

with app.app_context():
    db.create_all()
