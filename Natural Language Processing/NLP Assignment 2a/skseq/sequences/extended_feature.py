from skseq.sequences.id_feature import IDFeatures
from skseq.sequences.id_feature import UnicodeFeatures

# ----------
# Feature Class
# Extracts features from a labeled corpus (only supported features are extracted
# ----------
class ExtendedFeatures(IDFeatures):

    def add_emission_features(self, sequence, pos, y, features):
        x = sequence.x[pos]
        # Get tag name from ID.
        y_name = self.dataset.y_dict.get_label_name(y)

        # Get word name from ID.
        if isinstance(x, str):
            x_name = x
        else:
            x_name = self.dataset.x_dict.get_label_name(x)

        word = str(x_name)
        # Generate feature name.
        feat_name = "id:%s::%s" % (word, y_name)
        # Get feature ID from name.
        feat_id = self.add_feature(feat_name)
        # Append feature.
        if feat_id != -1:
            features.append(feat_id)

# region custom features
        # Title case
        if str.istitle(word):
            feat_name = "title_case::%s" % (y_name)
            feat_name = str(feat_name)

            feat_id = self.add_feature(feat_name)
            if feat_id != -1:
                features.append(feat_id)


        # Check if is upper
        if str.isupper(word):
            feat_name = "upper::%s" % y_name
            feat_name = str(feat_name)

            feat_id = self.add_feature(feat_name)
            if feat_id != -1:
                features.append(feat_id)

        # Lowercase word
        word_lower = word.lower()
        feat_name = "lower:%s::%s" % (word_lower, y_name)
        feat_id = self.add_feature(feat_name)
        if feat_id != -1:
            features.append(feat_id)


        # Feature: All caps and tag
        if word.isupper():
            feat_name = "all_caps::%s" % y_name
            feat_id = self.add_feature(feat_name)
            if feat_id != -1:
                features.append(feat_id)

        # Feature: Contains hyphen and tag
        if '-' in word:
            feat_name = "contains_hyphen::%s" % y_name
            feat_id = self.add_feature(feat_name)
            if feat_id != -1:
                features.append(feat_id)

        # Feature: Numeric and tag
        if word.isdigit():
            feat_name = "numeric::%s" % y_name
            feat_id = self.add_feature(feat_name)
            if feat_id != -1:
                features.append(feat_id)

        # Feature: Contains special characters and tag
        if any(char in '!@#$%^&*()_+[]{}|;:,.<>?/' for char in word):
            feat_name = "special_char::%s" % y_name
            feat_id = self.add_feature(feat_name)
            if feat_id != -1:
                features.append(feat_id)

        # Feature: Is stop word and tag
        stop_words =set( [
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", 
        "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", 
        "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", 
        "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", 
        "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
        "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", 
        "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", 
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", 
        "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", 
        "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", 
        "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", 
        "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", 
        "you've", "your", "yours", "yourself", "yourselves"
        ])

        if word.lower() in stop_words:
            feat_name = "stop_word::%s" % y_name
            feat_id = self.add_feature(feat_name)
            if feat_id != -1:
                features.append(feat_id)

        # region entity Features
        entity_prefix_suffix = {
            'geo': {'prefix': ['North', 'South', 'East', 'West'], 'suffix': ['land', 'ia', 'ville', 'ton']},
            'org': {'prefix': ['International', 'National', 'Global', 'Local'], 'suffix': ['Corp', 'Inc', 'Ltd', 'Organization']},
            'per': {'prefix': ['Mr', 'Mrs', 'Miss', 'Dr'], 'suffix': ['son', 'sen', 'man', 'stein']},
            'gpe': {'prefix': ['United', 'Republic', 'Federal', 'Democratic'], 'suffix': ['land', 'stan', 'istan', 'ville']},
            'tim': {'prefix': ['Early', 'Late', 'Old', 'New'], 'suffix': ['day', 'year', 'century', 'era']},
            'art': {'prefix': ['Ancient', 'Modern', 'Fine', 'Famous'], 'suffix': ['work', 'piece', 'art', 'creation']},
            'eve': {'prefix': ['Annual', 'Monthly', 'Weekly', 'International'], 'suffix': ['fest', 'celebration', 'event', 'conference']},
            'nat': {'prefix': ['National', 'International', 'Natural', 'World'], 'suffix': ['disaster', 'calamity', 'phenomenon', 'event']}
        }

        for entity, values in entity_prefix_suffix.items():
            for prefix in values['prefix']:
                if word.lower().startswith(prefix.lower()):
                    feat_name = f"prefix:{prefix.lower()}::{y_name}"
                    feat_id = self.add_feature(feat_name)
                    if feat_id != -1:
                        features.append(feat_id)

            for suffix in values['suffix']:
                if word.lower().endswith(suffix.lower()):
                    feat_name = f"suffix:{suffix.lower()}::{y_name}"
                    feat_id = self.add_feature(feat_name)
                    if feat_id != -1:
                        features.append(feat_id)
        # endregion 
        
# endregion
        return features


