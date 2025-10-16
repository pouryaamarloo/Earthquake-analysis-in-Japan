CREATE TABLE earthquakes (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    longitude FLOAT,
    latitude FLOAT,
    depth FLOAT,
    magnitude FLOAT,
    distance_to_tokyo FLOAT,
    region VARCHAR(255),
    source VARCHAR(50)
);
CREATE INDEX idx_time ON earthquakes(time);
CREATE INDEX idx_region ON earthquakes(region);
CREATE INDEX idx_magnitude ON earthquakes(magnitude);