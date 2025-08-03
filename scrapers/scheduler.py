import schedule
import time
import subprocess

def job():
    print("Fetching latest news...")
    subprocess.run(["python", "scrapers/newsapi_scraper.py"])

# Run every 30 minutes (you can change this)
schedule.every(30).minutes.do(job)

print("Scheduler started. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)
