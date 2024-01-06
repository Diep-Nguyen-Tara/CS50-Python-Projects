-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Find crime scene description
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = 'Humphrey Street';

-- Find hints from interviews
SELECT * FROM interviews
WHERE month = 7
AND day = 28;

-- Find license plate from bakery_security_logs
SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute = 14
AND activity = 'entrance';

-- Find name from people using license_plate
SELECT name FROM people
WHERE license_plate = '13FNH73';

-- Find passport_number from people table using license plate. Result passport_number = 3642612721
SELECT passport_number FROM people
WHERE name = 'Sophia'
AND license_plate = '13FNH73';

-- Find destination_airport_id from table flights. Result destination_airport_id = 5
SELECT destination_airport_id, month, day, hour, minute
FROM flights
WHERE id = (SELECT flight_id
            FROM passengers
            WHERE passport_number = '3642612721');

-- Find city where the thief escape to, using destination_airport_id. Result Dallas
SELECT city FROM airports
WHERE id = 5;

-- Find phone number of the accomplice using caller's phone number. Result receiver = (717) 555-1342
SELECT receiver, month, day, duration FROM phone_calls
WHERE month = 7
AND day >=28
AND caller = (
                SELECT phone_number FROM people
                WHERE name = 'Sophia'
                AND passport_number = '3642612721'
                );

-- Find the accomplice
SELECT name FROM people
WHERE phone_number = '(717) 555-1342';

-- others

SELECT receiver, month, day, duration FROM phone_calls
WHERE month = 7
AND day = 28
AND duration < 60;

SELECT * FROM flights WHERE origin_airport_id = 8
AND month = 7 and day = 29;

-- hints

Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

 I don't know the thief's name, but it was someone I recognized.
 Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Find license_plate
SELECT * FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- Find phone number of caller
SELECT * FROM phone_calls
WHERE month = 7
AND day = 28
AND duration < 60;

SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60
SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;
