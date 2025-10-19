import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class SQLConnector:
    def __init__(self) -> None:
        try:
            self.engine = create_engine(
                "postgresql+psycopg2://samaneh:123456@localhost:16584/postgres"
            )
            self.columns = [
                'time', 'longitude', 'latitude', 'depth', 'magnitude', 'region', 'source', 'distance_to_tokyo'
            ]
        except SQLAlchemyError as e:
            print(f"[ERROR] Database connection failed: {e}")
            self.engine = None

    def insert(self, df):
        if self.engine is None:
            print("[ERROR] Engine not initialized.")
            return

        try:
            final_df = df[self.columns]
            final_df.to_sql(
                'earthquakes',
                con=self.engine,
                if_exists='replace',
                index=True,
                index_label='id',
                chunksize=1000
            )
            print("[INFO] Data inserted successfully.")
        except KeyError as e:
            print(f"[ERROR] Missing required columns: {e}")
        except SQLAlchemyError as e:
            print(f"[ERROR] Database insertion failed: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")

    def fetch_all(self):
        if self.engine is None:
            print("[ERROR] Engine not initialized.")
            return pd.DataFrame()

        try:
            with self.engine.connect() as conn:
                res = conn.execute(text("SELECT * FROM earthquakes"))
            df = pd.DataFrame(res.all(), columns=list(res.keys()))
            df.index.name = 'id'
            df['time'] = pd.to_datetime(df['time'])
            return df
        except SQLAlchemyError as e:
            print(f"[ERROR] Failed to fetch data: {e}")
            return pd.DataFrame()

    def get_all_earthquakes(self):
        try:
            with self.engine.connect() as conn:
                res = conn.execute(
                    text("""
                        SELECT region, EXTRACT(MONTH FROM time::timestamp) AS month, COUNT(*)
                        FROM earthquakes
                        GROUP BY region, month
                    """)
                )
            return pd.DataFrame(res.all(), columns=list(res.keys()))
        except SQLAlchemyError as e:
            print(f"[ERROR] Query failed: {e}")
            return pd.DataFrame()

    def get_average_magnitude_by_region(self):
        try:
            with self.engine.connect() as conn:
                res = conn.execute(
                    text("""
                        SELECT region, source, AVG(magnitude) AS avg_magnitude
                        FROM earthquakes
                        GROUP BY region, source
                        ORDER BY region, source;
                    """)
                )
            return pd.DataFrame(res.all(), columns=list(res.keys()))
        except SQLAlchemyError as e:
            print(f"[ERROR] Query failed: {e}")
            return pd.DataFrame()

    def get_recent_earthquakes_by_region(self):
        try:
            with self.engine.connect() as conn:
                res = conn.execute(
                    text("""
                        SELECT *
                        FROM earthquakes
                        ORDER BY magnitude DESC, time DESC
                        LIMIT 10;
                    """)
                )
            return pd.DataFrame(res.all(), columns=list(res.keys()))
        except SQLAlchemyError as e:
            print(f"[ERROR] Query failed: {e}")
            return pd.DataFrame()

    def get_depth_by_region(self):
        try:
            with self.engine.connect() as conn:
                res = conn.execute(
                    text("""
                        SELECT region, MAX(depth) AS max_depth, MIN(depth) AS min_depth
                        FROM earthquakes
                        GROUP BY region
                        ORDER BY region;
                    """)
                )
            return pd.DataFrame(res.all(), columns=list(res.keys()))
        except SQLAlchemyError as e:
            print(f"[ERROR] Query failed: {e}")
            return pd.DataFrame()

    def delete_suspicious_rows(self):
        if self.engine is None:
            print("[ERROR] Engine not initialized.")
            return 0

        try:
            with self.engine.begin() as conn:
                res = conn.execute(text("SELECT magnitude, depth FROM earthquakes"))
                data = np.array(res.fetchall(), dtype=float)

                if data.size == 0:
                    print("[INFO] No data found to clean.")
                    return 0

                q1_mag, q3_mag = np.percentile(data[:, 0], [25, 75])
                q1_dep, q3_dep = np.percentile(data[:, 1], [25, 75])

                iqr_mag = q3_mag - q1_mag
                iqr_dep = q3_dep - q1_dep

                low_mag = max(q1_mag - 1.5 * iqr_mag, 0)
                high_mag = q3_mag + 1.5 * iqr_mag
                low_dep = max(q1_dep - 1.5 * iqr_dep, 0)
                high_dep = q3_dep + 1.5 * iqr_dep

                query = f"""
                    DELETE FROM earthquakes
                    WHERE magnitude < {low_mag}
                    OR magnitude > {high_mag}
                    OR depth < {low_dep}
                    OR depth > {high_dep};
                """
                result = conn.execute(text(query))
                print(f"[INFO] Deleted {result.rowcount} suspicious rows.")
                return result.rowcount
        except SQLAlchemyError as e:
            print(f"[ERROR] Failed to delete suspicious rows: {e}")
            return 0
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return 0
