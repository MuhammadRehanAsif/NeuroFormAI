# NeuroFormAI

NeuroFormAI is a Gradio-based AI exercise coach that uses MediaPipe pose tracking to monitor body movement, count repetitions, detect posture issues, and store workout history in MongoDB. It also includes a workout planner, authentication, analytics, and progress charts.

## What It Does

- Live exercise tracking from a webcam or uploaded video.
- Rep counting with angle smoothing and exercise-specific phase detection.
- Posture checking with rule-based alerts for common form mistakes.
- User sign-up and login with bcrypt password hashing.
- Workout session history, exercise-level stats, and leaderboard analytics.
- Workout plan management using custom data structures.

## Main Features

### Exercise Tracking

The app tracks a video stream frame by frame, detects 33 MediaPipe pose landmarks, calculates the angle for the primary exercise joint, smooths the angle with a circular queue, and feeds the result into a repetition state machine.

Supported exercise categories include:

- Arms
- Shoulders
- Legs
- Full Body
- Core

The seeded exercises are:

- Bicep Curl
- Tricep Extension
- Shoulder Press
- Lateral Raise
- Front Raise
- Squat
- Lunge
- Calf Raise
- Leg Raise
- Push-Up
- Jumping Jack
- High Knees
- Plank
- Deadlift

### Form Feedback

Each exercise defines:

- Primary target angles used for rep counting.
- Side-specific landmark mappings for left and right body tracking.
- Posture rules that trigger warnings when the form deviates from acceptable ranges.
- Phase sequences that define what counts as a complete rep.

### Session History and Analytics

Workout sessions are written to MongoDB and can be reviewed later in the History tab. The Analytics tab includes:

- A leaderboard sorted by reps, score, or session count.
- Per-exercise stats for the logged-in user.
- A progress chart showing reps and form score over time.
- Personal records extracted from past sessions.

### Workout Plan Builder

The Workout Plan tab lets you build a plan using:

- A doubly linked list to store and reorder exercises.
- A stack to support undo operations.

## Technology Stack

- Python
- Gradio
- MediaPipe
- OpenCV
- MongoDB / PyMongo
- bcrypt
- NumPy
- Matplotlib
- python-dotenv

## How The App Is Organized

### Core Pipeline

1. `PoseDetector` extracts pose landmarks from each frame.
2. `AngleCalculator` computes and smooths joint angles.
3. `RepCounter` detects phases and counts completed repetitions.
4. `PostureChecker` validates secondary form rules and generates alerts.
5. `ExerciseEngine` coordinates the full per-frame workflow.

### Data Structures

The project uses custom implementations to demonstrate classic algorithms and data structures:

- `DynamicArray` stores landmarks and rep angle history.
- `CircularQueue` smooths angle readings.
- `Stack` tracks rep state and undo history.
- `DoublyLinkedList` powers workout plan ordering and session navigation.
- `merge_sort` sorts session history and user exercise stats.
- `quick_sort` sorts the leaderboard.

## Project Structure

```text
neuroformai/
  app.py                 # Application entry point
  config.py              # Environment and exercise settings
  auth/                  # Login and signup logic
  core/                  # Pose detection, angle, rep, and posture engine
  data_structures/       # Custom arrays, stacks, queues, linked lists, sorting
  database/              # MongoDB connection, schema setup, and queries
  exercises/             # Exercise model and loaders
  ui/                    # Gradio tabs and event handlers
  utils/                 # Formatting and visualization helpers
  models/                # MediaPipe pose model asset
```

## Requirements

- Python 3.10+ recommended
- MongoDB running locally or remotely
- Webcam access if you want to use live tracking
- The MediaPipe pose model file already present at `neuroformai/models/pose_landmarker_full.task`

## Installation

1. Create and activate a virtual environment.
2. Install the dependencies from the repository root:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root if you want to override the defaults:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=neuroformai
```

If `.env` is missing, the app falls back to those same default values.

## Run The App

Start the application from the repository root:

```bash
python neuroformai/app.py
```

On startup the app will:

1. Connect to MongoDB.
2. Create collections and indexes if they do not already exist.
3. Seed the exercise catalog into the database.
4. Launch the Gradio interface on `127.0.0.1:7860`.

## Usage

1. Open the Gradio app in your browser after launch.
2. Sign up or log in.
3. Go to Live Exercise, select an exercise, and choose left or right side.
4. Start the exercise before processing webcam or uploaded video input.
5. Review live reps, angle, phase, form score, and posture alerts.
6. Stop the session to save the workout summary.
7. Use History and Analytics to review progress later.

## Database Collections

The app creates and uses these MongoDB collections:

- `users`
- `exercises`
- `workout_sessions`
- `session_details`
- `rep_logs`
- `posture_alerts`

## Notes

- Login state is also stored in Gradio browser storage so the app can auto-login on page load.
- Webcam input is mirrored horizontally in live mode so the on-screen view behaves like a selfie camera.
- Uploaded videos can be processed frame by frame, and the app samples every third frame to reduce load.
- Plank is treated as a timed hold exercise rather than a standard rep-based movement.

## Development Notes

- The repository includes its own implementations of linked lists, stacks, queues, and sorting algorithms for coursework-style demonstration.
- Exercise definitions live in `neuroformai/database/seed.py` and drive the angle thresholds, posture rules, and side mappings used by the engine.
- If you change exercise definitions, rerun the app so the seed step can add any new exercises.

## Troubleshooting

- If the app cannot connect to MongoDB, verify that the server is running and that `MONGO_URI` is correct.
- If MediaPipe fails to load, confirm that `neuroformai/models/pose_landmarker_full.task` exists.
- If webcam tracking does not work, check browser permissions and that your camera is not in use by another application.
