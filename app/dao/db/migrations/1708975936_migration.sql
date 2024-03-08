-- This migration creates all of the tables as per the first iteration of the DB model
CREATE TABLE modules (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    reference_point BIT NOT NULL DEFAULT 0,
    x_coordinate FLOAT DEFAULT NULL,
    y_coordinate FLOAT DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE victims (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    x_coordinate FLOAT DEFAULT NULL,
    y_coordinate FLOAT DEFAULT NULL,
    true_positive BIT DEFAULT NULL,
    location_checked BIT NOT NULL DEFAULT 0,

    -- timestamps for row
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audio_items (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    victim_id INTEGER DEFAULT NULL,
    recorded_at DATETIME NOT NULL,
    ref VARCHAR(150) NOT NULL,

    -- timestamps for row
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- keys
    FOREIGN KEY (module_id) REFERENCES modules(id),
    FOREIGN KEY (victim_id) REFERENCES victims(id)
);

CREATE TABLE neighbours (
    module_id INTEGER NOT NULL,
    neighbour_module_id INTEGER NOT NULL,

    -- timestamps for row
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- keys
    FOREIGN KEY (module_id) REFERENCES modules(id),
    FOREIGN KEY (neighbour_module_id) REFERENCES modules(id)
);

-- naming convention: idx__<column>__<other_column>, use double underscore between parts
CREATE INDEX idx__module_id ON neighbours (module_id);
