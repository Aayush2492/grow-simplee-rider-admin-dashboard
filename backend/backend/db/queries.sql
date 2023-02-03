-- name: insert_location!
INSERT INTO location (latitude, longitude) VALUES (:latitude, :longitude);

-- name: delete_package!
-- Delete a package from the database
DELETE FROM package WHERE object_id = :obj_id;

-- name: get_all_packages
SELECT * FROM package;

-- name: get_package_by_id^
SELECT * FROM package WHERE object_id= :obj_id;
