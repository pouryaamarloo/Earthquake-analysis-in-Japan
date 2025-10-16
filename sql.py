import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text


class SQLConnector:
    def __init__(self) -> None:
        self.engine = create_engine("postgresql+psycopg2://samaneh:123456@localhost:16584/postgres")
        
        self.columns = [
            'time','longitude','latitude','depth','magnitude','region','source', 'distance_to_tokyo'
        ]
    
    def insert(self, df):
        final_df = df[self.columns]
        
        final_df.to_sql(
            'earthquakes',
            con=self.engine,
            if_exists='append',
            index=False,
            chunksize=1000
        )
    
    def fetch_all(self):
        with self.engine.connect() as conn:
            res = conn.execute(
                text(
                    """
                    SELECT *
                    FROM earthquakes
                    """
                )
            )

        df = pd.DataFrame(res.all(), columns=list(res.keys())).set_index("id")
        df['time'] = pd.to_datetime(df['time'])
        return df
    
    def get_all_earthquakes(self):
        with self.engine.connect() as conn:
            res = conn.execute(
                text(
                    """
                    SELECT region, EXTRACT(MONTH FROM time) AS month, COUNT(*)
                    FROM earthquakes
                    GROUP BY region, month
                    """
                )
            )
        
        return pd.DataFrame(res.all(), columns=list(res.keys())).set_index("id")
    
    def get_average_magnitude_by_region(self):
        with self.engine.connect() as conn:
            res = conn.execute(
                text(
                    """
                    SELECT region, source, AVG(magnitude) AS avg_magnitude
                    FROM earthquakes
                    GROUP BY region, source
                    ORDER BY region, source;
                    """
                )
            )
        
        return pd.DataFrame(res.all(), columns=list(res.keys())).set_index("id")
    
    def get_recent_earthquakes_by_region(self):
        with self.engine.connect() as conn:
            res = conn.execute(
                text(
                    """
                    SELECT *
                    FROM earthquakes
                    ORDER BY magnitude DESC, time DESC
                    LIMIT 10;
                    """
                )
            )
        
        return pd.DataFrame(res.all(), columns=list(res.keys())).set_index("id")
    
    def get_depth_by_region(self):
        with self.engine.connect() as conn:
            res = conn.execute(
                text(
                    """
                    SELECT region, MAX(depth) AS max_depth, MIN(depth) AS min_depth
                    FROM earthquakes
                    GROUP BY region
                    ORDER BY region;
                    """
                )
            )
        
        return pd.DataFrame(res.all(), columns=list(res.keys())).set_index("id")
    
    def delete_suspicious_rows(self):
        with self.engine.begin() as conn:
            res = conn.execute(
                text(
                    """
                    SELECT magnitude, depth
                    FROM earthquakes
                    """
                )
            )
            
            data = np.array(res, dtype=float)
            if data.size == 0:
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
            res = conn.execute(text(query))
            
            return res.rowcount