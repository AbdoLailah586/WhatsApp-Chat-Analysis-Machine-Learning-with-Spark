from app.unified_categories import CATEGORIES
import re
from datetime import datetime

CATEGORY_PATTERNS = {
    "Work": [
        r'\b(meeting|deadline|report|project|client|boss|presentation|proposal|invoice|contract|schedule|agenda|brief|assignment|task|submit|approval|payroll|salary|offer letter|interview|resume|cv|colleague|office)\b',
        r'\b(zoom|teams|slack|google meet|conference call)\b',
        r'\b(attach|forward|cc|fwd)\b',
        r'\b(اجتماع|موعد|تقرير|مشروع|عميل|مدير|عرض|فاتورة|عقد|جدول|مهمة|تسليم|موافقة|راتب|مقابلة|زميل|مكتب)\b',
    ],
    "Friends": [
        r'\b(hang out|catch up|grab (a )?(drink|coffee|lunch|dinner)|movie|party|weekend|chill|bro|dude|mate|buddy|lol|haha|lmao|rofl|jk|ttyl|wyd|wbu)\b',
        r'\b(let\'s go|wanna|gonna|should we|you free\?|what\'s up|sup\b)',
        r'\b(joking|kidding|funny|hilarious|memes|gossip)\b',
        r'\b(نطلع|نتقابل|قهوة|غدا|عشا|فلم|حفلة|ويكند|ههه|ههههه|ضحك|مزح|شو أخبار|كيفك|وينك)\b',
    ],
    "Family": [
        r'\b(mom|dad|mama|papa|sister|brother|aunt|uncle|cousin|grandma|grandpa|nani|dadi|chacha|mami|khala|phuppo)\b',
        r'\b(dinner at home|family|ghar|home cooked|eid|ramadan|diwali|celebration)\b',
        r'\b(how are you|missing you|when are you coming|take care|bless you|praying)\b',
        r'\b(ماما|بابا|أمي|أبي|أخت|أخ|عم|عمة|خال|خالة|جدة|جد|بيت|عائلة|عزيمة|رمضان|عيد|حبايب)\b',
    ],
    "Urgent": [
        r'\b(asap|urgent|emergency|immediately|right now|critical|call me now|pick up|important|priority|time sensitive|deadline today|due today|last chance|final notice|overdue)\b',
        r'\b(911|help|fire|accident|hospital|sick|ambulance)\b',
        r'\b(ضروري|طارئ|حالة|فورا|الآن|مهم|حرج|آخر موعد|مستشفى|إسعاف|خطر)\b',
    ],
    "Promotional": [
        r'\b(sale|discount|offer|deal|coupon|promo|limited time|exclusive|subscribe|buy now|shop|order|free shipping|flash sale|clearance|buy one get one|BOGO)\b',
        r'\b(click here|visit our|check out our|new arrivals|new collection|launch|introducing)\b',
        r'\b(opt out|unsubscribe|text STOP|marketing|newsletter)\b',
    ],
    "Spam": [
        r'\b(you won|winner|congratulations.*selected|claim your prize|free money|earn \$|make \$|work from home.*\$|get rich|double your|investment opportunity|act now|don\'t miss out|guaranteed)\b',
        r'\b(click this link|verify your account|update your payment|suspicious activity|your account.*suspend)\b',
        r'\b(viagra|casino|lottery|jackpot|bitcoin giveaway|crypto giveaway|forex signals)\b',
    ],
    "Entertainment": [
        r'\b(youtube|tiktok|instagram reel|viral|trending|netflix|spotify|playlist|song|movie recommendation|watch this|check this out|funny video|cute video|epic|amazing video)\b',
        r'\b(sports|football|cricket|basketball|soccer|match|game|score|goal|player|team|champions league|world cup|ipl|nba|nfl|ufc|boxing)\b',
        r'\b(celebrity|actor|actress|singer|artist|concert|festival|event|show|episode|season|trailer)\b',
    ],
}

WORK_HOURS_WEEKDAY = range(9, 18)
SOCIAL_EVENING_HOURS = range(19, 23)

def classify_by_keywords(text: str) -> dict:
    text_lower = text.lower()
    scores = {cat: 0 for cat in CATEGORIES}
    
    for category, patterns in CATEGORY_PATTERNS.items():
        if category not in scores:
            scores[category] = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            scores[category] += len(matches) * 10
            
    if max(scores.values()) == 0:
        return {"category": None, "confidence": 0.0, "method": "rules", "all_scores": scores}
        
    top_category = max(scores, key=scores.get)
    total_score = sum(scores.values())
    confidence = (scores[top_category] / total_score) * 100 if total_score > 0 else 0
    
    return {
        "category": top_category,
        "confidence": min(confidence, 100.0),
        "method": "rules",
        "all_scores": scores
    }

def classify_with_context(message: str, sender: str, timestamp: datetime, sender_stats: dict = None) -> dict:
    result = classify_by_keywords(message)
    
    if result["category"] is not None:
        if timestamp.weekday() < 5 and timestamp.hour in WORK_HOURS_WEEKDAY:
            if "Work" in result.get("all_scores", {}):
                result["all_scores"]["Work"] += 5
                
        if timestamp.weekday() >= 5 or timestamp.hour in SOCIAL_EVENING_HOURS:
            for cat in ["Friends", "Family", "Entertainment"]:
                if cat in result.get("all_scores", {}):
                    result["all_scores"][cat] += 3
                    
        top_category = max(result["all_scores"], key=result["all_scores"].get)
        total_score = sum(result["all_scores"].values())
        confidence = (result["all_scores"][top_category] / total_score) * 100 if total_score > 0 else 0
        result["category"] = top_category
        result["confidence"] = min(confidence, 100.0)
        
    if result["category"] is None and sender_stats:
        if sender in sender_stats and sender_stats[sender]:
            most_common = max(sender_stats[sender], key=sender_stats[sender].get)
            if sender_stats[sender][most_common] > 3:
                result["category"] = most_common
                result["confidence"] = 40.0
                result["method"] = "sender_history"
                
    if result["category"] is None:
        if timestamp.weekday() < 5 and timestamp.hour in WORK_HOURS_WEEKDAY:
            result["category"] = "Work"
            result["confidence"] = 20.0
            result["method"] = "time_fallback"
        else:
            result["category"] = "Friends"
            result["confidence"] = 10.0
            result["method"] = "default_fallback"
            
    return result
