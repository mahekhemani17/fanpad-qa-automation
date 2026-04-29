import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def delete_test_fan():
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("QA_DB_HOST"),
            port=os.getenv("QA_DB_PORT"),
            dbname=os.getenv("QA_DB_NAME"),
            user=os.getenv("QA_DB_USER"),
            password=os.getenv("QA_DB_PASSWORD")
        )
        cursor = conn.cursor()
        phone = os.getenv("TWILIO_PHONE_NUMBER")
        
        for artist_id in [1, 92, 94]:
            cursor.execute(
                'SELECT public."SP_QAAuto_DeleteFan_By_PhoneNumber"(%s, %s)',
                (phone, artist_id)
            )
        
        conn.commit()
        print(f"✓ Test fan deleted for phone {phone} across all artist IDs")
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    delete_test_fan()