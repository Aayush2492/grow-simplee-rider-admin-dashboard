-- name: insert_location^
INSERT INTO location (latitude, longitude, address) VALUES (:latitude, :longitude, :address) RETURNING loc_id;

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

-- name: get_bags
SELECT * FROM bag ORDER BY bag_type DESC;

-- name: update_loc
-- WIP. This should also return trip status, if such a trip exists
UPDATE rider SET latitude = :latitude AND longitude = :longitude WHERE rider_id = :rider_id;

-- name: check_trip^
SELECT tour_id, tour_status FROM tour WHERE assigned_rider = :rider_id AND tour_status != 2;

-- name: accept_trip!
UPDATE tour SET tour_status = 1 WHERE assigned_rider = :rider_id AND tour_status = 0;

-- name: mark_delivered!
UPDATE package SET completed = true, delivered_time = CURRENT_TIMESTAMP WHERE object_id = :obj_id;

-- name: upcoming_deliveries
SELECT COUNT(*) FROM delivery WHERE id = :tour_id AND delivery_order > (SELECT delivery_order FROM delivery WHERE item = :object_id);

-- name: complete_trip!
UPDATE tour SET tour_status = 2 WHERE assigned_rider = :rider_id AND tour_status = 1;

-- name: get_trip_id^
SELECT id FROM delivery WHERE item = :object_id;

-- name: insert_tour^
INSERT INTO tour(assigned_rider, assigned_bag, tour_status) VALUES(:rider_id, :bag_id, :tour_status);

-- name: insert_delivery_item
INSERT INTO delivery(id, item, delivery_order) VALUES(:tour_id, :item, :delivery_order)

-- name: get_undelivered_packages
SELECT * FROM package LEFT JOIN location ON package.delivery_loc = location.loc_id WHERE package.completed = False ORDER BY location.loc_id;
