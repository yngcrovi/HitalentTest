WITH RECURSIVE department_tree AS (
    SELECT 
        id, 
        name, 
        parent_id, 
        TO_CHAR(created_at, 'DD.MM.YYYY HH24:MI:SS') AS created_at,
        0 AS level
    FROM department
    WHERE id = :dept_id
    
    UNION ALL
    
    SELECT 
        d.id, 
        d.name, 
        d.parent_id, 
        TO_CHAR(d.created_at, 'DD.MM.YYYY HH24:MI:SS'),
        dt.level + 1
    FROM department d
    INNER JOIN department_tree dt ON d.parent_id = dt.id
    WHERE dt.level + 1 <= :depth
)
SELECT * FROM department_tree
ORDER BY level, id