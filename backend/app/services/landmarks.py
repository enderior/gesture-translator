def extract_landmarks(frames: list) -> list:
    """В будущем здесь будет MediaPipe."""
    return [[[0.0, 0.0, 0.0]] * 21] * len(frames) # Фейковые лендмарки