CREATE OR REPLACE VIEW readings_curated AS
SELECT
    r.*,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'a'
              AND cw.issue_type = 'reversed_ct'
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_multiplier_fix(
            r.a_act_power,
            (SELECT cw.multiplier
             FROM correction_windows cw
             WHERE cw.phase = 'a'
               AND cw.issue_type = 'reversed_ct'
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        ELSE r.a_act_power
    END AS a_act_power_fixed,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'b'
              AND cw.issue_type IN ('missing_voltage', 'manual_estimate')
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_missing_voltage_fix(
            r.b_current,
            r.b_pf,
            (SELECT cw.assumed_voltage
             FROM correction_windows cw
             WHERE cw.phase = 'b'
               AND cw.issue_type IN ('missing_voltage', 'manual_estimate')
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1),
            (SELECT cw.assumed_power
             FROM correction_windows cw
             WHERE cw.phase = 'b'
               AND cw.issue_type IN ('missing_voltage', 'manual_estimate')
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1),
            (SELECT cw.issue_type
             FROM correction_windows cw
             WHERE cw.phase = 'b'
               AND cw.issue_type IN ('missing_voltage', 'manual_estimate')
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'b'
              AND cw.issue_type = 'reversed_ct'
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_multiplier_fix(
            r.b_act_power,
            (SELECT cw.multiplier
             FROM correction_windows cw
             WHERE cw.phase = 'b'
               AND cw.issue_type = 'reversed_ct'
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        ELSE r.b_act_power
    END AS b_act_power_fixed,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'c'
              AND cw.issue_type = 'reversed_ct'
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_multiplier_fix(
            r.c_act_power,
            (SELECT cw.multiplier
             FROM correction_windows cw
             WHERE cw.phase = 'c'
               AND cw.issue_type = 'reversed_ct'
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        ELSE r.c_act_power
    END AS c_act_power_fixed
FROM readings_raw r;
