from sklearn.tree import DecisionTreeClassifier

X_TRAIN = [
    [4.5, 10, 0, 0],
    [1.2,  1, 1, 0],
    [5.0,  8, 0, 1],
    [3.5,  7, 0, 0],
    [1.0,  0, 1, 0],
    [4.8, 12, 0, 1],
]

Y_TRAIN = [
    "single_switch",
    "voice_mode",
    "large_buttons",
    "standard",
    "voice_mode",
    "single_switch",
]

_model = DecisionTreeClassifier(random_state=42)
_model.fit(X_TRAIN, Y_TRAIN)


def recommend(avg_click_time: float, click_errors: int,
              keyboard_usage: int, voice_usage: int) -> str:
    features = [[avg_click_time, click_errors, keyboard_usage, voice_usage]]
    return _model.predict(features)[0]