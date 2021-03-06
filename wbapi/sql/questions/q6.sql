/* Q6. List 3 countries with lowest GDP per region. */
 WITH GDP AS
  (SELECT COUNTRY.NAME,
          COUNTRY.REG_ID,
              CASE
                  WHEN VALUE = '' THEN NULL
                  ELSE VALUE::FLOAT
              END AS GDP
   FROM GDPDATAPOINT AS GDP
   JOIN COUNTRY ON (COUNTRY.ISO3 = GDP.CTRY_CODE)
   WHERE GDP.YEAR::INTEGER = 2017)
SELECT X.NAME AS COUNTRY_NAME, X.REG_ID AS REGION_CODE, RANK AS POOREST_RANK
FROM
  (SELECT GDP.*,
          RANK() OVER (PARTITION BY GDP.REG_ID ORDER BY GDP.GDP) AS RANK
   FROM GDP
   WHERE GDP.GDP IS NOT NULL) X
WHERE X.RANK <= 3
ORDER BY X.REG_ID, X.RANK;
