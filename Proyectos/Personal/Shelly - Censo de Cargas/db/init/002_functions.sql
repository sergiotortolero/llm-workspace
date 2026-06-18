CREATE OR REPLACE FUNCTION apply_missing_voltage_fix(
    p_current DOUBLE PRECISION,
    p_pf DOUBLE PRECISION,
    p_assumed_voltage DOUBLE PRECISION,
    p_assumed_power DOUBLE PRECISION,
    p_strategy TEXT
)
RETURNS DOUBLE PRECISION
LANGUAGE SQL
AS $$
    SELECT CASE 
        WHEN p_strategy = 'manual_estimate' THEN COALESCE(p_assumed_power, 0)
        ELSE COALESCE(p_current, 0) * COALESCE(p_pf, 1) * COALESCE(p_assumed_voltage, 127.0)
    END;
$$;

CREATE OR REPLACE FUNCTION apply_multiplier_fix(
    p_value DOUBLE PRECISION,
    p_multiplier DOUBLE PRECISION
)
RETURNS DOUBLE PRECISION
LANGUAGE SQL
AS $$
    SELECT COALESCE(p_value, 0) * COALESCE(p_multiplier, 1.0);
$$;
