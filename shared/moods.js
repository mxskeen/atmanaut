export const MOODS = {
  OVERJOYED: {
    id: "overjoyed",
    label: "Overjoyed",
    emoji: "🤗",
    score: 10,
    color: "yellow",
    prompt: "What wonderful things happened today?",
    // pixabayQuery removed
  },
  ACCOMPLISHED: {
    id: "accomplished",
    label: "Accomplished",
    emoji: "⭐",
    score: 9,
    color: "amber",
    prompt: "What have you achieved?",
    
  },
  INSPIRED: {
    id: "inspired",
    label: "Inspired",
    emoji: "💫",
    score: 9,
    color: "violet",
    prompt: "What's sparking your creativity?",
    
  },
  PROUD: {
    id: "proud",
    label: "Proud",
    emoji: "🦁",
    score: 9,
    color: "amber",
    prompt: "What achievement are you proud of?",
    
  },
  LOVED: {
    id: "loved",
    label: "Loved",
    emoji: "🥰",
    score: 9,
    color: "pink",
    prompt: "Who or what is making you feel loved?",
    
  },
  APPRECIATED: {
    id: "appreciated",
    label: "Appreciated",
    emoji: "💝",
    score: 8,
    color: "rose",
    prompt: "Who showed you appreciation?",
    
  },
  MOTIVATED: {
    id: "motivated",
    label: "Motivated",
    emoji: "🎯",
    score: 8,
    color: "emerald",
    prompt: "What's driving you forward?",
    
  },
  HAPPY: {
    id: "happy",
    label: "Happy",
    emoji: "😊",
    score: 8,
    color: "amber",
    prompt: "What's making you smile today?",
    
  },
  EXCITED: {
    id: "excited",
    label: "Excited",
    emoji: "🎉",
    score: 8,
    color: "orange",
    prompt: "What are you looking forward to?",
    
  },
  CONFIDENT: {
    id: "confident",
    label: "Confident",
    emoji: "💪",
    score: 8,
    color: "emerald",
    prompt: "What's boosting your confidence?",
    
  },
  GRATEFUL: {
    id: "grateful",
    label: "Grateful",
    emoji: "🙏",
    score: 8,
    color: "green",
    prompt: "What are you thankful for today?",
    
  },
  CONNECTED: {
    id: "connected",
    label: "Connected",
    emoji: "🤝",
    score: 8,
    color: "indigo",
    prompt: "Who made you feel connected today?",
    
  },
  PEACEFUL: {
    id: "peaceful",
    label: "Peaceful",
    emoji: "😌",
    score: 7,
    color: "blue",
    prompt: "What's bringing you peace?",
    
  },
  HOPEFUL: {
    id: "hopeful",
    label: "Hopeful",
    emoji: "🌱",
    score: 7,
    color: "green",
    prompt: "What gives you hope?",
    
  },
  CREATIVE: {
    id: "creative",
    label: "Creative",
    emoji: "🎨",
    score: 7,
    color: "violet",
    prompt: "What's inspiring your creativity?",
    
  },
  THOUGHTFUL: {
    id: "thoughtful",
    label: "Thoughtful",
    emoji: "🤔",
    score: 6,
    color: "slate",
    prompt: "What's on your mind?",
    
  },
  CURIOUS: {
    id: "curious",
    label: "Curious",
    emoji: "🧐",
    score: 6,
    color: "teal",
    prompt: "What's caught your interest?",
    
  },
  NOSTALGIC: {
    id: "nostalgic",
    label: "Nostalgic",
    emoji: "🌅",
    score: 5,
    color: "fuchsia",
    prompt: "What memories are you thinking about?",
    
  },
  NEUTRAL: {
    id: "neutral",
    label: "Neutral",
    emoji: "😐",
    score: 5,
    color: "gray",
    prompt: "How has your day been?",
    
  },
  RESTLESS: {
    id: "restless",
    label: "Restless",
    emoji: "🌊",
    score: 4,
    color: "blue",
    prompt: "What's making you feel unsettled?",
    
  },
  TIRED: {
    id: "tired",
    label: "Tired",
    emoji: "😴",
    score: 4,
    color: "purple",
    prompt: "What's draining your energy?",
    
  },
  OVERWHELMED: {
    id: "overwhelmed",
    label: "Overwhelmed",
    emoji: "😵",
    score: 3,
    color: "sky",
    prompt: "What's feeling like too much?",
    
  },
  ANXIOUS: {
    id: "anxious",
    label: "Anxious",
    emoji: "😰",
    score: 3,
    color: "indigo",
    prompt: "What's causing your anxiety?",
    
  },
  DISAPPOINTED: {
    id: "disappointed",
    label: "Disappointed",
    emoji: "😞",
    score: 3,
    color: "stone",
    prompt: "What didn't go as expected?",
    
  },
  FRUSTRATED: {
    id: "frustrated",
    label: "Frustrated",
    emoji: "😤",
    score: 3,
    color: "orange",
    prompt: "What's blocking your progress?",
    
  },
  STRESSED: {
    id: "stressed",
    label: "Stressed",
    emoji: "😫",
    score: 3,
    color: "rose",
    prompt: "What's pressuring you?",
    
  },
  INSECURE: {
    id: "insecure",
    label: "Insecure",
    emoji: "🥺",
    score: 2,
    color: "lime",
    prompt: "What's making you doubt yourself?",
    
  },
  SAD: {
    id: "sad",
    label: "Sad",
    emoji: "😢",
    score: 2,
    color: "cyan",
    prompt: "What's bringing you down?",
    
  },
  LONELY: {
    id: "lonely",
    label: "Lonely",
    emoji: "🌙",
    score: 2,
    color: "zinc",
    prompt: "How could you connect with others?",
    
  },
  ANGRY: {
    id: "angry",
    label: "Angry",
    emoji: "😠",
    score: 1,
    color: "red",
    prompt: "What's frustrating you?",
    
  },
};

export const getMoodTrend = (averageScore) => {
  if (averageScore >= 8) return "You've been feeling great!";
  if (averageScore >= 6) return "You've been doing well overall.";
  if (averageScore >= 4) return "You've been feeling okay.";
  if (averageScore >= 2) return "Things have been challenging.";
  return "You've been having a tough time.";
};

export const getMoodById = (moodId) => {
  return MOODS[moodId?.toUpperCase()];
};
