query_template = """
SELECT
    up.id AS user_id,
    up.age AS age,
    up.first_name AS first_name,
    up.last_name AS last_name,
    up.country AS country,
    up.city AS city,
    COALESCE(array_agg(g.name) FILTER (WHERE g.name IS NOT NULL), '{{}}') AS genres
FROM user_profile up
LEFT JOIN user_profile_genre upg on upg.user_id = up.id
LEFT JOIN genre g on g.id = upg.genre_id
WHERE least(up.modified, upg.modified) > '{}'
GROUP BY up.id;
"""
