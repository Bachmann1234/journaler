import datetime
from hypothesis import given, assume
from hypothesis import strategies as st
from hypothesis.extra.datetime import datetimes
from journaler.log import format_tags, add_log_to_file
from journaler.models import VALID_MEALS, FoodLog, json_to_food_log, food_log_to_json, SNACK
from pytz import utc


@given(
    datetimes(timezones=['UTC']),
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=5),
    st.lists(st.text()),
    st.lists(st.text()),
    st.lists(st.text()),
    st.sampled_from(VALID_MEALS)
)
def test_to_from_json(
        date,
        mood_rating,
        food_rating,
        mood_tags,
        food_tags,
        entry_tags,
        meal
):
    assume(date > utc.localize(datetime.datetime(2000, 1, 1, 1)))
    original = FoodLog(
        date,
        mood_rating,
        food_rating,
        mood_tags,
        food_tags,
        entry_tags,
        meal

    )
    assert original == json_to_food_log(food_log_to_json(original))


@given(
    st.lists(st.text(min_size=1))
)
def test_format_tags(tags):
    assume(not any(',' in t for t in tags))
    tags = map(lambda x: x.strip(), tags)
    assume(all(tags))
    arg = ", ".join(tags)
    assert map(lambda x: x.lower(), tags) == format_tags(arg)


def test_add_to_log(tmpdir):
    logs = [
        FoodLog(
            utc.localize(datetime.datetime.utcnow()),
            1,
            5,
            ['sleepy', 'hungry'],
            ['broccoli'],
            ['test'],
            SNACK
        ),
        FoodLog(
            utc.localize(datetime.datetime.utcnow()),
            5,
            2,
            ['happy'],
            ['popcorn', 'butter'],
            ['movies', 'test'],
            SNACK
        )
    ]
    log_file = str(tmpdir.join("log.txt"))
    for l in logs:
        add_log_to_file(log_file, l)
    with open(log_file, 'r') as infile:
        results = [json_to_food_log(l) for l in infile]
    assert logs == results
