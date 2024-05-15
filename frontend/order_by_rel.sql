SELECT theme.id, theme.entry_name, COUNT(r_iconography_theme.id) AS c
FROM theme
JOIN r_iconography_theme ON theme.id = r_iconography_theme.id_theme
GROUP BY theme.id
ORDER BY c DESC;

