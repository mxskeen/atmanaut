"""
Mood constants and utilities (migrated from shared/moods.js)
"""

MOODS = {
    "OVERJOYED": {
        "id": "overjoyed",
        "label": "Overjoyed",
        "emoji": "🤗",
        "score": 10,
        "color": "yellow",
        "prompt": "What wonderful things happened today?",
        # pixabay_query removed
    },
    "ACCOMPLISHED": {
        "id": "accomplished",
        "label": "Accomplished",
        "emoji": "⭐",
        "score": 9,
        "color": "amber",
        "prompt": "What have you achieved?",
        
    },
    "INSPIRED": {
        "id": "inspired",
        "label": "Inspired",
        "emoji": "💫",
        "score": 9,
        "color": "violet",
        "prompt": "What's sparking your creativity?",
        
    },
    "PROUD": {
        "id": "proud",
        "label": "Proud",
        "emoji": "🦁",
        "score": 9,
        "color": "amber",
        "prompt": "What achievement are you proud of?",
        
    },
    "LOVED": {
        "id": "loved",
        "label": "Loved",
        "emoji": "🥰",
        "score": 9,
        "color": "pink",
        "prompt": "Who or what is making you feel loved?",
        
    },
    "APPRECIATED": {
        "id": "appreciated",
        "label": "Appreciated",
        "emoji": "💝",
        "score": 8,
        "color": "pink",
        "prompt": "How do you feel appreciated today?",
        
    },
    "HAPPY": {
        "id": "happy",
        "label": "Happy",
        "emoji": "😊",
        "score": 8,
        "color": "yellow",
        "prompt": "What's bringing you joy?",
        
    },
    "CONTENT": {
        "id": "content",
        "label": "Content",
        "emoji": "😌",
        "score": 7,
        "color": "green",
        "prompt": "What's giving you peace today?",
        
    },
    "HOPEFUL": {
        "id": "hopeful",
        "label": "Hopeful",
        "emoji": "🌅",
        "score": 7,
        "color": "orange",
        "prompt": "What are you looking forward to?",
        
    },
    "GRATEFUL": {
        "id": "grateful",
        "label": "Grateful",
        "emoji": "🙏",
        "score": 8,
        "color": "amber",
        "prompt": "What are you thankful for?",
        
    },
    "EXCITED": {
        "id": "excited",
        "label": "Excited",
        "emoji": "🎉",
        "score": 8,
        "color": "yellow",
        "prompt": "What's got you excited?",
        
    },
    "RELAXED": {
        "id": "relaxed",
        "label": "Relaxed",
        "emoji": "🧘",
        "score": 7,
        "color": "blue",
        "prompt": "How are you finding peace?",
        
    },
    "OPTIMISTIC": {
        "id": "optimistic",
        "label": "Optimistic",
        "emoji": "🌈",
        "score": 7,
        "color": "violet",
        "prompt": "What's looking bright?",
        
    },
    "NEUTRAL": {
        "id": "neutral",
        "label": "Neutral",
        "emoji": "😐",
        "score": 5,
        "color": "gray",
        "prompt": "How was your day overall?",
        
    },
    "TIRED": {
        "id": "tired",
        "label": "Tired",
        "emoji": "😴",
        "score": 4,
        "color": "blue",
        "prompt": "What's been draining your energy?",
        
    },
    "STRESSED": {
        "id": "stressed",
        "label": "Stressed",
        "emoji": "😰",
        "score": 3,
        "color": "red",
        "prompt": "What's causing you stress?",
        
    },
    "ANXIOUS": {
        "id": "anxious",
        "label": "Anxious",
        "emoji": "😟",
        "score": 3,
        "color": "yellow",
        "prompt": "What's making you feel anxious?",
        
    },
    "FRUSTRATED": {
        "id": "frustrated",
        "label": "Frustrated",
        "emoji": "😤",
        "score": 3,
        "color": "orange",
        "prompt": "What's frustrating you?",
        
    },
    "SAD": {
        "id": "sad",
        "label": "Sad",
        "emoji": "😢",
        "score": 2,
        "color": "blue",
        "prompt": "What's weighing on your heart?",
        
    },
    "LONELY": {
        "id": "lonely",
        "label": "Lonely",
        "emoji": "😔",
        "score": 2,
        "color": "gray",
        "prompt": "Tell me about feeling alone.",
        
    },
    "OVERWHELMED": {
        "id": "overwhelmed",
        "label": "Overwhelmed",
        "emoji": "😵",
        "score": 2,
        "color": "red",
        "prompt": "What feels like too much right now?",
        
    },
    "ANGRY": {
        "id": "angry",
        "label": "Angry",
        "emoji": "😡",
        "score": 2,
        "color": "red",
        "prompt": "What triggered your anger?",
        
    },
    "DISAPPOINTED": {
        "id": "disappointed",
        "label": "Disappointed",
        "emoji": "😞",
        "score": 3,
        "color": "gray",
        "prompt": "What didn't go as expected?",
        
    },
    "CONFUSED": {
        "id": "confused",
        "label": "Confused",
        "emoji": "😕",
        "score": 4,
        "color": "purple",
        "prompt": "What's unclear to you right now?",
        
    },
    "BORED": {
        "id": "bored",
        "label": "Bored",
        "emoji": "😑",
        "score": 4,
        "color": "gray",
        "prompt": "What would make things more interesting?",
        
    },
    "WORRIED": {
        "id": "worried",
        "label": "Worried",
        "emoji": "😨",
        "score": 3,
        "color": "yellow",
        "prompt": "What concerns are on your mind?",
        
    },
    "JEALOUS": {
        "id": "jealous",
        "label": "Jealous",
        "emoji": "😒",
        "score": 3,
        "color": "green",
        "prompt": "What's triggering these feelings?",
        
    },
    "GUILTY": {
        "id": "guilty",
        "label": "Guilty",
        "emoji": "😳",
        "score": 3,
        "color": "red",
        "prompt": "What's causing you to feel guilty?",
        
    },
    "EMBARRASSED": {
        "id": "embarrassed",
        "label": "Embarrassed",
        "emoji": "😳",
        "score": 3,
        "color": "pink",
        "prompt": "What made you feel embarrassed?",
        
    },
    "NOSTALGIC": {
        "id": "nostalgic",
        "label": "Nostalgic",
        "emoji": "🥺",
        "score": 6,
        "color": "purple",
        "prompt": "What memories are you reflecting on?",
        
    },
    "SURPRISED": {
        "id": "surprised",
        "label": "Surprised",
        "emoji": "😲",
        "score": 6,
        "color": "yellow",
        "prompt": "What caught you off guard?",
        
    },
    "CURIOUS": {
        "id": "curious",
        "label": "Curious",
        "emoji": "🤔",
        "score": 6,
        "color": "blue",
        "prompt": "What's piquing your interest?",
        
    },
    "DETERMINED": {
        "id": "determined",
        "label": "Determined",
        "emoji": "💪",
        "score": 8,
        "color": "orange",
        "prompt": "What are you working towards?",
        
    },
    "CONFIDENT": {
        "id": "confident",
        "label": "Confident",
        "emoji": "😎",
        "score": 8,
        "color": "blue",
        "prompt": "What's boosting your confidence?",
        
    },
    "PLAYFUL": {
        "id": "playful",
        "label": "Playful",
        "emoji": "😜",
        "score": 7,
        "color": "pink",
        "prompt": "What's bringing out your playful side?",
        
    },
    "CREATIVE": {
        "id": "creative",
        "label": "Creative",
        "emoji": "🎨",
        "score": 7,
        "color": "purple",
        "prompt": "What's inspiring your creativity?",
        
    },
    "FOCUSED": {
        "id": "focused",
        "label": "Focused",
        "emoji": "🎯",
        "score": 7,
        "color": "green",
        "prompt": "What has your complete attention?",
        
    },
    "PEACEFUL": {
        "id": "peaceful",
        "label": "Peaceful",
        "emoji": "☮️",
        "score": 7,
        "color": "green",
        "prompt": "What's bringing you inner peace?",
        
    },
    "ENERGETIC": {
        "id": "energetic",
        "label": "Energetic",
        "emoji": "⚡",
        "score": 8,
        "color": "yellow",
        "prompt": "What's fueling your energy?",
        
    },
    "MOTIVATED": {
        "id": "motivated",
        "label": "Motivated",
        "emoji": "🔥",
        "score": 8,
        "color": "orange",
        "prompt": "What's driving your motivation?",
        
    },
    "REFLECTIVE": {
        "id": "reflective",
        "label": "Reflective",
        "emoji": "🪞",
        "score": 6,
        "color": "blue",
        "prompt": "What are you contemplating?",
        
    },
    "MELANCHOLIC": {
        "id": "melancholic",
        "label": "Melancholic",
        "emoji": "🌧️",
        "score": 4,
        "color": "gray",
        "prompt": "What's creating this bittersweet feeling?",
        
    },
}


def get_mood_by_id(mood_id: str) -> dict:
    """
    Get mood data by ID
    """
    for mood_data in MOODS.values():
        if mood_data["id"] == mood_id:
            return mood_data
    return None


def get_mood_by_key(mood_key: str) -> dict:
    """
    Get mood data by key (uppercase)
    """
    return MOODS.get(mood_key.upper())


def get_all_moods() -> dict:
    """
    Get all moods
    """
    return MOODS
