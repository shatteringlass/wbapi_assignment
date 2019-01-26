/* Q5. Calculate percentage difference in value of GDP year-on-year per country. */
 WITH GDP AS
  (SELECT COUNTRY.NAME AS CTRY_NAME,
          YEAR::INTEGER,
          CASE
              WHEN VALUE = '' THEN NULL
              ELSE VALUE::FLOAT
          END AS GDP
   FROM GDPDATAPOINT
   JOIN COUNTRY ON COUNTRY.ISO3 = GDPDATAPOINT.CTRY_CODE)
SELECT *,
       TRUNC(100 * ((GDP/(LAG(GDP, 1) OVER (PARTITION BY CTRY_NAME
                                            ORDER BY YEAR)))::NUMERIC - 1),2) AS GDP_PCT_YOY_VAR
FROM GDP;
