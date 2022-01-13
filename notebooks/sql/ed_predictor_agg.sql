-- Returns approx 100k rows

SELECT

 extract_dttm
,num_adm_pred
,probs
--,description

FROM flow.ed_predictor_agg_audit ed
WHERE 
    ed.inc_nya=TRUE
AND contrib='All patients'
AND description='Num beds needed in 8 hours'
AND ed.extract_dttm > NOW() - '90 DAYS'::INTERVAL
ORDER BY extract_dttm DESC

;