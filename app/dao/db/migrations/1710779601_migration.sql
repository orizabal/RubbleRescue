-- This migration adds a new row to the modules table so that
-- each row will also have the id that is given to them from Kristen's system
ALTER TABLE modules
ADD physical_id VARCHAR(50) DEFAULT NULL;

-- naming convention: idx__<column>__<other_column>, use double underscore between parts
CREATE INDEX idx__physical_id ON modules (physical_id);
