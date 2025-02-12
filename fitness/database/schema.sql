-- drop tables
DROP TABLE IF EXISTS sets;
DROP TABLE IF EXISTS workout_exercises;
DROP TABLE IF EXISTS workouts;
DROP TABLE IF EXISTS exercises;
DROP TABLE IF EXISTS muscles;
DROP TABLE IF EXISTS equipment;

-- create tables
CREATE TABLE equipment (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(50) NOT NULL,
  date_added TIMESTAMP DEFAULT (TIMEZONE('utc', NOW()))
);

CREATE TABLE muscles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(50) NOT NULL,
  date_added TIMESTAMP DEFAULT (TIMEZONE('utc', NOW()))
);

CREATE TABLE exercises (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(50) NOT NULL,
  description text,
  muscle uuid REFERENCES muscles (id),
  equipment uuid NOT NULL REFERENCES equipment (id),
  date_added TIMESTAMP DEFAULT (TIMEZONE('utc', NOW()))
);

CREATE TABLE workouts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(50) NOT NULL,
  notes text,
  date_added TIMESTAMP DEFAULT (TIMEZONE('utc', NOW()))
);

CREATE TABLE workout_exercises (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_id uuid NOT NULL REFERENCES workouts (id),
  exercise_id uuid NOT NULL REFERENCES exercises (id),
  notes text,
  date_added TIMESTAMP DEFAULT (TIMEZONE('utc', NOW()))
);

CREATE TABLE sets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_exercise_id uuid NOT NULL REFERENCES workout_exercises (id),
  repetitions integer,
  weight integer,
  date_added TIMESTAMP DEFAULT (TIMEZONE('utc', NOW()))
);

-- default values
INSERT INTO equipment (name) VALUES ('Barbell');
INSERT INTO equipment (name) VALUES ('Bench Press Machine');
INSERT INTO equipment (name) VALUES ('Cable Machine');
INSERT INTO equipment (name) VALUES ('Crunch Machine');
INSERT INTO equipment (name) VALUES ('Dumbbells');
INSERT INTO equipment (name) VALUES ('Elliptical');
INSERT INTO equipment (name) VALUES ('EZ Bar');
INSERT INTO equipment (name) VALUES ('Kettlebell');
INSERT INTO equipment (name) VALUES ('Lat Pulldown Machine');
INSERT INTO equipment (name) VALUES ('Leg Curl Machine');
INSERT INTO equipment (name) VALUES ('Leg Extension Machine');
INSERT INTO equipment (name) VALUES ('Leg Press Machine');
INSERT INTO equipment (name) VALUES ('Overhead Press Machine');
INSERT INTO equipment (name) VALUES ('Pec Deck');
INSERT INTO equipment (name) VALUES ('Seated Row Machine');
INSERT INTO equipment (name) VALUES ('Smith Machine');
INSERT INTO equipment (name) VALUES ('Stationary Bicycle');
INSERT INTO equipment (name) VALUES ('Treadmill');

INSERT INTO muscles (name) VALUES ('Abdomen');
INSERT INTO muscles (name) VALUES ('Back');
INSERT INTO muscles (name) VALUES ('Biceps');
INSERT INTO muscles (name) VALUES ('Cardio');
INSERT INTO muscles (name) VALUES ('Chest');
INSERT INTO muscles (name) VALUES ('Legs');
INSERT INTO muscles (name) VALUES ('Shoulders');
INSERT INTO muscles (name) VALUES ('Triceps');

INSERT INTO exercises (name, muscle, equipment) SELECT 'Back Squat (Barbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Legs' AND e.name = 'Barbell';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Back Squat (Smith Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Legs' AND e.name = 'Smith Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Decline, Barbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Barbell';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Decline, Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Decline, Smith Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Smith Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Flat, Barbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Barbell';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Flat, Bench Press Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Bench Press Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Flat, Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Flat, Smith Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Smith Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Incline, Barbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Barbell';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Incline, Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bench Press (Incline, Smith Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Smith Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bicep Curl (Cable)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Biceps' AND e.name = 'Cable Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bicep Curl (EZ Bar)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Biceps' AND e.name = 'EZ Bar';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Bicep Curl (Incline)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Biceps' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Crunch (Cable)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Abdomen' AND e.name = 'Cable Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Crunch (Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Abdomen' AND e.name = 'Crunch Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Face Pull', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Cable Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Goblet Squat', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Legs' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Lat Pulldown (Standard)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Back' AND e.name = 'Lat Pulldown Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Lat Pulldown (Straight Arm)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Back' AND e.name = 'Lat Pulldown Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Lat Pulldown (Underhand)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Back' AND e.name = 'Lat Pulldown Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Lat Pulldown (V-Bar)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Back' AND e.name = 'Lat Pulldown Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Lateral Raise (Cable)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Cable Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Lateral Raise (Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Leg Extension', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Legs' AND e.name = 'Leg Extension Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Leg Press', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Legs' AND e.name = 'Leg Press Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Overhead Press (Barbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Barbell';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Overhead Press (Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Overhead Press (Overhead Press Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Overhead Press Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Overhead Press (Smith Machine)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Smith Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Overhead Tricep Extension (Cable)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Triceps' AND e.name = 'Cable Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Overhead Tricep Extension (Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Triceps' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Pec Deck', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Chest' AND e.name = 'Pec Deck';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Preacher Curl (EZ Bar)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Biceps' AND e.name = 'EZ Bar';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Romanian Deadlift (Barbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Legs' AND e.name = 'Barbell';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Romanian Deadlift (Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Legs' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Row (Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Back' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Run (Treadmill)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Cardio' AND e.name = 'Treadmill';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Seated Row', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Back' AND e.name = 'Seated Row Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Shrug (Barbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Barbell';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Shrug (Dumbbell)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Shoulders' AND e.name = 'Dumbbells';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Skull Crusher (EZ Bar)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Triceps' AND e.name = 'EZ Bar';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Tricep Pushdown (Rope)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Triceps' AND e.name = 'Cable Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Tricep Pushdown (Straight Bar)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Triceps' AND e.name = 'Cable Machine';
INSERT INTO exercises (name, muscle, equipment) SELECT 'Walk (Treadmill)', m.id, e.id FROM muscles m, equipment e WHERE m.name = 'Cardio' AND e.name = 'Treadmill';
