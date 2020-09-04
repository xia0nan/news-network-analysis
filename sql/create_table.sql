-- Network Analysis SQL

-- 1. Check dates

SELECT date(date) as real_date
FROM wm_alert.public.article
WHERE date >= '2020-07-01 00:00:00'
GROUP BY real_date
ORDER BY real_date DESC;

-- 2. Check news id
SELECT
    COUNT(DISTINCT guid) as cguid,
    COUNT(DISTINCT refinitiv_id) as crefinitiv_id,
    COUNT(DISTINCT permid) as cpermid,
    COUNT(1) as c
FROM wm_alert.public.article
WHERE date >= '2020-01-01 00:00:00';
# guid and refinitiv_id are identical for news id
# there are duplicated news

-- 2.1 Check duplicated refinitv_id


-- 3. Get news with multiple entities
SELECT COUNT(1)
FROM (
         SELECT multi_ent.guid
         FROM (
                  SELECT guid
                  FROM wm_alert.public.article
                  WHERE date >= '2020-01-01 00:00:00'
                  GROUP BY guid
                  HAVING COUNT(1) > 1
              ) as multi_ent
         GROUP BY guid
     ) as selected_guid

-- 3.1 Find targeted news
SELECT refinitiv_id, COUNT(1) as entity_counts
FROM
     (
    SELECT
        data->>'id' as refinitiv_id,
        jsonb_array_elements_text(subjects) subjects
    FROM wm_alert.public.article_raw
    WHERE timestamp >= '2019-01-01 00:00:00'
        AND data->>'pubStatus' = 'stat:usable'
        AND data->>'language' = 'en'
        AND data->>'subjects' LIKE '%P:%'
    GROUP BY refinitiv_id, subjects
    ) t
WHERE subjects LIKE '%P:%'
GROUP BY refinitiv_id
HAVING COUNT(1) > 1

-- 3.2 Join news with permid

WITH filtered AS (
    SELECT
        data->>'id' as refinitiv_id,
        jsonb_array_elements_text(subjects) subjects
    FROM wm_alert.public.article_raw
    WHERE timestamp >= '2020-07-01 00:00:00'
        AND data->>'pubStatus' = 'stat:usable'
        AND data->>'language' = 'en'
        AND data->>'subjects' LIKE '%P:%'
    GROUP BY refinitiv_id, subjects
)

SELECT refinitiv_id, RIGHT(subjects,10) AS permid
FROM filtered
WHERE subjects LIKE '%P:%'
    AND refinitiv_id IN (
        SELECT refinitiv_id
        FROM filtered
        WHERE subjects LIKE '%P:%'
        GROUP BY refinitiv_id
        HAVING COUNT(1) > 1
);


-- 4. Create news id vs permid [wm_alert.public.network_entity]
WITH filtered AS (
    SELECT
        data->>'id' as refinitiv_id,
        jsonb_array_elements_text(subjects) subjects
    FROM wm_alert.public.article_raw
    WHERE timestamp >= '2020-07-01 00:00:00'
        AND data->>'pubStatus' = 'stat:usable'
        AND data->>'language' = 'en'
        AND data->>'subjects' LIKE '%P:%'
    GROUP BY refinitiv_id, subjects
)

CREATE TABLE wm_alert.public.network_entity AS (
    SELECT refinitiv_id, RIGHT(subjects,10) AS permid
    FROM filtered
    WHERE subjects LIKE '%P:%'
        AND refinitiv_id IN (
            SELECT refinitiv_id
            FROM filtered
            WHERE subjects LIKE '%P:%'
            GROUP BY refinitiv_id
            HAVING COUNT(1) > 1
    )
);

-- 5. Join to get source and target permid
SELECT
    origin.refinitiv_id,
    origin.permid AS source_id,
    t.permid AS target_id
FROM wm_alert.public.network_entity origin
JOIN (
    SELECT
        refinitiv_id,
        permid
    FROM wm_alert.public.network_entity
    LIMIT 100
    ) t
    ON t.refinitiv_id = origin.refinitiv_id
       AND t.permid != origin.permid;

-- 6. Create news id vs source and target permid [wm_alert.public.network_link]
CREATE TABLE wm_alert.public.network_link AS (
    SELECT
        origin.refinitiv_id,
        origin.permid AS source_id,
        t.permid AS target_id
    FROM wm_alert.public.network_entity origin
    JOIN (
        SELECT
            refinitiv_id,
            permid
        FROM wm_alert.public.network_entity
        ) t
        ON t.refinitiv_id = origin.refinitiv_id
           AND t.permid != origin.permid;
)