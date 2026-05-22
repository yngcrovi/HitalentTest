WITH RECURSIVE department_tree AS (
    SELECT 
        id, 
        name, 
        parent_id, 
        strftime('%d.%m.%Y %H:%M:%S', created_at) AS created_at,
        0 AS level
    FROM department
    WHERE id = :dept_id
    
    UNION ALL
    
    SELECT 
        d.id, 
        d.name, 
        d.parent_id, 
        strftime('%d.%m.%Y %H:%M:%S', d.created_at),
        dt.level + 1
    FROM department d
    INNER JOIN department_tree dt ON d.parent_id = dt.id
    WHERE dt.level + 1 <= :depth
)
SELECT * FROM department_tree
ORDER BY level, id