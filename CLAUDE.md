Peter Pan Coop Preschool — Substitution Request App
A Flask web app that allows parents at a cooperative preschool to request and accept work shift substitutions.
Core flow:
	1	A parent visits the site, enters their name, the date they can't work, and a reason, and submits the form
	2	The app sends an email via SendGrid to all parents on the list with a unique link to accept the shift
	3	The first parent to click the link and confirm is recorded as the substitute; the shift is marked closed
	4	Any parent who clicks the link after that sees a page saying the shift has been filled and who accepted it
Parent list: Hardcoded in the app config to start. Each entry has a name and email address.
Data to store per substitution request: requesting parent name, date of shift, reason for absence, timestamp of request, accepting parent name, timestamp of acceptance, status (open/filled)
Report page: A full history of all substitution requests, showing date, requesting parent, accepting parent (or "unfilled"), and reason. Filterable by date range and searchable by parent name.
Email sending should be stubbed for now. Do not integrate SendGrid yet. Instead, create a send_substitution_email() function that prints clearly formatted output to the console simulating what would be sent. For each parent on the list, print a separate block showing: TO, SUBJECT, and BODY, so it's clear exactly what each parent would receive. Use a visual separator between each simulated email.

Accept link: A unique token per request (UUID). Visiting /accept/<token> either records the acceptance (if still open) or shows the filled message.
No authentication required — anyone with the link can use the site.
Database: SQLite via SQLAlchemy to start.
Stack: Flask, SQLAlchemy, SendGrid Python SDK, python-dotenv.

