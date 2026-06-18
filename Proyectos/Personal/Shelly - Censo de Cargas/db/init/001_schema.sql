CREATE TABLE IF NOT EXISTS readings_raw (
    id BIGSERIAL PRIMARY KEY,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source TEXT,
    em_id INTEGER,
    sent_at_unix BIGINT,

    a_voltage DOUBLE PRECISION,
    a_current DOUBLE PRECISION,
    a_act_power DOUBLE PRECISION,
    a_aprt_power DOUBLE PRECISION,
    a_pf DOUBLE PRECISION,
    a_freq DOUBLE PRECISION,
    a_energy DOUBLE PRECISION,

    b_voltage DOUBLE PRECISION,
    b_current DOUBLE PRECISION,
    b_act_power DOUBLE PRECISION,
    b_aprt_power DOUBLE PRECISION,
    b_pf DOUBLE PRECISION,
    b_freq DOUBLE PRECISION,
    b_energy DOUBLE PRECISION,
    c_aprt_power DOUBLE PRECISION,
    c_pf DOUBLE PRECISION,
    c_freq DOUBLE PRECISION,
    c_energy DOUBLE PRECISION,

    n_current DOUBLE PRECISION,
    total_current DOUBLE PRECISION,
    total_act_power DOUBLE PRECISION,
    total_aprt_power DOUBLE PRECISION,
    total_energy DOUBLE PRECISION,

    raw_json JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS correction_windows (
    id BIGSERIAL PRIMARY KEY,
    phase TEXT NOT NULL CHECK (phase IN ('a', 'b', 'c', 'total')),
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL,
    issue_type TEXT NOT NULL CHECK (issue_type IN ('missing_voltage', 'reversed_ct', 'manual_estimate')),
    note TEXT,
    assumed_voltage DOUBLE PRECISION,
    assumed_power DOUBLE PRECISION,
    multiplier DOUBLE PRECISION DEFAULT 1.0
);
