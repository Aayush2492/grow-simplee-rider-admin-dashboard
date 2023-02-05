-- name: insert_location!
INSERT INTO location (latitude, longitude, address) VALUES (:latitude, :longitude, :address);

-- name: get_location_by_id^
SELECT * FROM location WHERE loc_id = :loc_id;

-- name: get_all_locations
SELECT * FROM location;

-- name: delete_package!
-- Delete a package from the database
DELETE FROM package WHERE object_id = :obj_id;

-- name: get_all_packages
SELECT * FROM package;

-- name: get_package_by_id^
SELECT * FROM package WHERE object_id= :obj_id;

-- name: insert_package!
INSERT INTO package (weight, length, breadth, height, delivery_date, delivery_loc, erroneous, comments, obj_type, completed) VALUES (:weight, :length, :breadth, :height, :delivery_date, :delivery_loc, :erroneous, :comments, :obj_type, :completed);

-- name: get_rider_by_id^
SELECT * FROM rider WHERE rider_id = :rider_id;

-- name: get_riders
SELECT * FROM rider;

-- name: update_loc
-- WIP. This should also return trip status, if such a trip exists
UPDATE rider SET latitude = :latitude AND longitude = :longitude WHERE rider_id = :rider_id;

