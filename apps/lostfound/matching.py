import re
from datetime import timedelta
from .models import FoundItem

STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could',
    'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here',
    'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in',
    'into', 'is', 'isnt', 'it', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor',
    'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that',
    'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd',
    'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was',
    'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres',
    'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd',
    'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves'
}

def clean_text_to_words(text):
    if not text:
        return []
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return [w for w in words if w not in STOPWORDS and len(w) > 1]

def find_potential_matches(lost_item):
    """
    Finds unclaimed FoundItems that match lost_item.
    Scores them based on category, title, description, and date proximity.
    """
    unclaimed_found = FoundItem.objects.filter(status='unclaimed')
    matches = []
    
    lost_title_words = clean_text_to_words(lost_item.title)
    lost_desc_words = clean_text_to_words(lost_item.description)
    
    for found in unclaimed_found:
        score = 0
        
        # 1. Category Match
        category_match = False
        if found.category == lost_item.category:
            score += 50
            category_match = True
            
        # 2. Title Word Overlap
        found_title_words = clean_text_to_words(found.title)
        matching_title_words = set(lost_title_words).intersection(set(found_title_words))
        score += len(matching_title_words) * 15
        
        # 3. Description Word Overlap
        found_desc_words = clean_text_to_words(found.description)
        matching_desc_words = set(lost_desc_words).intersection(set(found_desc_words))
        score += len(matching_desc_words) * 5
        
        # If there is no category match and no keyword match, it's not a match at all
        if not category_match and not matching_title_words and not matching_desc_words:
            score = 0
        else:
            # 4. Date Proximity
            date_diff = abs((lost_item.date_lost - found.date_found).days)
            if date_diff <= 1:
                score += 30
            elif date_diff <= 3:
                score += 20
            elif date_diff <= 7:
                score += 10
            
        if score > 0:
            found.match_score = score
            matches.append(found)
            
    # Sort matches by score descending
    matches.sort(key=lambda x: x.match_score, reverse=True)
    return matches
