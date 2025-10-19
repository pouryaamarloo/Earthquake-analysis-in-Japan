import unittest
import pandas as pd
from sqlalchemy import create_engine, text

# مسیر فایل‌های CSV
csv_path = [
    "../clean_csv/JAPAN_USGS.csv",
    "../clean_csv/JAPAN_DATASET.csv",
    "../clean_csv/JAPAN_GEOFON.csv",
]


class TestProject(unittest.TestCase):
    # ۱. بررسی صحت دریافت داده‌ها
    def test_correct_data(self):
        for c in csv_path:
            df = pd.read_csv(c)
            self.assertGreater(len(df), 0, f"{c} is empty.")

    # ۲. بررسی وجود ستون‌های مهم
    def test_column_important(self):
        expected_columns = [
            "time", "latitude", "longitude", "depth", "magnitude",
            "region", "Category", "distance_to_tokyo"
        ]
        for c in csv_path:
            df = pd.read_csv(c)
            missing = [col for col in expected_columns if col not in df.columns]
            self.assertFalse(missing, f"{c} is missing columns: {', '.join(missing)}")

    # ۳. بررسی حذف داده‌های ناقص
    def test_remove_defective(self):
        for c in csv_path:
            df = pd.read_csv(c)
            self.assertFalse(df.isnull().values.any(), f"There is NaN in {c}")

    # ۴. بررسی نوع داده‌ها
    def test_data_type(self):
        numeric_columns = ["longitude", "latitude", "depth", "magnitude"]
        for c in csv_path:
            df = pd.read_csv(c)
            for i in numeric_columns:
                if i in df.columns:
                    self.assertTrue(
                        pd.api.types.is_numeric_dtype(df[i]),
                        f"ستون {i} در فایل {c} باید عددی باشد."
                    )

    # ۵. بررسی آماری (میانگین و انحراف معیار)
    def test_statistical_analysis(self):
        for c in csv_path:
            df = pd.read_csv(c)
            self.assertIn("magnitude", df.columns)
            self.assertIn("depth", df.columns)

            mean_mag = df["magnitude"].mean()
            std_mag = df["magnitude"].std()

            self.assertFalse(pd.isna(mean_mag))
            self.assertFalse(pd.isna(std_mag))
            self.assertTrue((df["magnitude"] >= 0).all())

            mean_depth = df["depth"].mean()
            std_depth = df["depth"].std()

            self.assertFalse(pd.isna(mean_depth))
            self.assertFalse(pd.isna(std_depth))
            self.assertTrue((df["depth"] >= 0).all())

    # ۶. بررسی درج داده در پایگاه داده
    def test_database_insert(self):
        engine = create_engine("postgresql+psycopg2://samaneh:123456@localhost:16584/postgres")

        with engine.begin() as conn:
            before = conn.execute(text("SELECT COUNT(*) FROM earthquakes")).scalar()

            conn.execute(text("""
                INSERT INTO earthquakes (time, longitude, latitude, depth, magnitude, distance_to_tokyo, region, source)
                VALUES ('2024-10-19 00:00:00', 139.76, 35.68, 10.5, 4.5, 50.0, 'Tokyo', 'test')
            """))

            after = conn.execute(text("SELECT COUNT(*) FROM earthquakes")).scalar()

            self.assertTrue(after > before, "No new data inserted")

            # پاک‌سازی رکورد تستی
            conn.execute(text("DELETE FROM earthquakes WHERE source = 'test'"))


if __name__ == "__main__":
    unittest.main()
